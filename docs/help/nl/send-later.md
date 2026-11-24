---
title: Later versturen
area: cards
summary: Tik naast **Nu versturen** op **Later versturen** om een e-mail of bericht in te plannen. Je keurt het nu goed en kiest wanneer het wordt verstuurd. Als de ander eerst iets stuurt, wacht het bericht weer op jou.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, schedule an email, send at a time, delay, tomorrow morning, unsend, take back
translated: 6fa6af155c337981
---
## Een bericht inplannen

Tik in het venster waarin je een bericht controleert naast **Nu versturen** op **Later versturen**. Kies **Over 2 uur**, **Morgen**, **maandag** of **Kies een datum** en tik op **Tijd opslaan**. Het bericht wordt precies zoals je het hebt gezien op dat tijdstip verstuurd, in je eigen tijdzone.

Dit werkt voor e-mail, Slack, WhatsApp, Telegram, Signal, Teams en Intercom. Het werkt niet voor LinkedIn en X, omdat je Machine vlak voor het versturen niet kan controleren of er een nieuw bericht is. Het werkt ook niet voor een antwoord in een document.

Je vindt deze optie ook in **Nieuwe e-mail**. Als je meerdere berichten tegelijk controleert, worden ze allemaal verstuurd op het tijdstip dat je kiest.

## Terwijl het bericht wacht

De to-do staat onder **Komt later terug** en op de dag waarop hij wordt verstuurd in de [Agenda](calendar.md), samen met het bericht en het tijdstip: "Wordt verstuurd do 26 nov. om 09:30". Met **Nu versturen** verstuur je het meteen, met **Tijd wijzigen** kies je een ander tijdstip en met **Annuleren** maak je er weer een concept van. In de chat zie je hetzelfde.

Als je het concept bewerkt, de to-do afrondt, afwijst of terughaalt, wordt het bericht niet verstuurd. Je moet het opnieuw goedkeuren.

## Als de ander eerst iets stuurt

Als de ander iets stuurt voordat het bericht wordt verstuurd, verstuurt je Machine het niet. De to-do komt terug met het bericht van de ander, bijvoorbeeld: "Niet verstuurd: Sam Lee heeft eerst iets gestuurd." Je krijgt ook de melding die je krijgt bij een gesnoozede to-do. Voor e-mail telt elk adres dat je Machine van die persoon kent, in elke mailbox die je hebt gekoppeld. Ook een reactie van iemand anders in het gesprek telt mee.

Een automatisch antwoord, zoals een afwezigheidsbericht, houdt het versturen niet tegen. Een bericht van jezelf ook niet.

Vlak voor het versturen leest je Machine het gesprek opnieuw. Als dat niet lukt, staat er bij de to-do: "Kan nog niet controleren of er een nieuw bericht is." Je Machine probeert het daarna een uur lang opnieuw. Daarna vraagt hij het aan jou in plaats van het bericht te versturen.

Op WhatsApp controleert je Machine de berichten die je eigen gekoppelde WhatsApp tot dan toe heeft ontvangen.

## Als The Machine uitstaat

Als je Machine op dat tijdstip uitstaat, slaapt of is uitgelogd, wordt het bericht verstuurd zodra hij weer beschikbaar is, tot een uur later. Daarna komt de to-do terug met "Niet verstuurd: het bericht was meer dan een uur te laat." Dan beslis jij wat er gebeurt.

Als je naar een andere computer overstapt, vragen geplande berichten daar opnieuw om je akkoord. Lees meer over [Overstappen](moving.md).

## Wie berichten kan inplannen

Alleen jij kunt dat, via het dashboard of de app. Je Machine, zijn chat, een AI die je hebt gekoppeld en andere Machines kunnen geen berichten inplannen. [Activiteit](activity.md) laat zien wanneer een bericht is ingepland, gewijzigd, geannuleerd, verstuurd of niet verstuurd.
