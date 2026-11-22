---
title: Vrienden en het Network
area: fleet
summary: Voeg vrienden toe met hun gebruikersnaam, vind bekenden die een Machine hebben en koppel een Machine op je eigen computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 637784bf811800bb
---
## Vrienden

Voeg iemand toe met diens exacte gebruikersnaam via het tabblad **Fleet**, onder Vrienden. Vrienden kunnen vragen wie iemand kent, meetingcontext en introducties via gemeenschappelijke contacten krijgen, en zien wanneer je bezet bent (alleen bezette tijden, nooit waarvoor). Je kunt een vriend op elk moment verwijderen of blokkeren.

## Bekenden vinden

Ga in **Fleet** naar **Network**:

- Met ‘Kijken welke van mijn contacten een Machine hebben’ krijg je bekenden voorgesteld.
- Met ‘Mensen met mijn e-mailadres kunnen mij vinden’ kunnen zij jou vinden.

Beide opties staan standaard aan en zijn uitgeschakeld bij het beveiligingsniveau Voorzichtig. Je kunt ze op elk moment uitzetten. Je keuze blijft bewaard. Mensen kunnen je vinden via het e-mailadres waarmee je inlogt (altijd aan) en je gekoppelde adressen. Elk adres heeft een eigen schakelaar onder **Vindbaar voor**, behalve gedeelde adressen zoals info@. Die blijven uit tot je ze aanzet.

Zodra je deze optie aanzet, verschijnen bekenden meteen als to-do. Nieuwe bekenden verschijnen zodra ze lid worden. Bij elke persoon kun je kiezen voor **Vriend** en **Familie** (**Verbinden** voor een collega), **Niet nu** of **Nooit voorstellen** in het ⋯-menu. Zodra jullie vrienden zijn, worden ze niet meer voorgesteld. Met **Het Network verlaten** haal je jezelf eruit.

Mensen die je Machine vindt, krijgen de aanduiding **Heeft een Machine** in je lijst met personen. Er wordt gekeken naar de adressen in je berichten en de adressen die je aan een persoon hebt toegevoegd met **Bewerken**. Heeft iemand zich met een ander adres aangemeld, voeg dat dan toe aan die persoon. Op de pagina van iemand die je Machine heeft gevonden, stuurt **Toevoegen als vriend** hetzelfde verzoek als Verbinden. **Toevoegen als familie** staat in het ⋯-menu.

Bij iemand zonder Machine verschijnt **Uitnodigen voor The Machine**. Daarmee open je de e-mail die diegene krijgt in **Deze e-mail versturen?**. Dit is dezelfde e-mail als bij elke to-do en je kunt die aanpassen. De e-mail wordt pas verstuurd als je op **Nu versturen** drukt. Sluit het venster en de uitnodiging blijft als to-do staan. Heb je geen mailbox waarmee je e-mail kunt versturen? Kies dan **Kopiëren** of **Openen in je mail**.

Telefoonnummers tellen ook mee: de nummers in je WhatsApp-chats met mensen aan wie je een bericht hebt gestuurd of die je hebt ontmoet, en de nummers die je met **Bewerken** hebt toegevoegd. Je gekoppelde WhatsApp-nummer en de nummers onder Over jou maken je vindbaar. Elk nummer heeft een eigen schakelaar onder **Vindbaar voor**. Een nummer kan iemand alleen vinden als diegene jou ook heeft opgezocht of als jullie vrienden zijn. Zo kan niemand nummers uitproberen om te zien wie een Machine heeft.

## Afspraken plannen met andere Machines

Als iemand met een Machine schrijft: ‘Laten we volgende week afspreken’, vraagt jouw Machine de Machine van die persoon om beschikbare tijden en zoekt een tijd die voor jullie allebei past, binnen je werkuren. Jullie krijgen allebei één to-do, zoals ‘Afspreken met Alex Example’, met de tijd eronder. Tik op **Boek het**, **Andere tijd** of **Niet nodig**. De uitnodiging wordt pas verstuurd als jullie allebei op Boek het hebben getikt.

Alleen beschikbaar of bezet wordt gedeeld, end-to-end versleuteld, voor maximaal 14 dagen en afgerond op 15 minuten. Privé-afspraken tellen als bezet. Een Machine kan dit alleen vragen als jullie over en weer e-mails naar elkaar hebben gestuurd. Stel dit in onder **Wat andere Machines de mijne mogen vragen**: **Vrij/bezet om af te spreken** of **Uit**, samen met de duur van je afspraken, de buffertijd en je voorkeurstijden. Elke aanvraag staat in Activiteit, onder Agenda.

Heeft de ander geen Machine of komt er geen antwoord? Dan krijgt het e-mailconcept een link waarmee die persoon een van je beschikbare tijden kan kiezen. De gekozen tijd verschijnt als to-do met **Boek het**. Er wordt niets geboekt voordat je erop tikt.

De link toont alleen beschikbare tijden, volgens dezelfde regels, en verder niets over jou. De link vervalt zodra de afspraak is geboekt of na 14 dagen. In de e-mail staat ‘Kies een tijd’. Onderaan de pagina staat ‘De Machine van Alex heeft deze tijden gevonden. Neem er zelf ook een.’, met je voornaam. Zet dit uit met **Voettekst bij boekingslinks**. Elke link en keuze staat in Activiteit.

## Een Machine op je eigen computer

Zo word je lid van het Network met een Machine die je zelf draait:

1. Open het dashboard van je Machine, ga naar **Instellingen** en druk op **Word lid van het Network**.
2. Log in op de pagina die wordt geopend (of maak een account aan) en bevestig. Je Machine pikt dit vanzelf op, zonder opnieuw opstarten.

De methode met een code werkt ook: druk op **Een zelf gehoste Machine koppelen** op je accountpagina op app.themachine.computer. Voer daarna `assistant fleet-pair` uit met de code op je computer en start opnieuw op. De code werkt één keer en is 15 minuten geldig.

Je kunt maximaal 5 Machines per account hebben. Je kunt ze daar allemaal ontkoppelen.
