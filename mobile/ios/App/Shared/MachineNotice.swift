import Foundation
import Security
import UserNotifications

/// What a notification says and does, shared by the app and its Notification Service extension (mobile/README.md),
/// the same as android/.../MachinePushService.java. The push carries only a kind and an opaque to-do id; the
/// extension asks the owner's own Machine (GET api/notice) with the sign-in the app kept in the app group's keychain,
/// and shows the to-do's title and next step. Its buttons (Prepare, Snooze, Mark done) are the dashboard's own
/// decisions, after the phone unlocks; nothing is ever sent to anyone from a notification.
enum MachineNotice {
    static let group = "group.computer.themachine.app"
    private static let service = "computer.themachine.app.notice"
    /// A button and the dashboard's decision it makes: Prepare starts a to-do not started yet, Snooze is until tomorrow.
    static let buttons = ["prepare": "accept", "snooze": "snooze", "done": "complete"]
    static let fresh = "machine.todo.new"  // Prepare, Snooze, Mark done
    static let waiting = "machine.todo"    // Snooze, Mark done

    struct Notice {
        var title: String?
        var body = ""
        var actions: [String] = []
        var labels: [String: String] = [:]
        var events: [String: String] = [:]
        var gone = false
    }

    static func validTag(_ tag: String?) -> Bool {
        guard let tag = tag else { return false }
        return tag.range(of: "^[A-Za-z0-9_-]{1,64}$", options: .regularExpression) != nil
    }

