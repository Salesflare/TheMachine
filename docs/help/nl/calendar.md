---
title: Agenda
area: calendar
summary: De komende week op één plek: meetings, to-do’s met een deadline, gesnoozede to-do’s en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: d6f800709c378338
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda’s die je hebt gekoppeld,
- to-do’s met een deadline die dag, en gesnoozede to-do’s op de dag dat ze terugkomen,
- updates over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een meeting die in twee agenda’s staat, zie je maar één keer. Een agenda die iemand met je heeft gedeeld, toont de afspraken van die persoon gedimd en met diens voornaam. Die afspraken leiden nooit tot een to-do. Afspraken die de hele dag of meerdere dagen duren, worden voor elke dag waarop ze vallen als dagvullend getoond. In Agenda staat een reis op elke reisdag bovenaan. In Week en Maand loopt één balk over alle reisdagen, bijvoorbeeld ‘Reis naar Lissabon’.

Een gezamenlijk plan is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een meeting met die persoon op die dag staat op de regel van die meeting.

**Te laat** komt bovenaan. Bij een meeting met een open to-do zie je **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die afgerond lijkt, omdat je al hebt geantwoord of omdat uit een uitvoering bleek dat hij klaar was, wordt niet getoond als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen of omhoog, of kies **Eerdere dagen tonen**, voor eerdere dagen. Je kunt terug tot een week voordat je je agenda koppelde. Bovenaan staat vanaf welke dag je agenda loopt. Zodra de [geschiedenis](history.md) is ingeladen, kun je ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik op een dag om de items te bekijken.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De gekozen weergave wordt op dat apparaat onthouden.

In het weekraster staan afspraken die op hetzelfde tijdstip plaatsvinden naast elkaar, zodat ze leesbaar blijven. De rest wordt getoond als **+N**. Daarmee open je die dag in Agenda.

## Iets openen

Klik op een regel om de chat van de to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt aanpassen, bijvoorbeeld die van iemand anders of een meeting met gasten, zie je de details: wanneer, waar en wie. Mensen die The Machine kent, en organisaties en projecten waaraan de meeting is gekoppeld, linken naar hun pagina. Met **Openen in Google Calendar** of **Openen in Outlook** open je de meeting daar. Alleen kijken verandert niets.

Een vergaderruimte die voor een meeting is geboekt, staat bij de locatie. Hij wordt nooit als persoon of in je Graph getoond.

Een link naar een meeting wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Wanneer een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor dezelfde reis komen bij elkaar op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden gecombineerd als hun datums elkaar overlappen of als de ene eindigt wanneer de andere begint.

De reis wordt als één balk over de reisdagen getoond. Open de reis om de boekingen op volgorde te bekijken, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of congres vormen één evenement per gebeurtenis, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt eraan toegevoegd. Een evenement dat via je werkmailbox is geboekt, valt onder Werk. Anders is het Persoonlijk. Tickets voor iets tijdens een reis worden aan de reis toegevoegd.

Voor een reis die nog moet plaatsvinden, laat je Machine zien wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten** of dat er niets is geboekt van de luchthaven naar je hotel. Deze regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder verblijf wordt niets over nachten getoond.

- Op elke regel staat van wie de boeking komt, bijvoorbeeld **Van Example Tickets**. Open de regel om de mail te bekijken.
- Als er een to-do uit de mail is gemaakt, bijvoorbeeld om de tickets te betalen, kun je die openen met **De to-do openen**.
- Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

De meeste boekingsbevestigingen bevatten gegevens in een formaat dat je Machine zonder AI kan lezen. Bij een bevestiging die dat niet heeft, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Bijna aan je gebruikslimiet? Dan wacht het model. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Meetingnotities en transcript

De details van een meeting bestaan uit twee delen. **Notities** is de samenvatting: beslissingen en actiepunten. **Transcript** is precies wat er is gezegd. Het transcript is eerst ingeklapt en toont hoelang het is. Met **Tonen** open je het.

