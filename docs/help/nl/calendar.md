---
title: Agenda
area: calendar
summary: De komende week op één plek: afspraken, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: ae462ef9e7316cb6
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- afspraken uit de agenda's die je hebt gekoppeld,
- to-do's met een deadline op die dag en gesnoozede to-do's op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit boekings- en ticketmails.

Een afspraak in twee agenda's wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd en met de voornaam van die persoon. Die afspraken leiden nooit tot een to-do. Afspraken die de hele dag of meerdere dagen duren, worden op elke dag waarop ze plaatsvinden als afspraken voor de hele dag getoond. In **Agenda** staat een reis op elke dag bovenaan. In **Week** en **Maand** staat er één balk over de dagen heen, bijvoorbeeld ‘Reis naar Lissabon’.

Een gezamenlijke afspraak is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een afspraak die dag met dezelfde persoon staat op de regel van die afspraak.

**Te laat** staat bovenaan. Bij een afspraak met een open to-do staat de status: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die al is afgehandeld, omdat je al hebt gereageerd of omdat de uitvoering heeft vastgesteld dat hij is afgehandeld, wordt niet getoond met **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen of omhoog (of tik op **Eerdere dagen tonen**) voor eerdere dagen. De weergave gaat terug tot een week vóór je je agenda koppelde. Bovenaan staat vanaf welke dag. Zodra je [geschiedenis](history.md) is ingeladen, gaat de weergave ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik op een dag om de lijst voor die dag te openen.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De gekozen weergave wordt op dat apparaat onthouden.

In het weekraster staan afspraken op hetzelfde tijdstip naast elkaar, maar blijven ze goed leesbaar. De overige afspraken staan als **+N**. Tik daarop om die dag in de agenda te openen.

## Iets openen

Klik op een regel om de chat van de to-do, de belofte, de reis of het evenement, of de afspraak te openen. Bij een afspraak die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een afspraak met gasten, zie je de details: wanneer, waar en wie. Iemand die je Graph kent, en de organisaties en projecten die bij de afspraak horen, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) open je de afspraak daar. Alleen bekijken verandert niets.

Een vergaderruimte die bij een afspraak is geboekt, staat bij de locatie. Hij wordt nooit als persoon of in je Graph getoond.

Een link voor een afspraak wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de afspraak om deel te nemen.

## Reizen en evenementen

Als een boeking voor een vlucht, hotel, vakantiewoning, trein, bus, veerboot, huurauto, taxi of parkeerplaats op het vliegveld in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen samen in één reis, uit al je mailboxen: de trein naar het vliegveld, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden samengevoegd als de datums elkaar overlappen of als de ene aansluit op de andere.

De reis wordt als één balk over de dagen heen getoond. Open de reis om alle boekingen op volgorde van tijd te zien, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie vormen één evenement per gelegenheid, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat via je werkmailbox is geboekt, is Werk. Anders is het Privé. Tickets voor iets dat tijdens een reis plaatsvindt, worden aan de reis toegevoegd.

Voor een reis die nog moet plaatsvinden, vertelt je Machine wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten**, of dat er niets is geboekt van het vliegveld naar je hotel. Die regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder overnachtingen wordt niets over nachten vermeld.

- Op elke regel staat waar de boeking vandaan komt, bijvoorbeeld **Van Example Tickets**. Open de regel om die mail te openen.
- Als er een to-do uit de mail is gemaakt, bijvoorbeeld om voor de tickets te betalen, toont **De to-do openen** die to-do.
- Een gewijzigde boeking werkt de regel bij en een geannuleerde boeking wordt verwijderd. Als alle boekingen zijn geannuleerd, wordt ook de reis of het evenement verwijderd.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

De meeste bevestigingen bevatten gegevens in een indeling die je Machine zonder AI kan lezen. Als dat niet zo is, bijvoorbeeld bij een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Het wacht daarmee als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Notities en transcript van afspraken

De details van een afspraak bestaan uit twee delen. **Notities** is de samenvatting: beslissingen en actiepunten. **Transcript** is woord voor woord wat er is gezegd. Het transcript is eerst ingeklapt en toont hoe lang het is. Met **Tonen** open je het.

Als de notities of het transcript niet laden, probeert de app het ongeveer een halve minuut lang vanzelf opnieuw. Tik daarna op **Opnieuw proberen**.

Voor elk onderdeel zijn er aparte opties: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een afspraak die je kunt wijzigen, open je de notities met **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities bij Notities en het transcript bij Transcript. Ze krijgen het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden beide getoond.

