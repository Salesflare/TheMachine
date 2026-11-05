package computer.themachine.app;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

/**
 * The name a shared or opened file goes to the Machine with (MachineShellPlugin.readShare). The Machine takes a file by
 * its extension (chat_files.py), and some apps hand one over without it ("Invoice 4471" from Drive, "document" from
 * mail): then the extension of its type is added. Tested on its own (ShareNameTest).
 */
final class ShareName {

    static final Map<String, String> EXTENSION = new HashMap<>();  // not Map.of: that needs Android 11

    static {
        String[][] pairs = {{"application/pdf", "pdf"}, {"image/png", "png"}, {"image/jpeg", "jpg"}, {"image/gif", "gif"},
            {"image/webp", "webp"}, {"text/plain", "txt"}, {"text/markdown", "md"}, {"text/csv", "csv"}, {"text/calendar", "ics"},
            {"application/json", "json"}};
        for (String[] p : pairs) EXTENSION.put(p[0], p[1]);
    }

    private ShareName() {}

    static String of(String name, String type) {
        String clean = name == null ? "" : name.replaceAll("[\\x00-\\x1f/\\\\]", "_").trim();
        if (clean.isEmpty()) clean = "file";
        String ext = type == null ? null : EXTENSION.get(type.toLowerCase(Locale.ROOT).split(";")[0].trim());
        if (ext == null) return clean;
        String lower = clean.toLowerCase(Locale.ROOT);
        if (lower.endsWith("." + ext) || (ext.equals("jpg") && lower.endsWith(".jpeg")) || (ext.equals("md") && lower.endsWith(".markdown"))) return clean;
        return clean + "." + ext;
    }
}
