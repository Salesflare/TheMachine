import UIKit
import Capacitor
import UserNotifications

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        MachineActions.shared.install()  // a notification's button can start the app in the background
        MachineNotice.register()
        return true
    }

    // A clear push (content-available, no text): the to-do no longer waits, its notification goes. iOS may hold these
    // back, so opening the app also takes stale ones away (MachineNotice.sweep).
    func application(_ application: UIApplication, didReceiveRemoteNotification userInfo: [AnyHashable: Any],
                     fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {
        guard userInfo["kind"] as? String == "clear", let tag = userInfo["tag"] as? String, MachineNotice.validTag(tag) else {
            return completionHandler(.noData)
        }
        MachineNotice.clear(tag) { completionHandler(.newData) }
    }

    // Push: the token goes to @capacitor/push-notifications (www/app.js hands it on to MachineShellPlugin)
    func application(_ application: UIApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
        NotificationCenter.default.post(name: .capacitorDidRegisterForRemoteNotifications, object: deviceToken)
    }

    func application(_ application: UIApplication, didFailToRegisterForRemoteNotificationsWithError error: Error) {
        NotificationCenter.default.post(name: .capacitorDidFailToRegisterForRemoteNotifications, object: error)
    }

    func application(_ application: UIApplication,
                     configurationForConnecting connectingSceneSession: UISceneSession,
                     options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        let config = UISceneConfiguration(name: "Default Configuration",
                                          sessionRole: connectingSceneSession.role)
        config.delegateClass = SceneDelegate.self
        return config
    }
}

/// A notification's Do it, Snooze and Mark done (MachineNotice.register): the dashboard's own decision, sent after
/// the phone unlocks, without opening the app. Every other tap goes on to Capacitor's own delegate, as before.
final class MachineActions: NSObject, UNUserNotificationCenterDelegate {
    static let shared = MachineActions()
    private weak var inner: UNUserNotificationCenterDelegate?

    /// In front of whatever delegate is there (Capacitor sets its own when its page starts: installed again then).
    func install() {
        let center = UNUserNotificationCenter.current()
        guard center.delegate !== self else { return }
        inner = center.delegate
        center.delegate = self
    }

    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        if inner?.userNotificationCenter?(center, willPresent: notification, withCompletionHandler: completionHandler) == nil {
            completionHandler([.banner, .list, .sound])
        }
    }

    func userNotificationCenter(_ center: UNUserNotificationCenter, didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        let action = response.actionIdentifier, content = response.notification.request.content
        guard MachineNotice.buttons[action] != nil, let tag = content.userInfo["tag"] as? String, MachineNotice.validTag(tag) else {
            if inner?.userNotificationCenter?(center, didReceive: response, withCompletionHandler: completionHandler) == nil { completionHandler() }
            return
        }
        let events = content.userInfo["events"] as? [String: String] ?? [:]
        let app = UIApplication.shared
        var task = UIBackgroundTaskIdentifier.invalid, finished = false
        let finish = {
            DispatchQueue.main.async {
                guard !finished else { return }
                finished = true
                completionHandler()
                if task != .invalid { app.endBackgroundTask(task) }
            }
        }
        task = app.beginBackgroundTask { finish() }
        MachineNotice.decide(tag, action) { ok in
            guard ok else { return self.show(tag, content.title, events["failed"], stays: true, finish) }
            if action != "prepare" { return self.show(tag, content.title, events[action], stays: false, finish) }
            // Prepare: "Preparing: <title>" stays until the Ready notification for the same to-do replaces it
            MachineNotice.fetch(tag) { n in self.show(tag, n?.title ?? content.title, events[action], stays: true, finish) }
        }
    }

    /// What happened ("Snoozed it"), quietly in the list under the to-do's title; done or snoozed, it then goes.
    private func show(_ tag: String, _ title: String, _ line: String?, stays: Bool, _ finish: @escaping () -> Void) {
        guard let line = line, !line.isEmpty else { return stays ? finish() : MachineNotice.clear(tag, done: finish) }
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = line
        content.userInfo = ["tag": tag]
        content.interruptionLevel = .passive
        let center = UNUserNotificationCenter.current()
        center.add(UNNotificationRequest(identifier: tag, content: content, trigger: nil)) { _ in
            guard !stays else { return finish() }
            DispatchQueue.main.asyncAfter(deadline: .now() + 4) { MachineNotice.clear(tag, done: finish) }
        }
    }
}
