package computer.themachine.app;

import android.Manifest;
import android.content.ContentResolver;
import android.content.pm.PackageManager;
import android.provider.Settings;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import android.content.ActivityNotFoundException;
import android.content.ContentValues;
import android.os.Build;
import android.provider.MediaStore;
import android.webkit.MimeTypeMap;
import android.webkit.PermissionRequest;
import android.webkit.URLUtil;
import android.widget.Toast;
import androidx.core.content.FileProvider;
import androidx.core.app.NotificationManagerCompat;
import androidx.webkit.JavaScriptReplyProxy;
import androidx.webkit.WebViewCompat;
import com.google.firebase.messaging.FirebaseMessaging;
import androidx.webkit.WebViewFeature;
import com.getcapacitor.Bridge;
import com.getcapacitor.BridgeWebChromeClient;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.Collections;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.provider.OpenableColumns;
import android.util.Base64;
import android.webkit.WebView;
import androidx.browser.customtabs.CustomTabsIntent;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.WebViewListener;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.Inet4Address;
import java.net.Inet6Address;
import java.net.InetAddress;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * The app's whole native part on Android (mobile/README.md): where the owner's Machine is, the account's sign-in in the
 * system browser (Custom Tab, so passkeys and the phone's own unlock work), which pages the app's WebView may open,
 * push tokens and the share sheet. What it does inside the Machine's page is www/inject.js, the same on iOS.
 *
 * Only the app's own start page (https://localhost) may change the saved Machine or start a sign-in: the Machine's
 * page, or anything it links to, never can.
 */
@CapacitorPlugin(name = "MachineShell")
public class MachineShellPlugin extends Plugin {

    static final String HOSTED = "app.themachine.computer";
    static final int OWN_PORT = 8443;
    static final String SCHEME = "computer.themachine.app";
    private static final String PREFS = "machine_shell";
    private static final Pattern LABEL = Pattern.compile("[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?");
    private static final Pattern TOKEN = Pattern.compile("[A-Za-z0-9_-]{20,100}");
    private static final Pattern TAG = Pattern.compile("[A-Za-z0-9_-]{1,64}");
    private static final long SIGNIN_TTL = 10 * 60 * 1000L;
    private static final int SHARE_FILES = 5;
    private static final long SHARE_BYTES = 10L * 1024 * 1024;

    private JSONObject pendingShare;
    private String pendingTag;
    private String injectSource;

    @Override
    public void load() {
        handleIntent(getActivity().getIntent());
    }

    /**
     * From MainActivity once the bridge is built: Capacitor sets a bridge's page listeners after its plugins load, so
     * one added in load() is dropped and the Machine's page would never get www/inject.js (push, share, a tapped
     * notification). Also the page's microphone (only for the Machine itself) and its downloads.
     */
    void attach() {
        bridge.addWebViewListener(
            new WebViewListener() {
                @Override
                public void onPageLoaded(WebView webView) {
                    onMachinePage(webView.getUrl());
                }
            }
        );
        WebView webView = bridge.getWebView();
        webView.setWebChromeClient(new MachineChrome(bridge, this));
        webView.setDownloadListener((url, userAgent, disposition, mime, length) -> onDownload(url, disposition, mime));
        ensureFiles();
    }

    /** The saved Machine's origin, "https://host[:port]", or null. */
    String machineOrigin() {
        String saved = machine();
        if (saved == null) return null;
        Uri m = Uri.parse(saved);
        return "https://" + m.getHost() + (m.getPort() == -1 ? "" : ":" + m.getPort());
    }

    /** Whether a page's origin is the saved Machine's (scheme, host and port). */
    boolean isMachine(Uri origin) {
        String want = machineOrigin();
        if (want == null || origin == null || !"https".equals(origin.getScheme()) || origin.getHost() == null) return false;
        return want.equals("https://" + origin.getHost().toLowerCase() + (origin.getPort() == -1 || origin.getPort() == 443 ? "" : ":" + origin.getPort()));
    }

    /**
     * The WebView's microphone: only for the Machine's own page, and only audio; Capacitor's client asks the phone.
     * A No the phone won't ask again for (a second No, or no question shown at all) is kept, for micState.
     */
    static class MachineChrome extends BridgeWebChromeClient {
        private final MachineShellPlugin shell;

        MachineChrome(Bridge bridge, MachineShellPlugin shell) {
            super(bridge);
            this.shell = shell;
        }

        @Override
        public void onPermissionRequest(PermissionRequest request) {
            boolean audioOnly = request.getResources().length > 0;
            for (String r : request.getResources()) audioOnly &= PermissionRequest.RESOURCE_AUDIO_CAPTURE.equals(r);
            if (!audioOnly || !shell.isMachine(request.getOrigin())) {
                request.deny();
                return;
            }
            long asked = System.currentTimeMillis();
            super.onPermissionRequest(new PermissionRequest() {
                @Override
                public Uri getOrigin() {
                    return request.getOrigin();
                }

                @Override
                public String[] getResources() {
                    return request.getResources();
                }

                @Override
                public void grant(String[] resources) {
                    shell.prefs().edit().remove("micDenied").remove("micBlocked").apply();
                    request.grant(resources);
                }

                @Override
                public void deny() {
                    boolean again = ActivityCompat.shouldShowRequestPermissionRationale(shell.getActivity(), Manifest.permission.RECORD_AUDIO);
                    boolean fast = System.currentTimeMillis() - asked < 400; // no question was shown
                    boolean before = shell.prefs().getBoolean("micDenied", false);
                    shell.prefs().edit().putBoolean("micDenied", true).putBoolean("micBlocked", !again && (fast || before)).apply();
                    request.deny();
                }
            });
        }
    }

    // -- the phone's own questions, for the Machine's page (www/inject.js, MachinePhone): the microphone's and
    // notifications' state, notifications on (the phone's own question, then the push token) and the app's settings page

    static final int ASK_PUSH = 7301;
    private JavaScriptReplyProxy pushReply;
    private String pushId;
    private long pushAsked;

    private void phone(JSONObject m, JavaScriptReplyProxy reply) {
        String id = m.optString("id", "");
        switch (m.optString("ask", "")) {
            case "mic":
                answer(reply, id, micState(), null);
                break;
            case "push":
                answer(reply, id, pushState(), null);
                break;
            case "settings":
                Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", getContext().getPackageName(), null));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                try {
                    getContext().startActivity(intent);
                    answer(reply, id, "ok", null);
                } catch (ActivityNotFoundException e) {
                    answer(reply, id, "off", null);
                }
                break;
            case "pushOn":
                pushOn(reply, id);
                break;
            default:
                break;
        }
    }

    private void answer(JavaScriptReplyProxy reply, String id, String state, String token) {
        bridge.executeOnMainThread(() -> {
            try {
                JSONObject out = new JSONObject().put("id", id).put("state", state);
                if (token != null) out.put("token", token);
                reply.postMessage(out.toString());
            } catch (JSONException | RuntimeException e) {
                // the page is gone
            }
        });
    }

    /** granted, prompt (the phone asks) or blocked (only the phone's settings change it). */
    private String micState() {
        if (ContextCompat.checkSelfPermission(getContext(), Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            prefs().edit().remove("micDenied").remove("micBlocked").apply(); // allowed in settings: asked afresh if taken back
            return "granted";
        }
        boolean again = ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.RECORD_AUDIO);
        return !again && prefs().getBoolean("micBlocked", false) ? "blocked" : "prompt";
    }

    private boolean pushReady() {
        Context c = getContext();
        return c.getResources().getIdentifier("google_app_id", "string", c.getPackageName()) != 0;
    }

    private String pushState() {
        if (!pushReady()) return "off";
        boolean shown = NotificationManagerCompat.from(getContext()).areNotificationsEnabled();
        if (Build.VERSION.SDK_INT < 33) return shown ? "granted" : "blocked"; // no question to ask: only settings
        String perm = Manifest.permission.POST_NOTIFICATIONS;
        if (ContextCompat.checkSelfPermission(getContext(), perm) == PackageManager.PERMISSION_GRANTED) {
            prefs().edit().remove("pushDenied").remove("pushBlocked").apply();
            return shown ? "granted" : "blocked";
        }
        if (ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), perm)) return "prompt";
        // a No for good: from this question, or from the start page's (Capacitor keeps that one)
        boolean capacitor = "denied".equals(getContext().getSharedPreferences("PluginPermStates", Context.MODE_PRIVATE).getString(perm, null));
        return prefs().getBoolean("pushBlocked", false) || capacitor ? "blocked" : "prompt";
    }

    private void pushOn(JavaScriptReplyProxy reply, String id) {
        String state = pushState();
        if (state.equals("granted")) pushToken(reply, id);
        else if (!state.equals("prompt") || Build.VERSION.SDK_INT < 33) answer(reply, id, state, null);
        else {
            pushReply = reply;
            pushId = id;
            pushAsked = System.currentTimeMillis();
            ActivityCompat.requestPermissions(getActivity(), new String[] {Manifest.permission.POST_NOTIFICATIONS}, ASK_PUSH);
        }
    }

    /** From MainActivity: the phone's answer to pushOn's question. */
    void pushAnswered(boolean granted) {
        JavaScriptReplyProxy reply = pushReply;
        String id = pushId;
        pushReply = null;
        if (reply == null) return;
        if (granted) {
            prefs().edit().remove("pushBlocked").apply();
            pushToken(reply, id);
            return;
        }
        boolean again = Build.VERSION.SDK_INT >= 33 && ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.POST_NOTIFICATIONS);
        boolean fast = System.currentTimeMillis() - pushAsked < 400; // no question was shown
        boolean blocked = !again && (fast || prefs().getBoolean("pushDenied", false));
        prefs().edit().putBoolean("pushDenied", true).putBoolean("pushBlocked", blocked).apply();
        answer(reply, id, blocked ? "blocked" : "off", null);
    }

    private void pushToken(JavaScriptReplyProxy reply, String id) {
        try {
            FirebaseMessaging.getInstance().getToken().addOnCompleteListener(task -> {
                String token = task.isSuccessful() ? task.getResult() : null;
                if (token == null || !token.matches("[A-Za-z0-9_:-]{20,4096}")) {
                    answer(reply, id, "off", null);
                    return;
                }
                prefs().edit().putString("pushToken", token).apply();
                answer(reply, id, "on", token);
            });
        } catch (RuntimeException e) { // Firebase not set up
            answer(reply, id, "off", null);
        }
    }

    // -- downloads: www/inject.js hands the Machine's files over (MachineFiles), saved to the phone's Downloads

    private static final long FILE_BYTES = 25L * 1024 * 1024;
    private String filesOrigin;

    /** The page's MachineFiles and MachinePhone objects, there for the saved Machine's origin only (from its next page on). */
    void ensureFiles() {
        String origin = machineOrigin();
        if (origin == null || origin.equals(filesOrigin) || !WebViewFeature.isFeatureSupported(WebViewFeature.WEB_MESSAGE_LISTENER)) return;
        WebView webView = bridge.getWebView();
        if (filesOrigin != null) {
            WebViewCompat.removeWebMessageListener(webView, "MachineFiles");
            WebViewCompat.removeWebMessageListener(webView, "MachinePhone");
        }
        filesOrigin = origin;
        WebViewCompat.addWebMessageListener(webView, "MachineFiles", Collections.singleton(origin), (view, message, source, mainFrame, reply) -> {
            if (!mainFrame || !isMachine(source) || message.getData() == null) return;
            String data = message.getData();
            new Thread(() -> saveFile(data)).start();
        });
        WebViewCompat.addWebMessageListener(webView, "MachinePhone", Collections.singleton(origin), (view, message, source, mainFrame, reply) -> {
            if (!mainFrame || !isMachine(source) || message.getData() == null) return;
            try {
                phone(new JSONObject(message.getData()), reply);
            } catch (JSONException e) {
                // not a question
            }
        });
    }

    private void onDownload(String url, String disposition, String mime) {
        String origin = machineOrigin();
        if (url == null) return;
        if (origin != null && (url.startsWith(origin + "/") || url.startsWith("blob:" + origin + "/"))) {
            String name = URLUtil.guessFileName(url, disposition, mime);
            bridge.getWebView().evaluateJavascript("window.__machineFiles&&window.__machineFiles(" + JSONObject.quote(url) + "," + JSONObject.quote(name) + ")", null);
            return;
        }
        if (url.startsWith("https://")) openOutside(Uri.parse(url));
    }

    static String fileName(String name) {
        String clean = name == null ? "" : name.replaceAll("[\\\\/:*?\"<>|\\x00-\\x1f]", "_").trim();
        if (clean.isEmpty() || clean.startsWith(".")) clean = "file" + clean;
        return clean.length() > 120 ? clean.substring(clean.length() - 120) : clean;
    }

    private void saveFile(String json) {
        try {
            JSONObject o = new JSONObject(json);
            String b64 = o.optString("data", "");
            if (b64.length() > FILE_BYTES * 4 / 3 + 4) return;
            byte[] bytes = Base64.decode(b64, Base64.DEFAULT);
            String name = fileName(o.optString("name", "file"));
            String type = o.optString("type", "");
            if (!type.matches("[a-z]+/[A-Za-z0-9.+-]+") || type.equals("application/octet-stream")) { // by its name, then
                String ext = MimeTypeMap.getFileExtensionFromUrl(Uri.encode(name)).toLowerCase(java.util.Locale.ROOT);
                String guess = MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext);
                type = guess != null ? guess : "application/octet-stream";
            }
            Context c = getContext();
            // A file the owner opened (a link to it, not a download): an app on the phone shows it; none, it's saved
            if (o.optBoolean("open", false) && !type.equals("application/octet-stream")) {
                Uri u = FileProvider.getUriForFile(c, c.getPackageName() + ".fileprovider", cacheFile(c, name, bytes));
                Intent view = new Intent(Intent.ACTION_VIEW).setDataAndType(u, type)
                        .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
                try {
                    c.startActivity(view);
                    return;
                } catch (ActivityNotFoundException e) {
                    // nothing opens this type: saved below
                }
            }
            if (Build.VERSION.SDK_INT >= 29) {
                ContentValues v = new ContentValues();
                v.put(MediaStore.Downloads.DISPLAY_NAME, name);
                v.put(MediaStore.Downloads.MIME_TYPE, type);
                v.put(MediaStore.Downloads.IS_PENDING, 1);
                Uri item = c.getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
                if (item == null) return;
                try (OutputStream out = c.getContentResolver().openOutputStream(item)) {
                    out.write(bytes);
                    v.clear();
                    v.put(MediaStore.Downloads.IS_PENDING, 0);
                    c.getContentResolver().update(item, v, null, null);
                } catch (IOException | RuntimeException e) { // e.g. a stale Downloads entry of that name: not kept half
                    c.getContentResolver().delete(item, null, null);
                    throw e;
                }
                String said = c.getString(R.string.saved_download, name);
                bridge.executeOnMainThread(() -> Toast.makeText(c, said, Toast.LENGTH_SHORT).show());
            } else { // before Android 10 there is no Downloads to write to without a storage permission: share it
                Uri u = FileProvider.getUriForFile(c, c.getPackageName() + ".fileprovider", cacheFile(c, name, bytes));
                Intent send = new Intent(Intent.ACTION_SEND).setType(type).putExtra(Intent.EXTRA_STREAM, u).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                Intent chooser = Intent.createChooser(send, name).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                c.startActivity(chooser);
            }
        } catch (JSONException | IOException | RuntimeException e) { // on its own thread: never takes the app down
            bridge.executeOnMainThread(() -> Toast.makeText(getContext(), R.string.not_saved, Toast.LENGTH_SHORT).show());
        }
    }

    private static File cacheFile(Context c, String name, byte[] bytes) throws IOException {
        File dir = new File(c.getCacheDir(), "files");
        dir.mkdirs();
        File f = new File(dir, name);
        try (OutputStream out = new FileOutputStream(f)) {
            out.write(bytes);
        }
        return f;
    }

    // -- which pages the WebView opens

    static boolean hostedHost(String host) {
        if (host == null || !host.endsWith("." + HOSTED)) return false;
        String name = host.substring(0, host.length() - HOSTED.length() - 1);
        return !name.contains(".") && LABEL.matcher(name).matches();
    }

    static boolean tailnetHost(String host) {
        if (host == null || !host.endsWith(".ts.net")) return false;
        String[] parts = host.split("\\.", -1);
        if (parts.length < 4) return false;
        for (String p : parts) if (!LABEL.matcher(p).matches()) return false;
        return true;
    }

    /**
     * A self-hosted Machine's host: a tailnet name, or a public DNS name (two labels or more, a top level of letters, so
     * never an IP address or a bare name). Never a hosted Machine's: those come through sign-in. Same as www/machine-url.js.
     */
    static boolean ownHost(String host) {
        if (host == null) return false;
        if (host.endsWith(".ts.net")) return tailnetHost(host);
        if (host.length() > 253 || host.equals(HOSTED) || host.endsWith("." + HOSTED)) return false;
        String[] parts = host.split("\\.", -1);
        if (parts.length < 2 || !parts[parts.length - 1].matches("[a-z]{2,63}")) return false;
        for (String p : parts) if (!LABEL.matcher(p).matches()) return false;
        return true;
    }

    /** The port a URL goes to: 443 when it names none. */
    static int portOf(Uri u) {
        return u.getPort() == -1 ? 443 : u.getPort();
    }

    /**
     * A Machine address the app may save: https and no user, a hosted Machine's root on 443, or a self-hosted one
     * (ownHost) on 443 or 8443 (a self-hosted Machine's default port). No other port. Plain java.net.URI, so the rules
     * run in a JVM unit test (src/test).
     */
    static String normalMachine(String url) {
        if (url == null) return null;
        URI u;
        try {
            u = new URI(url);
        } catch (URISyntaxException e) {
            return null;
        }
        String host = u.getHost() == null ? null : u.getHost().toLowerCase();
        if (!"https".equals(u.getScheme()) || u.getRawUserInfo() != null || host == null) return null;
        int port = u.getPort() == -1 ? 443 : u.getPort();
        if (hostedHost(host)) return port == 443 ? "https://" + host + "/" : null;
        if (!ownHost(host) || (port != 443 && port != OWN_PORT)) return null;
        if (port == OWN_PORT) host += ":" + OWN_PORT;
        String path = u.getRawPath() == null || u.getRawPath().isEmpty() ? "/" : u.getRawPath();
        if (!path.endsWith("/")) path += "/";
        if (!path.matches("/(?:[A-Za-z0-9._~-]+/)*")) return null;
        return "https://" + host + path;
    }

    SharedPreferences prefs() {
        return getContext().getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    private String machine() {
        return normalMachine(prefs().getString("machine", null));
    }

    private boolean onStartPage() {
        String url = bridge.getWebView().getUrl();
        return url != null && Uri.parse(url).getHost() != null && Uri.parse(url).getHost().equals(bridge.getHost());
    }

    @Override
    public Boolean shouldOverrideLoad(Uri url) {
        String scheme = url.getScheme();
        String host = url.getHost() == null ? "" : url.getHost().toLowerCase();
        if ("https".equals(scheme) && host.equals(bridge.getHost())) return false; // the app's own pages
        String saved = machine();
        if ("https".equals(scheme) && saved != null) {
            Uri m = Uri.parse(saved);
            // A hosted Machine may move to its owner's new name: any hosted dashboard host, the account checks whose
            if (host.equals(m.getHost()) && portOf(url) == portOf(m)) return false;
            if (hostedHost(m.getHost()) && hostedHost(host) && portOf(url) == 443) return false;
            if (host.equals(HOSTED) && hostedHost(m.getHost())) {
                String path = url.getPath() == null ? "/" : url.getPath();
                if (path.equals("/open") || path.equals("/login")) { // the dashboard's sign-in ran out: sign in again
                    bridge.executeOnMainThread(() -> startSignIn(null));
                    return true;
                }
            }
        }
        openOutside(url); // everything else (links in mail, the account's other pages): the phone's browser
        return true;
    }

    private void openOutside(Uri url) {
        String scheme = url.getScheme();
        if (!"https".equals(scheme) && !"http".equals(scheme) && !"mailto".equals(scheme) && !"tel".equals(scheme)) return;
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW, url);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(intent);
        } catch (Exception e) {
            // nothing on the phone opens it
        }
    }

    // -- methods for the start page (www/app.js)

    @PluginMethod
    public void get(PluginCall call) {
        JSObject out = new JSObject();
        out.put("machine", machine());
        String connect = prefs().getString("connect", null);
        if (connect != null) out.put("connect", connect);
        if (prefs().getBoolean("signinStopped", false)) {
            out.put("signin", "stopped");
            prefs().edit().remove("signinStopped").apply();
        }
        call.resolve(out);
    }

    @PluginMethod
    public void info(PluginCall call) {
        JSObject out = new JSObject();
        out.put("platform", "android");
        // Firebase is set up when the build had a google-services.json (mobile/README.md, Push)
        Context c = getContext();
        out.put("pushReady", c.getResources().getIdentifier("google_app_id", "string", c.getPackageName()) != 0);
        boolean tailscale;
        try {
            c.getPackageManager().getPackageInfo("com.tailscale.ipn", 0);
            tailscale = true;
        } catch (android.content.pm.PackageManager.NameNotFoundException e) {
            tailscale = false;
        }
        out.put("tailscale", tailscale);
        call.resolve(out);
    }

    @PluginMethod
    public void setMachine(PluginCall call) {
        bridge.executeOnMainThread(() -> { // the WebView is only read on its own thread
            if (!onStartPage()) {
                call.reject("not allowed");
                return;
            }
            String url = normalMachine(call.getString("url"));
            if (url == null || !url.equals(call.getString("url"))) {
                call.reject("not a Machine address");
                return;
            }
            prefs().edit().putString("machine", url).remove("connect").apply();
            ensureFiles();
            call.resolve();
        });
    }

    /**
     * Before a Machine of their own is saved: {machine: true} when its manifest answers as a Machine's (the same rule
     * as www/machine-url.js isMachine), else {machine: false}. Never the answer itself. Rejects when it can't be
     * reached, or when its name leads to the phone itself or its local network (publicOrTailnet). No redirects
     * followed, no cookies, a short wait and a small body.
     */
    @PluginMethod
    public void check(PluginCall call) {
        bridge.executeOnMainThread(() -> { // only the start page asks, never a Machine's page or what it links to
            if (!onStartPage()) {
                call.reject("not allowed");
                return;
            }
            String url = normalMachine(call.getString("url"));
            if (url == null || !url.equals(call.getString("url")) || !ownHost(Uri.parse(url).getHost())) {
                call.reject("not a Machine address");
                return;
            }
            new Thread(() -> fetchManifest(call, url)).start();
        });
    }

    /**
     * Where check may go: a public address, or a tailnet one (100.64.0.0/10, fd7a:115c:a1e0::/48). Never the phone
     * itself, its local network, link-local or multicast addresses, so a typed or linked name can't reach them.
     */
    static boolean publicOrTailnet(InetAddress a) {
        if (a.isAnyLocalAddress() || a.isLoopbackAddress() || a.isLinkLocalAddress() || a.isSiteLocalAddress()
                || a.isMulticastAddress()) return false;
        byte[] b = a.getAddress();
        if (a instanceof Inet4Address) {
            int x = b[0] & 0xff, y = b[1] & 0xff;
            if (x == 100 && (y & 0xc0) == 64) return true; // tailnet (CGNAT)
            return x != 0 && x != 127 && !(x == 169 && y == 254) && !(x == 192 && y == 0 && (b[2] & 0xff) == 0)
                    && !(x == 198 && (y == 18 || y == 19)) && x < 224;
        }
        if (a instanceof Inet6Address) {
            if ((b[0] & 0xff) == 0xfd && (b[1] & 0xff) == 0x7a && (b[2] & 0xff) == 0x11 && (b[3] & 0xff) == 0x5c
                    && (b[4] & 0xff) == 0xa1 && (b[5] & 0xff) == 0xe0) return true; // tailnet
            return (b[0] & 0xfe) != 0xfc; // unique local fc00::/7
        }
        return false;
    }

    /** A Machine's manifest, or its refusal to anyone off its tailnet: the same rule as www/machine-url.js isMachine. */
    static boolean manifestIsMachine(int status, String body) {
        try {
            JSONObject data = new JSONObject(body);
            if (status == 200) return "The Machine".equals(data.opt("name")) && data.opt("start_url") instanceof String
                    && data.opt("icons") instanceof JSONArray;
            if (status == 403) return "Use the owner-authenticated Tailscale dashboard".equals(data.opt("error"));
        } catch (JSONException | RuntimeException e) {
            return false;
        }
        return false;
    }

    /** The owner's own typed address only (check): https on 443 or 8443 to a DNS name, never an IP address. */
    private static void fetchManifest(PluginCall call, String url) {
        HttpURLConnection c = null;
        try {
            for (InetAddress a : InetAddress.getAllByName(Uri.parse(url).getHost())) {
                if (!publicOrTailnet(a)) {
                    call.reject("not a Machine address");
                    return;
                }
            }
            c = (HttpURLConnection) new URL(url + "manifest.webmanifest").openConnection();
            c.setInstanceFollowRedirects(false);
            c.setUseCaches(false);
            c.setConnectTimeout(8000);
            c.setReadTimeout(8000);
            c.setRequestProperty("Accept", "application/manifest+json, application/json");
            int status = c.getResponseCode();
            InputStream in = status >= 400 ? c.getErrorStream() : c.getInputStream();
            byte[] body = in == null ? new byte[0] : read(in, 64 * 1024);
            JSObject out = new JSObject();
            out.put("machine", body != null && manifestIsMachine(status, new String(body, StandardCharsets.UTF_8)));
            call.resolve(out);
        } catch (IOException | ClassCastException e) {
            call.reject("unreachable");
        } finally {
            if (c != null) c.disconnect();
        }
    }

    @PluginMethod
    public void clearConnect(PluginCall call) {
        prefs().edit().remove("connect").apply();
        call.resolve();
    }

    @PluginMethod
    public void forget(PluginCall call) {
        bridge.executeOnMainThread(() -> { // the WebView is only read on its own thread
            if (!onStartPage()) {
                call.reject("not allowed");
                return;
            }
            prefs().edit().remove("machine").apply();
            call.resolve();
        });
    }

    @PluginMethod
    public void pushToken(PluginCall call) {
        String token = call.getString("token", "");
        if (token == null || !token.matches("[A-Za-z0-9_:-]{20,4096}")) {
            call.reject("not a push token");
            return;
        }
        prefs().edit().putString("pushToken", token).apply();
        call.resolve();
    }

    @PluginMethod
    public void signIn(PluginCall call) {
        bridge.executeOnMainThread(() -> { // the WebView is only read on its own thread
            if (!onStartPage()) {
                call.reject("not allowed");
                return;
            }
            startSignIn(call);
        });
    }

    /** The account's sign-in in a Custom Tab; it comes back as computer.themachine.app://signed-in (handleIntent). */
    private void startSignIn(PluginCall call) {
        byte[] raw = new byte[32];
        new SecureRandom().nextBytes(raw);
        String verifier = b64(raw);
        String challenge;
        try {
            challenge = b64(MessageDigest.getInstance("SHA-256").digest(verifier.getBytes(StandardCharsets.US_ASCII)));
        } catch (NoSuchAlgorithmException e) {
            if (call != null) call.reject("no sha-256");
            return;
        }
        prefs().edit().putString("verifier", verifier).putLong("verifierAt", System.currentTimeMillis()).apply();
        Uri start = Uri.parse("https://" + HOSTED + "/open").buildUpon().appendQueryParameter("to", "app")
            .appendQueryParameter("c", challenge).build();
        try {
            new CustomTabsIntent.Builder().setShowTitle(true).build().launchUrl(getActivity(), start);
        } catch (Exception e) {
            openOutside(start);
        }
        if (call != null) call.resolve();
    }

    private static String b64(byte[] bytes) {
        return Base64.encodeToString(bytes, Base64.URL_SAFE | Base64.NO_PADDING | Base64.NO_WRAP);
    }

    // -- coming back: the sign-in, a connect link, the share sheet, a tapped notification

    @Override
    protected void handleOnNewIntent(Intent intent) {
        super.handleOnNewIntent(intent);
        handleIntent(intent);
    }

    @Override
    protected void handleOnResume() {
        super.handleOnResume();
        // Back from the Custom Tab without finishing: show the start page again, with a note
        long at = prefs().getLong("verifierAt", 0);
        if (at != 0 && System.currentTimeMillis() - at > 1500 && !returning) {
            prefs().edit().remove("verifier").remove("verifierAt").putBoolean("signinStopped", true).apply();
            if (onStartPage()) bridge.getWebView().loadUrl(bridge.getLocalUrl() + "/index.html");
        }
        returning = false;
    }

    private boolean returning;

    private void handleIntent(Intent intent) {
        if (intent == null) return;
        String action = intent.getAction();
        Uri data = intent.getData();
        if (Intent.ACTION_VIEW.equals(action) && data != null && SCHEME.equals(data.getScheme())) {
            if ("signed-in".equals(data.getHost())) {
                returning = true;
                if (data.getQueryParameter("m") != null) signedInOwn(data.getQueryParameter("m"));
                else signedIn(data.getQueryParameter("u"));
            } else if ("connect".equals(data.getHost())) {
                String url = normalMachine(data.getQueryParameter("u"));
                if (url != null && tailnetHost(Uri.parse(url).getHost())) { // asked on the start page before it counts
                    prefs().edit().putString("connect", url).apply();
                    bridge.getWebView().loadUrl(bridge.getLocalUrl() + "/index.html");
                }
            }
            intent.setData(null);
            return;
        }
        if (Intent.ACTION_SEND.equals(action) || Intent.ACTION_SEND_MULTIPLE.equals(action)) {
            pendingShare = readShare(intent);
            intent.setAction(null);
            String url = bridge.getWebView().getUrl();
            if (url != null && machine() != null && url.startsWith(machine())) onMachinePage(url);
            return;
        }
        String tag = intent.getStringExtra("tag"); // a tapped notification (FCM data: kind, tag)
        if (tag != null && TAG.matcher(tag).matches()) {
            pendingTag = tag;
            intent.removeExtra("tag");
            String url = bridge.getWebView().getUrl();
            if (url != null && machine() != null && url.startsWith(machine())) onMachinePage(url);
        }
    }

    private void signedIn(String u) {
        String verifier = prefs().getString("verifier", null);
        long at = prefs().getLong("verifierAt", 0);
        prefs().edit().remove("verifier").remove("verifierAt").apply();
        Uri target = u == null ? null : Uri.parse(u);
        if (
            verifier == null || System.currentTimeMillis() - at > SIGNIN_TTL || target == null ||
            !"https".equals(target.getScheme()) || target.getPort() != -1 || target.getUserInfo() != null ||
            !hostedHost(target.getHost()) || !"/_machine/auth".equals(target.getPath()) ||
            target.getQueryParameter("t") == null || !TOKEN.matcher(target.getQueryParameter("t")).matches()
        ) {
            prefs().edit().putBoolean("signinStopped", true).apply();
            bridge.getWebView().loadUrl(bridge.getLocalUrl() + "/index.html");
            return;
        }
        prefs().edit().putString("machine", "https://" + target.getHost() + "/").apply();
        ensureFiles();
        Uri auth = target.buildUpon().appendQueryParameter("v", verifier).build();
        bridge.getWebView().loadUrl(auth.toString());
    }

    /**
     * A self-hosted Machine on The Machine Network: the account knows its address (its Tailscale one, else the
     * dashboard's own https address it reported; its owner's only) and the sign-in hands it back. No token: the Machine's own Tailscale sign-in applies, as in its browser.
     */
    private void signedInOwn(String m) {
        boolean pending = prefs().getString("verifier", null) != null &&
            System.currentTimeMillis() - prefs().getLong("verifierAt", 0) <= SIGNIN_TTL;
        prefs().edit().remove("verifier").remove("verifierAt").apply();
        String url = normalMachine(m);
        if (!pending || url == null || !ownHost(Uri.parse(url).getHost())) { // only right after a sign-in it started
            prefs().edit().putBoolean("signinStopped", true).apply();
            bridge.getWebView().loadUrl(bridge.getLocalUrl() + "/index.html");
            return;
        }
        prefs().edit().putString("machine", url).apply();
        ensureFiles();
        bridge.getWebView().loadUrl(url);
    }

    private JSONObject readShare(Intent intent) {
        JSONObject share = new JSONObject();
        try {
            StringBuilder text = new StringBuilder();
            String subject = intent.getStringExtra(Intent.EXTRA_SUBJECT);
            CharSequence body = intent.getCharSequenceExtra(Intent.EXTRA_TEXT);
            if (subject != null && !subject.isEmpty()) text.append(subject);
            if (body != null && body.length() > 0 && (subject == null || !body.toString().contains(subject))) {
                if (text.length() > 0) text.append("\n");
                text.append(body);
            }
            share.put("text", text.length() > 20000 ? text.substring(0, 20000) : text.toString());
            List<Uri> uris = new ArrayList<>();
            if (Intent.ACTION_SEND_MULTIPLE.equals(intent.getAction())) {
                ArrayList<Uri> list = Build.VERSION.SDK_INT >= 33
                    ? intent.getParcelableArrayListExtra(Intent.EXTRA_STREAM, Uri.class)
                    : intent.getParcelableArrayListExtra(Intent.EXTRA_STREAM);
                if (list != null) uris.addAll(list);
            } else {
                Uri one = Build.VERSION.SDK_INT >= 33
                    ? intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri.class)
                    : intent.getParcelableExtra(Intent.EXTRA_STREAM);
                if (one != null) uris.add(one);
            }
            JSONArray files = new JSONArray();
            long total = 0;
            ContentResolver resolver = getContext().getContentResolver();
            for (Uri uri : uris) {
                if (files.length() >= SHARE_FILES || !"content".equals(uri.getScheme())) continue;
                byte[] bytes = read(resolver, uri, SHARE_BYTES - total);
                if (bytes == null) continue;
                total += bytes.length;
                JSONObject file = new JSONObject();
                file.put("name", displayName(resolver, uri));
                file.put("type", resolver.getType(uri) == null ? "application/octet-stream" : resolver.getType(uri));
                file.put("data", Base64.encodeToString(bytes, Base64.NO_WRAP));
                files.put(file);
            }
            share.put("files", files);
        } catch (JSONException e) {
            return null;
        }
        return share;
    }

    private static byte[] read(ContentResolver resolver, Uri uri, long limit) {
        try (InputStream in = resolver.openInputStream(uri)) {
            if (in == null) return null;
            return read(in, limit);
        } catch (IOException | SecurityException e) {
            return null;
        }
    }

    /** At most limit bytes of a stream, else null (too big). */
    private static byte[] read(InputStream in, long limit) {
        try (InputStream stream = in) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[16384];
            int n;
            while ((n = in.read(buf)) > 0) {
                if (out.size() + n > limit) return null; // too big for the app to hand over: left out
                out.write(buf, 0, n);
            }
            return out.toByteArray();
        } catch (IOException | SecurityException e) {
            return null;
        }
    }

    private static String displayName(ContentResolver resolver, Uri uri) {
        try (Cursor c = resolver.query(uri, new String[] { OpenableColumns.DISPLAY_NAME }, null, null, null)) {
            if (c != null && c.moveToFirst()) {
                String name = c.getString(0);
                if (name != null) return name.replaceAll("[/\\\\]", "_");
            }
        } catch (Exception e) {
            // fall through
        }
        return "file";
    }

    // -- in the Machine's page: www/inject.js

    private void onMachinePage(String url) {
        String saved = machine();
        if (url == null || saved == null) return;
        String host = Uri.parse(url).getHost();
        if (hostedHost(Uri.parse(saved).getHost()) && hostedHost(host) && !host.equals(Uri.parse(saved).getHost())) {
            saved = "https://" + host + "/"; // the hosted Machine moved to its owner's name: follow it
            prefs().edit().putString("machine", saved).apply();
            ensureFiles();
        }
        if (!url.startsWith(saved) || url.contains("/_machine/")) return;
        try {
            JSONObject payload = new JSONObject();
            payload.put("base", saved);
            JSONObject device = new JSONObject(); // for a push token, now (push) or later (machinePhone.pushOn)
            device.put("platform", "fcm");
            device.put("label", Build.MODEL == null ? "Android" : Build.MODEL);
            payload.put("device", device);
            String token = prefs().getString("pushToken", null);
            if (token != null) { // inject.js hands it to the Machine once a week at most
                JSONObject push = new JSONObject(device.toString());
                push.put("token", token);
                payload.put("push", push);
            }
            if (pendingShare != null) {
                payload.put("share", pendingShare);
                pendingShare = null;
            }
            if (pendingTag != null) {
                payload.put("tag", pendingTag);
                pendingTag = null;
            }
            bridge.getWebView().evaluateJavascript("(" + inject() + ")(" + payload + ")", null);
        } catch (JSONException e) {
            // nothing to hand over
        }
    }

    private String inject() {
        if (injectSource == null) {
            try (InputStream in = getContext().getAssets().open("public/inject.js")) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                byte[] buf = new byte[8192];
                int n;
                while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
                injectSource = out.toString("UTF-8");
            } catch (IOException e) {
                injectSource = "(async()=>({}))";
            }
        }
        return injectSource;
    }
}
