---
title: Agenda
area: calendar
summary: De komende week op één plek: meetings, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9b7475608bb04e5c
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda's die je hebt gekoppeld,
- to-do's met een deadline op die dag en gesnoozede to-do's op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een meeting die in twee agenda's staat, wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd en met diens voornaam. Die leiden nooit tot een to-do. Afspraken die een hele dag of meerdere dagen duren, worden op elke dag waarop ze plaatsvinden als afspraken voor de hele dag getoond. Een reis staat in Agenda op elke dag bovenaan en wordt in Week en Maand weergegeven als één balk over alle reisdagen, bijvoorbeeld ‘Reis naar Lissabon’.

Een plan dat jullie samen hebben gemaakt, is één belofte, met ‘Met’ en de naam van de ander. Een belofte over een meeting met die persoon die dag staat bij die meeting.

**Te laat** komt eerst. Bij een meeting met een open to-do zie je **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die afgerond lijkt, omdat je al hebt geantwoord of omdat de uitvoering ervan heeft vastgesteld dat hij afgerond is, wordt niet getoond als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag. Scrol omlaag voor latere dagen of omhoog (of tik op **Eerdere dagen tonen**) voor eerdere dagen. De agenda gaat terug tot een week vóór je je agenda hebt gekoppeld. Bovenaan staat vanaf welke dag. Zodra je [geschiedenis](history.md) is ingeladen, gaat de agenda ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen; tik erop om de afspraken van die dag te zien.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De weergave die je kiest, wordt onthouden op dat apparaat.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat je ze allebei kunt lezen. De rest wordt weergegeven als **+N**. Tik daarop om die dag in de agenda te openen.

## Iets openen

Klik op een regel om de chat van de to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een meeting met gasten, zie je de details: wanneer, waar en wie. Mensen die je Graph kent en de organisaties en projecten waarvoor de meeting plaatsvindt, linken naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de meeting daar. Alleen kijken brengt niets teweeg.

Een vergaderruimte die voor een meeting is geboekt, staat onder ‘Waar’, nooit als persoon of in je Graph.

Een meetinglink wordt weergegeven met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Wanneer een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of parkeerplaats op de luchthaven in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden gecombineerd als de dagen elkaar overlappen of als de ene aansluit op het einde van de andere.

De reis wordt als één balk over de reisdagen weergegeven. Open de reis om alle boekingen op tijdsvolgorde te zien, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken één evenement per evenement aan, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat via je werkmailbox is geboekt, is Werk. Anders is het Persoonlijk. Tickets voor iets dat tijdens een reis plaatsvindt, worden aan de reis toegevoegd.

Voor een reis die nog moet plaatsvinden, geeft je Machine aan wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten** of dat er niets is geboekt van de luchthaven naar je hotel. Die regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder verblijf staat niets over overnachtingen.

- Op elke regel staat van wie de boeking komt, bijvoorbeeld **Van Example Tickets**. Klik erop om de mail te openen.
- Komt er een to-do uit de mail, bijvoorbeeld om de tickets te betalen, dan zie je die met **De to-do openen**.
- Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals de vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

De meeste bevestigingen bevatten hun gegevens in een vorm die je Machine zonder AI kan lezen. Bij bevestigingen die dat niet doen, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Dat gebeurt pas als je niet bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Meetingnotities en transcript

De details van een meeting bestaan uit twee delen. **Notities** is de samenvatting, met beslissingen en actiepunten. **Transcript** is woord voor woord wat er is gezegd. Het transcript is eerst ingeklapt en toont hoelang het duurt. Met **Tonen** open je het.

Als de gegevens niet laden, probeert de app het ongeveer een halve minuut automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Je kunt voor elk onderdeel afzonderlijk **Notities toevoegen** of **Transcript toevoegen**, een Markdown- of tekstbestand **Bestand uploaden**, en het **Bewerken** of **Verwijderen** (tik twee keer). Wat je aan het ene toevoegt, blijft daar staan. Bij een meeting die je kunt wijzigen, open je de notities met **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities ervan onder Notities en het transcript onder Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide er zijn, worden ze allebei getoond.

