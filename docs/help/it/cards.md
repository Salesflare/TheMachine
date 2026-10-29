---
title: Attività
area: cards
summary: Un'attività per ogni cosa che ha bisogno di te, pronta per il tuo sì. Cosa significano le parti di un'attività.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
La tua Machine legge tutto ciò che è nuovo e crea un'attività solo quando qualcosa ha bisogno di te. Un'attività per questione, per quanti messaggi comprenda.

## Dove stanno le attività

La scheda **Suggerimenti** le raggruppa:

- **Pronta per te**: preparata e in attesa della tua approvazione.
- **Serve una tua decisione**: qualcosa che puoi decidere solo tu.
- **In preparazione**: la tua Machine ci sta lavorando. Un'attività a cui hai appena detto **Fallo** resta dov'era mentre si prepara, poi passa in **Pronta per te**.
- **Torna più tardi**: posticipate.
- **Sembrano fatte**: attività che sembrano già concluse. Chiuse, subito sopra **Fatte / ignorate**.
- **Fatte / ignorate**: tutte le attività concluse, dalla più recente, 30 alla volta mentre scorri.

In **Sembrano fatte** ogni attività è una riga: il titolo e ciò che mostra che è fatta, come "PR #3451 unita". **Fatto** ne chiude una, **Segna tutte come fatte** le chiude tutte (con **Annulla**), e **Non fatto** la rimette come attività normale, così la tua Machine ne tiene conto. Tocca una riga per vedere l’attività intera. Non risultano mai in ritardo e non contano come in attesa di te. Niente si chiude senza di te.

Un’attività il cui ultimo passo è ancora aperto da parte di qualcun altro, come una revisione, un merge o una risposta, mostra **In attesa di:** quel passo e resta aperta. Aspetta in **In attesa di altri**, chiusa sopra Torna più tardi, e non conta come pronta per te. Un nuovo messaggio su di essa la riporta indietro.

**Tutto a posto.** significa che ora niente ha bisogno di te. La riga sotto dice quando la tua Machine ha controllato l’ultima volta.

**Tutti**, **Lavoro** e **Personale** sopra l'elenco nella barra laterale mostrano tutte le attività o solo un tipo. La tua Machine ricorda la scelta, così telefono e computer mostrano lo stesso elenco. Quando è attivo Lavoro o Personale, la parte alta dell'elenco lo indica, con **Mostra tutto** per tornare indietro.

Un'attività su un progetto mostra il nome del progetto nella riga sotto il titolo, che apre il progetto. **Cambia progetto** in **Altro** lo cambia (su un'attività fatta, in **Dettagli**). Vedi [le attività di un progetto](graph.md#a-projects-to-dos).

## I pulsanti

Una nuova attività ha **Fallo**, **Segna come fatto**, **Posticipa**, **Fallo diversamente** e **Non serve**. Se ne vedono solo alcuni alla volta; gli altri sono in **Altro**, con **Rinomina**.

- **Fallo**: la tua Machine la prepara. Vedi [Fallo](do-it.md).
- **Segna come fatto**: è sistemata.
- **Posticipa**: falla tornare più tardi. Vedi [Posticipa](snooze.md).
- **Fallo diversamente**: dille cosa preferiresti, in poche parole. Su un'attività preparata diventa **Chiedi modifiche**: di' cosa cambiare nella bozza e la rifà. **Rivedi e invia** resta accanto.
- **Non serve**: sparisce. Scegli il motivo, se vuoi: **Non pertinente**, **Fatti sbagliati** o **Già gestito**. La tua Machine ne impara.

Un'attività chiusa può tornare con **Riapri**. Torna anche da sola quando succede qualcosa di nuovo, come un nuovo messaggio dall'altra persona. La tua risposta non la fa tornare.

Un'attività che contava solo fino a un certo momento, come una conferma prima di una riunione, si chiude da sola quando quel momento è passato. Passa tra quelle fatte con "Non serve più" e quando era. **Annulla** la riporta indietro per un giorno.

Sulle tue prime attività, una riga breve sotto i pulsanti mostra l'essenziale: **Fallo diversamente** (o **Chiedi modifiche**) e **Non serve** quando un'attività non è proprio giusta, e sulla tua prima bozza pronta, che non parte nulla finché non premi **Invia**. Un suggerimento sparisce per sempre appena usi il suo pulsante o premi ×, su tutti i tuoi dispositivi.

Ogni attività inizia con il suo titolo. La riga sotto dice chi riguarda, la sua organizzazione, il progetto, Lavoro o Personale (sotto **Tutti**) e quando è arrivata, più a che punto è quando il suo gruppo non lo dice già. Tocca un nome per aprirne la pagina nel Graph.

Un titolo dice cosa c'è da fare. Cambia solo quando cambia quello, come per una nuova richiesta. Un'attività fatta mantiene il suo titolo, con sotto come è finita, come cosa è stato inviato o "Fatto: Sam ha firmato martedì".

**Dettagli** mostra il messaggio da cui viene (toccalo per leggere la conversazione), la tua ultima nota e il risultato di un agente di codice. **Chat ›** alla fine di quella riga apre la chat. Un'attività fatta resta breve: il titolo, una riga e cosa è partito.

Un'attività "In attesa di" (qualcuno ti ha promesso qualcosa) ha il link al tuo ultimo messaggio a quella persona, quello a cui aspetti risposta: "Email a Pat · mar".

## Creane una tu

**Nuova attività** (sotto **Trova un’attività** su un computer) aggiunge un'attività per qualsiasi cosa. Crearla non invia niente.

- **Scadenza**: scrivi un giorno o un'ora, come "domani", "ven prossimo", "3 nov", "15:00", "2pm", "tra 2 ore" o "domani 9". Capisce anche altre lingue ("over 2 uur", "morgen 9u"). L'icona del calendario ha scelte rapide, come quando posticipi, e **Scegli una data**.
- **Email**: allega l'email a cui si riferisce. Cerca solo nella tua email, per oggetto o mittente.
- **File**: tocca la graffetta nel riquadro, incolla uno screenshot o trascina i file sul modulo. Su un telefono puoi anche scattare una foto. Fino a 5 file, degli stessi tipi e dimensioni della chat (vedi [Aggiungi file](card-chat.md#add-files)). × ne toglie uno.

I file restano con l'attività: compaiono sull'attività e nella sua chat, e The Machine li legge quando ci lavora.
