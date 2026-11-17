---
title: Disconnessione da un sito
area: troubleshooting
summary: LinkedIn o X hanno disconnesso la tua Machine. Accedi di nuovo, una volta o definitivamente.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
Siti come LinkedIn e X si aprono nel browser della tua Machine. A volte un sito ti disconnette.

## Accedi di nuovo

**Connessioni** e la parte superiore delle tue attività indicano che hai effettuato la disconnessione. Premi **Accedi qui** e accedi nella piccola finestra sulla dashboard.

Seleziona **Salva per la prossima volta** per accedere di nuovo con un tocco quando succede ancora. La password resta crittografata sulla tua Machine e l’AI non può vederla. Se hai più account sullo stesso sito, **Salva come** assegna un nome a questo account (Lavoro, Personale) e, se l’attività non specifica quale usare, la finestra di dialogo te lo chiede.

## Password e codici

Inserisci tu le password. Anche i codici per la verifica in due passaggi devi inserirli tu.

Gli accessi salvati si trovano in **Connessioni**, **Accessi**. **Dimentica** rimuove un accesso. **Importa** li importa da un gestore di password.

## Se il sito rifiuta l’accesso o chiede una verifica anti-robot

LinkedIn, X e i siti che usano una verifica Cloudflare spesso rifiutano gli accessi da un browser nel cloud. Su una Machine ospitata, per accedere appare **Accedi dalla tua connessione di casa**. Si apre la pagina di configurazione, dove il browser della tua Machine può connettersi a Internet tramite la rete di casa con Tailscale o tramite un proxy tuo. Poi accedi di nuovo.

Sul tuo computer non serve: il suo browser è già sulla tua rete di casa.
