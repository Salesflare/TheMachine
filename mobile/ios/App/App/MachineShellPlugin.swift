import AVFoundation
import AuthenticationServices
import Capacitor
import CryptoKit
import Network
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
    private var connecting: ASWebAuthenticationSession?  // a connection's sign-in (startConnection)
    private var loading: NSKeyValueObservation?
    private var pendingShare: [String: Any]?
    private var mediaGate: MediaGate?
    private var filePreview: FilePreview?  // the open preview's data source (the controller holds it weakly)
    private var pageWatch: PageWatch?  // the WebView holds its navigation delegate weakly
    private let network = NWPathMonitor()
    private var networkWasDown = false
    private var wakeTimer: Timer?
    private var lastTick = Date()
    private var pageGone = false
    private var probing = false
    private var lastReopen = Date.distantPast
    private var loadStarted: Date?  // the load under way since then (none: no load)
    private var badTries = 0  // checks in a row that found the page gone, blank or not painted
    private var wasActive = true
    private var activeAt = Date()  // came in front then
    private var lastFlat = Date.distantPast  // the last look that counted as unpainted
    private var asleepSeen = MachineShellPlugin.asleep()  // the sleep up to the last load, or the last look at a page in use
    private var againSoon = false  // a check is already waiting for reopenGap to pass
    private static var lastFresh = Date.distantPast

    override public func load() {
        MachineActions.shared.install()  // in front of Capacitor's notification delegate, which it set by now
        NotificationCenter.default.addObserver(self, selector: #selector(openURL(_:)), name: .capacitorOpenURL, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(becameActive), name: UIApplication.didBecomeActiveNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(cameBack), name: UIApplication.willEnterForegroundNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(cameBack), name: UIApplication.protectedDataDidBecomeAvailableNotification, object: nil)
        loading = bridge?.webView?.observe(\.isLoading, options: [.new]) { [weak self] webView, change in
            guard let self = self else { return }
            if change.newValue == true {
                let started = Date()
                self.loadStarted = started
                // a load that never ends (the link went away halfway) is checked without waiting for a return
                DispatchQueue.main.asyncAfter(deadline: .now() + MachineShellPlugin.loadLimit + 1) { [weak self] in
                    if self?.loadStarted == started { self?.checkPage() }
                }
            } else if change.newValue == false {
                self.loadStarted = nil
                self.pageGone = false
                self.asleepSeen = MachineShellPlugin.asleep()
                self.onMachinePage(webView.url)
                // a page that loaded but shows nothing (an empty answer on the way) is caught at once, not on the next return
                DispatchQueue.main.asyncAfter(deadline: .now() + MachineShellPlugin.afterLoad) { [weak self] in self?.checkPage() }
            }
        }
        DispatchQueue.main.async { [weak self] in
            guard let self = self, let webView = self.bridge?.webView else { return }
            self.watchForWake()  // on the main run loop, where its timer runs
            // Capacitor's navigation delegate, told first when the page's process ends (PageWatch)
            self.pageWatch = PageWatch(inner: webView.navigationDelegate, plugin: self)
            webView.navigationDelegate = self.pageWatch
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
        if machine != nil, let start = MachineShellPlugin.connectionStart(url) { // a connection's sign-in: the sign-in sheet
            DispatchQueue.main.async { self.startConnection(start) }
            return true
        }
        if ["https", "http", "mailto", "tel"].contains(url.scheme ?? "") {
            DispatchQueue.main.async { UIApplication.shared.open(url) } // links in mail, the account's other pages
        }
        return true
    }

    /// A connection's sign-in the Machine's page starts ("Sign in with Shortcut"): the hosted dashboard's hop to the
    /// account (/hop?t=...&app=1, which the account gives the app's WebView only) or a self-hosted Machine's start link
    /// (/connect/start/<id>). The address to open in the sign-in sheet, with app=1, or nil for anything else (the
    /// account's other pages keep opening in Safari). Same as www/machine-url.js connectionStart.
    static func connectionStart(_ url: URL) -> URL? {
        guard url.scheme == "https", url.host == hosted, url.port == nil, url.user == nil, url.fragment == nil else { return nil }
        let query = url.query
        if url.path == "/hop", let q = query, q.hasPrefix("t="), q.hasSuffix("&app=1"),
           String(q.dropFirst(2).dropLast(6)).range(of: "^[A-Za-z0-9_-]{20,100}\\z", options: .regularExpression) != nil {
            return url
        }
        if query == nil, url.path.range(of: "^/connect/start/[A-Za-z0-9_-]{32}\\z", options: .regularExpression) != nil {
            return URL(string: "https://\(hosted)\(url.path)?app=1")
        }
        return nil
    }

    /// Where such a sign-in ends (computer.themachine.app://connected?h=...): the part of the saved Machine's dashboard to
    /// open, + Add's form (connect=<source>[/<ref>|/stopped]) or "connected" (signed-in=<source>[/again]); nil otherwise.
    /// Same as www/machine-url.js connectedPart.
    static func connectedPart(_ h: String?) -> String? {
        guard let h = h, h.range(of: "^(?:connect=[a-z_]{1,32}(?:/(?:[cf]_[0-9a-f]{16}|stopped))?|signed-in=[a-z_]{1,32}(?:/again)?)\\z",
                                 options: .regularExpression) != nil else { return nil }
        return h
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

    /// Before a Machine of their own is saved: {machine: true} when its manifest answers as a Machine's (the same rule
    /// as www/machine-url.js isMachine), else {machine: false}. Never the answer itself. Rejects when it can't be
    /// reached, or when its name leads to the phone itself or its local network (publicOrTailnet). No redirects
    /// followed, no cookies or cache, a short wait and a small body.
    @objc func check(_ call: CAPPluginCall) {
        DispatchQueue.main.async { // only the start page asks, never a Machine's page or what it links to
            guard self.onStartPage else { return call.reject("not allowed") }
            self.fetchManifest(call)
        }
    }

    /// Where check may go: a public address, or a tailnet one (100.64.0.0/10, fd7a:115c:a1e0::/48). Never the phone
    /// itself, its local network, link-local or multicast addresses, so a typed or linked name can't reach them.
    static func publicOrTailnet(_ b: [UInt8]) -> Bool {
        if b.count == 4 {
            let (x, y) = (b[0], b[1])
            if x == 100 && y & 0xc0 == 64 { return true } // tailnet (CGNAT)
            return !(x == 0 || x == 10 || x == 127 || x >= 224 || (x == 169 && y == 254) || (x == 172 && y & 0xf0 == 16)
                || (x == 192 && y == 168) || (x == 192 && y == 0 && b[2] == 0) || (x == 198 && (y == 18 || y == 19)))
        }
        guard b.count == 16 else { return false }
        if Array(b[0..<6]) == [0xfd, 0x7a, 0x11, 0x5c, 0xa1, 0xe0] { return true } // tailnet
        if b[0..<10].allSatisfy({ $0 == 0 }) && b[10] == 0xff && b[11] == 0xff { return publicOrTailnet(Array(b[12...])) } // ::ffff:a.b.c.d
        if b[0..<15].allSatisfy({ $0 == 0 }) { return false } // :: and ::1
        return b[0] & 0xfe != 0xfc && !(b[0] == 0xfe && b[1] & 0xc0 == 0x80) && !(b[0] == 0xfe && b[1] & 0xc0 == 0xc0) && b[0] != 0xff
    }

    /// Every address a name resolves to, as bytes; empty when it doesn't resolve.
    static func addresses(_ host: String) -> [[UInt8]] {
        var hints = addrinfo()
        hints.ai_family = AF_UNSPEC
        hints.ai_socktype = SOCK_STREAM
        var list: UnsafeMutablePointer<addrinfo>?
        guard getaddrinfo(host, nil, &hints, &list) == 0 else { return [] }
        defer { freeaddrinfo(list) }
        var out: [[UInt8]] = []
        var at = list
        while let ai = at?.pointee {
            if ai.ai_family == AF_INET, let sa = ai.ai_addr {
                let a = sa.withMemoryRebound(to: sockaddr_in.self, capacity: 1) { $0.pointee.sin_addr }
                out.append(withUnsafeBytes(of: a) { Array($0) })
            } else if ai.ai_family == AF_INET6, let sa = ai.ai_addr {
                let a = sa.withMemoryRebound(to: sockaddr_in6.self, capacity: 1) { $0.pointee.sin6_addr }
                out.append(withUnsafeBytes(of: a) { Array($0) })
            }
            at = ai.ai_next
        }
        return out
    }

    /// A Machine's manifest, or its refusal to anyone off its tailnet: the same rule as www/machine-url.js isMachine.
    static func manifestIsMachine(_ status: Int, _ data: Data) -> Bool {
        guard let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return false }
        if status == 200 { return json["name"] as? String == "The Machine" && json["start_url"] is String && json["icons"] is [Any] }
        if status == 403 { return json["error"] as? String == "Use the owner-authenticated Tailscale dashboard" }
        return false
    }

    /// The owner's own typed address only (check): https on 443 or 8443 to a DNS name, never an IP address.
    private func fetchManifest(_ call: CAPPluginCall) {
        let asked = call.getString("url")
        guard let url = MachineShellPlugin.normalMachine(asked), url == asked, let host = URL(string: url)?.host,
              MachineShellPlugin.ownHost(host),
              let manifest = URL(string: url + "manifest.webmanifest") else { return call.reject("not a Machine address") }
        DispatchQueue.global(qos: .userInitiated).async {
            let found = MachineShellPlugin.addresses(host)
            guard !found.isEmpty else { return call.reject("unreachable") }
            guard found.allSatisfy(MachineShellPlugin.publicOrTailnet) else { return call.reject("not a Machine address") }
            self.askManifest(call, manifest)
        }
    }

    private func askManifest(_ call: CAPPluginCall, _ manifest: URL) {
        var request = URLRequest(url: manifest, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 8)
        request.setValue("application/manifest+json, application/json", forHTTPHeaderField: "Accept")
        let session = URLSession(configuration: .ephemeral, delegate: NoRedirects(), delegateQueue: nil)
        session.dataTask(with: request) { data, response, error in
            session.finishTasksAndInvalidate()
            guard error == nil, let http = response as? HTTPURLResponse else { return call.reject("unreachable") }
            let body = data ?? Data()
            call.resolve(["machine": body.count <= 64 * 1024 && MachineShellPlugin.manifestIsMachine(http.statusCode, body)])
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
            MachineNotice.forget()
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

    /// A connection's sign-in in the same sheet as the account's, so it never leaves the owner in Safari: it ends on
    /// computer.themachine.app://connected?h=<part> (cloud docs/mobile-app.md), and the Machine's dashboard opens at that
    /// part. Closed or stopped in the sheet: the dashboard as it was.
    private func startConnection(_ start: URL) {
        guard session == nil, connecting == nil else { return }
        let sheet = ASWebAuthenticationSession(url: start, callbackURLScheme: MachineShellPlugin.scheme) { [weak self] url, _ in
            DispatchQueue.main.async {
                self?.connecting = nil
                guard let url = url, url.host == "connected" else { return }
                self?.connected(url)
            }
        }
        sheet.presentationContextProvider = self
        sheet.prefersEphemeralWebBrowserSession = false // the account's own sign-in in Safari carries over
        connecting = sheet
        sheet.start()
    }

    /// Back from a connection's sign-in: the saved Machine's dashboard at that part (on it already: only its #part).
    private func connected(_ url: URL) {
        let h = URLComponents(url: url, resolvingAgainstBaseURL: false)?.queryItems?.first(where: { $0.name == "h" })?.value
        guard let part = MachineShellPlugin.connectedPart(h), let saved = machine, let webView = bridge?.webView,
              let target = URL(string: saved + "#" + part) else { return }
        if let now = webView.url?.absoluteString, now.hasPrefix(saved) {
            webView.evaluateJavaScript("location.hash=\"\(part)\"", completionHandler: nil) // part: checked, no quotes
        } else {
            webView.load(URLRequest(url: target))
        }
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
            } else if url.host == "connected" { // a connection's sign-in the app started that ended in Safari: the same
                self.connected(url)
            }
        }
    }

    /// What the Share extension left in the app group (ShareExtension/ShareViewController.swift): read once, then gone.
    @objc private func becameActive() {
        activeAt = Date()
        checkPage()
        MachineNotice.sweep()
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

    // MARK: never a blank page

    // After the computer or phone slept, the page's own process can be gone (the system ended it, or it ran out of
    // memory) or hang, and the WebView then stays white until the app is closed and opened again. Capacitor reloads when
    // it hears the process ended, but that reload is lost when it comes while the app is away (asleep, in the
    // background), and a hung process isn't reported at all. So whenever the app comes back (in front again, unlocked,
    // the network back, a wake: the clock jumped between two ticks) the page is asked whether it shows anything, and
    // opened again when no answer comes in time or it shows nothing. A page alive but white still answers a script, so
    // "it answered" is not enough: an empty page (an empty answer on the way, a load that never ended) is opened again
    // once, then the app's own offline page says so with Try again. After a real sleep the page is opened again when
    // nothing is typed or open in it, so whatever the sleep did to the window is gone.
    //
    // On a Mac a page can also be alive, full of words and still not painted: the window shows only the WebView's own
    // plain background. No script can tell, so there the app looks at its own window (paints). One flat color twice in
    // a row: the page is put in the window anew, which loses nothing; still flat: a new WebView (freshView), as if the
    // app was closed and opened. That also goes for a page in use: nobody can use it, and chat drafts come back.

    static let pageAnswer: TimeInterval = 8  // a busy page still answers in this time; a gone or hung one never does
    static let reopenGap: TimeInterval = 15  // never in a loop
    static let loadLimit: TimeInterval = 30  // a load still going after this is stuck
    static let afterLoad: TimeInterval = 3  // a finished page is asked this long after
    static let onMac = ProcessInfo.processInfo.isiOSAppOnMac
    static let longSleep: TimeInterval = 5 * 60  // a sleep this long opens the page again when it isn't in use
    static let lookAgain: TimeInterval = 2  // an unpainted page gets this long before the next step
    static let justBack: TimeInterval = 60  // in front since less than this: someone is there
    static let freshGap: TimeInterval = 5 * 60  // never in a loop
    static let edge: CGFloat = 24  // left out of the look: the scrollbar is the app's own, drawn also over a blank page
    // What the page shows: "shown" (words or a picture), "empty" (a white page, or the Machine's restarting note in
    // place of the page), "busy" (the dashboard has typing or an open panel: shell-tabs.js pageInUse)
    static let pageProbe = "(()=>{const b=document.body;if(document.contentType==='application/json'||!b)return 'empty';"
        + "if(!b.querySelector('img,svg,canvas,video,iframe')&&!(b.innerText||'').trim())return 'empty';"
        + "try{if(typeof pageInUse==='function'&&pageInUse())return 'busy'}catch(e){}return 'shown'})()"

    private func watchForWake() {
        network.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                guard let self = self else { return }
                if path.status != .satisfied { self.networkWasDown = true; return }
                if self.networkWasDown { self.networkWasDown = false; self.checkPage() }
            }
        }
        network.start(queue: DispatchQueue.global(qos: .utility))
        // Timers don't run while the computer sleeps: a tick that comes late is a wake
        wakeTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            let now = Date(), late = now.timeIntervalSince(self.lastTick) > 90
            let active = UIApplication.shared.applicationState == .active
            let back = active && !self.wasActive  // in front again, also when no notification said so
            self.lastTick = now
            self.wasActive = active
            if back { self.activeAt = now }
            if late || back || self.sleptLong { self.checkPage() }
        }
    }

    /// How long the computer slept since it started: the clock that counts sleep less the one that doesn't. Unlike a
    /// late tick it can't be missed: short wakes in the night, where the timer ticks, add up too.
    static func asleep() -> TimeInterval {
        (TimeInterval(clock_gettime_nsec_np(CLOCK_MONOTONIC_RAW)) - TimeInterval(clock_gettime_nsec_np(CLOCK_UPTIME_RAW))) / 1_000_000_000
    }

    /// A Mac only: the window stays open for days, where a phone's system ends the page itself.
    private var sleptLong: Bool {
        MachineShellPlugin.onMac && MachineShellPlugin.asleep() - asleepSeen > MachineShellPlugin.longSleep
    }

    @objc private func cameBack() { checkPage() }

    /// The page's process ended (PageWatch, before Capacitor reloads): until a page has loaded again, the next check opens it again.
    func pageEnded() {
        pageGone = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) { [weak self] in self?.checkPage() }
    }

    /// Opens the page again when it has no address, its process ended without a page loading since, it doesn't answer
    /// a one-line script in time, or it shows nothing; a load stuck for loadLimit, or a second empty page in a row, gets
    /// the app's offline page (what happened, with Try again). A page that answers is looked at too (looked). Only while
    /// the app is in front: in the background it would be lost again.
    func checkPage() {
        guard UIApplication.shared.applicationState != .background, let webView = bridge?.webView, !probing else { return }
        if pageGone || webView.url == nil { return reopen() }
        if webView.isLoading {
            guard let started = loadStarted, Date().timeIntervalSince(started) > MachineShellPlugin.loadLimit else { return }
            webView.stopLoading()
            return showOffline()
        }
        probing = true
        var done = false
        let finish: (String?) -> Void = { [weak self] shows in
            guard let self = self, !done else { return }
            done = true
            self.probing = false
            switch shows {
            case "shown"?, "busy"?: self.looked(webView, inUse: shows == "busy")
            case "empty"?:
                self.badTries += 1
                if self.badTries >= 2 { self.showOffline() } else { self.reopen(force: true) }  // once at once, then offline
            default:  // no answer: the page is gone or hung, and on a Mac its WebView may be too
                guard MachineShellPlugin.onMac else { return self.reopen() }
                self.badTries += 1
                if self.badTries < 2 { self.reopen() } else if !self.freshView() { self.showOffline() }
            }
        }
        webView.evaluateJavaScript(MachineShellPlugin.pageProbe) { result, error in finish(error == nil ? result as? String : nil) }
        DispatchQueue.main.asyncAfter(deadline: .now() + MachineShellPlugin.pageAnswer) { finish(nil) }
    }

    /// A page that says it shows something: does the window? A page not in use is opened again after a long sleep anyway.
    private func looked(_ webView: WKWebView, inUse: Bool) {
        let painted = paints(webView)
        if painted == false && store.bool(forKey: "paintSeen") {
            // Several checks come at once on a return: one look counts, the next one a moment later
            guard Date().timeIntervalSince(lastFlat) > MachineShellPlugin.lookAgain / 2 else { return }
            lastFlat = Date()
            badTries += 1
            switch badTries {
            case 1: checkSoon(MachineShellPlugin.lookAgain)  // perhaps it only just came back
            case 2: redraw()
            // What is typed is only given up when the owner just came back to a window that can't be used
            case _ where inUse && Date().timeIntervalSince(activeAt) > MachineShellPlugin.justBack: break
            default: if freshView() { store.set(false, forKey: "paintSeen") }  // once: until a look sees a page again
            }
            return
        }
        badTries = 0
        if painted == true { store.set(true, forKey: "paintSeen") }  // looks work on this Mac: a flat one means something
        if !inUse && sleptLong { return reopen(force: true) }  // a long sleep: a fresh page, nothing in use is lost
        if painted == true { asleepSeen = MachineShellPlugin.asleep() }
    }

    private func checkSoon(_ wait: TimeInterval) {
        DispatchQueue.main.asyncAfter(deadline: .now() + wait) { [weak self] in self?.checkPage() }
    }

    /// Whether the window shows more than one flat color where the page is, as it is on screen now. On a Mac only, with
    /// the app in front and nothing over the page; nil when there is nothing to tell by.
    private func paints(_ webView: WKWebView) -> Bool? {
        guard MachineShellPlugin.onMac, UIApplication.shared.applicationState == .active, webView.window != nil,
              let vc = bridge?.viewController, vc.presentedViewController == nil else { return nil }
        let area = webView.bounds.insetBy(dx: MachineShellPlugin.edge, dy: MachineShellPlugin.edge)
        guard area.width >= 100, area.height >= 100 else { return nil }
        let format = UIGraphicsImageRendererFormat()
        format.scale = 1
        var whole = false
        let picture = UIGraphicsImageRenderer(bounds: area, format: format).image { _ in
            whole = webView.drawHierarchy(in: webView.bounds, afterScreenUpdates: false)
        }
        guard whole, let image = picture.cgImage else { return nil }
        let width = image.width, height = image.height
        var pixels = [UInt8](repeating: 0, count: width * height * 4)
        let copied = pixels.withUnsafeMutableBytes { buffer -> Bool in
            guard let context = CGContext(data: buffer.baseAddress, width: width, height: height, bitsPerComponent: 8, bytesPerRow: width * 4,
                                          space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return false }
            context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
            return true
        }
        guard copied, pixels.count >= 4, pixels[3] > 0 else { return nil }  // nothing drawn at all: no look
        return !MachineShellPlugin.oneColor(pixels)
    }

    /// Every pixel (RGBA) the first one's color, give or take. The colors don't matter: white in the light mode, black
    /// or dark in the dark one. A page with any word or line in sight never is.
    static func oneColor(_ pixels: [UInt8]) -> Bool {
        guard pixels.count >= 4 else { return false }
        let (r, g, b) = (Int(pixels[0]), Int(pixels[1]), Int(pixels[2]))
        for i in stride(from: 0, to: pixels.count - 3, by: 4)
        where abs(Int(pixels[i]) - r) > 6 || abs(Int(pixels[i + 1]) - g) > 6 || abs(Int(pixels[i + 2]) - b) > 6 { return false }
        return true
    }

    /// The same page put in the window anew, in two turns so the WebView notices: it draws again, nothing is reloaded.
    private func redraw() {
        guard let vc = bridge?.viewController, let window = vc.view.window, window.rootViewController === vc else { return }
        window.rootViewController = nil
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
            if window.rootViewController == nil { window.rootViewController = vc }
            self?.checkSoon(MachineShellPlugin.lookAgain)
        }
    }

    /// The last resort, what closing and opening the app does: a new WebView, which starts at the start page and opens
    /// the saved Machine. At most every freshGap. False when it can't be now.
    private func freshView() -> Bool {
        guard Date().timeIntervalSince(MachineShellPlugin.lastFresh) > MachineShellPlugin.freshGap, let vc = bridge?.viewController,
              let window = vc.view.window, window.rootViewController === vc, vc.presentedViewController == nil else { return false }
        MachineShellPlugin.lastFresh = Date()
        // This plugin goes with its view; until then it hears and asks nothing
        NotificationCenter.default.removeObserver(self)
        loading?.invalidate()
        wakeTimer?.invalidate()
        network.cancel()
        probing = true
        window.rootViewController = MachineViewController()
        return true
    }

    /// The app's own offline page (www/offline.html: can't reach your Machine, Try again), which tries again by itself
    /// once online or in front again. Never a white window, whatever came back instead of a page.
    private func showOffline() {
        guard let webView = bridge?.webView, let local = bridge?.config.localURL else { return }
        badTries = 0
        lastReopen = Date()
        webView.load(URLRequest(url: local.appendingPathComponent("offline.html")))
    }

    /// Cmd+R on a Mac or an iPad's keyboard: the page again, now.
    @objc func reloadPage() { reopen(force: true) }

    /// The page it had (the Machine's, or the app's own start or offline page), else the saved Machine, else the start page.
    private func reopen(force: Bool = false) {
        guard let webView = bridge?.webView else { return }
        guard force || Date().timeIntervalSince(lastReopen) > MachineShellPlugin.reopenGap else {
            if !againSoon { // too soon after the last one: checked again once it may, so the one that matters isn't lost
                againSoon = true
                DispatchQueue.main.asyncAfter(deadline: .now() + MachineShellPlugin.reopenGap) { [weak self] in
                    self?.againSoon = false
                    self?.checkPage()
                }
            }
            return
        }
        lastReopen = Date()
        pageGone = false
        let local = bridge?.config.localURL
        var target: URL?
        if let url = webView.url, url.scheme == "https" || (url.scheme == local?.scheme && url.host == local?.host) {
            target = url
        } else if let saved = machine {
            target = URL(string: saved)
        } else {
            target = local?.appendingPathComponent("index.html")
        }
        if let target = target { webView.load(URLRequest(url: target)) }
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
        // fetch: the Notification Service extension shows the to-do's title and next step (Shared/MachineNotice.swift)
        let device: [String: Any] = ["platform": "apns", "sandbox": sandbox, "label": UIDevice.current.model, "fetch": true]
        keepSignIn(saved)
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

extension MachineShellPlugin {
    /// The sign-in on the saved Machine (its cookies), for the Notification Service extension: in the app group's
    /// keychain, on this device only.
    func keepSignIn(_ saved: String) {
        guard let url = URL(string: saved), let host = url.host?.lowercased(),
              let cookies = bridge?.webView?.configuration.websiteDataStore.httpCookieStore else { return }
        cookies.getAllCookies { all in
            let mine = all.filter { c in
                let domain = c.domain.lowercased()
                let matches = domain.hasPrefix(".") ? host == String(domain.dropFirst()) || host.hasSuffix(domain) : host == domain
                return matches && url.path.hasPrefix(c.path) && (c.expiresDate.map { $0 > Date() } ?? true)
            }
            let header = HTTPCookie.requestHeaderFields(with: mine)["Cookie"] ?? ""
            DispatchQueue.global(qos: .utility).async { MachineNotice.save(machine: saved, cookies: header) }
        }
    }
}

/// The app's root view: Capacitor's, with MachineShellPlugin registered (it lives in the app, not in a package).
class MachineViewController: CAPBridgeViewController {
    private let shell = MachineShellPlugin()

    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(shell)
    }

    // Cmd+R (a Mac, an iPad's keyboard): always a way to bring the page back by hand
    override var keyCommands: [UIKeyCommand]? {
        (super.keyCommands ?? []) + [UIKeyCommand(input: "r", modifierFlags: .command, action: #selector(reloadPage))]
    }

    @objc func reloadPage() { shell.reloadPage() }
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

/// The WebView's navigation delegate (Capacitor's), and first to hear that the page's process ended, so the plugin
/// makes sure a page comes back (MachineShellPlugin.pageEnded) whatever happens to Capacitor's own reload.
private final class PageWatch: NSObject, WKNavigationDelegate {
    weak var inner: WKNavigationDelegate?
    weak var plugin: MachineShellPlugin?

    init(inner: WKNavigationDelegate?, plugin: MachineShellPlugin) {
        self.inner = inner
        self.plugin = plugin
    }

    override func responds(to aSelector: Selector!) -> Bool {
        super.responds(to: aSelector) || (inner?.responds(to: aSelector) ?? false)
    }

    override func forwardingTarget(for aSelector: Selector!) -> Any? {
        inner?.responds(to: aSelector) == true ? inner : nil
    }

    func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
        plugin?.pageEnded()
        inner?.webViewWebContentProcessDidTerminate?(webView)
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
