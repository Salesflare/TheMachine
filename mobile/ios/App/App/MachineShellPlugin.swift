import AVFoundation
import AuthenticationServices
import Capacitor
import CryptoKit
import QuickLook
import UIKit
import UserNotifications
import WebKit

/// The app's whole native part on iOS, the same as android/.../MachineShellPlugin.java (mobile/README.md): where the
/// owner's Machine is, the account's sign-in in the system's web sign-in sheet (ASWebAuthenticationSession, so passkeys
/// and Face ID work), which pages the WebView may open, the push token and what the Share extension handed over.
/// What it does inside the Machine's page is www/inject.js, the same on Android.
///
/// Only the app's own start page may change the saved Machine or start a sign-in: the Machine's page never can.
@objc(MachineShellPlugin)
public class MachineShellPlugin: CAPPlugin, CAPBridgedPlugin, ASWebAuthenticationPresentationContextProviding {
    public let identifier = "MachineShellPlugin"
    public let jsName = "MachineShell"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "get", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "info", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "setMachine", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "check", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "clearConnect", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "forget", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "pushToken", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "signIn", returnType: CAPPluginReturnPromise),
    ]

    static let hosted = "app.themachine.computer"
    static let scheme = "computer.themachine.app"
    static let appGroup = "group.computer.themachine.app"
    private let store = UserDefaults.standard
    private var session: ASWebAuthenticationSession?
    private var loading: NSKeyValueObservation?
    private var pendingShare: [String: Any]?
    private var mediaGate: MediaGate?
    private var filePreview: FilePreview?  // the open preview's data source (the controller holds it weakly)

    override public func load() {
        NotificationCenter.default.addObserver(self, selector: #selector(openURL(_:)), name: .capacitorOpenURL, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(becameActive), name: UIApplication.didBecomeActiveNotification, object: nil)
        loading = bridge?.webView?.observe(\.isLoading, options: [.new]) { [weak self] webView, change in
            if change.newValue == false { self?.onMachinePage(webView.url) }
        }
        DispatchQueue.main.async { [weak self] in
            guard let self = self, let webView = self.bridge?.webView else { return }
            webView.allowsBackForwardNavigationGestures = true  // swipe from the edge: back in the Machine's pages
            // The microphone (Talk, dictation) for the Machine's own page only; Capacitor's delegate does the rest
            self.mediaGate = MediaGate(inner: webView.uiDelegate, plugin: self)
            webView.uiDelegate = self.mediaGate
            webView.configuration.userContentController.add(FilesHandler(plugin: self), name: "machineFiles")
            webView.configuration.userContentController.addScriptMessageHandler(PhoneHandler(plugin: self), contentWorld: .page, name: "machinePhone")
        }
    }

    /// Whether a page's origin is the saved Machine's (scheme, host and port).
    func isMachine(_ origin: WKSecurityOrigin) -> Bool {
        guard let saved = machine, let m = URLComponents(string: saved) else { return false }
        return origin.protocol == "https" && origin.host.lowercased() == m.host && (origin.port == 0 ? 443 : origin.port) == (m.port ?? 443)
    }

    /// A file from the Machine's page (www/inject.js, files): the share sheet, where Save to Files keeps it.
    func saveFile(_ body: Any) {
        guard let text = body as? String, text.count < 36_000_000, let json = text.data(using: .utf8),
              let o = try? JSONSerialization.jsonObject(with: json) as? [String: Any], let b64 = o["data"] as? String,
              let data = Data(base64Encoded: b64) else { return }
        var name = ((o["name"] as? String) ?? "file").replacingOccurrences(of: "[/\\\\:\\x00-\\x1f]", with: "_", options: .regularExpression)
            .trimmingCharacters(in: .whitespaces)
        if name.isEmpty || name.hasPrefix(".") { name = "file" + name }
        let dir = FileManager.default.temporaryDirectory.appendingPathComponent("files", isDirectory: true)
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        let file = dir.appendingPathComponent(String(name.suffix(120)))
        guard (try? data.write(to: file)) != nil, let vc = bridge?.viewController else { return }
        // A file the owner opened (a link to it, not a download): shown, with the share button there to keep it
        if o["open"] as? Bool == true, QLPreviewController.canPreview(file as NSURL) {
            let preview = QLPreviewController()
            let source = FilePreview(file)
            filePreview = source
            preview.dataSource = source
            vc.present(preview, animated: true)
            return
        }
        let sheet = UIActivityViewController(activityItems: [file], applicationActivities: nil)
        sheet.popoverPresentationController?.sourceView = vc.view
        vc.present(sheet, animated: true)
    }

    // MARK: which pages the WebView opens

    static func label(_ s: Substring) -> Bool {
        s.range(of: "^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", options: .regularExpression) != nil
    }

    static func hostedHost(_ host: String?) -> Bool {
        guard let host = host, host.hasSuffix("." + hosted) else { return false }
        let name = host.dropLast(hosted.count + 1)
        return !name.contains(".") && label(name)
    }

    static func tailnetHost(_ host: String?) -> Bool {
        guard let host = host, host.hasSuffix(".ts.net") else { return false }
        let parts = host.split(separator: ".", omittingEmptySubsequences: false)
        return parts.count >= 4 && parts.allSatisfy(label)
    }

    /// A self-hosted Machine's host: a tailnet name, or a public DNS name (two labels or more, a top level of letters,
    /// so never an IP address or a bare name). Never a hosted Machine's: those come through sign-in. Same as www/machine-url.js.
    static func ownHost(_ host: String?) -> Bool {
        guard let host = host else { return false }
        if host.hasSuffix(".ts.net") { return tailnetHost(host) }
        guard host.count <= 253, host != hosted, !host.hasSuffix("." + hosted) else { return false }
        let parts = host.split(separator: ".", omittingEmptySubsequences: false)
        guard parts.count >= 2, let top = parts.last, top.range(of: "^[a-z]{2,63}$", options: .regularExpression) != nil else { return false }
        return parts.allSatisfy(label)
    }

    /// A self-hosted Machine's default port; besides it only 443.
    static let ownPort = 8443

    /// A Machine address the app may save: https and no user, a hosted Machine's root on 443, or a self-hosted one
    /// (ownHost) on 443 or 8443. No other port.
    static func normalMachine(_ text: String?) -> String? {
        guard let text = text, let u = URLComponents(string: text), u.scheme == "https", u.user == nil,
              let host = u.host?.lowercased() else { return nil }
        let port = u.port ?? 443
        if hostedHost(host) { return port == 443 ? "https://\(host)/" : nil }
        guard ownHost(host), port == 443 || port == ownPort else { return nil }
        let authority = port == ownPort ? "\(host):\(ownPort)" : host
        var path = u.percentEncodedPath.isEmpty ? "/" : u.percentEncodedPath
        if !path.hasSuffix("/") { path += "/" }
        guard path.range(of: "^/(?:[A-Za-z0-9._~-]+/)*$", options: .regularExpression) != nil else { return nil }
        return "https://\(authority)\(path)"
    }

    private var machine: String? { MachineShellPlugin.normalMachine(store.string(forKey: "machine")) }

    private var onStartPage: Bool {
        guard let url = bridge?.webView?.url, let local = bridge?.config.localURL else { return false }
        return url.scheme == local.scheme && url.host == local.host
    }

    override public func shouldOverrideLoad(_ navigationAction: WKNavigationAction) -> NSNumber? {
        guard let url = navigationAction.request.url else { return nil }
        if navigationAction.targetFrame?.isMainFrame == false { return nil } // frames inside a page: its own business
        if let local = bridge?.config.localURL, url.scheme == local.scheme, url.host == local.host { return false }
        let host = url.host?.lowercased() ?? ""
        if url.scheme == "https", let saved = machine, let m = URL(string: saved) {
            // A hosted Machine may move to its owner's new name: any hosted dashboard host, the account checks whose
            if host == m.host, (url.port ?? 443) == (m.port ?? 443) { return false }
            if MachineShellPlugin.hostedHost(m.host), MachineShellPlugin.hostedHost(host), (url.port ?? 443) == 443 { return false }
            if host == MachineShellPlugin.hosted, MachineShellPlugin.hostedHost(m.host), ["/open", "/login"].contains(url.path) {
                DispatchQueue.main.async { self.startSignIn(nil) } // the dashboard's sign-in ran out: sign in again
                return true
            }
        }
        if ["https", "http", "mailto", "tel"].contains(url.scheme ?? "") {
            DispatchQueue.main.async { UIApplication.shared.open(url) } // links in mail, the account's other pages
        }
        return true
    }

    // MARK: methods for the start page (www/app.js)

    @objc func get(_ call: CAPPluginCall) {
        var out: [String: Any] = [:]
        out["machine"] = machine ?? NSNull()
        if let connect = store.string(forKey: "connect") { out["connect"] = connect }
        if store.bool(forKey: "signinStopped") {
            out["signin"] = "stopped"
            store.removeObject(forKey: "signinStopped")
        }
        call.resolve(out)
    }

    @objc func info(_ call: CAPPluginCall) {
        // Tailscale registers no URL scheme iOS lets apps check for, so "not installed" is never claimed here
        call.resolve(["platform": "ios", "pushReady": true])
    }

    @objc func setMachine(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            guard self.onStartPage else { return call.reject("not allowed") }
            let asked = call.getString("url")
            guard let url = MachineShellPlugin.normalMachine(asked), url == asked else { return call.reject("not a Machine address") }
            self.store.set(url, forKey: "machine")
            self.store.removeObject(forKey: "connect")
            call.resolve()
        }
    }

    /// Before a Machine of their own is saved: its manifest's answer, {status, body}, for www/machine-url.js isMachine.
    /// Rejects when it can't be reached. No redirects followed, no cookies or cache, a short wait and a small body.
    @objc func check(_ call: CAPPluginCall) {
        DispatchQueue.main.async { // only the start page asks, never a Machine's page or what it links to
            guard self.onStartPage else { return call.reject("not allowed") }
            self.fetchManifest(call)
        }
    }

    /// The owner's own typed address only (check): https on 443 or 8443 to a DNS name, never an IP address.
    private func fetchManifest(_ call: CAPPluginCall) {
        let asked = call.getString("url")
        guard let url = MachineShellPlugin.normalMachine(asked), url == asked, MachineShellPlugin.ownHost(URL(string: url)?.host),
              let manifest = URL(string: url + "manifest.webmanifest") else { return call.reject("not a Machine address") }
        var request = URLRequest(url: manifest, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 8)
        request.setValue("application/manifest+json, application/json", forHTTPHeaderField: "Accept")
        let session = URLSession(configuration: .ephemeral, delegate: NoRedirects(), delegateQueue: nil)
        session.dataTask(with: request) { data, response, error in
            session.finishTasksAndInvalidate()
            guard error == nil, let http = response as? HTTPURLResponse else { return call.reject("unreachable") }
            let body = (data ?? Data()).count <= 64 * 1024 ? String(data: data ?? Data(), encoding: .utf8) ?? "" : ""
            call.resolve(["status": http.statusCode, "body": body])
        }.resume()
    }

    @objc func clearConnect(_ call: CAPPluginCall) {
        store.removeObject(forKey: "connect")
        call.resolve()
    }

    @objc func forget(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            guard self.onStartPage else { return call.reject("not allowed") }
            self.store.removeObject(forKey: "machine")
            call.resolve()
        }
    }

    @objc func pushToken(_ call: CAPPluginCall) {
        guard let token = call.getString("token"), token.range(of: "^[0-9a-fA-F]{64,200}$", options: .regularExpression) != nil else {
            return call.reject("not a push token")
        }
        store.set(token.lowercased(), forKey: "pushToken")
        call.resolve()
    }

    // MARK: the phone's own questions, for the Machine's page (www/inject.js, machinePhone): the microphone's and
    // notifications' state, notifications on (the phone's own question, then the push token) and the app's Settings

    private var pushDone: (([String: Any]) -> Void)?
    private var pushWatch: [NSObjectProtocol] = []

    func phone(_ ask: String, done: @escaping ([String: Any]) -> Void) {
        switch ask {
        case "mic":
            switch AVCaptureDevice.authorizationStatus(for: .audio) {
            case .authorized: done(["state": "granted"])
            case .denied, .restricted: done(["state": "blocked"])  // iOS asks once; then only Settings
            default: done(["state": "prompt"])
            }
        case "push":
            UNUserNotificationCenter.current().getNotificationSettings { s in
                DispatchQueue.main.async { done(["state": MachineShellPlugin.pushState(s.authorizationStatus)]) }
            }
        case "settings":
            if let url = URL(string: UIApplication.openSettingsURLString) { UIApplication.shared.open(url) }
            done(["state": "ok"])
        case "pushOn":
            UNUserNotificationCenter.current().getNotificationSettings { s in
                DispatchQueue.main.async {
                    switch MachineShellPlugin.pushState(s.authorizationStatus) {
                    case "granted": self.pushRegister(done)
                    case "blocked": done(["state": "blocked"])
                    default:
                        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, _ in
                            DispatchQueue.main.async { if granted { self.pushRegister(done) } else { done(["state": "blocked"]) } }
                        }
                    }
                }
            }
        default:
            done(["state": "off"])
        }
    }

    private static func pushState(_ s: UNAuthorizationStatus) -> String {
        switch s {
        case .authorized, .provisional, .ephemeral: return "granted"
        case .denied: return "blocked"
        default: return "prompt"
        }
    }

    /// The push token from the AppDelegate (Capacitor's notifications), kept and handed to the page.
    private func pushRegister(_ done: @escaping ([String: Any]) -> Void) {
        pushFinish(["state": "off"])  // one at a time
        pushDone = done
        let center = NotificationCenter.default
        pushWatch = [
            center.addObserver(forName: .capacitorDidRegisterForRemoteNotifications, object: nil, queue: .main) { [weak self] note in
                guard let data = note.object as? Data else { return }
                let token = data.map { String(format: "%02x", $0) }.joined()
                self?.store.set(token, forKey: "pushToken")
                self?.pushFinish(["state": "on", "token": token])
            },
            center.addObserver(forName: .capacitorDidFailToRegisterForRemoteNotifications, object: nil, queue: .main) { [weak self] _ in
                self?.pushFinish(["state": "off"])
            },
        ]
        UIApplication.shared.registerForRemoteNotifications()
        DispatchQueue.main.asyncAfter(deadline: .now() + 10) { [weak self] in self?.pushFinish(["state": "off"]) }
    }

    private func pushFinish(_ answer: [String: Any]) {
        pushWatch.forEach { NotificationCenter.default.removeObserver($0) }
        pushWatch = []
        let done = pushDone
        pushDone = nil
        done?(answer)
    }

    @objc func signIn(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            guard self.onStartPage else { return call.reject("not allowed") }
            self.startSignIn(call)
        }
    }

    // MARK: the account's sign-in

    private static func b64(_ data: Data) -> String {
        data.base64EncodedString().replacingOccurrences(of: "+", with: "-").replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "=", with: "")
    }

    /// The account's sign-in in the system sheet; it comes back as computer.themachine.app://signed-in. The verifier
    /// never leaves the app until the dashboard redeems the handoff with it (cloud docs/mobile-app.md).
    private func startSignIn(_ call: CAPPluginCall?) {
        guard session == nil else { call?.resolve(); return }
        var raw = Data(count: 32)
        _ = raw.withUnsafeMutableBytes { SecRandomCopyBytes(kSecRandomDefault, 32, $0.baseAddress!) }
        let verifier = MachineShellPlugin.b64(raw)
        let challenge = MachineShellPlugin.b64(Data(SHA256.hash(data: Data(verifier.utf8))))
        var start = URLComponents(string: "https://\(MachineShellPlugin.hosted)/open")!
        start.queryItems = [URLQueryItem(name: "to", value: "app"), URLQueryItem(name: "c", value: challenge)]
        let session = ASWebAuthenticationSession(url: start.url!, callbackURLScheme: MachineShellPlugin.scheme) { [weak self] url, _ in
            DispatchQueue.main.async {
                self?.session = nil
                guard let self = self else { return }
                guard let url = url, url.host == "signed-in" else { return self.stopped() }
                let items = URLComponents(url: url, resolvingAgainstBaseURL: false)?.queryItems ?? []
                if let own = items.first(where: { $0.name == "m" })?.value { self.signedInOwn(own) } else {
                    self.signedIn(items.first(where: { $0.name == "u" })?.value, verifier: verifier)
                }
            }
        }
        session.presentationContextProvider = self
        session.prefersEphemeralWebBrowserSession = false // the account's own sign-in in Safari carries over: no new sign-in each time
        self.session = session
        session.start()
        call?.resolve()
    }

    public func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        bridge?.webView?.window ?? ASPresentationAnchor()
    }

    private func stopped() {
        store.set(true, forKey: "signinStopped")
        if let local = bridge?.config.localURL { bridge?.webView?.load(URLRequest(url: local.appendingPathComponent("index.html"))) }
    }

    private func signedIn(_ u: String?, verifier: String) {
        guard let u = u, var target = URLComponents(string: u), target.scheme == "https", target.port == nil, target.user == nil,
              MachineShellPlugin.hostedHost(target.host), target.path == "/_machine/auth",
              let t = target.queryItems?.first(where: { $0.name == "t" })?.value,
              t.range(of: "^[A-Za-z0-9_-]{20,100}$", options: .regularExpression) != nil else { return stopped() }
        store.set("https://\(target.host!)/", forKey: "machine")
        target.queryItems = (target.queryItems ?? []) + [URLQueryItem(name: "v", value: verifier)]
        bridge?.webView?.load(URLRequest(url: target.url!))
    }

    /// A self-hosted Machine on The Machine Network: the account hands back its address (its Tailscale one, else the
    /// dashboard's own https address it reported; no token: the Machine's own sign-in applies).
    private func signedInOwn(_ m: String) {
        guard let url = MachineShellPlugin.normalMachine(m), MachineShellPlugin.ownHost(URL(string: url)?.host) else { return stopped() }
        store.set(url, forKey: "machine")
        bridge?.webView?.load(URLRequest(url: URL(string: url)!))
    }

    // MARK: links into the app and the Share extension

    @objc private func openURL(_ note: Notification) {
        guard let info = note.object as? [String: Any], let url = info["url"] as? URL, url.scheme == MachineShellPlugin.scheme else { return }
        DispatchQueue.main.async {
            if url.host == "connect" { // a scanned link to a Machine of the owner's own: asked on the start page first
                let u = URLComponents(url: url, resolvingAgainstBaseURL: false)?.queryItems?.first(where: { $0.name == "u" })?.value
                if let found = MachineShellPlugin.normalMachine(u), MachineShellPlugin.tailnetHost(URL(string: found)?.host) {
                    self.store.set(found, forKey: "connect")
                    if let local = self.bridge?.config.localURL {
                        self.bridge?.webView?.load(URLRequest(url: local.appendingPathComponent("index.html")))
                    }
                }
            } else if url.host == "share" {
                self.becameActive()
            }
        }
    }

    /// What the Share extension left in the app group (ShareExtension/ShareViewController.swift): read once, then gone.
    @objc private func becameActive() {
        guard let dir = FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: MachineShellPlugin.appGroup)?
            .appendingPathComponent("share", isDirectory: true),
              let data = try? Data(contentsOf: dir.appendingPathComponent("pending.json")),
              let found = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return }
        var files: [[String: String]] = []
        for f in (found["files"] as? [[String: String]] ?? []).prefix(5) {
            guard let name = f["file"], !name.contains("/"), let bytes = try? Data(contentsOf: dir.appendingPathComponent(name)) else { continue }
            files.append(["name": f["name"] ?? "file", "type": f["type"] ?? "application/octet-stream", "data": bytes.base64EncodedString()])
        }
        try? FileManager.default.removeItem(at: dir)
        pendingShare = ["text": found["text"] as? String ?? "", "files": files]
        if let url = bridge?.webView?.url, let saved = machine, url.absoluteString.hasPrefix(saved) { onMachinePage(url) }
    }

    // MARK: in the Machine's page: www/inject.js

    private func onMachinePage(_ url: URL?) {
        guard let url = url, var saved = machine, let savedHost = URL(string: saved)?.host else { return }
        if MachineShellPlugin.hostedHost(savedHost), MachineShellPlugin.hostedHost(url.host), url.host != savedHost {
            saved = "https://\(url.host!)/" // the hosted Machine moved to its owner's name: follow it
            store.set(saved, forKey: "machine")
        }
        guard url.absoluteString.hasPrefix(saved), !url.path.hasPrefix("/_machine/") else { return }
        #if DEBUG
        let sandbox = true
        #else
        let sandbox = false
        #endif
        let device: [String: Any] = ["platform": "apns", "sandbox": sandbox, "label": UIDevice.current.model]
        var payload: [String: Any] = ["base": saved, "listen": true, "device": device]  // device: for a token now or later
        if let token = store.string(forKey: "pushToken") {
            payload["push"] = device.merging(["token": token]) { $1 }
        }
        if let share = pendingShare {
            payload["share"] = share
            pendingShare = nil
        }
        guard let json = try? JSONSerialization.data(withJSONObject: payload), let text = String(data: json, encoding: .utf8),
              let source = Bundle.main.url(forResource: "public/inject", withExtension: "js").flatMap({ try? String(contentsOf: $0) })
        else { return }
        bridge?.webView?.evaluateJavaScript("(\(source))(\(text)); undefined", completionHandler: nil)
    }
}

