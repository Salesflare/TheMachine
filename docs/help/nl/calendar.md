---
title: Agenda
area: calendar
summary: De komende week op één plek: meetings, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 479aa9c3fadda8bd
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda's die je hebt gekoppeld,
- to-do's met een deadline op die dag en gesnoozede to-do's op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit boekings- en ticketmails.

Een meeting die in twee agenda's staat, wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont de afspraken van die persoon gedempt en met diens voornaam. Die afspraken leiden nooit tot een to-do. Afspraken die de hele dag duren of meerdere dagen beslaan, worden op elke dag waarop ze vallen als afspraken voor de hele dag getoond. Een reis staat in Agenda op elke dag bovenaan, en in Week en Maand als één balk over de dagen, bijvoorbeeld ‘Reis naar Lissabon’.

Een gezamenlijke afspraak is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een meeting die die dag plaatsvindt met dezelfde persoon, staat op de rij van die meeting.

**Te laat** staat bovenaan. Bij een meeting met een open to-do staat **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die klaar lijkt (je hebt al geantwoord of de uitvoering heeft vastgesteld dat hij klaar is), wordt niet getoond als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scrol omlaag voor latere dagen of omhoog (of kies **Eerdere dagen tonen**) voor eerdere dagen. De agenda gaat terug tot een week vóór je je agenda hebt gekoppeld. Bovenaan staat vanaf welke dag de weergave begint. Zodra de [geschiedenis](history.md) is ingeladen, gaat de agenda ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon worden drie dagen getoond.
- **Maand** toont de hele maand. Op een computer worden maximaal drie items per dag getoond. Op een telefoon zie je stippen. Tik op een dag om de afspraken van die dag te zien.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De gekozen weergave wordt op dat apparaat onthouden.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat je ze goed kunt lezen. De rest wordt getoond als **+N**. Tik daarop om die dag in de agenda te openen.

## Iets openen

Klik op een rij om de chat van de bijbehorende to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een meeting met gasten, zie je de details: wanneer, waar en wie. Iemand die je Graph kent, en de organisaties en projecten die bij de meeting horen, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de meeting daar. Alleen kijken verandert niets.

Een vergaderzaal die bij een meeting is geboekt, staat onder de locatie, nooit als persoon of in je Graph.

Een link voor een meeting wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Als er een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden samengevoegd als hun dagen overlappen of als de ene eindigt wanneer de andere begint.

De reis wordt als één balk over de dagen getoond. Open de reis om alle boekingen op volgorde te zien, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken één evenement per evenement aan, met de locatie, boekingscode, stoel en aantal tickets. Een tweede bestelling voor hetzelfde evenement komt erbij te staan. Een evenement dat via je werkmailbox is geboekt, valt onder Werk. Anders valt het onder Persoonlijk. Tickets voor iets dat tijdens een reis plaatsvindt, komen bij de reis te staan.

Bij een reis die nog moet beginnen, geeft je Machine aan wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten** of dat er niets is geboekt van de luchthaven naar je hotel. Deze regels worden gedempt getoond en krijgen het label **Geen boeking**. Bij een reis zonder verblijf wordt niets over overnachtingen vermeld.

- Op elke regel staat van wie de boeking afkomstig is, bijvoorbeeld **Van Example Tickets**. Open de regel om die mail te bekijken.
- Als er een to-do uit de mail is gemaakt, bijvoorbeeld om de tickets te betalen, toont **De to-do openen** die to-do.
- Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen zijn geannuleerd, wordt ook de reis of het evenement verwijderd.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar jou is doorgestuurd, komt niet bij je reizen te staan.

De meeste bevestigingen bevatten details in een vorm die je Machine zonder AI kan lezen. Bij bevestigingen die dat niet doen, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Het wacht daarmee als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Notities en transcript van meetings

De details van een meeting bestaan uit twee delen. **Notities** is de samenvatting met beslissingen en actiepunten. **Transcript** is een woordelijke weergave van wat er is gezegd. Het transcript is eerst ingeklapt en toont de duur. Met **Tonen** open je het.

Als de gegevens niet worden geladen, probeert de app het ongeveer een halve minuut vanzelf opnieuw. Tik daarna op **Opnieuw proberen**.

