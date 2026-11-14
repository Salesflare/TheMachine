---
title: La connessione di casa del tuo browser
area: troubleshooting
summary: Fai uscire il browser della tua Machine ospitata dalla tua internet di casa con Tailscale, così i siti accettano i suoi accessi.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
translated: 9935ac3c09fa5c00
---
Alcuni siti, come LinkedIn, X e quelli dietro un controllo Cloudflare, rifiutano gli accessi da un browser nel cloud. La tua pagina di configurazione può far uscire il browser della tua Machine ospitata dalla tua internet di casa, con Tailscale. È gratis, richiede circa 10 minuti e quasi tutto succede da solo.

## Configurarlo

1. Nella tua pagina di configurazione, al browser della tua Machine, scegli **Tailscale** e premi **Accedi a Tailscale**. Accedi, o crea lì un account gratuito.
2. Installa Tailscale su un computer di casa che resta acceso e accedi lì con lo stesso account. Non un telefono: va in standby.
3. Rendi quel computer un exit node. La pagina di configurazione mostra il menu per il suo sistema. Su Linux, esegui `sudo tailscale set --advertise-exit-node`.
4. Premi **Aprilo in Tailscale** e consentilo: Machine settings, Edit route settings, Use as exit node, Save. Nello stesso menu, scegli Disable key expiry.

La pagina di configurazione spunta ogni passo da sola. Con un solo exit node, il tuo browser inizia subito a usarlo. Con più di uno, scegline uno e premi **Usa questo exit node**.

## Verificarlo

Premi **Provalo**. La pagina mostra dove il web vede il tuo browser: la tua città e il tuo provider internet.

## Quando il computer di casa è spento

Il tuo browser esce allora direttamente dalla tua Machine, e torna a passare da casa appena il computer si riaccende. Disconnesso da Tailscale? Premi **Accedi di nuovo**. Tailscale disconnette i dispositivi dopo 6 mesi, a meno che key expiry sia disattivato. La pagina di configurazione mostra la data.

## Smettere di usarlo

Premi **Smetti di usarlo** per tornare diretto. **Disconnettilo anche da Tailscale** disconnette anche il browser della tua Machine da Tailscale. La console di amministrazione di Tailscale lo mostra poi come Expired, e lì puoi rimuoverlo.