Als de gegevens niet laden, probeert de app het ongeveer een halve minuut lang vanzelf opnieuw. Tik daarna op **Opnieuw proberen**.

Voor beide kun je apart **Notities toevoegen** of **Transcript toevoegen**. Gebruik **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** om iets aan te passen en **Verwijderen** om iets te verwijderen. Tik twee keer om te verwijderen. Wat je aan het ene toevoegt, blijft daar staan. Bij een meeting die je kunt aanpassen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities bij Notities en het transcript bij Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden beide getoond.

Notities kunnen ook in de eigen agenda-afspraak van de meeting staan, nadat die is begonnen zijn toegevoegd, of per mail van Zoom of Gemini binnenkomen. Na afloop van de meeting maakt The Machine alleen to-do’s van duidelijke vervolgstappen. Als dezelfde notities op twee manieren binnenkomen, wordt er één to-do van gemaakt, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities zie je **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met erbij wie ze uitvoert, in de taal van de meeting.

Je ziet **Notities schrijven…**. The Machine gaat door als je de meeting sluit. Bij een lange meeting duurt dit een paar minuten en wordt je eigen model gebruikt. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

Je kunt The Machine ook vragen om notities toe te voegen. Vraag het in een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de meeting van vandaag over het bord’. Een transcript komt bij Transcript en een samenvatting bij Notities. Bij een meeting met notities of een transcript zie je in de agenda **Notities** of **Transcript**.

The Machine leest beide om de vervolgstappen van de meeting te bepalen. Ze vallen onder Werk of Persoonlijk, net als de meeting, en worden alleen met je team gedeeld als de meeting dat ook is.

Je kunt de details van een meeting overal openen waar je die tegenkomt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Onderaan kun je met **Originele uitnodiging** de uitnodiging bekijken zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je kunt je eigen Google-agenda hier wijzigen. Outlook en andere agenda’s zijn alleen zichtbaar. Met **Nieuwe afspraak** voeg je een afspraak toe. Op een telefoon vind je deze optie onder **+** in de bovenste balk. Kies de agenda, een titel en een tijdstip. Klik op een afspraak zonder gasten in die agenda om deze te wijzigen of **Verwijderen** te kiezen. Tik twee keer om te verwijderen.

Bij **Waar** verschijnen suggesties terwijl je typt: eerst plaatsen die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om op te zoeken. Kies een suggestie of gebruik je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat hoeveel mensen je uitnodigt: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas wanneer je erop tikt. Zonder gasten krijgt niemand een uitnodiging of update.

Een to-do kan ook een wijziging voorstellen, zoals een ophaalafspraak toevoegen. Je ziet precies wat er verandert. De wijziging wordt pas doorgevoerd als je op **Toevoegen**, **Opslaan** of **Verwijderen** tikt.

