---
title: Passaggi
area: fleet
summary: Passa un’attività alla Machine di un collega, con tutte le informazioni necessarie. Chiedi un aggiornamento più tardi o riprendila.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: acb60a24ef374625
---
## Passa un’attività

1. Nell’attività, apri **…**, poi **Passa…** e scegli **Un collega**.
2. Scegli a chi passarla, controlla cosa includere (× esclude una parte) e aggiungi una nota. Non vengono incluse informazioni di un account personale o di un’altra azienda.
3. Invia. La Machine del collega gliela mostra come attività.

La sua Machine gli invia una notifica sul telefono o su Telegram. Se non ha configurato nessuna delle due opzioni, gli invia un’unica email con il nome di chi gliel’ha passata, il titolo e un link. Vedi [Notifiche](notifications.md).

Viene inclusa anche una conversazione di Intercom. Se la sua Machine accede allo stesso spazio di lavoro Intercom, **Leggi il messaggio** la apre e la sua risposta viene inviata su Intercom. In caso contrario, l’attività contiene un link alla conversazione.

Mentre aspetti, l’attività indica cosa hai chiesto e quando ("Chiesto a Pat mar 3 nov: …"), ma solo se questo aggiunge informazioni al titolo. È nella sezione **Torna più tardi**, con la dicitura "Con Pat · in attesa" e una data per chiedere un aggiornamento. **Ricontatta ora** prepara un breve sollecito per Pat da inviare; **Cambia orario** sposta la data del promemoria.

Se la Machine di Pat non può inviargli notifiche, l’attività indica "Pat non riceverà una notifica. Avvisalo." Avvisa Pat tu. La dicitura scompare quando attiva le notifiche.

L’attività torna in cima solo quando c’è qualcosa da decidere: Pat ha risposto, ha rifiutato o ha completato l’attività, il passaggio non è riuscito oppure è arrivata una scadenza. Il promemoria dipende dalla scadenza: dopo qualche ora se è oggi, il giorno lavorativo precedente se è imminente, la mattina successiva se è urgente, altrimenti dopo 3 giorni lavorativi.

Quando torna per un promemoria, l’attività indica "Ancora con Pat". **Ricontatta ora** prepara un breve sollecito per Pat, nel posto in cui hai fatto la richiesta (Slack, WhatsApp, Telegram o email), direttamente nell’attività. Non viene inviato nulla finché non scegli **Invia**; poi l’attività resta in attesa di Pat. Se nessuna delle app collegate può inviare messaggi a Pat, si apre la chat e te lo comunica. Trovi **Riprendi** e **Passa a qualcun altro** sotto **…**, poi **Passa…**.

La chat dell’attività mostra quando è stata passata ("Passata alla Machine di Pat · 14:02") e cosa è successo: accettata, rifiutata (con una nota) o completata. Se non c’è ancora una risposta, propone **Segna come fatto**, **Posticipa** e **Non serve**. Per sollecitare Pat o riprendere l’attività, scrivilo nella chat.

Se il passaggio non è riuscito, l’attività e la chat lo indicano e mostrano **Riprova**.

## Passala a qualcun altro

Mentre l’attività è in mano a un collega, lo indica in una riga ("Con Pat · in attesa"). Trovi **Riprendi** e **Passa a qualcun altro** sotto **…**, poi **Passa…**. Se scegli **Riprendi**, l’attività torna a te: la Machine di Pat ne viene informata e le sue risposte non la spostano più.

**Passa a qualcun altro** apre il modulo per il passaggio. Puoi anche scriverlo nella chat dell’attività ("questa va passata a Kim"): l’attività indica allora "Ancora con Pat finché non la passi a Kim" e mostra **Rivedi il passaggio a** Kim.

Puoi passare un’attività a ciascun collega una sola volta: mentre è in mano a Pat, se lo scegli di nuovo nel modulo, puoi chiedergli un aggiornamento. **Chiedi un aggiornamento** prepara lo stesso sollecito, con una tua nota se ne aggiungi una.

**Riprendi da** Pat è attivo per impostazione predefinita; disattivalo per lasciare l’attività a entrambi. Non viene inviato nulla finché non scegli **Passa**. La Machine di Pat ne viene informata e la sua copia dell’attività scompare.

## Se rifiuta

Può spiegare il motivo: l’attività non è sua, è già stata completata o non ha tempo questa settimana. Poi puoi scegliere **Lo faccio io**, **Passa a qualcun altro** o **Segna come fatto**. Vale lo stesso se non risponde in tempo. **Lo faccio io** rimette l’attività tra le tue, nella sezione Per te.

## Qualcuno fuori dal Network

Scegli **Per email**: la tua Machine prepara un’email da inviare. Mentre scrivi, ti suggerisce prima le persone nella tua Fleet, poi quelle della tua azienda. Aggiungi una pagina attività per permettere loro di rispondere con un solo tocco: vedi [Pagine attività](task-pages.md).

Disponibile solo per le attività di Lavoro. Seleziona cosa includere: qualche riga sull’attività, la sua bozza, link e file. I contenuti Personali e Solo tu restano esclusi. **Prepara email** aggiunge l’email all’attività: leggila e poi inviala dalla tua casella di posta. Non viene tracciata.

Un’attività proveniente da Intercom o Slack non ha una propria casella di posta, quindi l’email viene inviata dalla tua casella di posta di Lavoro.

L’attività resta in attesa di una promessa finché la persona non risponde che l’ha completata o finché non la segni come completata. L’email termina con "Accetta l’attività nella tua Machine": se si iscrive tramite quel link, la persona può entrare nella tua Fleet e l’attività viene spostata nella sua Machine. Puoi disattivare questa riga in **Impostazioni**, nella sezione Fleet.
