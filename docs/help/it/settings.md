---
title: Impostazioni
area: settings
summary: Dove trovare tutte le impostazioni, dalla modalità chiara alla sicurezza e al tuo account.
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
Apri **Impostazioni** con l’icona a forma di ingranaggio in alto. Le schede:

- **Account**: in alto trovi **I tuoi indirizzi** (quelli che ti identificano) e **Esci**. Se hai una Machine ospitata, trovi anche il piano, le fatture, Fleet, gli amici, l’accesso e i dati, con **Annulla il piano** e **Elimina l’account** in fondo. Se usi una Machine sul tuo computer, collegata al Network, trovi Fleet, il nome utente, gli amici e l’accesso, ognuno con un link che apre la relativa sezione del tuo account (dove accedere), e **Elimina l’account** in fondo. Se non hai ancora effettuato il collegamento, in alto trovi **Unisciti al Network**. Vedi [Piani e fatturazione](plans-and-billing.md).
- **Generale**: lingua e area geografica, questo dispositivo, input vocale, il browser della tua Machine, Fleet, esportazione e importazione, e la versione in uso. Se non c’è la scheda Account, **Unisciti al Network** si trova in fondo.
- **Sicurezza**: Standard o Prudente. Vedi [Livelli di sicurezza](security-levels.md). Trovi anche **Accesso per l’assistenza**, quando è attivo: vedi [Contatta l’assistenza](get-support.md#support-access).
- **Movimenti**: tutte le operazioni svolte da The Machine per te, dalla più recente. Vedi [Movimenti](activity.md).
- **Notifiche**: quali notifiche ricevi e dove, e il tuo orario di lavoro. Vedi [Notifiche](notifications.md) e [Orario di lavoro](work-hours.md).
- **Scrittura**: firme e stile di scrittura. Vedi [Scrittura](writing.md).
- **Skill**: le guide che la tua Machine segue. Vedi [Skill](skills.md).
- **App**: le app di The Machine per telefono e computer, poi Claude, ChatGPT e le altre IA che hai collegato, e le relative autorizzazioni. Sul computer trovi l’app desktop per Windows, Mac e Linux, con **Scarica** per ciascuna, e l’indicazione di quella per **Questo computer**. Vedi [L’app per dispositivi mobili](mobile-app.md), [L’app desktop](desktop-app.md) e [Collegare altre IA](ai-connections.md).
- **Modello**: l’IA che legge e prepara bozze per te, e i suoi limiti. Vedi [Modello](model.md). Qui trovi anche **Codex e Claude Code**: vedi [Passa a Claude Code o Codex](hand-to-agent.md). E **Ricerca per significato**, più sotto.

Le schede senza contenuti non vengono mostrate.

## Generale

- **Lingua e area geografica**: **Area geografica** determina il formato di date, orari e numeri (24 ott o 24 ott). **Formato dell’ora** imposta il formato a 12 ore (2:05 PM) o a 24 ore (14:05). Le attività, Telegram, il riepilogo e i messaggi Fleet seguono entrambe le impostazioni. Una Machine ospitata usa il fuso orario scelto al momento della registrazione.
- **Lingua**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 o Русский. Inizialmente usa la lingua del browser. La dashboard, la Guida, le notifiche, Telegram, il riepilogo settimanale e le attività scritte dalla tua Machine cambiano lingua non appena ne scegli una. I testi precedenti restano invariati. I colleghi ricevono le domande di Fleet e Family nella propria lingua, mentre le bozze per altre persone restano nella lingua della conversazione.
- **Questo dispositivo**: **Installa l’app**, **Notifiche** con **Invia una prova** e **Modalità chiara**, solo per questo browser o telefono. Vedi [Installa l’app e attiva le notifiche](phone-app.md). Su [Omarchy](omarchy.md) trovi anche **Tema Omarchy**.
- **Input vocale**: come le parole che pronunci diventano testo e quale voce usa Talk live. Vedi [Input vocale](voice-input.md) e [Conversazione dal vivo](talk-live.md).
- **Apri il browser della Machine ↗**: il browser che la tua Machine usa per siti come LinkedIn.
- **Regole Fleet**: vedi [Regole di condivisione](sharing-rules.md).
- **Esporta**:
  - **Tutto**: tutto ciò che la tua Machine sa, in un unico file cifrato, da trasferire o conservare. Usa **Importa** per caricare un file. Vedi [Passa a un altro computer](moving.md).
  - **Conoscenze per un’altra IA**: ciò che la tua Machine ha imparato, in file leggibili da qualsiasi IA. Vedi [Conoscenze per un’altra IA](knowledge-export.md).

## Versione

La versione in uso sulla tua Machine. Gli aggiornamenti si installano automaticamente. Quando è disponibile una nuova versione per una Machine ospitata, **Aggiorna ora** la installa subito. L’operazione richiede qualche minuto e i tuoi dati restano al sicuro.

Sul tuo computer, un timer giornaliero installa ogni nuova versione firmata su Linux. Vedi [Usa la tua Machine sul tuo computer](self-hosted-setup.md).

## Ricerca per significato

In **Impostazioni**, **Modello**. Trova email, messaggi e note in base all’argomento, non solo alle parole usate. Su una Machine ospitata, se ne occupa una piccola IA che gira sulla Machine stessa, senza inviare nulla altrove. La funzione è attiva a partire da 8 GB di memoria. Con 4 GB, attivala con l’interruttore. Occupa circa mezzo gigabyte, quindi una Machine molto impegnata può rallentare. Se è disattivata, la preparazione di un’attività continua a cercare messaggi pertinenti usando le parole.

Sul tuo computer, è il blocco `embeddings` in `config.json`. Riavvia la Machine dopo ogni modifica.

## Sulla Machine

Quando la tua Machine gira sul tuo computer, alcune operazioni si svolgono lì, in un terminale:

- Il file delle impostazioni, `config.json`: tutte le impostazioni in un unico posto. Riavvia la Machine dopo ogni modifica.
- `assistant connect`: aggiunge una fonte, come `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: messaggi su Telegram. Vedi [Telegram](telegram.md).
- `assistant doctor`: controlla tutto e mostra una soluzione per ogni problema.

## I tuoi indirizzi

Tutti i tuoi indirizzi trovati dalla Machine: i tuoi account, gli alias Gmail o Outlook, il calendario e i profili Slack e Intercom. Le email e le riunioni provenienti da uno qualsiasi di questi indirizzi vengono considerate tue. **Rimuovi** quelli che non ti appartengono.

Un indirizzo condiviso, come info@ o un Google Group, non viene mai considerato tuo automaticamente. Se la Machine non è sicura, l’indirizzo resta in **Forse tuoi**. Scegli una voce:

- **Mio: rispondo solo io**: l’indirizzo viene considerato tuo. Le email ricevute lì possono diventare attività.
- **Del team: rispondono anche altri**: l’indirizzo non viene considerato tuo. Le email inviate solo a quell’indirizzo non generano attività né bozze per te. Contribuiscono comunque al Graph.
- **Non è mio**: l’indirizzo non verrà considerato tuo.

Scegli in base a chi risponde oggi. Una casella del team come support@ appartiene al team. Una casella come partnerships@, a cui rispondi solo tu, è tua. Cambia la selezione quando anche altre persone iniziano a rispondere.

Con **Cambia** puoi modificare la selezione in seguito. L’indirizzo che usi per accedere è sempre tuo.

### I domini della tua azienda

I domini dei tuoi indirizzi personali vengono considerati quelli della tua azienda. Ne usi anche un altro, come acme.co oltre ad acme.com? Inseriscilo in **I domini della tua azienda** e premi **Aggiungi**.

Le persone con quegli indirizzi vengono considerate colleghi, non clienti: le loro conversazioni restano fuori dal Graph del team e non viene creata un’organizzazione per loro. Con **Rimuovi** puoi eliminarli. Non puoi aggiungere domini di email gratuite come gmail.com.

Un tuo alias Gmail può anche comparire nel campo **From** di una bozza, se Gmail conferma che puoi inviare email da quell’indirizzo. Vedi [Gmail](gmail.md#what-it-can-send).