Notities kunnen ook worden toegevoegd aan de eigen agenda-afspraak, nadat die is begonnen, of via een mail van Zoom of Gemini. Na afloop van de afspraak maakt The Machine er alleen to-do's van als er duidelijke vervolgstappen in staan. Als dezelfde notities op twee manieren binnenkomen, ontstaat er één to-do, met de afspraak als bron: ‘Bron: notities van’ de afspraak.

Bij een afspraak met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met erbij wie ze uitvoert, in de taal van de afspraak.

De status **Notities schrijven…** verschijnt. The Machine gaat door als je de afspraak sluit. Bij een lange afspraak duurt dit een paar minuten en wordt je eigen model gebruikt. De notities krijgen het label **Geschreven door The Machine** en vervangen nooit notities die je zelf hebt toegevoegd.

Je kunt The Machine ook vragen om notities toe te voegen, bijvoorbeeld bij een to-do: ‘voeg dit transcript toe aan de vergadering van vandaag over het bord’. Een transcript komt bij Transcript te staan, een samenvatting bij Notities. Bij een afspraak met notities of een transcript staat **Notities** of **Transcript** in de Agenda.

The Machine leest beide om de vervolgstappen van de afspraak te vinden. Ze zijn Werk of Privé, net als de afspraak, en worden alleen met je team gedeeld als de afspraak dat ook wordt.

De details van een afspraak zijn overal beschikbaar waar je die vindt: op een tijdlijn, in een zoekresultaat bij berichten of als bron van een to-do. Onderaan toont **Originele uitnodiging** de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je kunt je eigen Google-agenda hier wijzigen. Outlook en andere agenda's zijn alleen-lezen. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon staat deze optie onder **+** in de bovenbalk): kies de agenda, een titel en het tijdstip. Klik op een afspraak zonder gasten in die agenda om die te wijzigen, of tik twee keer op **Verwijderen**.

**Waar** stelt tijdens het typen locaties voor: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om de locatie op te zoeken. Kies een suggestie of gebruik je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat om hoeveel mensen het gaat: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten wordt niemand uitgenodigd of op de hoogte gebracht.

Een to-do kan ook voorstellen om iets te wijzigen, zoals een ophaalmoment toevoegen. Je ziet precies wat er verandert. De wijziging wordt alleen doorgevoerd als je op **Toevoegen**, **Opslaan** of **Verwijderen** tikt.

Nog geen afspraken? Als je geen agenda hebt gekoppeld, opent **Koppel je agenda** de Koppelingen. Koppel daar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een werkafspraak overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de afspraak die het laatst is toegevoegd. The Machine kan een kort bericht opstellen om de afspraak te verplaatsen, of voorstellen om die af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Afspraken die de hele dag duren, als vrij gemarkeerde afspraken en voorlopige afspraken tellen niet mee. Elk conflict wordt één keer gemeld. Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit te zien krijgt. Alleen jij ziet waarmee de afspraak conflicteert.

## Goed voorbereid naar je afspraken

Voor een afspraak met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de afspraak. Dat is een korte briefing:

- **Wie:** wie ze zijn, op basis van je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet dat relevant is voor de afspraak.
- **Tot nu toe:** wat je hebt besproken, gevraagd en aangeboden, en wat de status is. Na de afspraak worden die berichten als bronnen aan de to-do toegevoegd.
- **Openstaande beloftes:** wat jij of de ander nog moet doen.
- **Openstaande vragen:** wat nog niet is beantwoord.
- **Beslissen of meenemen:** wat je moet afspreken of meenemen, en wat de ander waarschijnlijk belangrijk vindt.

De to-do verschijnt op de ochtend van een werkdag: op de dag van de afspraak als die 's middags plaatsvindt, anders op de werkdag ervoor. Je kunt de briefing alleen lezen. Tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag in de briefing die om actie vraagt, krijgt een eigen to-do.

The Machine gebruikt informatie die al op je Machine staat. Voor een eerste afspraak met iemand van een bedrijf zoekt The Machine ook kort op het web naar de naam van die persoon en het bedrijf. Naast de gevonden informatie staat een link. Alleen de openbare naam van die persoon, de bedrijfsnaam en de website worden naar de zoekopdracht gestuurd, nooit je berichten. Een zoekopdracht wordt 30 dagen hergebruikt. Als **Werkcontacten opzoeken** is uitgeschakeld (Instellingen, Beveiliging), wordt er niet gezocht.

Zonder bruikbare geschiedenis wordt er geen to-do gemaakt. Voor terugkerende, interne of persoonlijke afspraken en afspraken die zijn geweigerd, wordt er geen to-do gemaakt. Als een afspraak wordt verplaatst, blijft de to-do behouden en wordt het tijdstip aangepast. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde afspraak wordt automatisch gesloten.

De details van de afspraak tonen de bijbehorende to-do onder **To-do**. Met één tik open je de chat.
