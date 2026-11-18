---
title: Disconnessione da un sito
area: troubleshooting
summary: LinkedIn o X ha disconnesso la tua Machine. Accedi di nuovo, una volta sola o in modo permanente.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
I siti come LinkedIn e X vengono consultati nel browser della tua Machine. A volte un sito la disconnette.

## Accedi di nuovo

**Connessioni** e l’inizio delle tue attività indicano che hai effettuato la disconnessione. Premi **Accedi qui** e accedi nella piccola finestra che si apre nella dashboard.

Seleziona **Salva per la prossima volta** per accedere di nuovo con un tocco la prossima volta che succede. La password resta crittografata sulla tua Machine e l’AI non la vede mai. Se hai più account sullo stesso sito, **Salva come** assegna un nome a questo account (Lavoro, Personale) e, se l’attività non specifica quale usare, la finestra di dialogo ti chiede di scegliere.

## Password e codici

Inserisci tu le password. Anche i codici di verifica in due passaggi devi inserirli tu.

Gli accessi salvati si trovano in **Connessioni**, **Accessi**. **Dimentica** rimuove un accesso. **Importa** li importa da un gestore di password, tramite la sua pagina di esportazione aperta nel browser della tua Machine oppure da un file di esportazione.

## Se il sito rifiuta l’accesso o chiede di verificare che non sei un robot

LinkedIn, X e i siti che usano un controllo Cloudflare spesso rifiutano gli accessi da un browser nel cloud. Su una Machine ospitata, nella schermata di accesso compare **Accedi dalla tua connessione di casa**. Si apre la pagina di configurazione, dove il browser della tua Machine può connettersi a Internet tramite la rete di casa con Tailscale oppure tramite il tuo proxy. Poi accedi di nuovo.

Sul tuo computer non serve: il suo browser è già connesso dalla rete di casa.