Voor beide kun je **Notities toevoegen** of **Transcript toevoegen**, een Markdown- of tekstbestand **Bestand uploaden**, **Bewerken** of **Verwijderen** (tik twee keer). Wat je aan het ene toevoegt, blijft daar staan. Bij een meeting die je kunt wijzigen, open je de notities met **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities onder Notities en het transcript onder Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als ze er allebei zijn, worden ze allebei getoond.

Notities kunnen ook worden toegevoegd aan de agenda-afspraak zelf, nadat de meeting is begonnen, of via een mail van Zoom of Gemini. Na afloop van de meeting maakt The Machine alleen to-do's van duidelijke vervolgstappen. Als dezelfde notities op twee manieren binnenkomen, wordt er één to-do gemaakt, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met de namen van degenen die ze uitvoeren, in de taal van de meeting.

De melding **Notities schrijven…** blijft staan, ook als je de meeting sluit. Bij een lange meeting duurt dit een paar minuten en wordt je eigen model gebruikt. De notities krijgen het label **Geschreven door The Machine** en vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag ernaar in een to-do-chat, bijvoorbeeld: ‘voeg dit transcript toe aan de vergadering van vandaag’. Een transcript komt onder Transcript te staan en een samenvatting onder Notities. Bij een meeting met notities of een transcript staat in de Agenda **Notities** of **Transcript**.

The Machine leest beide om de vervolgacties van de meeting te bepalen. Die vallen onder Werk of Persoonlijk, net als de meeting zelf. Ze gaan alleen naar je team als de meeting dat ook doet.

Je kunt een meeting met deze details openen vanaf elke plek waar je hem vindt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Onderaan toont **Originele uitnodiging** de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook en andere agenda's zijn alleen zichtbaar. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon staat deze optie onder **+** in de bovenbalk). Kies de agenda, een titel en een tijdstip. Klik op een afspraak zonder gasten in die agenda om deze te wijzigen of **Verwijderen** (tik twee keer).

Bij **Waar** verschijnen tijdens het typen suggesties: eerst plaatsen die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om ze op te zoeken. Kies een suggestie of laat je eigen tekst staan.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop staat wie een uitnodiging krijgt. Op de knop staat hoeveel mensen dat zijn: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten wordt niemand uitgenodigd en krijgt niemand een update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld een ophaalmoment om toe te voegen. Je ziet precies wat er wordt gewijzigd. De wijziging wordt pas doorgevoerd als je op **Toevoegen**, **Opslaan** of **Verwijderen** tikt.

Nog geen meetings? Als je geen agenda hebt, open je met **Koppel je agenda** de Koppelingen. Koppel daar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een meeting op je werk overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de meest recente van de twee. The Machine kan een kort bericht opstellen om de meeting te verplaatsen of voorstellen om deze af te zeggen. Er wordt niets verstuurd voordat je dit goedkeurt.

Een afspraak die met meerdere afspraken overlapt, leidt tot één to-do over die afspraak. Een nieuwe overlap wordt aan die to-do toegevoegd zolang deze openstaat. Zodra de to-do is afgerond of afgewezen, komt hij alleen terug als een meeting later wordt aangemaakt of gewijzigd.

Afspraken die de hele dag duren, afspraken waarbij je als vrij staat en voorlopige afspraken tellen nooit mee. Elk conflict wordt maar één keer gemeld. Ook Google's werklocatie, focustijd en afwezigheidsmelding tellen niet mee. Een tijdsblok van jezelf met daarin andere meetings, zoals een kantoordag, telt ook niet mee. Alleen de meetings in dat blok kunnen een conflict vormen. Een blok zonder anderen en zonder meetings, zoals een vlucht, vormt wel een conflict met een afspraak waar anderen bij betrokken zijn.

Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak botst: de eerste twee afspraken en daarna het aantal overige afspraken. Een to-do waar je niets mee hebt gedaan, wordt vanzelf gesloten als de conflicterende afspraak bij een andere to-do hoort of toch geen conflict blijkt te zijn.

## Klaar voor je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do aan: **Voorbereiden op** de meeting. Dit is een korte briefing:

