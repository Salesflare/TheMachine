---
title: ChatGPT
area: connections
summary: Accedi con ChatGPT per usare la tua Machine con il tuo piano ChatGPT e importare le tue skill di ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## A cosa serve

Accedi con ChatGPT e la tua Machine lo userà per leggere e preparare bozze, con il tuo piano ChatGPT. The Machine non ha una propria AI: le richieste vanno direttamente a OpenAI, con il tuo account e secondo i loro termini.

## Accedi

Su una Machine ospitata, premi **Accedi con ChatGPT** nella pagina di configurazione e inserisci su ChatGPT il codice che compare. Hai effettuato la disconnessione? Premi **Riconnetti ChatGPT**.

OpenAI rifiuta il codice? Apri le [impostazioni di sicurezza di ChatGPT](https://chatgpt.com/settings/security), scorri fino in fondo e attiva l'opzione "Consenti l'accesso con codice dispositivo per Codex, Excel, PowerPoint e Word". Poi inserisci di nuovo il codice.

Non trovi l'opzione? Se usi un account di lavoro (Business, Enterprise o Edu), l'amministratore di ChatGPT può attivarla in [Autorizzazioni e ruoli](https://chatgpt.com/admin/permissions), nella sezione "Codex e Work Local".

Sul tuo computer, esegui `openclaw models auth login` in un terminale.

## Limiti di utilizzo

Un piano ChatGPT ha un limite di 5 ore e un limite settimanale. In **Impostazioni**, **Modello** puoi vedere quanto hai utilizzato di ciascun limite e quando si azzera. Le attività in background si interrompono molto prima del limite, così puoi continuare a usare le tue chat. Quando raggiungi un limite, nella parte superiore della dashboard trovi l'ora in cui si azzera. Vedi [Modello](model.md).

## Importa le tue skill di ChatGPT

In **Impostazioni**, **Skill**, premi **Importa**, scegli **Da ChatGPT** e premi **Trova le mie skill**. Verranno importate solo le istruzioni. Vedi [Skill](skills.md).

## Rimuovi ChatGPT

Scegli un altro modello nella pagina di configurazione oppure, sul tuo computer, accedi a un altro provider nello stesso modo. Per revocare l'accesso da OpenAI, esci dalla sessione nelle impostazioni di sicurezza di ChatGPT.
