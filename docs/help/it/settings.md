---
title: Impostazioni
area: settings
summary: Dove trovare ogni impostazione, dalla modalità chiara alla sicurezza e al tuo account.
covers: settings:general
code: dashboard.html
order: 1
---
Apri **Impostazioni** con l’ingranaggio in alto. Le sue schede:

- **Account**: **I tuoi indirizzi**, quelli che contano come te, con la loro provenienza. Il tuo piano in breve, i pulsanti per le pagine del tuo account ed **Esci**. Vedi [Piani e fatturazione](plans-and-billing.md).
- **Generale**: lingua e area geografica, questo dispositivo, il browser della tua Machine, la tua Fleet e il tuo account.
- **Sicurezza**: Standard o Prudente, e le impostazioni che applicano. Vedi [Livelli di sicurezza](security-levels.md). C’è anche **Accesso per l’assistenza**, finché è attivo: vedi [Ricevi assistenza](get-support.md#support-access).
- **Notifiche**: cosa ti arriva e dove, e il tuo orario di lavoro. Vedi [Notifiche](notifications.md) e [Orario di lavoro](work-hours.md).
- **Scrittura**: firme e il tuo modo di scrivere. Vedi [Scrittura](writing.md).
- **Skill**: istruzioni che la tua Machine segue. Vedi [Skill](skills.md).
- **Modello**: chi risponde per te, e i suoi limiti. Vedi [Modello](model.md). C’è anche **Codex e Claude Code**: vedi [Passa a Claude Code o Codex](hand-to-agent.md).

Una scheda senza niente da mostrare resta nascosta.

## Generale

- **Lingua e area geografica**: la tua **Area geografica** decide come si leggono le date (Oct 24 o 24 ott) e il formato orario abituale. **Formato dell’ora** sceglie invece 12 ore (2:05 PM) o 24 ore (14:05). Attività, Telegram, il riepilogo e i messaggi della Fleet lo seguono. Una Machine in hosting parte dal paese del fuso orario scelto all’iscrizione. Anche indicazioni come "3 ore fa" e i numeri lo seguono.
- **Lingua**: English, Nederlands, Français, Deutsch, Español, Italiano o Português (Brasil). La prima volta che apri la dashboard sceglie la lingua del tuo browser, se è una di queste (per ora il portoghese del Portogallo diventa portoghese brasiliano). La dashboard, le date, i messaggi Telegram, le notifiche, il riepilogo settimanale e le note e i titoli delle attività che la tua Machine scrive per te la seguono dal momento in cui la scegli; quello che era già scritto resta com’era. Le domande della Fleet e della Family arrivano nella lingua di ogni membro. Le bozze per altre persone restano nella lingua della loro conversazione. Anche Aiuto e le sue pagine la seguono.
- **Questo dispositivo**: l’app (**Installa l’app**), **Notifiche** con **Invia una prova**, e **Modalità chiara**, solo per questo browser o telefono. Vedi [Installa l’app e attiva le notifiche](phone-app.md).
- **Apri il browser della Machine ↗**: il browser che la tua Machine usa per siti come LinkedIn.
- **Regole Fleet**: vedi [Regole di condivisione](sharing-rules.md).
- **Account**: **Apri l’account** ed **Esci**, su una Machine in hosting.

## Su questa Machine

Alcune impostazioni stanno sul computer dove gira la tua Machine, non nell’app:

- `config.json`: tutte le impostazioni, in un solo file. Riavvia la Machine dopo una modifica.
- `assistant connect`: aggiungi una fonte, come `assistant connect gmail` o `assistant connect outlook`.
- `assistant telegram on` o `off`: messaggi su Telegram. Vedi [Telegram](telegram.md).
- `assistant doctor`: controlla tutto e indica una soluzione per ogni problema.

## I tuoi indirizzi

Ogni tuo indirizzo che la Machine ha trovato: i tuoi account, gli alias di Gmail o Outlook, il tuo calendario, il tuo profilo Slack e Intercom. Email e riunioni da uno qualsiasi di questi risultano come tue. **Rimuovi** quello che non è tuo.

Un indirizzo condiviso, come info@ o un Google Group, non conta mai da solo. Uno di cui la Machine non è sicura è sotto **Forse tuoi**, e non viene scelto nulla per te. Scegli:

- **Mio: rispondo solo io**: conta come tuo. La posta che gli arriva può diventare tue attività.
- **Del team: rispondono anche altri**: non sei tu. La posta inviata solo a quell’indirizzo non crea attività né bozze per te. Continua ad alimentare il Graph, condiviso con il tuo team come prima.
- **Non è mio**: non conta come tuo.

Scegli in base a chi risponde oggi. Una casella del team come support@ è del team. Una come partnerships@ a cui ora rispondi solo tu è tua; passala al team quando rispondono anche altri.

**Cambia** sulla sua riga lo modifica in seguito. Il tuo indirizzo di accesso è sempre tuo.

### I domini della tua azienda

I domini dei tuoi indirizzi contano come quelli della tua azienda. Se ne usa un altro, come acme.co accanto a acme.com, scrivilo sotto **I domini della tua azienda** e premi **Aggiungi**.

Le persone di quel dominio diventano tuoi colleghi, mai clienti: le loro conversazioni restano fuori dal Team Graph come ogni conversazione solo tra colleghi, e non viene creata un’organizzazione. **Rimuovi** lo toglie. Un dominio email gratuito come gmail.com non si può aggiungere.
