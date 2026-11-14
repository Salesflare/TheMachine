---
title: Impostazioni
area: settings
summary: Dove trovare ogni impostazione: dalla modalità chiara alla sicurezza e al tuo account.
covers: settings:general
code: dashboard.html
order: 1
translated: 00e42f9aeb395d21
---
Apri **Impostazioni** con l’icona a forma di ingranaggio in alto. Le schede:

- **Account**: **I tuoi indirizzi** (quelli che vengono considerati tuoi) e **Esci**, in alto. Se hai una Machine ospitata, trovi anche il piano, le fatture, Fleet, gli amici, l’accesso e i dati, con **Annulla il piano** e **Elimina l’account** in fondo. Se usi una Machine sul tuo computer, collegata al Network, trovi Fleet, il nome utente, gli amici e l’accesso, ognuno con un link che apre la sezione corrispondente del tuo account (accedi da lì), e **Elimina l’account** in fondo. Se non hai ancora effettuato il collegamento, trovi **Unisciti al Network** in alto. Vedi [Piani e fatturazione](plans-and-billing.md).
- **Generale**: lingua e area geografica, questo dispositivo, input vocale, il browser della tua Machine, Fleet, esportazione e importazione, e la versione in uso. Se non c’è la scheda Account, **Unisciti al Network** è in fondo.
- **Sicurezza**: Standard o Prudente. Vedi [Livelli di sicurezza](security-levels.md). Trovi anche **Accesso per l’assistenza**, quando è attivo: vedi [Richiedere assistenza](get-support.md#support-access).
- **Movimenti**: tutto quello che The Machine ha fatto per te, dal più recente. Vedi [Movimenti](activity.md).
- **Notifiche**: cosa ti arriva e dove, e il tuo orario di lavoro. Vedi [Notifiche](notifications.md) e [Orario di lavoro](work-hours.md).
- **Scrittura**: firme e il tuo modo di scrivere. Vedi [Scrittura](writing.md).
- **Skill**: guide che la tua Machine segue. Vedi [Skill](skills.md).
- **App**: le app di The Machine per il telefono e il computer, poi Claude, ChatGPT e le altre IA a cui ti sei collegato, e cosa può fare ciascuna. Vedi [L’app mobile](mobile-app.md) e [Collegare altre IA](ai-connections.md).
- **Modello**: l’IA che legge e scrive bozze per te, e i suoi limiti. Vedi [Modello](model.md). Trovi anche **Codex e Claude Code**: vedi [Passare il lavoro a Claude Code o Codex](hand-to-agent.md). E **Ricerca per significato**, più sotto.

Le schede senza contenuti non vengono mostrate.

## Generale

- **Lingua e area geografica**: **Area geografica** determina il formato di date, orari e numeri (24 ott o 24 ott). **Formato dell’ora** imposta il formato a 12 ore (2:05 PM) o a 24 ore (14:05). Attività, Telegram, il riepilogo e i messaggi Fleet seguono entrambe le impostazioni. Una Machine ospitata usa inizialmente il fuso orario che hai scelto al momento della registrazione.
- **Lingua**: English, Nederlands, Français, Deutsch, Español, Italiano o Português (Brasil). All’inizio viene usata la lingua del browser. La dashboard, la guida, le notifiche, Telegram, il riepilogo settimanale e le attività che la tua Machine scrive cambiano lingua appena la selezioni. I testi precedenti restano come sono. I tuoi compagni di squadra ricevono le domande di Fleet e Family nella propria lingua, mentre le bozze per gli altri restano nella lingua della conversazione.
- **Questo dispositivo**: **Installa l’app**, **Notifiche** con **Invia una prova** e **Modalità chiara**, solo per questo browser o telefono. Vedi [Installare l’app e attivare le notifiche](phone-app.md). Su [Omarchy](omarchy.md) trovi anche **Tema Omarchy**.
- **Input vocale**: come le tue parole diventano testo e la voce di Talk live. Vedi [Input vocale](voice-input.md) e [Talk live](talk-live.md).
- **Apri il browser della Machine ↗**: il browser che la tua Machine usa per siti come LinkedIn.
- **Regole Fleet**: vedi [Regole di condivisione](sharing-rules.md).
- **Esporta**:
  - **Tutto**: tutto quello che la tua Machine sa, in un unico file crittografato, da trasferire o conservare. Usa **Importa** per caricare un file. Vedi [Passare a un altro computer](moving.md).
  - **Conoscenze per un’altra IA**: ciò che la tua Machine ha imparato, in file leggibili da qualsiasi IA. Vedi [Conoscenze per un’altra IA](knowledge-export.md).

## Versione

La versione in uso sulla tua Machine. Gli aggiornamenti si installano automaticamente. Quando è disponibile una versione più recente su una Machine ospitata, **Aggiorna ora** la installa subito. L’operazione richiede qualche minuto e i tuoi dati restano al sicuro.

Sul tuo computer, un timer giornaliero installa ogni nuova versione firmata su Linux. Vedi [Usare The Machine sul tuo computer](self-hosted-setup.md).

## Ricerca per significato

In **Impostazioni**, **Modello**. Trova email, messaggi e note in base all’argomento, non solo alle parole usate. Su una Machine ospitata, se ne occupa una piccola IA sulla Machine stessa, senza inviare nulla altrove. È attiva a partire da 8 GB di memoria. Con 4 GB, puoi attivarla con l’interruttore. Usa circa mezzo gigabyte, quindi una Machine molto impegnata potrebbe rallentare.

Sul tuo computer, è il blocco `embeddings` in `config.json`. Riavvia la Machine dopo ogni modifica.

## Su questa Machine

Quando la tua Machine è sul tuo computer, alcune operazioni vengono eseguite lì, in un terminale:

- Il file delle impostazioni, `config.json`: tutte le impostazioni in un unico posto. Riavvia la Machine dopo ogni modifica.
- `assistant connect`: aggiungi una fonte, come `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: messaggi su Telegram. Vedi [Telegram](telegram.md).
- `assistant doctor`: controlla tutto e stampa una correzione per ogni problema.

## I tuoi indirizzi

Tutti gli indirizzi tuoi trovati dalla Machine: i tuoi account, gli alias Gmail o Outlook, il calendario, i profili Slack e Intercom. Le email e le riunioni provenienti da uno qualsiasi di questi indirizzi vengono considerate tue. Seleziona **Rimuovi** per un indirizzo che non è tuo.

Un indirizzo condiviso, come info@ o un Google Group, non viene mai considerato tuo da solo. Gli indirizzi di cui la Machine non è sicura si trovano in **Forse tuoi**. Scegli un’opzione:

- **Mio: rispondo solo io**: l’indirizzo viene considerato tuo. Le email che ricevi lì possono diventare tue attività.
- **Del team: rispondono anche altri**: l’indirizzo non è tuo. Le email inviate solo a quell’indirizzo non creano attività né bozze per te. Contribuiscono comunque a Graph.
- **Non è mio**: l’indirizzo non viene considerato tuo.

Scegli in base a chi risponde oggi. Una casella del team come support@ appartiene al team. Una come partnerships@, a cui rispondi solo tu, è tua. Cambia l’impostazione quando iniziano a rispondere anche altri.

Seleziona **Cambia** nella riga dell’indirizzo per modificare l’impostazione in seguito. Il tuo indirizzo di accesso personale è sempre tuo.

### I domini della tua azienda

I domini dei tuoi indirizzi personali vengono considerati domini della tua azienda. Ne usi anche un altro, come acme.co oltre ad acme.com? Inseriscilo in **I domini della tua azienda** e premi **Aggiungi**.

Le persone con quegli indirizzi vengono considerate colleghi, mai clienti: le loro conversazioni non compaiono nel Graph del team e non viene creata un’organizzazione per loro. Seleziona **Rimuovi** per eliminare di nuovo un dominio. Non puoi aggiungere domini email gratuiti come gmail.com.

Un tuo alias Gmail può anche essere usato come **Da** in una bozza, se Gmail conferma che puoi inviare messaggi da quell’indirizzo. Vedi [Gmail](gmail.md#what-it-can-send).
