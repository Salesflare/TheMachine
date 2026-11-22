---
title: Impostazioni
area: settings
summary: Dove trovare ogni impostazione, dalla modalità chiara alla sicurezza e al tuo account.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Apri **Impostazioni** con l’icona a forma di ingranaggio in alto. Le schede sono:

- **Account**: **I tuoi indirizzi** (quelli che la Machine considera tuoi) e **Esci**, in alto. Se hai una Machine ospitata, trovi anche il piano, le fatture, Fleet, gli amici, l’accesso e i dati, con **Annulla il piano** e **Elimina l’account** in fondo. Se hai una Machine sul tuo computer collegata al Network, trovi Fleet, il nome utente, gli amici e l’accesso, ognuno con un link che apre la sezione corrispondente del tuo account (da cui puoi accedere), e **Elimina l’account** in fondo. Se non è ancora collegata: **Unisciti al Network**, in alto. Vedi [Piani e fatturazione](plans-and-billing.md).
- **Generale**: lingua e area geografica, questo dispositivo, input vocale, il browser della tua Machine, Fleet, esportazione e importazione, e la versione in uso. Se non c’è la scheda Account, **Unisciti al Network** è in fondo.
- **Sicurezza**: Standard o Prudente. Vedi [Livelli di sicurezza](security-levels.md). C’è anche **Accesso per l’assistenza**, quando è attivo: vedi [Contatta l’assistenza](get-support.md#support-access).
- **Movimenti**: tutto quello che The Machine ha fatto per te, dal più recente. Vedi [Movimenti](activity.md).
- **Notifiche**: cosa ti arriva e dove, e il tuo orario di lavoro. Vedi [Notifiche](notifications.md) e [Orario di lavoro](work-hours.md).
- **Scrittura**: firme e il tuo modo di scrivere. Vedi [Scrittura](writing.md).
- **Skill**: le guide che la tua Machine segue. Vedi [Skill](skills.md).
- **App**: le app di The Machine per il telefono e il computer, poi Claude, ChatGPT e le altre IA che hai collegato, e cosa può fare ciascuna. Vedi [L’app mobile](mobile-app.md) e [Collega altre IA](ai-connections.md).
- **Modello**: l’IA che legge e prepara bozze per te, e i suoi limiti. Vedi [Modello](model.md). C’è anche **Codex e Claude Code**: vedi [Passa a Claude Code o Codex](hand-to-agent.md). E **Ricerca per significato**, più sotto.

Le schede senza contenuti da mostrare sono nascoste.

## Generale

- **Lingua e area geografica**: **Area geografica** imposta il formato di date, ore e numeri (24 ott o ott 24). **Formato dell’ora** sceglie tra 12 ore (2:05 PM) e 24 ore (14:05). Le attività, Telegram, il riepilogo e i messaggi Fleet seguono entrambe le impostazioni. Una Machine ospitata usa il fuso orario che hai scelto al momento della registrazione.
- **Lingua**: inglese, olandese, francese, tedesco, spagnolo, italiano, portoghese (Brasile), cinese semplificato, giapponese, coreano o russo. La lingua iniziale dipende da quella del browser. La dashboard, la Guida, le notifiche, Telegram, il riepilogo settimanale e le attività scritte dalla tua Machine cambiano lingua da quando fai la scelta. I testi più vecchi restano invariati. I compagni di squadra ricevono le domande di Fleet e Famiglia nella propria lingua, mentre le bozze per gli altri restano nella lingua della conversazione.
- **Questo dispositivo**: **Installa l’app**, **Notifiche** con **Invia una prova** e **Modalità chiara**, solo per questo browser o telefono. Vedi [Installa l’app e attiva le notifiche](phone-app.md). Su [Omarchy](omarchy.md) trovi anche **Tema Omarchy**.
- **Input vocale**: come le tue parole diventano testo e quale voce usa Talk live. Vedi [Input vocale](voice-input.md) e [Parla dal vivo](talk-live.md).
- **Apri il browser della Machine ↗**: il browser che la tua Machine usa per siti come LinkedIn.
- **Regole Fleet**: vedi [Regole di condivisione](sharing-rules.md).
- **Esporta**:
  - **Tutto**: tutto quello che la tua Machine sa, in un unico file crittografato, da trasferire o conservare; usa **Importa** per importarne uno. Vedi [Passa a un altro computer](moving.md).
  - **Conoscenze per un’altra IA**: ciò che la tua Machine ha imparato, in file leggibili da qualsiasi IA. Vedi [Conoscenze per un’altra IA](knowledge-export.md).

## Versione

La versione in uso sulla tua Machine. Gli aggiornamenti si installano automaticamente. Quando una nuova versione è pronta su una Machine ospitata, **Aggiorna ora** la installa subito. L’operazione richiede qualche minuto e i tuoi dati restano al sicuro.

Sul tuo computer, un timer giornaliero installa ogni nuova versione firmata su Linux. Vedi [Usa la tua Machine sul tuo computer](self-hosted-setup.md).

## Ricerca per significato

In **Impostazioni**, **Modello**. Trova email, messaggi e note in base all’argomento, non solo alle parole usate. Su una Machine ospitata, se ne occupa una piccola IA direttamente sulla Machine, senza inviare nulla altrove. È attiva da 8 GB di memoria. Con 4 GB, attivala con l’interruttore. Usa circa mezzo gigabyte, quindi una Machine molto occupata potrebbe rallentare.

Sul tuo computer, è il blocco `embeddings` in `config.json`. Riavvia la Machine dopo ogni modifica.

## Su questa Machine

Quando la tua Machine è sul tuo computer, alcune operazioni si fanno lì, in un terminale:

- Il file delle impostazioni, `config.json`: tutte le impostazioni in un unico posto. Riavvia la Machine dopo ogni modifica.
- `assistant connect`: aggiunge una fonte, come `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: messaggi su Telegram. Vedi [Telegram](telegram.md).
- `assistant doctor`: controlla tutto e mostra una correzione per ogni problema.

## I tuoi indirizzi

Tutti gli indirizzi che la Machine ha trovato: i tuoi account, gli alias di Gmail o Outlook, il tuo calendario e i tuoi profili Slack e Intercom. Le email e le riunioni provenienti da uno qualsiasi di questi indirizzi vengono considerate tue. Usa **Rimuovi** per eliminare un indirizzo che non è tuo.

Un indirizzo condiviso, come info@ o un Google Group, non viene mai considerato tuo automaticamente. Gli indirizzi su cui la Machine ha dei dubbi si trovano in **Forse tuoi**. Scegli una voce:

- **Mio: rispondo solo io**: viene considerato tuo. Le email ricevute lì possono diventare attività.
- **Del team: rispondono anche altri**: non è tuo. Le email inviate solo a quell’indirizzo non creano attività o bozze per te. Continuano comunque a completare il Graph.
- **Non è mio**: non verrà considerato tuo.

Scegli in base a chi risponde oggi. Una casella del team come support@ appartiene al team. Una come partnerships@, a cui rispondi solo tu, è tua. Cambiala quando iniziano a rispondere anche altri.

**Cambia**, nella riga dell’indirizzo, ti permette di modificarlo in seguito. L’indirizzo che usi per accedere è sempre tuo.

### I domini della tua azienda

I domini dei tuoi indirizzi appartengono alla tua azienda. Ne usi anche un altro, come acme.co oltre ad acme.com? Inseriscilo in **I domini della tua azienda** e premi **Aggiungi**.

A quel punto, le persone con questi domini sono considerate colleghe, mai clienti: le loro conversazioni restano fuori dal Graph del team e non viene creata un’organizzazione per loro. **Rimuovi** elimina di nuovo il dominio. Non puoi aggiungere domini di email gratuite come gmail.com.

Un alias Gmail tuo può anche essere indicato come **Da** in una bozza, se Gmail conferma che puoi inviare email da quell’indirizzo. Vedi [Gmail](gmail.md#what-it-can-send).