- **Wie:** wie ze zijn volgens je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet, voor wie en tegen welke prijs, als dat relevant is voor de meeting.
- **Tot nu toe:** wat je hebt besproken, gevraagd en aangeboden, en wat de stand van zaken is. Na de meeting staan die berichten als bronnen bij de to-do.
- **Eerder afgesproken:**, **Sindsdien veranderd:** en **Nog open:** wat uit eerdere meetings met dezelfde mensen is gekomen. Bij elke regel staat de meeting of het bericht waar die informatie vandaan komt.
- **Open beloftes:** wat jij of de anderen nog moeten doen, op basis van de beloftes op je Machine.
- **Open vragen:** wat nog geen antwoord heeft.
- **Beslissen of meenemen:** wat je moet regelen of meenemen en wat de anderen waarschijnlijk belangrijk vinden.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de meeting zelf als die 's middags plaatsvindt, anders op de werkdag ervoor. Je hoeft hem alleen te lezen. De to-do is **Gedaan** als je hem hebt gelezen. Een belofte of vraag in de briefing die actie vereist, krijgt een eigen to-do.

Stel vragen over de meeting in de bijbehorende chat of voeg informatie toe die je al weet. The Machine geeft antwoord of verwerkt je notitie in de briefing, bijvoorbeeld onder **Beslissen of meenemen**, en leert daarvan. Vanuit een briefing wordt niets verstuurd.

Eerdere meetings tellen mee als iemand van buiten je bedrijf bij beide meetings aanwezig is, ongeacht de naam van de meeting en het adres dat die persoon gebruikte. The Machine leest de notities die je Machine heeft: die van jou, die van je meetingapp of de notities die per mail zijn verstuurd. Als die er niet zijn, leest The Machine het transcript of de notities in de agenda-afspraak. De meest recente informatie weegt het zwaarst. Een punt dat later is afgehandeld, wordt niet als open getoond.

Notities en berichten uit [Geschiedenis](history.md) tellen ook mee. Zo bevat een briefing informatie over meetings van voordat je begon.

Een werkbriefing leest geen persoonlijke notities en niets van de Machine van iemand anders. De tekst blijft bij jou: een overdracht neemt hem niet mee en je kunt hem niet ter beoordeling versturen. Zonder notities worden deze regels niet getoond.

De briefing gebruikt wat er al op je Machine staat. Voor een eerste meeting met iemand van een bedrijf wordt ook de startpagina van de website van dat bedrijf gelezen.

Als zoeken op internet is ingesteld op je Machine, wordt er ook kort op internet gezocht naar de naam en het bedrijf van de andere persoon. Op een gehoste Machine is dit niet beschikbaar. Op je eigen computer kun je het instellen in OpenClaw. Bij de gevonden informatie staat een link. Alleen de openbare naam van de persoon, de bedrijfsnaam en de website worden naar de zoekopdracht gestuurd, nooit je berichten. De gevonden informatie wordt 30 dagen opnieuw gebruikt.

Zo kan een eerste meeting waarmee je hebt ingestemd al een briefing krijgen voordat je met iemand hebt gesproken: wat het bedrijf doet, wat dat voor jou betekent en, als dat bekend is, wie de persoon is. Als je alleen een voornaam hebt, gebruikt The Machine de zoekresultaten alleen als die naar één persoon verwijzen. Als **Werkcontacten opzoeken** uitstaat (Instellingen, Beveiliging), wordt er niets opgezocht.

Een terugkerende meeting krijgt alleen een briefing als er iets is gebeurd sinds de vorige meeting: een bericht, notities of een belofte. De briefing vermeldt wat nieuw is, niet wat er in de vorige briefing stond. Hij verschijnt nadat de vorige meeting is afgelopen, voor maximaal twee terugkerende meetings per dag.

Als er niets nuttigs te melden is, wordt er geen to-do gemaakt. Interne, persoonlijke en afgewezen meetings krijgen geen briefing. Als een meeting wordt verplaatst, blijft de bijbehorende to-do bestaan op het nieuwe tijdstip. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde meeting wordt vanzelf gesloten.

Als een update de inhoud van een briefing verandert, worden briefings voor meetings die nog moeten plaatsvinden één keer opnieuw geschreven met de nieuwe informatie. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft ongewijzigd. Dat geldt ook voor een briefing van een meeting die binnen enkele minuten begint.

De details van de meeting tonen de bijbehorende to-do onder **To-do**. Tik erop om de chat te openen.
