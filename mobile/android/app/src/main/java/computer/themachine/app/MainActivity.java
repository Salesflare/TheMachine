package computer.themachine.app;

import android.content.pm.PackageManager;
import android.os.Bundle;
import android.webkit.WebView;
import androidx.activity.OnBackPressedCallback;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(MachineShellPlugin.class);
        super.onCreate(savedInstanceState);
        ((MachineShellPlugin) bridge.getPlugin("MachineShell").getInstance()).attach();
        // Back goes back in the Machine's pages (a closed drawer, the view before); from the first page it leaves the app
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                WebView webView = bridge.getWebView();
                if (webView.canGoBack()) webView.goBack();
                else moveTaskToBack(true);
            }
        });
    }

    @Override
    public void onResume() {
        super.onResume();
        MachinePushService.seen(this); // what the notifications counted is on screen now
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == MachineShellPlugin.ASK_PUSH) {
            boolean granted = grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED;
            ((MachineShellPlugin) bridge.getPlugin("MachineShell").getInstance()).pushAnswered(granted);
        }
    }
}
