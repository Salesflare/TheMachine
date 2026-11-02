import AuthenticationServices
import Capacitor
import CryptoKit
import UIKit
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

    override public func load() {
        NotificationCenter.default.addObserver(self, selector: #selector(openURL(_:)), name: .capacitorOpenURL, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(becameActive), name: UIApplication.didBecomeActiveNotification, object: nil)
        loading = bridge?.webView?.observe(\.isLoading, options: [.new]) { [weak self] webView, change in
            if change.newValue == false { self?.onMachinePage(webView.url) }
        }
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

    /// A self-hosted Machine's default port; besides it only 443.
    static let ownPort = 8443

    /// A Machine address the app may save: https and no user, a hosted Machine's root on 443, or a tailnet host on 443
    /// or 8443. No other port.
    static func normalMachine(_ text: String?) -> String? {
        guard let text = text, let u = URLComponents(string: text), u.scheme == "https", u.user == nil,
              let host = u.host?.lowercased() else { return nil }
        let port = u.port ?? 443
        if hostedHost(host) { return port == 443 ? "https://\(host)/" : nil }
        guard tailnetHost(host), port == 443 || port == ownPort else { return nil }
        let authority = port == ownPort ? "\(host):\(ownPort)" : host
        var path = u.path.isEmpty ? "/" : u.path
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

    /// A self-hosted Machine on The Machine Network: the account hands back its Tailscale address (no token: the
    /// Machine's own Tailscale sign-in applies).
    private func signedInOwn(_ m: String) {
        guard let url = MachineShellPlugin.normalMachine(m), MachineShellPlugin.tailnetHost(URL(string: url)?.host) else { return stopped() }
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
        var payload: [String: Any] = ["base": saved, "listen": true]
        if let token = store.string(forKey: "pushToken") {
            #if DEBUG
            let sandbox = true
            #else
            let sandbox = false
            #endif
            payload["push"] = ["platform": "apns", "token": token, "sandbox": sandbox, "label": UIDevice.current.model]
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
