import UIKit
import UniformTypeIdentifiers

/// "Add to The Machine" in the share sheet. It only hands what was shared to the app, through the app group: text and
/// links, up to 5 files (10 MB together). The app opens it in the owner's Machine as a New to-do to check
/// (MachineShellPlugin.becameActive, www/inject.js). Nothing leaves the phone from here.
class ShareViewController: UIViewController {
    static let appGroup = "group.computer.themachine.app"
    static let maxFiles = 5
    static let maxBytes = 10 * 1024 * 1024

    private let label = UILabel()

    /// The same languages as the app and the dashboard (here, as this extension has no other strings)
    static let words: [String: (String, String)] = [
        "en": ("Added. Open The Machine to check it.", "That didn’t work. Try again from the app."),
        "nl": ("Toegevoegd. Open The Machine om het na te kijken.", "Dat lukte niet. Probeer het opnieuw vanuit de app."),
        "fr": ("Ajouté. Ouvrez The Machine pour le vérifier.", "Cela n’a pas marché. Réessayez depuis l’app."),
        "de": ("Hinzugefügt. Öffne The Machine, um es zu prüfen.", "Das hat nicht geklappt. Versuch es in der App noch mal."),
        "es": ("Añadido. Abre The Machine para revisarlo.", "No ha funcionado. Inténtalo de nuevo desde la app."),
        "it": ("Aggiunto. Apri The Machine per controllarlo.", "Non ha funzionato. Riprova dall’app."),
        "pt-BR": ("Adicionado. Abra The Machine para conferir.", "Não deu certo. Tente de novo pelo app."),
    ]

    static var lang: String {
        for l in Locale.preferredLanguages {
            if l.hasPrefix("pt") { return "pt-BR" }
            let base = String(l.prefix(2))
            if words[base] != nil { return base }
        }
        return "en"
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        label.numberOfLines = 0
        label.textAlignment = .center
        label.font = .preferredFont(forTextStyle: .body)
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)
        NSLayoutConstraint.activate([
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            label.leadingAnchor.constraint(equalTo: view.layoutMarginsGuide.leadingAnchor),
            label.trailingAnchor.constraint(equalTo: view.layoutMarginsGuide.trailingAnchor),
        ])
        Task { await collect() }
    }

    private func collect() async {
        var texts: [String] = []
        var files: [[String: String]] = []
        var bytes = 0
        guard let dir = FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: Self.appGroup)?
            .appendingPathComponent("share", isDirectory: true) else { return finish(ok: false) }
        try? FileManager.default.removeItem(at: dir)
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        let items = (extensionContext?.inputItems as? [NSExtensionItem]) ?? []
        for item in items {
            if let t = item.attributedContentText?.string, !t.isEmpty { texts.append(t) }
            for p in item.attachments ?? [] {
                if p.hasItemConformingToTypeIdentifier(UTType.url.identifier), !p.hasItemConformingToTypeIdentifier(UTType.fileURL.identifier),
                   let u = try? await p.loadItem(forTypeIdentifier: UTType.url.identifier) as? URL {
                    texts.append(u.absoluteString)
                } else if p.hasItemConformingToTypeIdentifier(UTType.plainText.identifier),
                          let t = try? await p.loadItem(forTypeIdentifier: UTType.plainText.identifier) as? String {
                    texts.append(t)
                } else if files.count < Self.maxFiles, let type = Self.fileType(p),
                          let data = await Self.data(p, type), bytes + data.count <= Self.maxBytes {
                    let name = "f\(files.count)"
                    guard (try? data.write(to: dir.appendingPathComponent(name))) != nil else { continue }
                    bytes += data.count
                    let ut = UTType(type)
                    files.append(["file": name, "name": Self.fileName(p.suggestedName ?? "file", ut?.preferredFilenameExtension),
                                  "type": ut?.preferredMIMEType ?? "application/octet-stream"])
                }
            }
        }
        var seen = Set<String>()
        let text = String(texts.filter { seen.insert($0).inserted }.joined(separator: "\n").prefix(20000))
        guard !text.isEmpty || !files.isEmpty,
              let json = try? JSONSerialization.data(withJSONObject: ["text": text, "files": files]),
              (try? json.write(to: dir.appendingPathComponent("pending.json"))) != nil else { return finish(ok: false) }
        finish(ok: true)
    }

    /// The file's own type (a PDF from Files or Mail is "com.adobe.pdf"), never the link to it ("public.file-url"),
    /// whose data would be the address instead of the file.
    static func fileType(_ p: NSItemProvider) -> String? {
        let ids = p.registeredTypeIdentifiers
        let isFile: (String) -> Bool = { id in UTType(id).map { $0.conforms(to: .data) && !$0.conforms(to: .url) } ?? false }
        let notLink: (String) -> Bool = { id in !(UTType(id)?.conforms(to: .url) ?? false) }
        return ids.first(where: isFile) ?? ids.first(where: notLink)
    }

    /// Its name with its extension once: the Machine takes a file by its extension ("Invoice 4471" gets ".pdf",
    /// "Invoice 4471.pdf" stays as it is).
    static func fileName(_ name: String, _ ext: String?) -> String {
        guard let ext = ext, !ext.isEmpty, !name.lowercased().hasSuffix("." + ext.lowercased()),
              !(ext == "jpeg" && name.lowercased().hasSuffix(".jpg")) else { return name }
        return name + "." + ext
    }

    private static func data(_ p: NSItemProvider, _ type: String) async -> Data? {
        await withCheckedContinuation { done in
            p.loadDataRepresentation(forTypeIdentifier: type) { data, _ in done.resume(returning: data) }
        }
    }

    private func finish(ok: Bool) {
        DispatchQueue.main.async {
            let words = Self.words[Self.lang] ?? Self.words["en"]!
            self.label.text = ok ? words.0 : words.1
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.6) {
                self.extensionContext?.completeRequest(returningItems: nil)
            }
        }
    }
}