Nog geen meetings? Als je geen agenda hebt gekoppeld, opent **Koppel je agenda** Koppelingen. Koppel daar [Google Calendar](google-calendar.md), [Outlook Agenda](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een werkmeeting overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de meest recente van de twee afspraken. The Machine kan een kort bericht opstellen om de afspraak te verzetten of voorstellen om de uitnodiging af te wijzen. Er wordt niets verstuurd voordat je dit goedkeurt.

Afspraken die de hele dag duren, als vrij zijn gemarkeerd of voorlopig zijn, tellen niet mee. Elk conflict komt maar één keer aan bod. In een to-do voor Werk staat alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit te zien krijgt. Alleen jij ziet waarmee de afspraak botst.

## Klaar voor je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de meeting. Daarin staat een korte briefing:

- **Wie:** wie ze zijn, op basis van je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet, voor wie en tegen welke prijs, als dat relevant is voor de meeting.
- **Tot nu toe:** wat jullie hebben besproken, gevraagd en aangeboden, en wat de stand van zaken is. Na de meeting zijn die berichten de bronnen van de to-do.
- **Eerder afgesproken:**, **Sindsdien veranderd:** en **Nog open:** wat er uit eerdere meetings met dezelfde mensen kwam. Bij elke regel staat de meeting of het bericht waar die vandaan komt.
- **Open beloftes:** wat jij of de ander nog moet doen, op basis van de beloftes op je Machine.
- **Open vragen:** wat nog onbeantwoord is.
- **Beslissen of meenemen:** wat je moet bespreken of meenemen, en wat de anderen waarschijnlijk belangrijk vinden.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de meeting zelf als die in de middag plaatsvindt, anders op de werkdag ervoor. De briefing is alleen bedoeld om te lezen. Tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag uit de briefing die actie vereist, krijgt een eigen to-do.

Eerdere meetings tellen mee als er bij allebei iemand van buiten je organisatie aanwezig is, ongeacht de naam van de meeting en het e-mailadres dat die persoon heeft gebruikt. The Machine leest de notities die je Machine heeft: jouw notities, die van je meetingapp of notities die de app je heeft gemaild. Als die er niet zijn, leest The Machine het transcript of de notities in de agenda-afspraak. De nieuwste informatie weegt het zwaarst. Een punt dat later is afgehandeld, wordt niet meer als open getoond.

Notities en berichten uit [Geschiedenis](history.md) tellen ook mee. Zo weet een briefing ook van meetings die plaatsvonden voordat je begon.

Een briefing voor Werk leest geen persoonlijke notities en niets van de Machine van iemand anders. De tekst blijft van jou: bij een overdracht wordt die niet meegenomen en je kunt de briefing niet ter controle versturen. Zonder notities worden die regels niet getoond.

De briefing gebruikt informatie die al op je Machine staat. Voor een eerste meeting met iemand bij een bedrijf leest The Machine ook de startpagina van de website van dat bedrijf.

Als er een webzoekprovider is ingesteld in OpenClaw, voert The Machine ook een korte zoekopdracht op het web uit naar de naam en het bedrijf van die persoon. Een gehoste Machine heeft niet standaard zo’n provider. De gevonden informatie bevat een link. Alleen de openbare naam, bedrijfsnaam en website van de persoon worden met de zoekprovider gedeeld, nooit je berichten. De gevonden informatie wordt 30 dagen hergebruikt.

Zo kan een eerste meeting waar je mee hebt ingestemd al een briefing krijgen voordat jullie contact hebben gehad: wat het bedrijf doet, wat dat voor jou betekent en, als het bekend is, wie de persoon is. Als alleen een voornaam bekend is, bewaart The Machine de zoekresultaten alleen als ze naar één persoon verwijzen. Als **Werkcontacten opzoeken** uitstaat (Instellingen, Beveiliging), wordt er niets opgezocht.

Een terugkerende meeting krijgt alleen een briefing als er sinds de vorige keer iets is gebeurd: een bericht, notities of een belofte. De briefing vertelt wat er nieuw is, niet wat er in de vorige briefing stond. Je krijgt de briefing zodra de vorige meeting voorbij is, met maximaal twee terugkerende meetings per dag.

Als er niets nuttigs te melden is, wordt er geen to-do gemaakt. Voor interne, persoonlijke en afgewezen meetings wordt geen briefing gemaakt. Als een meeting wordt verzet, blijft de to-do bestaan op het nieuwe tijdstip. Een afgewezen briefing komt niet terug. De to-do van een geannuleerde meeting wordt vanzelf afgesloten.

Als een update de inhoud van een briefing verandert, worden open briefings voor meetings die nog moeten plaatsvinden één keer opnieuw geschreven, met de nieuwe informatie. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt aangepast, gesnoozed of gesloten blijft ongewijzigd. Dat geldt ook voor een briefing van een meeting die binnen een paar minuten begint.

De to-do van een meeting staat bij de details onder **To-do**. Je opent de chat met één tik.
