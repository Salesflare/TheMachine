---
title: Impostazioni
area: settings
summary: Dove trovare le impostazioni: dalla modalità chiara alla sicurezza e al tuo account.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Apri **Impostazioni** con l’icona a ingranaggio in alto. Le schede sono:

- **Account**: **I tuoi indirizzi** (quelli che vengono riconosciuti come tuoi) e **Esci**, in alto. Su una Machine ospitata trovi anche il tuo piano, le fatture, Fleet, gli amici, l’accesso e i dati, con **Annulla il piano** e **Elimina l’account** in fondo. Su una Machine sul tuo computer, collegata al Network, trovi Fleet, nome utente, amici e accesso, ciascuno con un link che apre quella sezione del tuo account (accedi da lì), e **Elimina l’account** in fondo. Se non hai ancora effettuato il collegamento, trovi **Unisciti al Network** in alto. Vedi [Piani e fatturazione](plans-and-billing.md).
- **Generale**: lingua e area geografica, questo dispositivo, input vocale, il browser della tua Machine, Fleet, esportazione e importazione e la versione in uso. Se non c’è la scheda Account, **Unisciti al Network** si trova in fondo.
- **Sicurezza**: Standard o Attenta. Vedi [Livelli di sicurezza](security-levels.md). Trovi anche **Accesso per l’assistenza** quando è attivo: vedi [Richiedere assistenza](get-support.md#support-access).
- **Movimenti**: tutto quello che The Machine ha fatto per te, dal più recente. Vedi [Movimenti](activity.md).
- **Notifiche**: cosa ti viene inviato e dove, e il tuo orario di lavoro. Vedi [Notifiche](notifications.md) e [Orario di lavoro](work-hours.md).
- **Scrittura**: firme e il tuo modo di scrivere. Vedi [Scrittura](writing.md).
- **Skill**: le guide che la tua Machine segue. Vedi [Skill](skills.md).
- **App**: le app di The Machine per il tuo telefono e computer, poi Claude, ChatGPT e le altre IA a cui ti sei collegato, e cosa può fare ciascuna. Vedi [L’app per dispositivi mobili](mobile-app.md) e [Collegare altre IA](ai-connections.md).
- **Modello**: l’IA che legge e prepara bozze per te, e i suoi limiti. Vedi [Modello](model.md). Trovi anche **Codex e Claude Code**: vedi [Passare il lavoro a Claude Code o Codex](hand-to-agent.md). E **Ricerca per significato**, più sotto.

Le schede senza contenuti non vengono mostrate.

## Generale

- **Lingua e area geografica**: **Area geografica** determina il formato di date, orari e numeri (24 ott oppure ott 24). **Formato dell’ora** consente di scegliere il formato a 12 ore (2:05 PM) o a 24 ore (14:05). Le attività, Telegram, il riepilogo e i messaggi Fleet seguono entrambe le impostazioni. Una Machine ospitata parte dal fuso orario scelto al momento dell’iscrizione.
- **Lingua**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 o Русский. Viene impostata in base alla lingua del browser. La dashboard, la Guida, le notifiche, Telegram, il riepilogo settimanale e le attività scritte dalla tua Machine cambiano lingua appena fai la scelta. I testi precedenti restano com’erano. I tuoi compagni di team ricevono le domande di Fleet e Family nella loro lingua, mentre le bozze per le altre persone restano nella lingua della conversazione.
- **Questo dispositivo**: **Installa l’app**, **Notifiche** con **Invia una prova** e **Modalità chiara**, solo per questo browser o telefono. Vedi [Installare l’app e attivare le notifiche](phone-app.md). Su [Omarchy](omarchy.md) trovi anche **Tema Omarchy**.
- **Input vocale**: come le parole che dici diventano testo e quale voce usa Talk live. Vedi [Input vocale](voice-input.md) e [Talk live](talk-live.md).
- **Apri il browser della Machine ↗**: il browser che la tua Machine usa per siti come LinkedIn.
- **Regole Fleet**: vedi [Regole di condivisione](sharing-rules.md).
- **Esporta**:
  - **Tutto**: tutto quello che la tua Machine sa, in un unico file crittografato da trasferire o conservare, e **Importa** per caricare un file. Vedi [Passare a un altro computer](moving.md).
  - **Conoscenze per un’altra IA**: ciò che la tua Machine ha imparato, in file leggibili da qualsiasi IA. Vedi [Conoscenze per un’altra IA](knowledge-export.md).

## Versione

La versione in uso sulla tua Machine. Gli aggiornamenti si installano automaticamente. Quando una versione più recente è disponibile su una Machine ospitata, **Aggiorna ora** la installa subito. L’operazione richiede qualche minuto e i tuoi dati restano al sicuro.

Sul tuo computer, un timer giornaliero installa ogni nuova versione firmata su Linux. Vedi [Usare la Machine sul tuo computer](self-hosted-setup.md).

## Ricerca per significato

In **Impostazioni**, **Modello**. Trova email, messaggi e note in base all’argomento, non solo alle parole usate. Su una Machine ospitata, se ne occupa una piccola IA che gira sulla Machine stessa, senza inviare nulla altrove. La funzione è attiva da 8 GB di memoria. Con 4 GB, attivala con l’interruttore. Usa circa mezzo gigabyte, quindi una Machine molto impegnata può rallentare.

Sul tuo computer, si tratta del blocco `embeddings` in `config.json`. Riavvia la Machine dopo averlo modificato.

## Su questa Machine

Quando la tua Machine gira sul tuo computer, alcune operazioni si svolgono lì, in un terminale:

- Il file delle impostazioni, `config.json`: contiene tutte le impostazioni in un unico posto. Riavvia la Machine dopo averlo modificato.
- `assistant connect`: aggiunge una fonte, come `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: messaggi su Telegram. Vedi [Telegram](telegram.md).
- `assistant doctor`: controlla tutto e stampa una correzione per ogni problema.

## I tuoi indirizzi

Tutti gli indirizzi che la Machine ha trovato: i tuoi account, gli alias Gmail o Outlook, il tuo calendario e i tuoi profili Slack e Intercom. Le email e le riunioni provenienti da questi indirizzi vengono riconosciute come tue. **Rimuovi** quelli che non sono tuoi.

Un indirizzo condiviso, come info@ o un Google Group, non viene mai riconosciuto come tuo automaticamente. Gli indirizzi su cui la Machine ha dei dubbi si trovano in **Forse tuoi**. Scegli una di queste opzioni:

- **Mio: rispondo solo io**: l’indirizzo viene riconosciuto come tuo. Le email ricevute lì possono diventare tue attività.
- **Del team: rispondono anche altri**: l’indirizzo non viene riconosciuto come tuo. Le email inviate solo a quell’indirizzo non generano attività né bozze per te. Vengono comunque aggiunte al Graph.
- **Non è mio**: l’indirizzo non viene riconosciuto come tuo.

Scegli in base a chi risponde oggi. Una casella del team come support@ appartiene al team. Un indirizzo come partnerships@ a cui rispondi solo tu è tuo. Cambia l’impostazione quando iniziano a rispondere anche altre persone.

Con **Cambia** sulla riga puoi modificare l’impostazione in seguito. Il tuo indirizzo di accesso personale è sempre riconosciuto come tuo.

### I domini della tua azienda

I domini dei tuoi indirizzi personali vengono riconosciuti come domini della tua azienda. Ne usi anche un altro, come acme.co oltre ad acme.com? Inseriscilo in **I domini della tua azienda** e premi **Aggiungi**.

Le persone che usano questi domini vengono considerate colleghe, mai clienti: le loro conversazioni non vengono incluse nel Team Graph e non viene creata un’organizzazione per loro. **Rimuovi** elimina di nuovo il dominio. Non puoi aggiungere domini di email gratuite come gmail.com.

Un tuo alias Gmail può essere usato anche come **Da** per una bozza, se Gmail conferma che puoi inviare email da quell’indirizzo. Vedi [Gmail](gmail.md#what-it-can-send).
