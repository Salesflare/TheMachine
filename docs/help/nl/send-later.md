---
title: Later versturen
area: cards
summary: Keur een bericht nu goed en kies wanneer het wordt verstuurd. Schrijft de ander eerst, dan komt het weer bij jou terug.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
translated: 29860e4848acce2e
---
## Een bericht inplannen

Klik in het venster waarin je een bericht controleert op **Later versturen**, naast **Nu versturen**. Kies **Over 2 uur**, **Morgen**, **maandag** of **Kies een datum** en klik op **Tijd opslaan**. Het bericht wordt op dat tijdstip in je eigen tijdzone verstuurd, precies zoals je het hebt gezien.

Dit werkt voor e-mail, Slack, WhatsApp, Telegram, Signal, Teams en Intercom. Het werkt niet voor LinkedIn en X, omdat je Machine vlak voor het versturen niet kan controleren of er een nieuw bericht is. Ook werkt het niet voor een antwoord in een document.

Je vindt deze optie ook bij **Nieuwe e-mail**. Als je meerdere berichten tegelijk controleert, worden ze allemaal verstuurd op het tijdstip dat je kiest.

## Terwijl het bericht wacht

De to-do staat onder **Komt later terug** en op de dag waarop het wordt verstuurd in de [Agenda](calendar.md), samen met het bericht en het tijdstip: ‘Wordt verstuurd op do 26 nov, 09:30’. Met **Nu versturen** verstuur je het meteen, met **Tijd wijzigen** kies je een ander tijdstip en met **Annuleren** maak je er weer een concept van. In de chat zie je hetzelfde.

Pas je het concept aan, rond je de to-do af, markeer je hem als niet nodig of haal je hem terug, dan wordt het bericht niet verstuurd. Je moet het opnieuw goedkeuren.

## Als de ander eerst schrijft

Schrijft de ander voordat het bericht wordt verstuurd, dan verstuurt je Machine het niet. De to-do komt terug met het bericht van die persoon, bijvoorbeeld: ‘Niet verstuurd: Sam Lee heeft eerst geschreven.’ Je krijgt ook de melding die je krijgt bij een gesnoozede to-do. Bij e-mail telt elk adres dat je Machine van die persoon kent, in elke mailbox die je hebt gekoppeld. Ook een antwoord van iemand anders in het gesprek telt.

Een automatisch antwoord, zoals een afwezigheidsbericht, houdt het versturen niet tegen. Een bericht van jezelf ook niet.

Vlak voordat het bericht wordt verstuurd, leest je Machine het gesprek opnieuw. Lukt dat niet, dan staat er bij de to-do: ‘Kan nog niet controleren of er een nieuw bericht is.’ Je Machine probeert het een uur lang opnieuw. Daarna vraagt hij het jou in plaats van het bericht te versturen.

Op WhatsApp controleert je Machine de berichten die je eigen gekoppelde WhatsApp tot dan toe heeft ontvangen.

## Als The Machine uitstaat

Staat je Machine op dat tijdstip uit, in slaapstand of ben je uitgelogd, dan wordt het bericht verstuurd zodra je Machine weer beschikbaar is, met maximaal een uur vertraging. Daarna komt de to-do terug met de melding ‘Niet verstuurd: het was meer dan een uur te laat.’ Jij beslist dan wat je doet.

Als je naar een andere computer overstapt, vragen geplande berichten daar opnieuw om je goedkeuring. Lees meer over [Overstappen](moving.md).

## Wie berichten kan inplannen

Alleen jij kunt berichten inplannen, in het dashboard of de app. Je Machine, de chat, een AI die je hebt gekoppeld en andere Machines kunnen geen berichten inplannen. Bij [Activiteit](activity.md) zie je wanneer een bericht is ingepland, gewijzigd, geannuleerd, verstuurd of niet verstuurd.
