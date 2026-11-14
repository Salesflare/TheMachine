---
title: Livelli di sicurezza
area: security
summary: Un solo interruttore, Standard o Prudente, imposta le tue preferenze di sicurezza e privacy. L’amministratore di una Fleet di lavoro sceglie il livello per la Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
translated: cf3ba86c8c1a23f3
---
## Due livelli

Apri **Impostazioni**, poi **Sicurezza**.

- **Standard**: le impostazioni predefinite di oggi. Non cambia nulla.
- **Prudente**: più restrittivo, se vuoi tenere meno informazioni sul telefono e conservarne meno.

Un livello è un punto di partenza. Puoi modificare qualsiasi impostazione: il livello diventa **Personalizzato**. Scegli di nuovo un livello per ripristinare le impostazioni.

## Cosa cambia per te con Prudente

- **Testo nelle notifiche** disattivato: una notifica dice «Nuova attività» o «Pronta», non cosa dice l’attività.
- **Proponi di salvare gli accessi** disattivato. I siti a cui hai effettuato l’accesso e che hai salvato restano finché non tocchi **Dimentica tutti gli accessi salvati**.
- **Cerca i contatti di lavoro**, **Proponi di condividere apprendimenti** e **Condividi cosa si chiede all’aiuto** disattivati.
- **Controlla quali dei miei contatti hanno una Machine** e **Lascia che mi trovi chi ha la mia email** disattivati.
- **Conserva i dettagli di Fallo per 90 giorni** disattivato: i dettagli vengono conservati per 30 giorni.
- **Cosa possono chiedere altre Machine alla mia** impostato su **Disattivata**: non è possibile pianificare con altre Machine. Vedi [Amici e Network](friends.md#scheduling-with-other-machines).
- In una Famiglia, gli orari di disponibilità richiedono prima la tua conferma. Con gli amici, il contesto della riunione viene rifiutato.

## Il livello di una Fleet di lavoro

Il proprietario della Fleet o un amministratore lo sceglie nelle impostazioni della Fleet: in **Impostazioni** › **Account**, premi **Fleet**. Tutti nella Fleet possono vederlo. Quando è impostato su Prudente:

- Le risposte ai colleghi aspettano la tua conferma, senza nomi e solo se riguardano persone dei tuoi account di lavoro.
- Anche le presentazioni e i passaggi aspettano la tua conferma.
- Il Graph del team condivide le email dei clienti senza gli allegati.
- Le notifiche delle attività di lavoro non mostrano il testo.
- I contatti di lavoro non vengono cercati.
- La tua Machine non controlla i tuoi contatti sul Network né permette di trovarti tramite email, a meno che tu non abbia attivato questa opzione.
- Tutti devono effettuare di nuovo l’accesso ogni 7 giorni.
- Un link d’invito funziona solo con l’indirizzo email a cui è stato inviato.

I membri possono scegliere impostazioni più restrittive di quelle della Fleet, ma non meno restrittive. Le loro scelte vengono conservate e ripristinate se la Fleet torna a Standard.

## Cosa non cambia

Non viene inviato nulla senza la tua conferma: vedi ogni bozza e premi Invia. Fallo e gli agenti di programmazione funzionano allo stesso modo. Per accedere serve sempre un codice di autenticazione o una passkey.
