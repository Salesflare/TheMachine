---
title: Impostazioni
area: settings
summary: Dove trovare ogni impostazione, dalla modalità chiara alla sicurezza e al tuo account.
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
Apri **Impostazioni** con l’icona a forma di ingranaggio in alto. Le schede:

- **Account**: **I tuoi indirizzi** (quelli che risultano tuoi) e **Esci**, in alto. Su una Machine ospitata trovi anche il tuo piano, le fatture, Fleet, gli amici, l’accesso e i dati, con **Annulla il piano** e **Elimina l’account** in fondo. Su una Machine sul tuo computer, collegata al Network, trovi Fleet, il nome utente, gli amici e l’accesso, ognuno con un link che apre la relativa sezione del tuo account (accedi lì), e **Elimina l’account** in fondo. Se non hai ancora effettuato il collegamento, trovi **Unisciti al Network** in alto. Vedi [Piani e fatturazione](plans-and-billing.md).
- **Generale**: lingua e area geografica, questo dispositivo, input vocale, il browser della tua Machine, Fleet, esportazione e importazione, e la versione in uso. Se non c’è la scheda Account, **Unisciti al Network** si trova in fondo.
- **Sicurezza**: Standard o Attenta. Vedi [Livelli di sicurezza](security-levels.md). Trovi anche **Accesso per l’assistenza**, quando è attivo: vedi [Contatta l’assistenza](get-support.md#support-access).
- **Movimenti**: tutto ciò che The Machine ha fatto per te, dal più recente. Vedi [Movimenti](activity.md).
- **Notifiche**: cosa ricevi e dove, e il tuo orario di lavoro. Vedi [Notifiche](notifications.md) e [Orario di lavoro](work-hours.md).
- **Scrittura**: firme e il tuo modo di scrivere. Vedi [Scrittura](writing.md).
- **Skill**: le guide che la tua Machine segue. Vedi [Skill](skills.md).
- **App**: le app di The Machine per il telefono e il computer, poi Claude, ChatGPT e le altre IA che hai collegato, e cosa può fare ognuna. Vedi [L’app mobile](mobile-app.md) e [Collegare altre IA](ai-connections.md).
- **Modello**: l’IA che legge e prepara bozze per te, e i suoi limiti. Vedi [Modello](model.md). C’è anche **Codex e Claude Code**: vedi [Passa a Claude Code o Codex](hand-to-agent.md). E **Ricerca per significato**, qui sotto.

Le schede senza contenuti sono nascoste.

## Generale

- **Lingua e area geografica**: **Area geografica** determina come vengono visualizzati date, orari e numeri (Oct 24 o 24 Oct). **Formato dell’ora** permette di scegliere il formato a 12 ore (2:05 PM) o a 24 ore (14:05). Attività, Telegram, il riepilogo e i messaggi Fleet seguono entrambe le impostazioni. Una Machine ospitata usa inizialmente il fuso orario scelto al momento della registrazione.
- **Lingua**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 o Русский. Inizialmente viene usata la lingua del browser. La dashboard, la guida, le notifiche, Telegram, il riepilogo settimanale e le attività che la tua Machine scrive passano alla nuova lingua non appena la selezioni. I testi precedenti restano invariati. I tuoi colleghi ricevono le domande Fleet e Fleet di famiglia nella propria lingua, mentre le bozze per altre persone restano nella lingua della conversazione.
- **Questo dispositivo**: **Installa l’app**, **Notifiche** con **Invia una prova** e **Modalità chiara**, solo per questo browser o telefono. Vedi [Installa l’app e attiva le notifiche](phone-app.md). Su [Omarchy](omarchy.md), c’è anche **Tema Omarchy**.
- **Input vocale**: come le parole che pronunci vengono trasformate in testo e quale voce usa Talk live. Vedi [Input vocale](voice-input.md) e [Conversazione dal vivo](talk-live.md).
- **Apri il browser della Machine ↗**: il browser che la tua Machine usa per siti come LinkedIn.
- **Regole Fleet**: vedi [Regole di condivisione](sharing-rules.md).
- **Esporta**:
  - **Tutto**: tutto ciò che la tua Machine sa, in un unico file crittografato, da trasferire o conservare. Usa **Importa** per importare un file. Vedi [Passa a un altro computer](moving.md).
  - **Conoscenze per un’altra IA**: ciò che la tua Machine ha imparato, in file leggibili da qualsiasi IA. Vedi [Conoscenze per un’altra IA](knowledge-export.md).

## Versione

La versione in uso sulla tua Machine. Gli aggiornamenti si installano automaticamente. Quando una nuova versione è pronta su una Machine ospitata, **Aggiorna ora** la installa subito. L’operazione richiede alcuni minuti e i tuoi dati restano al sicuro.

Sul tuo computer, un timer giornaliero installa ogni nuova versione firmata su Linux. Vedi [Usa la tua Machine sul tuo computer](self-hosted-setup.md).

## Ricerca per significato

In **Impostazioni**, **Modello**. Trova email, messaggi e note in base all’argomento, non solo alle parole usate. Su una Machine ospitata, se ne occupa una piccola IA direttamente sulla Machine, senza inviare nulla altrove. È attiva a partire da 8 GB di memoria. Con 4 GB, puoi attivarla con l’interruttore. Usa circa mezzo gigabyte, quindi una Machine molto impegnata può rallentare. Se è disattivata, la preparazione delle attività cerca comunque i messaggi correlati in base alle parole.

Sul tuo computer, è il blocco `embeddings` in `config.json`. Riavvia la Machine dopo una modifica.

## Su questa Machine

Quando la tua Machine è sul tuo computer, alcune operazioni si svolgono lì, in un terminale:

- Il file delle impostazioni, `config.json`: raccoglie tutte le impostazioni in un unico posto. Riavvia la Machine dopo una modifica.
- `assistant connect`: aggiungi una fonte, come `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: messaggi su Telegram. Vedi [Telegram](telegram.md).
- `assistant doctor`: controlla tutto e mostra una correzione per ogni problema.

## I tuoi indirizzi

Tutti gli indirizzi che la Machine ha associato a te: i tuoi account, gli alias Gmail o Outlook, il calendario e i profili Slack e Intercom. Le email e le riunioni provenienti da uno qualsiasi di questi indirizzi risultano tue. **Rimuovi** quelli che non ti appartengono.

Un indirizzo condiviso, come info@ o un Google Group, non risulta mai tuo automaticamente. Gli indirizzi di cui la Machine non è sicura si trovano in **Forse tuoi**. Scegli un’opzione:

- **Mio: rispondo solo io**: l’indirizzo risulta tuo. Le email ricevute lì possono diventare tue attività.
- **Del team: rispondono anche altri**: l’indirizzo non risulta tuo. Le email inviate solo a quell’indirizzo non creano attività né bozze per te. Contribuiscono comunque al Graph.
- **Non è mio**: l’indirizzo non risulterà tuo.

Scegli in base a chi risponde oggi. Una casella del team come support@ appartiene al team. Una come partnerships@ a cui rispondi solo tu è tua. Cambia l’impostazione quando iniziano a rispondere anche altre persone.

Seleziona **Cambia** sulla riga per modificare l’impostazione in seguito. L’indirizzo che usi per accedere resta sempre tuo.

### I domini della tua azienda

I domini dei tuoi indirizzi risultano appartenere alla tua azienda. Ne usi anche un altro, come acme.co oltre ad acme.com? Inseriscilo in **I domini della tua azienda** e premi **Aggiungi**.

Le persone di quei domini risultano quindi colleghi, non clienti: le loro conversazioni restano fuori dal Graph del team e non viene creata alcuna organizzazione per loro. **Rimuovi** elimina di nuovo il dominio. Non puoi aggiungere domini di email gratuite come gmail.com.

Un tuo alias Gmail può anche comparire nel campo **Da** di una bozza, se Gmail conferma che puoi inviare email da quell’indirizzo. Vedi [Gmail](gmail.md#what-it-can-send).
