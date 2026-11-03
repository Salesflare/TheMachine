package computer.themachine.app;

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
}
