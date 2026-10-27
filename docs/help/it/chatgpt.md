---
title: ChatGPT
area: connections
summary: Accedi con ChatGPT per far funzionare la tua Machine con il tuo piano ChatGPT, e importa le tue skill di ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## A cosa serve

ChatGPT è il modello che legge e prepara le bozze per te, con il tuo piano ChatGPT. The Machine non ha un’AI propria. Le richieste della tua Machine vanno dal tuo server direttamente a OpenAI, con il tuo account e alle sue condizioni.

## Accedi

Su una Machine in hosting, nella tua pagina di configurazione, premi **Accedi con ChatGPT** e inserisci su ChatGPT il codice che compare. Sei stato disconnesso? Premi **Riconnetti ChatGPT**.

OpenAI rifiuta il codice? Apri le tue [impostazioni di sicurezza di ChatGPT](https://chatgpt.com/settings/security), scorri fino in fondo e attiva l’interruttore "Enable device code sign-in for Codex, Excel, PowerPoint, and Word". Poi inserisci di nuovo il codice.

Non c’è? Su un account di lavoro (Business, Enterprise o Edu), un amministratore del workspace lo attiva in [Permissions & roles](https://chatgpt.com/admin/permissions), sotto "Codex and Work Local". Un solo interruttore vale per entrambi i codici: se il codice del tuo modello ha funzionato, funziona anche quello di Codex.

Sul tuo computer, fai accedere OpenClaw a ChatGPT con `openclaw models auth login`.

## Limiti di utilizzo

Un piano ChatGPT ha un limite di 5 ore e uno settimanale. **Impostazioni**, poi **Modello**, mostra quanto ne hai usato e quando si azzera. Il lavoro in background si ferma ben prima di un limite, per lasciare spazio alle tue chat. Quando raggiungi un limite, in cima alla dashboard compare quale e quando si azzera, e poi il lavoro riprende. Vedi [Modello](model.md).

## Importa le tue skill di ChatGPT

In **Impostazioni**, **Skill**, premi **Importa**, scegli **Da ChatGPT** e premi **Trova le mie skill**. Legge le skill che hai creato, nel browser della tua Machine. Arrivano solo le istruzioni. Vedi [Skill](skills.md).

## Rimuovilo

Scegli un altro modello nella tua pagina di configurazione, oppure fai accedere OpenClaw a un altro fornitore. Per chiudere il suo accesso dal lato di OpenAI, disconnetti la sessione nelle impostazioni di sicurezza di ChatGPT.
