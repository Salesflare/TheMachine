package computer.themachine.app;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import java.net.InetAddress;
import java.net.UnknownHostException;

import org.junit.Test;

/** Which addresses the app saves as the owner's Machine: the same rules as www/machine-url.js (mobile/tests). */
public class MachineAddressTest {

    @Test
    public void aHostedMachineIsItsRootOn443() {
        assertEquals("https://sam.app.themachine.computer/", MachineShellPlugin.normalMachine("https://sam.app.themachine.computer/x"));
        assertNull(MachineShellPlugin.normalMachine("https://sam.app.themachine.computer:8443/"));
    }

    @Test
    public void aMachineOfTheirOwnIsATailnetOrItsOwnHttpsAddress() {
        assertEquals("https://machine.tail1234.ts.net/", MachineShellPlugin.normalMachine("https://machine.tail1234.ts.net"));
        assertEquals("https://machine.tail1234.ts.net:8443/assistant/", MachineShellPlugin.normalMachine("https://machine.tail1234.ts.net:8443/assistant"));
        assertEquals("https://my.themachine.computer/", MachineShellPlugin.normalMachine("https://my.themachine.computer/"));
        assertEquals("https://desk.example.co.uk:8443/a/", MachineShellPlugin.normalMachine("https://Desk.Example.co.uk:8443/a"));
        assertTrue(MachineShellPlugin.ownHost("my.themachine.computer"));
        assertFalse(MachineShellPlugin.ownHost("sam.app.themachine.computer"));
    }

    @Test
    public void nothingElse() {
        String[] bad = {
            null, "", "http://my.example.com/", "https://u@my.example.com/", "https://u:p@my.example.com/",
            "https://my.example.com:8080/", "https://my.example.com:444/", "https://192.168.1.10/", "https://10.0.0.1:8443/",
            "https://[fd7a::1]/", "https://100.64.0.1/", "https://desk/", "https://localhost/", "https://desk.local1/",
            "https://tail1234.ts.net/", "https://a.b.sam.app.themachine.computer/", "https://app.themachine.computer:8443/",
            "https://-x.example.com/", "https://my.example.com/a%2f../", "https://my.example.com/a b/", "javascript:alert(1)",
        };
        for (String url : bad) assertNull(url, MachineShellPlugin.normalMachine(url));
    }

    @Test
    public void checkGoesOnlyToPublicOrTailnetAddresses() throws UnknownHostException {
        String[] ok = {"93.184.216.34", "100.64.0.1", "100.127.255.254", "2606:4700::1111", "fd7a:115c:a1e0::1"};
        for (String a : ok) assertTrue(a, MachineShellPlugin.publicOrTailnet(InetAddress.getByName(a)));
        String[] bad = {
            "127.0.0.1", "0.0.0.0", "10.0.0.1", "172.16.0.1", "172.31.255.1", "192.168.1.1", "169.254.169.254",
            "224.0.0.1", "255.255.255.255", "192.0.0.1", "198.18.0.1", "::", "::1", "fe80::1", "fc00::1", "fd00::1",
            "fd7a:115c:a1e1::1", "ff02::1", "::ffff:127.0.0.1", "::ffff:192.168.1.1",
        };
        for (String a : bad) assertFalse(a, MachineShellPlugin.publicOrTailnet(InetAddress.getByName(a)));
    }
}
