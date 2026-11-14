---
title: Vrienden en het Network
area: fleet
summary: Voeg vrienden toe op gebruikersnaam, vind bekenden met een Machine en koppel een Machine op je eigen computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 3565b3898b234575
---
## Vrienden

Voeg iemand toe met de exacte gebruikersnaam, op het tabblad **Fleet** onder Vrienden. Vrienden kunnen vragen wie iemand kent, context over afspraken en introducties via gezamenlijke contacten krijgen, en zien wanneer je bezet bent (alleen wanneer, nooit waarvoor). Je kunt een vriend altijd verwijderen of blokkeren.

## Bekenden vinden

In **Fleet**, onder **Network**:

- **Controleren welke van mijn contacten een Machine hebben** stelt mensen voor die je kent.
- **Mensen met mijn e-mailadres toestaan mij te vinden** zorgt ervoor dat zij je kunnen vinden.

Beide staan standaard aan en staan uit op het beveiligingsniveau Zorgvuldig. Je kunt ze altijd uitzetten. Je keuze blijft bewaard. Mensen kunnen je vinden via je e-mailadres voor aanmelden (altijd aan) en je gekoppelde adressen. Je kunt elk adres apart in- en uitschakelen onder **Vindbaar voor**, behalve gedeelde adressen zoals info@, die uit blijven tot je ze aanzet.

Bekenden verschijnen meteen zodra je dit aanzet, en ook wanneer ze zich later aanmelden. Bij elke persoon kun je kiezen voor **Verbinden**, **Niet nu** of **Nooit voorstellen**. Zodra jullie vrienden zijn, wordt die persoon niet meer voorgesteld. Met **Het Network verlaten** word je uit het Network verwijderd.

Bij mensen die het systeem vindt, staat **Heeft een Machine** in je lijst Personen. Er wordt gekeken naar de adressen in je berichten en naar adressen die je aan iemand hebt toegevoegd met **Bewerken**. Als iemand zich met een ander adres heeft aangemeld, voeg dat adres dan toe aan die persoon. Op de pagina van iemand die is gevonden, stuurt **Toevoegen als vriend** hetzelfde verzoek als Verbinden (**Toevoegen als familie** staat in het ⋯-menu).

Bij iemand zonder Machine staat **Uitnodigen voor The Machine**. Daarmee open je de e-mail die diegene krijgt bij **Deze e-mail versturen?**, dezelfde e-mail als bij elke to-do. Je kunt die nog aanpassen. Er wordt niets verstuurd voordat je op **Nu versturen** drukt. Sluit je het venster, dan blijft de uitnodiging als to-do staan. Kun je geen e-mail versturen vanuit je mailbox? Kies dan **Kopiëren** of **Openen in je mail**.

Telefoonnummers tellen ook mee: de nummers in je WhatsApp-chats met mensen aan wie je hebt geschreven of die je hebt ontmoet, en nummers die je hebt toegevoegd met **Bewerken**. Je gekoppelde WhatsApp-nummer en de nummers onder **Over jou** maken je vindbaar. Je kunt elk nummer apart in- en uitschakelen onder **Vindbaar voor**. Een nummer vindt iemand alleen als diegene jou ook heeft opgezocht of als jullie vrienden zijn. Zo kan niemand nummers proberen om te zien wie een Machine heeft.

## Afspraken maken met andere Machines

Als iemand met een Machine schrijft: "Laten we volgende week afspreken", vraagt jouw Machine aan die van die persoon wanneer je vrij bent en zoekt hij een moment dat jullie allebei uitkomt, binnen je werkuren. Jullie krijgen allebei één to-do, zoals "Afspreken met Alex Example", met de tijd eronder. Tik op **Boek het**, **Andere tijd** of **Niet nodig**. De uitnodiging wordt pas verstuurd als jullie allebei op Boek het hebben getikt.

Alleen je beschikbaarheid, vrij of bezet, wordt gedeeld, end-to-end versleuteld, voor maximaal 14 dagen en afgerond op 15 minuten. Privéafspraken tellen als bezet. Een Machine kan dit alleen vragen als jullie allebei over en weer hebben gemaild. Stel dit in onder **Wat andere Machines de mijne mogen vragen**: **Vrij/bezet om af te spreken** of **Uit**, samen met de duur van je afspraak, de buffer en je voorkeurstijden. Elke vraag staat onder Agenda in **Activiteit**.

Is er geen Machine aan de andere kant, of komt er geen antwoord? Dan bevat het e-mailconcept een link waarmee de ander een van je vrije momenten kan kiezen. Die keuze wordt een to-do met **Boek het**. Er wordt niets geboekt voordat je erop tikt.

De link toont alleen vrije momenten, volgens dezelfde regels, en verder niets over jou. De link verloopt zodra de afspraak is geboekt of na 14 dagen. In de e-mail staat "Kies een tijd". Onderaan de pagina staat "Je Machine heeft deze tijden gevonden. Ontdek de jouwe." met je voornaam. Zet dit uit met **Voettekst bij boekingslinks**. Elke link en keuze staat in **Activiteit**.

## Een Machine op je eigen computer

Zo word je lid van het Network met een Machine die je zelf beheert:

1. Open in het dashboard van je Machine **Instellingen** en druk op **Word lid van het Network**.
2. Meld je aan op de pagina die wordt geopend (of maak een account aan) en bevestig. Je Machine pikt dit vanzelf op, zonder opnieuw opstarten.

Je kunt ook nog steeds de code gebruiken: druk op **Een zelfgehoste Machine koppelen** op je accountpagina op app.themachine.computer, voer daarna `assistant fleet-pair` uit met de code op je computer en start opnieuw op. De code werkt één keer en is 15 minuten geldig.

Je kunt maximaal 5 Machines per account hebben. Je kunt elke Machine daar loskoppelen.
