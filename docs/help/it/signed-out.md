---
title: Disconnesso da un sito
area: troubleshooting
summary: LinkedIn o X hanno disconnesso la tua Machine. Fai di nuovo l'accesso, una volta o per sempre.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: b77b372b9332ca2b
---
Siti come LinkedIn e X vengono letti nel browser della tua Machine. A volte un sito la disconnette.

## Accedi di nuovo

La fonte in **Connessioni** e la parte alta delle tue Attività dicono che è disconnessa. Premi **Accedi di nuovo** e accedi, in una piccola finestra sulla dashboard.

Spunta **Salva per la prossima volta** quando accedi. La prossima volta che il sito disconnette la tua Machine, rientra con un tocco. La password resta crittografata sulla tua Machine; l'AI non la vede mai.

## Password e codici

Le password le scrivi tu. Anche i codici della verifica in due passaggi li inserisci tu.

Gli accessi salvati sono in **Connessioni**, **Accessi**. **Dimentica** ne rimuove uno.

## Se il sito rifiuta o chiede una verifica anti-robot

LinkedIn, X e i siti dietro una verifica di Cloudflare spesso rifiutano gli accessi da un browser nel cloud. Su una Machine ospitata, l’accesso mostra allora **Accedi dalla tua connessione di casa**. Apre la tua pagina di configurazione, dove il browser della tua Machine può uscire dalla tua connessione internet di casa con Tailscale, o dal tuo proxy. Poi accedi di nuovo.

Sul tuo computer non serve: il suo browser è già a casa.
