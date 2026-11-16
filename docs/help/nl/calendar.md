---
title: Agenda
area: calendar
summary: De komende week op één plek: afspraken, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 93fe9794660b0ab2
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- afspraken uit de agenda's die je hebt gekoppeld,
- to-do's met die dag als deadline en gesnoozede to-do's op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een afspraak die in twee agenda's staat, wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd en met de voornaam van die persoon. Zulke afspraken maken nooit een to-do. Afspraken die de hele dag of meerdere dagen duren, worden op elke dag waarop ze vallen als hele-dagafspraken getoond. In Agenda staat een reis op elke dag bovenaan. In Week en Maand staat hij als één balk over de dagen heen, bijvoorbeeld ‘Reis naar Lissabon’.

Een gezamenlijke afspraak is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een afspraak die dag met diezelfde persoon staat op de regel van die afspraak.

**Te laat** komt bovenaan. Bij een afspraak met een open to-do staat **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die klaar lijkt, omdat je al hebt geantwoord of omdat de uitvoering heeft vastgesteld dat hij klaar is, wordt niet getoond als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen, of omhoog (of gebruik **Eerdere dagen tonen**) voor eerdere dagen. Je kunt terug tot een week voordat je je agenda koppelde. Bovenaan staat vanaf welke dag je de agenda bekijkt. Zodra de [geschiedenis](history.md) is ingeladen, kun je ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik op een dag om de items te bekijken.

Met **Vandaag**, ‹ en › bovenaan ga je naar andere weken of maanden. De weergave die je kiest, wordt onthouden op dat apparaat.

In het weekraster staan afspraken die tegelijk plaatsvinden naast elkaar, zodat ze leesbaar blijven. De rest wordt getoond als **+N**. Tik daarop om die dag in Agenda te openen.

## Iets openen

Klik op een regel om de chat van de to-do, de belofte, de reis of het evenement, of de afspraak te openen. Bij een afspraak die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een afspraak met gasten, zie je de details: wanneer, waar en wie. Iemand die Graph kent, en de organisaties en projecten waaraan de afspraak is gekoppeld, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de afspraak daar. Alleen kijken brengt niets teweeg.

Een vergaderruimte die bij een afspraak is geboekt, staat bij de locatie. Hij verschijnt nooit als persoon of in je Graph.

Een link voor een afspraak wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de afspraak om deel te nemen.

## Reizen en evenementen

Als er een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar: de heenreis, het hotel en de terugreis. De reis wordt als één balk over de dagen heen getoond. Open de reis om de boekingscode, stoel en het ticket van elke boeking op chronologische volgorde te bekijken.

Tickets voor een concert, wedstrijd, festival of conferentie maken een evenement aan, één per evenement, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat via je werkmailbox is geboekt, is Werk. Anders is het Persoonlijk.

- Op elke regel staat van wie de boeking komt, bijvoorbeeld **Van Example Tickets**. Klik erop om de mail te openen.
- Als er een to-do uit de mail is gemaakt, bijvoorbeeld om de tickets te betalen, toont **De to-do openen** die to-do.
- Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen zijn geannuleerd, wordt ook de reis of het evenement verwijderd.

The Machine leest de gegevens uit de bevestigingsmails van luchtvaartmaatschappijen, hotels, boekingssites en ticketverkopers, zonder AI. Een mail zonder die gegevens levert niets op. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Aantekeningen en transcript van een afspraak

De details van een afspraak hebben twee onderdelen. **Notities** is de samenvatting: beslissingen en actiepunten. **Transcript** is woord voor woord wat er is gezegd. Het transcript is in eerste instantie ingeklapt en toont hoelang het duurt. Met **Tonen** open je het.

Als ze niet laden, probeert The Machine dat ongeveer een halve minuut automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Voor elk onderdeel zijn er aparte opties: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een afspraak die je kunt wijzigen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md) of [Google Meet](google-meet.md) is gekoppeld, staan de notities bij Notities en het transcript bij Transcript, met de aanduiding **Van Zoom** of **Van Google Meet**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden ze allebei getoond.