Notities kunnen ook in de agenda-afspraak van de meeting zelf staan, nadat de meeting is begonnen zijn toegevoegd of via mail van Zoom of Gemini binnenkomen. Na afloop van de meeting maakt The Machine er alleen to-do's van als er duidelijke vervolgstappen in staan. Als dezelfde notities op twee manieren binnenkomen, maken ze samen één to-do, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities staat **Notities maken**. The Machine maakt dan notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met erbij wie ze uitvoert, in de taal van de meeting.

De app toont **Notities schrijven…** en gaat door als je de meeting sluit. Voor een lange meeting duurt dit een paar minuten en wordt je eigen model gebruikt. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag dat in een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de meeting van vandaag op het bord’. Een transcript wordt toegevoegd onder Transcript, een samenvatting onder Notities. In de Agenda staat bij een meeting met notities of een transcript **Notities** of **Transcript**.

The Machine leest beide voor de vervolgstappen van de meeting. Die zijn Werk of Persoonlijk, net als de meeting, en worden alleen met je team gedeeld als de meeting dat ook wordt.

De details van een meeting zijn overal beschikbaar waar je die opent: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Met **Originele uitnodiging** onderaan zie je de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook-agenda's en andere agenda's zijn alleen zichtbaar. Met **Nieuwe afspraak** voeg je er een toe (op een telefoon staat die optie onder **+** in de bovenbalk): kies de agenda, een titel en het tijdstip. Klik op een afspraak zonder gasten in die agenda om die te wijzigen of **Verwijderen** (tik twee keer).

**Waar** stelt locaties voor terwijl je typt: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om de locatie op te zoeken. Kies een suggestie of gebruik je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie staat alleen in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat het aantal, bijvoorbeeld **Toevoegen en uitnodigen: 2**. Google verstuurt de uitnodigingen wanneer je erop tikt, niet eerder. Zonder gasten wordt niemand uitgenodigd of op de hoogte gebracht.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld een afhaling om toe te voegen. Je ziet precies wat er verandert. Pas als je op **Toevoegen**, **Opslaan** of **Verwijderen** tikt, wordt de wijziging doorgevoerd.

