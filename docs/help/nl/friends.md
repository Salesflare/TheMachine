---
title: Vrienden en het Network
area: fleet
summary: Voeg vrienden toe met hun gebruikersnaam, ontdek wie je kent met een Machine en koppel een Machine op je eigen computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 70a39b4999d112b7
---
## Vrienden

Voeg iemand toe met de exacte gebruikersnaam, in het tabblad **Fleet** onder Vrienden. Vrienden kunnen vragen wie iemand kent, meetingcontext en kennismakingen via gezamenlijke contacten krijgen en zien wanneer je bezet bent (alleen bezette tijden, nooit waarvoor). Dagen waarover je agenda niets zegt, worden weergegeven als onbekend, nooit als vrij. Je kunt een vriend op elk moment verwijderen of blokkeren.

## Mensen die je kent vinden

In **Fleet**, onder **Network**:

- Met ‘Controleren welke van mijn contacten een Machine hebben’ worden mensen voorgesteld die je kent.
- Met ‘Mensen met mijn e-mailadres mogen mij vinden’ kunnen zij jou vinden.

Beide staan standaard aan en staan uit bij het beveiligingsniveau Zorgvuldig. Je kunt ze op elk moment uitzetten. Je keuze blijft bewaard. Mensen kunnen je vinden via het e-mailadres waarmee je inlogt (staat altijd aan) en je gekoppelde adressen. Elk adres heeft een eigen schakelaar onder **Vindbaar voor**, behalve gedeelde adressen zoals info@, die uit blijven tot je ze aanzet.

Mensen die je kent verschijnen meteen als to-do zodra je dit aanzet, en later wanneer ze lid worden. Bij elk van hen kun je kiezen voor **Vriend** en **Familie** (**Koppelen** voor een collega), **Niet nu** en **Nooit voorstellen** in het ⋯-menu. Zodra jullie vrienden zijn, worden ze niet meer voorgesteld. Met **Het Network verlaten** verlaat je het Network.

Mensen die het systeem vindt, krijgen **Heeft een Machine** in je lijst met Personen. Het controleert de adressen in je berichten en de adressen die je bij iemand hebt gezet met **Bewerken**. Heeft iemand zich met een ander adres aangemeld, voeg dat dan toe. Op de pagina van iemand die het systeem heeft gevonden, verstuurt **Toevoegen als vriend** hetzelfde verzoek als Koppelen (**Toevoegen als familie** staat in het ⋯-menu).

Bij iemand zonder Machine staat **Uitnodigen voor The Machine**. Hiermee open je de e-mail die die persoon ontvangt bij **Deze e-mail versturen?**. Dit is dezelfde e-mail als bij elke to-do en je kunt hem aanpassen. Er wordt pas iets verstuurd nadat je op **Nu versturen** hebt gedrukt. Sluit het venster en de uitnodiging blijft als to-do staan. Heb je geen mailbox waarmee je kunt versturen, dan kun je **Kopiëren** of **Openen in je mail** kiezen.

Telefoonnummers tellen ook mee: de nummers in je WhatsApp-chats met mensen aan wie je hebt geschreven of die je hebt ontmoet, en de nummers die je hebt toegevoegd met **Bewerken**. Je gekoppelde WhatsApp-nummer en de nummers onder Over jou maken je vindbaar. Elk nummer heeft een eigen schakelaar onder **Vindbaar voor**. Met een nummer kan iemand je alleen vinden als diegene jou ook heeft opgezocht of als jullie vrienden zijn. Zo kan niemand nummers uitproberen om te zien wie een Machine heeft.

## Afspraken plannen met andere Machines

Als iemand met een Machine schrijft: ‘Laten we volgende week afspreken’, vraagt jouw Machine die van de ander om vrije tijden en zoekt hij een tijd die jullie allebei uitkomt, binnen je werkuren. Jullie krijgen allebei één to-do, zoals ‘Afspreken met Alex Example’, met de tijd eronder. Tik op **Boek het**, **Andere tijd** of **Niet nodig**. De uitnodiging wordt pas verstuurd nadat jullie allebei op Boek het hebben getikt.

Alleen beschikbaarheid, vrij of bezet, wordt end-to-end versleuteld gedeeld, voor maximaal 14 dagen en afgerond op 15 minuten. Privé-items tellen als bezet. Een Machine kan dit alleen vragen als jullie allebei elkaar een e-mail hebben gestuurd. Stel dit in bij **Wat andere Machines de mijne mogen vragen**: **Vrij/bezet om af te spreken** of **Uit**, samen met de duur van je meeting, de buffer en je voorkeurstijden. Elk verzoek staat in Activiteit, onder Agenda.

Een tijd geldt alleen als vrij wanneer je agenda dat aangeeft. Je Machine stelt geen tijden voor als er geen agenda is gekoppeld, als de agenda een dag lang niet kon worden gelezen of als de tijd meer dan 30 dagen vooruit ligt. Items die de hele dag duren tellen mee als bezet wanneer ze als Bezet zijn gemarkeerd. Items die als Vrij zijn gemarkeerd tellen nooit mee. Een agenda-item dat de hele dag duurt en door een to-do wordt toegevoegd, is Vrij, tenzij je die dagen afwezig of bezet bent. In dat geval staat er ‘bezet’ voordat je het toevoegt.

Is er geen Machine beschikbaar of komt er geen antwoord, dan krijgt het concept van de e-mail een link waarmee de ander een van je vrije tijden kan kiezen. De gekozen tijd wordt een to-do met **Boek het**. Er wordt niets geboekt voordat je erop tikt.

De link toont alleen vrije tijden, volgens dezelfde regels, en verder niets over jou. De link verloopt zodra de meeting is geboekt of na 14 dagen. In de e-mail staat ‘Kies een tijd’. Onderaan de pagina staat ‘De Machine van Alex heeft deze tijden gevonden. Ontdek die van jou.’, met je voornaam. Zet dit uit met **Voettekst bij boekingslinks**. Elke link en gekozen tijd staat in Activiteit.

## Een Machine op je eigen computer

Zo word je lid van het Network met een Machine die je zelf beheert:

1. Open in het dashboard van je Machine **Instellingen** en druk op **Word lid van het Network**.
2. Log in op de pagina die wordt geopend (of maak een account aan) en bevestig. Je Machine pikt dit vanzelf op, zonder opnieuw op te starten.

De methode met code werkt ook: druk op **Een zelfgehoste Machine koppelen** op je accountpagina op app.themachine.computer. Voer daarna `assistant fleet-pair` uit met de code op je computer en start opnieuw op. De code werkt één keer en is 15 minuten geldig.

Je kunt maximaal 5 Machines per account hebben. Je kunt elke Machine daar ontkoppelen.
