import UserNotifications

/// The Notification Service extension: a push from the control plane carries only the to-do's kind, its opaque id
/// and fixed words ("A to-do is ready"). This asks the owner's own Machine for the to-do's title and next step
/// (Shared/MachineNotice.swift) and shows those, with its buttons. Without an answer the fixed words stay. When the
/// phone hides previews on the lock screen, iOS shows neither.
class NotificationService: UNNotificationServiceExtension {
    private var handler: ((UNNotificationContent) -> Void)?
    private var content: UNMutableNotificationContent?
    private let lock = NSLock()

    override func didReceive(_ request: UNNotificationRequest, withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {
        let content = (request.content.mutableCopy() as? UNMutableNotificationContent) ?? UNMutableNotificationContent()
        lock.lock(); handler = contentHandler; self.content = content; lock.unlock()
        guard let tag = content.userInfo["tag"] as? String, MachineNotice.validTag(tag) else { return finish(nil) }
        MachineNotice.fetch(tag, kind: content.userInfo["kind"] as? String) { [weak self] notice in self?.finish(notice) }
    }

    override func serviceExtensionTimeWillExpire() {
        finish(nil)  // the fixed words
    }

    private func finish(_ notice: MachineNotice.Notice?) {
        lock.lock()
        let done = handler, content = self.content
        handler = nil
        lock.unlock()
        guard let deliver = done, let content = content else { return }
        if let n = notice, !n.gone, let title = n.title {
            content.title = title
            content.body = n.body
            if let category = MachineNotice.category(n.actions) {
                MachineNotice.register(labels: n.labels, actions: n.actions)
                content.categoryIdentifier = category
            }
            content.userInfo["events"] = n.events
        }
        deliver(content)
    }
}