/// The app's root view: Capacitor's, with MachineShellPlugin registered (it lives in the app, not in a package).
class MachineViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(MachineShellPlugin())
    }
}

/// The WebView's own delegate (Capacitor's), except for the microphone: granted to the saved Machine's page only.
private final class MediaGate: NSObject, WKUIDelegate {
    weak var inner: WKUIDelegate?
    weak var plugin: MachineShellPlugin?

    init(inner: WKUIDelegate?, plugin: MachineShellPlugin) {
        self.inner = inner
        self.plugin = plugin
    }

    override func responds(to aSelector: Selector!) -> Bool {
        super.responds(to: aSelector) || (inner?.responds(to: aSelector) ?? false)
    }

    override func forwardingTarget(for aSelector: Selector!) -> Any? {
        inner?.responds(to: aSelector) == true ? inner : nil
    }

    func webView(_ webView: WKWebView, requestMediaCapturePermissionFor origin: WKSecurityOrigin, initiatedByFrame frame: WKFrameInfo,
                 type: WKMediaCaptureType, decisionHandler: @escaping (WKPermissionDecision) -> Void) {
        decisionHandler(type == .microphone && frame.isMainFrame && plugin?.isMachine(origin) == true ? .grant : .deny)
    }
}

/// window.webkit.messageHandlers.machineFiles: only what the Machine's own page hands over.
private final class FilesHandler: NSObject, WKScriptMessageHandler {
    weak var plugin: MachineShellPlugin?

