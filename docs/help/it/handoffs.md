---
title: Passaggi
area: fleet
summary: Condividi un’attività con un collega o passala alla sua Machine con **Passa…**. Ricontatta la persona più tardi oppure riprendi l’attività.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: d9b21c04fb0d34a6
---
## Passa un’attività

1. Nell’attività, apri **…**, poi **Passa…** e scegli **Un collega**.
2. Scegli a chi passarla, controlla cosa includere (× esclude una parte) e aggiungi una nota. Non viene condiviso nulla da un account Personal o da un’altra azienda.
3. Inviala. La sua Machine la mostra come attività.

La sua Machine lo avvisa sul telefono o su Telegram. Se non ha configurato nessuno dei due, riceve una sola email con il nome di chi ha passato l’attività, il titolo e un link. Vedi [Notifiche](notifications.md).

Viene passata anche una conversazione Intercom. Se la sua Machine legge lo stesso spazio di lavoro Intercom, **Leggi il messaggio** la apre e la risposta viene inviata su Intercom. Altrimenti, l’attività contiene un link alla conversazione.

Nel frattempo, l’attività indica cosa hai chiesto e quando ("Chiesto a Pat mar 3 nov: …"), ma solo se queste informazioni aggiungono qualcosa al titolo. Compare sotto **Torna più tardi**, con la dicitura "Con Pat · in attesa" e una data per ricontattare la persona. **Ricontatta ora** prepara un breve sollecito per Pat da inviare; **Cambia orario** sposta la data del ricontatto.

Se la Machine di Pat non può avvisarlo, l’attività indica "Pat non riceverà una notifica. Avvisalo tu." Contatta Pat direttamente. Questa dicitura scompare quando attiva le notifiche.

L’attività torna in cima solo quando c’è qualcosa da decidere: Pat ha risposto, ha rifiutato o completato l’attività, il passaggio non è riuscito oppure è arrivata una scadenza. Il ricontatto segue la data di scadenza: dopo qualche ora se è oggi, il giorno lavorativo precedente se è vicina, la mattina successiva se è urgente, altrimenti dopo 3 giorni lavorativi.

Quando torna per un ricontatto, l’attività indica "Ancora con Pat". **Ricontatta ora** prepara un breve sollecito per Pat nel canale in cui hai fatto la richiesta (Slack, WhatsApp, Telegram o email), direttamente nell’attività. Il messaggio non viene inviato finché non scegli **Invia**; poi l’attività resta in attesa di Pat. Se nessuno dei servizi che hai collegato può inviare un messaggio a Pat, si apre la chat e te lo indica. **Riprendi** e **Passa a qualcun altro** si trovano in **…**, poi **Passa…**.

La chat dell’attività mostra quando è stata passata ("Passata alla Machine di Pat · 14:02") e l’esito: accettata, rifiutata (con la sua nota) o completata. Se non ha ancora risposto, trovi **Segna come fatto**, **Posticipa** e **Non serve**. Per sollecitarlo o riprendere l’attività, scrivilo nella chat.

Se il passaggio non è riuscito, l’attività e la chat lo indicano e mostrano **Riprova**.

## Cosa vede

Solo quell’attività: la tua richiesta, la tua nota, la data di scadenza e il contatto, oltre alle copie dei messaggi inclusi (fino a tre, senza allegati). Non vede la tua casella di posta né le altre tue attività. Può scegliere **Accetta** o **Rifiuta**.

Quando accetta, l’attività diventa sua. La tua risulta completata oppure resta in attesa del suo esito se ha un **Fatto quando**. Non lavorate entrambi sulla stessa attività: se vuoi chiedere a qualcuno di esaminarla mentre resta tua, usa [Chiedi una revisione](ask-to-review.md).

## Passala invece a qualcun altro

Mentre un collega ha l’attività, una riga lo indica ("Con Pat · in attesa"). In **…**, poi **Passa…**, trovi **Riprendi** e **Passa a qualcun altro**. **Riprendi** ti restituisce l’attività: la Machine di Pat riceve una notifica e la sua risposta non la sposterà più.

**Passa a qualcun altro** apre il modulo per passare l’attività. Oppure scrivilo nella chat dell’attività ("questa dovrebbe andare a Kim"): l’attività indica "Ancora con Pat finché non la passi a Kim" e mostra **Rivedi il passaggio a** Kim.

Puoi passare un’attività a ogni collega una sola volta: mentre Pat ce l’ha, sceglierlo di nuovo nel modulo serve a ricontattarlo. **Chiedi un aggiornamento** prepara lo stesso sollecito, con una tua riga se ne aggiungi una.

**Riprendi da** Pat è attivo per impostazione predefinita. Disattivalo per lasciare l’attività a entrambi. Il passaggio non viene inviato finché non scegli **Passa**. La Machine di Pat riceve una notifica e la sua copia dell’attività viene rimossa.

## Quando rifiuta

Può indicare il motivo: l’attività non è sua, è già stata completata oppure non ha tempo questa settimana. Poi puoi scegliere **Lo faccio io**, **Passa a qualcun altro** o **Segna come fatto**. Lo stesso vale se non risponde in tempo. **Lo faccio io** fa tornare l’attività tra le tue, sotto Per te.

## Qualcuno fuori dal Network

Scegli **Per email**: la tua Machine prepara un’email da inviare. Mentre scrivi, suggerisce prima le persone della tua Fleet, poi quelle della tua azienda. Aggiungi una pagina attività, così può rispondere con un solo tocco: vedi [Pagine delle attività](task-pages.md).

Disponibile solo per le attività di lavoro. Seleziona cosa includere: qualche riga sull’attività, la bozza, i link e i file. I contenuti Personal e Solo tu restano esclusi. **Prepara email** aggiunge l’email all’attività: leggila, poi inviala dalla tua casella di posta. Non viene tracciata.

Un’attività proveniente da Intercom o Slack non ha una propria casella di posta, quindi l’email viene inviata dalla tua casella di lavoro.

L’attività tiene traccia della promessa finché la persona non risponde che è stata completata oppure finché non la contrassegni come completata. L’email termina con "Occupatene nella tua Machine": se si iscrive tramite quel link, può entrare nella tua Fleet e l’attività passa alla sua Machine. Puoi disattivare questa riga in **Impostazioni**, nella sezione Fleet.