Nog geen meetings? Als je geen agenda hebt, opent **Koppel je agenda** de Koppelingen. Koppel [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een meeting op je werk overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de meest recente van de twee. The Machine kan een kort bericht opstellen om de afspraak te verplaatsen of voorstellen om die af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Als een afspraak met meerdere andere afspraken overlapt, wordt er één to-do over die afspraak gemaakt. Zolang die openstaat, wordt elke nieuwe overlap eraan toegevoegd. Zodra de to-do is afgerond of afgewezen, ontstaat er pas weer een nieuwe als er later een meeting wordt gemaakt of gewijzigd.

Afspraken voor de hele dag, als vrij gemarkeerde afspraken en voorlopige afspraken tellen nooit mee. Elk conflict komt maar één keer aan bod. De werkplek, focustijd en afwezigheidsstatus van Google tellen ook niet mee. Een eigen blok met andere meetings, zoals een kantoordag, telt evenmin mee. Alleen de meetings in dat blok kunnen conflicten opleveren. Een blok zonder anderen en zonder meetings, zoals een vlucht, kan wel conflicteren met een afspraak waarbij anderen betrokken zijn.

Bij een Werk-to-do staat alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee die botst: de eerste twee afspraken en daarna het aantal overige. Een to-do waar je niets mee hebt gedaan, wordt vanzelf gesloten als het conflict bij een andere to-do hoort of toch geen conflict blijkt te zijn.

## Klaar voor je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de meeting. Dat is een korte briefing:

- **Wie:** wie ze zijn, op basis van je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet, voor wie en tegen welke prijs, als dat relevant is voor de meeting.
- **Tot nu toe:** wat jullie hebben besproken, gevraagd en aangeboden, en wat de status is. Na de meeting zijn die berichten de bronnen van de to-do.
- **Eerder afgesproken:**, **Sindsdien gewijzigd:** en **Nog open:** wat er is voortgekomen uit eerdere meetings met dezelfde mensen. Bij elke regel staat de meeting of het bericht waaruit die komt.
- **Openstaande beloftes:** wat jij of zij nog moeten doen, op basis van de beloftes op je Machine.
- **Openstaande vragen:** wat nog onbeantwoord is.
- **Beslissen of meenemen:** wat je moet afspreken of meenemen en wat voor hen waarschijnlijk belangrijk is.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de meeting zelf als die 's middags plaatsvindt, anders op de werkdag ervoor. Je kunt de briefing alleen lezen. Tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag erin waarvoor actie nodig is, krijgt een eigen to-do.

Eerdere meetings tellen mee als er bij beide iemand van buiten aanwezig is, ongeacht de naam van de meeting en het gebruikte e-mailadres. The Machine leest de notities die op je Machine staan: jouw notities, die van je meetingapp of de notities die je per mail hebt gekregen. Anders gebruikt The Machine het transcript of de notities in de agenda-afspraak. De nieuwste notities wegen het zwaarst. Een punt dat later is afgehandeld, wordt niet als openstaand getoond.

Ook notities en berichten uit [Geschiedenis](history.md) tellen mee. Zo weet de briefing ook van meetings van vóór je ermee begon.

Een werkbriefing leest geen persoonlijke notities en niets van de Machine van iemand anders. De tekst blijft van jou: bij een overdracht gaat hij niet mee en je kunt hem niet ter controle versturen. Als er geen notities zijn, worden die regels niet getoond.

De briefing gebruikt wat al op je Machine staat. Voor een eerste meeting met iemand van een bedrijf leest The Machine ook de homepage van de website van het bedrijf.

Als webzoeken is ingesteld op je Machine, wordt er ook kort op internet gezocht naar de naam en het bedrijf van de ander. Een gehoste Machine heeft die functie niet. Op je eigen computer kun je die instellen in OpenClaw. De zoekresultaten worden met een link weergegeven. Alleen de openbare naam, bedrijfsnaam en website van de ander worden naar de zoekfunctie gestuurd, nooit je berichten. De zoekresultaten worden 30 dagen bewaard.

Zo kan een briefing klaarstaan voor een eerste meeting waarvoor je hebt toegezegd, nog vóór jullie contact hebben gehad: wat het bedrijf doet, wat dat voor jou betekent en, als het bekend is, wie de ander is. Als alleen de voornaam bekend is, gebruikt The Machine de zoekresultaten alleen als die naar één persoon wijzen. Als **Werkcontacten opzoeken** is uitgeschakeld (Instellingen, Beveiliging), wordt er niets opgezocht.

Bij een terugkerende meeting wordt alleen een briefing gemaakt als er sinds de vorige keer iets is gebeurd: een bericht, notities of een belofte. De briefing beschrijft wat er nieuw is, niet wat er in de vorige briefing stond. Hij verschijnt nadat de vorige meeting is afgelopen. Er worden maximaal twee briefings per dag voor terugkerende meetings gemaakt.

Als er niets nuttigs te melden is, komt er geen to-do. Voor interne, persoonlijke en afgewezen meetings wordt geen briefing gemaakt. Als een meeting wordt verplaatst, blijft de to-do behouden en krijgt die het nieuwe tijdstip. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde meeting wordt vanzelf gesloten.

Als een update de inhoud van een briefing verandert, worden open briefings voor meetings die nog moeten plaatsvinden één keer opnieuw geschreven. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft ongewijzigd. Dat geldt ook voor een meeting die binnen een paar minuten begint.

De details van de meeting tonen de to-do onder **To-do**. Tik erop om de chat te openen.