    init(plugin: MachineShellPlugin) { self.plugin = plugin }

    func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.frameInfo.isMainFrame, plugin?.isMachine(message.frameInfo.securityOrigin) == true else { return }
        plugin?.saveFile(message.body)
    }
}

/// window.webkit.messageHandlers.machinePhone: the Machine's own page asks; the answer comes back to it.
private final class PhoneHandler: NSObject, WKScriptMessageHandlerWithReply {
    weak var plugin: MachineShellPlugin?

    init(plugin: MachineShellPlugin) { self.plugin = plugin }

    func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage,
                               replyHandler: @escaping (Any?, String?) -> Void) {
        guard message.frameInfo.isMainFrame, let plugin = plugin, plugin.isMachine(message.frameInfo.securityOrigin),
              let body = message.body as? [String: Any], let ask = body["ask"] as? String else { return replyHandler(nil, "not allowed") }
        plugin.phone(ask) { replyHandler($0, nil) }
    }
}

/// The check's request answers for itself: a redirect is not followed (its 3xx is the answer, so not a Machine).
private final class NoRedirects: NSObject, URLSessionTaskDelegate {
    func urlSession(_ session: URLSession, task: URLSessionTask, willPerformHTTPRedirection response: HTTPURLResponse,
                    newRequest request: URLRequest, completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(nil)
    }
}

private final class FilePreview: NSObject, QLPreviewControllerDataSource {
    let file: URL
    init(_ file: URL) { self.file = file }
    func numberOfPreviewItems(in controller: QLPreviewController) -> Int { 1 }
    func previewController(_ controller: QLPreviewController, previewItemAt index: Int) -> QLPreviewItem { file as NSURL }
}