    /// One plain line of at most `limit` characters, cut at a word with an ellipsis.
    static func clip(_ text: String?, _ limit: Int) -> String {
        let plain = (text ?? "").replacingOccurrences(of: "[\\x00-\\x1f\\x7f]", with: " ", options: .regularExpression)
            .replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression).trimmingCharacters(in: .whitespaces)
        if plain.count <= limit { return plain }
        var cut = String(plain.prefix(limit - 1))
        if let space = cut.lastIndex(of: " "), cut.distance(from: cut.startIndex, to: space) >= limit / 2 { cut = String(cut[..<space]) }
        return cut.replacingOccurrences(of: "[ ,;:.-]+$", with: "", options: .regularExpression) + "…"
    }

    // MARK: the sign-in, kept by the app for the extension (this device only, readable after the first unlock)

    private static func query() -> [String: Any] {
        [kSecClass as String: kSecClassGenericPassword, kSecAttrService as String: service,
         kSecAttrAccount as String: "machine", kSecAttrAccessGroup as String: group]
    }

    static func save(machine: String, cookies: String) {
        guard let data = try? JSONSerialization.data(withJSONObject: ["machine": machine, "cookies": cookies]) else { return }
        if let old = saved(), old.machine == machine, old.cookies == cookies { return }
        SecItemDelete(query() as CFDictionary)
        var item = query()
        item[kSecValueData as String] = data
        item[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
        SecItemAdd(item as CFDictionary, nil)
    }

    static func saved() -> (machine: String, cookies: String)? {
        var item = query()
        item[kSecReturnData as String] = true
        item[kSecMatchLimit as String] = kSecMatchLimitOne
        var found: CFTypeRef?
        guard SecItemCopyMatching(item as CFDictionary, &found) == errSecSuccess, let data = found as? Data,
              let o = try? JSONSerialization.jsonObject(with: data) as? [String: String],
              let machine = o["machine"], machine.hasPrefix("https://"), machine.hasSuffix("/") else { return nil }
        return (machine, o["cookies"] ?? "")
    }

    static func forget() {
        SecItemDelete(query() as CFDictionary)
    }

    // MARK: the Machine

    private final class NoRedirect: NSObject, URLSessionTaskDelegate {
        // a signed-out hosted Machine sends its sign-in page: no answer, never followed
        func urlSession(_ session: URLSession, task: URLSessionTask, willPerformHTTPRedirection response: HTTPURLResponse,
                        newRequest request: URLRequest, completionHandler: @escaping (URLRequest?) -> Void) {
            completionHandler(nil)
        }
    }

    private static let session: URLSession = {
        let config = URLSessionConfiguration.ephemeral
        config.timeoutIntervalForRequest = 8
        config.httpShouldSetCookies = false
        config.httpCookieAcceptPolicy = .never
        config.urlCache = nil
        return URLSession(configuration: config, delegate: NoRedirect(), delegateQueue: nil)
    }()

    private static func request(_ path: String, body: [String: Any]? = nil, csrf: String? = nil,
                                done: @escaping ([String: Any]?) -> Void) {
        guard let s = saved(), let url = URL(string: s.machine + path), let host = url.host else { return done(nil) }
        var r = URLRequest(url: url)
        r.setValue("application/json", forHTTPHeaderField: "Accept")
        if !s.cookies.isEmpty { r.setValue(s.cookies, forHTTPHeaderField: "Cookie") }
        if let body = body {
            r.httpMethod = "POST"
            r.httpBody = try? JSONSerialization.data(withJSONObject: body)
            r.setValue("application/json", forHTTPHeaderField: "Content-Type")
            r.setValue("https://" + host + (url.port.map { ":\($0)" } ?? ""), forHTTPHeaderField: "Origin")  // as its page sends
            r.setValue(csrf, forHTTPHeaderField: "X-CSRF-Token")
        }
        session.dataTask(with: r) { data, response, _ in
            guard (response as? HTTPURLResponse)?.statusCode == 200, let data = data, data.count <= 4096,
                  let o = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return done(nil) }
            done(o)
        }.resume()
    }

    /// What the Machine says about a to-do now, or nil when it can't be reached or says nothing.
    static func fetch(_ tag: String, done: @escaping (Notice?) -> Void) {
        guard validTag(tag) else { return done(nil) }
        request("api/notice?tag=" + tag) { o in
            guard let o = o else { return done(nil) }
            var n = Notice()
            n.gone = o["gone"] as? Bool == true
            let title = clip((o["title"] as? String) ?? (o["line"] as? String), 60)
            n.title = title.isEmpty ? nil : title
            n.body = clip(o["body"] as? String, 120)
            n.actions = ((o["actions"] as? [Any]) ?? []).compactMap { $0 as? String }.filter { buttons[$0] != nil }
            for (k, v) in (o["labels"] as? [String: Any]) ?? [:] { n.labels[k] = clip(v as? String, 24) }
            for (k, v) in (o["events"] as? [String: Any]) ?? [:] { n.events[k] = clip(v as? String, 120) }
            done(n.gone || n.title != nil ? n : nil)
        }
    }

    /// A button: the dashboard's own decision for this to-do, with its CSRF token. True when the Machine took it.
    static func decide(_ tag: String, _ action: String, done: @escaping (Bool) -> Void) {
        guard validTag(tag), let choice = buttons[action] else { return done(false) }
        request("api/session") { s in
            guard let csrf = s?["csrf"] as? String, !csrf.isEmpty else { return done(false) }
            var args: [String: Any] = ["suggestion_id": tag, "choice": choice, "feedback": "", "decision_id": UUID().uuidString.lowercased()]
            if choice == "snooze" { args["snooze_option"] = "tomorrow" }
            request("api/action", body: ["action": "decide", "args": args], csrf: csrf) { done($0 != nil) }
        }
    }

    // MARK: buttons

    static func category(_ actions: [String]) -> String? {
        actions.contains("prepare") ? fresh : actions.contains("done") || actions.contains("snooze") ? waiting : nil
    }

    /// The two kinds of buttons, in the owner's language (the Machine's labels, kept for the next start).
    /// Each needs the phone unlocked first and runs without opening the app.
    static func register(labels: [String: String]? = nil) {
        let defaults = UserDefaults(suiteName: group)
        if let labels = labels, !labels.isEmpty { defaults?.set(labels, forKey: "noticeLabels") }
        let kept = (defaults?.dictionary(forKey: "noticeLabels") as? [String: String]) ?? [:]
        func button(_ id: String, _ fallback: String) -> UNNotificationAction {
            UNNotificationAction(identifier: id, title: kept[id].flatMap { $0.isEmpty ? nil : $0 } ?? fallback, options: [.authenticationRequired])
        }
        let snooze = button("snooze", "Snooze"), done = button("done", "Mark done")
        UNUserNotificationCenter.current().setNotificationCategories([
            UNNotificationCategory(identifier: fresh, actions: [button("prepare", "Do it"), snooze, done], intentIdentifiers: []),
            UNNotificationCategory(identifier: waiting, actions: [snooze, done], intentIdentifiers: []),
        ])
    }

    // MARK: taking notifications away

    /// A to-do's notifications go (done, snoozed or sent, here or elsewhere).
    static func clear(_ tag: String, done: (() -> Void)? = nil) {
        let center = UNUserNotificationCenter.current()
        center.getDeliveredNotifications { list in
            let ids = list.filter { $0.request.identifier == tag || $0.request.content.userInfo["tag"] as? String == tag }.map { $0.request.identifier }
            center.removeDeliveredNotifications(withIdentifiers: ids)
            done?()
        }
    }

    /// Opening the app: the notifications for to-dos that no longer wait go (a clear push iOS held back).
    static func sweep() {
        UNUserNotificationCenter.current().getDeliveredNotifications { list in
            var tags: [String] = []
            for n in list { if let t = n.request.content.userInfo["tag"] as? String, validTag(t), !tags.contains(t) { tags.append(t) } }
            for tag in tags.prefix(20) {
                fetch(tag) { notice in if notice?.gone == true { clear(tag) } }
            }
        }
    }
}