Notities kunnen ook worden toegevoegd aan de agenda-afspraak zelf nadat die is begonnen, of per mail van Zoom of Gemini binnenkomen. Na afloop van de afspraak maakt The Machine er alleen to-do's van als er duidelijke vervolgstappen in staan. Als dezelfde notities op twee manieren binnenkomen, wordt er één to-do gemaakt, met de afspraak als bron: ‘Bron: notities van’ de afspraak.

Bij een afspraak met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met erbij wie ze uitvoert, in de taal van de afspraak.

The Machine toont **Notities schrijven…** en gaat door als je de afspraak sluit. Bij een lange afspraak duurt dat een paar minuten en gebruikt hij je eigen model. De notities zijn voorzien van de vermelding **Geschreven door The Machine** en vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook zelf notities toevoegen. Vraag het op een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de teamvergadering van vandaag’. Een transcript komt bij Transcript te staan, een samenvatting bij Notities. Bij een afspraak met notities of een transcript staat **Notities** of **Transcript** in Agenda.

The Machine leest beide om de vervolgstappen van de afspraak te vinden. Die zijn Werk of Persoonlijk, net als de afspraak, en worden alleen met je team gedeeld als de afspraak ook met je team wordt gedeeld.

Je kunt een afspraak met deze details openen waar je hem ook tegenkomt: op een tijdlijn, in een zoekresultaat voor berichten of als bron van een to-do. Onderaan toont **Originele uitnodiging** de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. In Outlook en andere agenda's kun je alleen afspraken bekijken. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze onder **+** in de bovenbalk): kies de agenda, een titel en het tijdstip. Klik op een afspraak zonder gasten in die agenda om hem te wijzigen of **Verwijderen** (tik twee keer) om hem te verwijderen.

**Waar** stelt locaties voor terwijl je typt: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om locaties op te zoeken. Kies een suggestie of laat je eigen tekst staan.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Dit kan alleen in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat hoeveel mensen dat zijn: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten krijgt niemand een uitnodiging of update.

Een to-do kan ook een wijziging voorstellen, zoals een ophaalmoment toevoegen. Je ziet precies wat er verandert. Alleen met **Toevoegen**, **Opslaan** of **Verwijderen** voer je de wijziging door.

Nog geen afspraken? Als je geen agenda hebt, opent **Koppel je agenda** Koppelingen. Daar kun je [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md) koppelen.

## Conflicten met je andere agenda

Als een werkafspraak overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de afspraak die het laatst is toegevoegd. Hij kan een kort bericht opstellen om de afspraak te verplaatsen, of voorstellen om af te zeggen. Er wordt niets verstuurd totdat je het goedkeurt.

Afspraken die de hele dag duren, als vrij zijn gemarkeerd of voorlopig zijn, tellen niet mee. Elk conflict wordt één keer getoond. Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak conflicteert.

## Voorbereid op je afspraken

Voor een afspraak met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de afspraak. Dat is een korte briefing:

- **Wie:** wie ze zijn, volgens je Graph.
- **Laatste contact:** je laatste uitwisseling met hen. Na de afspraak is dat bericht de bron van de to-do.
- **Open beloftes:** wat jij of zij nog moeten doen.
- **Open vragen:** wat nog niet is beantwoord.
- **Beslissen of meenemen:** wat je moet bespreken of meenemen.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de afspraak als die 's middags plaatsvindt, anders op de werkdag ervoor. Hij gebruikt alleen informatie die al op je Machine staat. Je hoeft er alleen iets mee te doen door hem te lezen: tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag uit de briefing die actie vereist, krijgt een eigen to-do.

Zonder bruikbare geschiedenis wordt er geen to-do gemaakt. Terugkerende, interne en persoonlijke afspraken, en afspraken die zijn afgewezen, krijgen er geen. Als een afspraak wordt verplaatst, blijft de bijbehorende to-do bestaan en wordt het tijdstip aangepast. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde afspraak wordt automatisch afgesloten.

De details van de afspraak tonen de to-do onder **To-do**. Je opent de chat met één tik.
