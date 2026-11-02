package computer.themachine.app;

import android.content.ContentResolver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
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
        bridge.addWebViewListener(
            new WebViewListener() {
                @Override
                public void onPageLoaded(WebView webView) {
                    onMachinePage(webView.getUrl());
                }
            }
        );
        handleIntent(getActivity().getIntent());
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

    /** A Machine address the app may save: https, no port or user, a hosted Machine's root or a tailnet host. */
    static String normalMachine(String url) {
        if (url == null) return null;
        Uri u = Uri.parse(url);
        String host = u.getHost() == null ? null : u.getHost().toLowerCase();
        if (!"https".equals(u.getScheme()) || u.getPort() != -1 || u.getUserInfo() != null || host == null) return null;
        if (hostedHost(host)) return "https://" + host + "/";
        if (!tailnetHost(host)) return null;
        String path = u.getPath() == null || u.getPath().isEmpty() ? "/" : u.getPath();
        if (!path.endsWith("/")) path += "/";
        if (!path.matches("/(?:[A-Za-z0-9._~-]+/)*")) return null;
        return "https://" + host + path;
    }

    private SharedPreferences prefs() {
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
            if (host.equals(m.getHost()) || (hostedHost(m.getHost()) && hostedHost(host))) return false;
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
            call.resolve();
        });
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
        Uri auth = target.buildUpon().appendQueryParameter("v", verifier).build();
        bridge.getWebView().loadUrl(auth.toString());
    }

    /**
     * A self-hosted Machine on The Machine Network: the account knows its Tailscale address (its owner's only) and the
     * sign-in hands it back. No token: the Machine's own Tailscale sign-in applies, as in its browser.
     */
    private void signedInOwn(String m) {
        boolean pending = prefs().getString("verifier", null) != null &&
            System.currentTimeMillis() - prefs().getLong("verifierAt", 0) <= SIGNIN_TTL;
        prefs().edit().remove("verifier").remove("verifierAt").apply();
        String url = normalMachine(m);
        if (!pending || url == null || !tailnetHost(Uri.parse(url).getHost())) { // only right after a sign-in it started
            prefs().edit().putBoolean("signinStopped", true).apply();
            bridge.getWebView().loadUrl(bridge.getLocalUrl() + "/index.html");
            return;
        }
        prefs().edit().putString("machine", url).apply();
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
        }
        if (!url.startsWith(saved) || url.contains("/_machine/")) return;
        try {
            JSONObject payload = new JSONObject();
            payload.put("base", saved);
            String token = prefs().getString("pushToken", null);
            if (token != null) { // inject.js hands it to the Machine once a week at most
                JSONObject push = new JSONObject();
                push.put("platform", "fcm");
                push.put("token", token);
                push.put("label", Build.MODEL == null ? "Android" : Build.MODEL);
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
