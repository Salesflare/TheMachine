---
title: Agenda
area: calendar
summary: De komende week op één plek: meetings, to-do’s met deadline, gesnoozede to-do’s en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 4b5bc600fefb624c
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda’s die je hebt gekoppeld,
- to-do’s met die dag als deadline en gesnoozede to-do’s op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit boekings- en ticketmails.

Een meeting in twee agenda’s wordt één keer getoond. Een agenda die iemand met je heeft gedeeld, toont de afspraken van die persoon gedempt en met diens voornaam. Die leiden nooit tot een to-do. Afspraken die de hele dag of meerdere dagen duren, worden op elke dag waarop ze vallen als afspraken voor de hele dag getoond. Een reis staat in Agenda op elk van de dagen als eerste. In Week en Maand loopt er één balk over die dagen, bijvoorbeeld ‘Reis naar Lissabon’.

Een gezamenlijk gemaakt plan is één belofte, gemarkeerd met ‘Met’ en de naam van de ander. Een belofte over een meeting met die persoon die dag staat op de rij van die meeting.

**Te laat** staat bovenaan. Bij een meeting met een open to-do zie je die als **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die klaar lijkt, bijvoorbeeld omdat je al hebt geantwoord of omdat de run hem als afgerond heeft aangemerkt, wordt niet getoond als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scrol omlaag voor latere dagen of omhoog, of kies **Eerdere dagen tonen**, voor eerdere dagen. De weergave gaat terug tot een week vóór je je agenda hebt gekoppeld. Bovenaan staat vanaf welke dag. Zodra de [geschiedenis](history.md) is ingelezen, gaat de weergave ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen; tik op een dag om de afspraken te bekijken.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De gekozen weergave wordt onthouden op dat apparaat.

In het weekraster staan afspraken op hetzelfde tijdstip naast elkaar, zodat ze leesbaar blijven. De rest wordt getoond als **+N**. Daarmee open je die dag in de agenda.

## Iets openen

Klik op een rij om de chat van de to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een meeting met gasten, zie je de gegevens: wanneer, waar en met wie. Iemand die je Graph kent en de organisaties en projecten waaraan de meeting is gekoppeld, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de meeting daar. Alleen kijken brengt niets in wijzigingen.

Een vergaderruimte die voor een meeting is geboekt, staat onder de locatie. Die wordt nooit als persoon of in je Graph getoond.

Een meetinglink wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Wanneer een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen samen op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden gecombineerd als de datums elkaar overlappen of de ene eindigt waar de andere begint.

De reis wordt als één balk over de verschillende dagen getoond. Open de reis voor alle boekingen op volgorde, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken een evenement aan, één per evenement. Je ziet waar het is, de boekingscode, de stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt eraan toegevoegd. Een evenement dat je via je werkmail hebt geboekt, is Werk. Anders is het Privé. Tickets voor iets dat tijdens een reis plaatsvindt, worden aan de reis toegevoegd.

Bij een reis die nog moet beginnen, vertelt je Machine wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten** of dat er niets is geboekt van de luchthaven naar je hotel. Die regels zijn gedempt en gemarkeerd als **Geen boeking**. Bij een reis zonder verblijf staat er niets over overnachtingen.

- Elke regel vermeldt van wie de boeking afkomstig is, bijvoorbeeld **Van Example Tickets**, en opent die mail.
- Als er op basis van de mail een to-do is aangemaakt, bijvoorbeeld om de tickets te betalen, toont **De to-do openen** die.
- Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals de vlucht van een collega die naar jou is doorgestuurd, wordt niet aan je reizen toegevoegd.

In de meeste bevestigingen staan gegevens in een formaat dat je Machine zonder AI kan lezen. Bij een bevestiging die dat niet heeft, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Het wacht daarmee als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bijhoudt, worden op de achtergrond gelezen zodra die geschiedenis is ingelezen.

## Meetingnotities en transcript

De gegevens van een meeting bestaan uit twee delen. **Notities** is de samenvatting, met besluiten en actiepunten. **Transcript** is wat er woord voor woord is gezegd. Het transcript is standaard ingeklapt en toont hoe lang het duurt. Met **Tonen** open je het.

Als de gegevens niet laden, probeert de app het ongeveer een halve minuut automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Voor elk onderdeel zijn er aparte opties: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene toevoegt, blijft daar staan. Bij een meeting die je kunt wijzigen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, staan de notities daarvan onder Notities en het transcript onder Transcript. Ze zijn gemarkeerd als **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden ze allebei getoond.

Notities kunnen ook worden toegevoegd aan de agenda-afspraak van de meeting zelf, nadat die is begonnen, of per mail van Zoom of Gemini binnenkomen. Na afloop van de meeting maakt The Machine er alleen to-do’s van als het om duidelijke vervolgstappen gaat. Als dezelfde notities op twee manieren binnenkomen, wordt er één to-do gemaakt, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, besluiten en actiepunten met erbij wie ze uitvoert, in de taal van de meeting.

De status wordt **Notities schrijven…** en het schrijven gaat door als je de meeting sluit. Bij een lange meeting duurt het een paar minuten en wordt je eigen model gebruikt. De notities zijn gemarkeerd als **Geschreven door The Machine** en vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag ernaar in een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de teammeeting van vandaag’. Een transcript komt onder Transcript en een samenvatting onder Notities. In de agenda heeft een meeting met notities of een transcript het label **Notities** of **Transcript**.

The Machine leest beide voor de vervolgacties van de meeting. Die zijn Werk of Privé, net als de meeting, en worden alleen met je team gedeeld als de meeting ook met je team wordt gedeeld.

Je kunt de meeting met deze gegevens openen waar je die ook tegenkomt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. **Originele uitnodiging** onderaan toont de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook en andere agenda’s zijn alleen-lezen. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze onder **+** in de bovenbalk): kies de agenda, een titel en een tijdstip. Klik op een afspraak zonder gasten in die agenda om die te wijzigen of **Verwijderen** om die te verwijderen (tik twee keer).

**Waar** stelt tijdens het typen locaties voor: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om locaties op te zoeken. Kies een locatie of houd je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph toe, of een e-mailadres. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop staan de mensen die een uitnodiging krijgen. Op de knop staat hoeveel het er zijn: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen als je erop tikt, niet eerder. Zonder gasten wordt niemand uitgenodigd en krijgt niemand een update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld een ophaalmoment om toe te voegen. Je ziet precies wat er verandert. Alleen als je **Toevoegen**, **Opslaan** of **Verwijderen** kiest, wordt de wijziging doorgevoerd.

Nog geen meetings? Als je geen agenda hebt gekoppeld, opent **Koppel je agenda** de Koppelingen. Koppel [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een werkmeeting overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de nieuwste van de twee. The Machine kan een kort bericht opstellen om de afspraak te verplaatsen, of voorstellen om die af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Eén gebeurtenis die met meerdere afspraken overlapt, levert één to-do over die gebeurtenis op. Een nieuwe overlap wordt aan de to-do toegevoegd zolang die open is. Zodra de to-do is afgerond of afgewezen, zorgt alleen een later aangemaakte of gewijzigde meeting ervoor dat die terugkomt.

Afspraken voor de hele dag, afspraken waarbij je als vrij staat en voorlopige afspraken tellen nooit mee. Elk conflict wordt maar één keer gemeld. De werklocatie, focustijd en afwezigheidsstatus van Google tellen ook niet mee. Een eigen blok met andere meetings erin, zoals een kantoordag, telt evenmin mee. Alleen de meetings in dat blok kunnen een conflict opleveren. Een blok zonder andere deelnemers en zonder meetings, zoals een vlucht, kan wel conflicteren met een afspraak waaraan anderen deelnemen.

Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit te zien krijgt. Alleen jij ziet waarmee de afspraak conflicteert: de eerste twee afspraken en daarna hoeveel er nog meer zijn. Een to-do waar je niets mee hebt gedaan, wordt vanzelf gesloten als het conflict bij een andere to-do hoort of toch geen conflict blijkt te zijn.

## Klaar voor je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de meeting. Dat is een korte briefing:

- **Wie:** wie ze zijn volgens je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet, voor wie en tegen welke prijs, als dat relevant is voor de meeting.
- **Tot nu toe:** wat je hebt besproken, gevraagd en aangeboden, en wat de stand van zaken is. Na de meeting staan die berichten bij de bronnen van de to-do.
- **Eerder afgesproken:**, **Sindsdien gewijzigd:** en **Nog open:** wat er uit eerdere meetings met dezelfde mensen is gekomen. Bij elke regel staat de meeting of het bericht waar die vandaan komt.
- **Openstaande beloftes:** wat jij of de anderen nog moeten doen, op basis van de beloftes op je Machine.
- **Open vragen:** wat nog geen antwoord heeft.
- **Te beslissen of mee te nemen:** wat je moet afspreken of meenemen, en wat voor de anderen waarschijnlijk belangrijk is.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de meeting als die in de namiddag plaatsvindt, anders op de werkdag ervoor. De briefing is bedoeld om te lezen. Zodra je die hebt gelezen, staat er **Gedaan**. Een belofte of vraag waar iets mee moet gebeuren, krijgt een eigen to-do.

Stel vragen over de meeting in de chat of voeg toe wat je weet. The Machine antwoordt of verwerkt je notitie in de briefing, bijvoorbeeld onder **Te beslissen of mee te nemen**, en leert ervan. Vanuit een briefing wordt niets verstuurd.

Eerdere meetings tellen mee als er iemand van buitenaf aan beide meetings deelneemt, ongeacht de naam van de meeting of het adres dat die persoon gebruikte. The Machine leest de notities die op je Machine staan: die van jou, van je meetingapp of uit een mail die de notities bevat. Als die er niet zijn, gebruikt The Machine het transcript of de notities uit de agenda-afspraak. De nieuwste informatie weegt het zwaarst. Een punt dat later is afgehandeld, wordt niet meer als openstaand getoond.

Notities en berichten uit [Geschiedenis](history.md) tellen ook mee. Zo kan de briefing informatie bevatten over meetings van vóór je begon.

Een werkbriefing leest geen persoonlijke notities en niets van de Machine van iemand anders. De tekst blijft bij jou: bij een overdracht wordt die niet meegestuurd en je kunt die niet ter beoordeling versturen. Als er geen notities zijn, verschijnen deze regels niet.

De briefing gebruikt informatie die al op je Machine staat. Voor je eerste meeting met iemand van een bedrijf leest The Machine ook de startpagina van de website van dat bedrijf.

Als zoeken op internet is ingesteld op je Machine, zoekt The Machine ook kort op de naam en het bedrijf van de ander. Een gehoste Machine heeft deze functie niet. Op je eigen computer kun je die instellen in OpenClaw. De gevonden informatie bevat een link. Alleen de openbare naam, bedrijfsnaam en website van de ander worden gebruikt voor de zoekopdracht, nooit je berichten. De gevonden informatie wordt 30 dagen hergebruikt.

Zo kan een briefing klaarstaan voor een eerste meeting waarvoor je hebt toegezegd, nog voordat je iets hebt uitgewisseld. Je ziet wat het bedrijf doet, wat dat voor jou betekent en, als dat bekend is, wie de ander is. Met alleen een voornaam bewaart The Machine alleen informatie uit de zoekresultaten als die naar één persoon verwijst. Als **Werkcontacten opzoeken** uitstaat (Instellingen, Beveiliging), wordt er niets opgezocht.

Een terugkerende meeting krijgt alleen een briefing als er sinds de vorige keer iets is gebeurd: een bericht, notities of een belofte. De briefing vermeldt wat nieuw is, niet wat er in de vorige stond. Er verschijnt maximaal één briefing per dag voor terugkerende meetings, nadat de vorige meeting is afgelopen.

Een meeting met alleen je eigen team krijgt alleen een briefing als uit de notities van eerdere meetings blijkt dat er nog een besluit openstaat, iemand nog een stap moet zetten of er nieuws is. Die informatie komt uit dezelfde reeks meetings, of uit meetings met dezelfde titel waar minstens één deelnemer van de huidige meeting bij was. Informatie komt nooit uit een andere meeting met dezelfde collega’s. De briefing introduceert je collega’s niet en zoekt niets over hen op. Een gewone stand-up krijgt geen briefing.

Als er niets nuttigs te melden is, wordt er geen to-do gemaakt. Persoonlijke en afgewezen meetings krijgen geen briefing. Als een meeting wordt verplaatst, blijft de bijbehorende to-do bestaan en wordt die naar het nieuwe tijdstip verplaatst. Een afgewezen briefing komt niet terug. De to-do van een geannuleerde meeting wordt automatisch gesloten.

Als een update de inhoud van een briefing verandert, worden open briefings voor meetings die nog moeten plaatsvinden één keer opnieuw opgesteld, met de nieuwe informatie. De titel, bronnen en plek op je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft zoals die is. Dat geldt ook voor een briefing van een meeting die binnen enkele minuten begint.

In de gegevens van de meeting staat de to-do onder **To-do**. Tik erop om naar de chat te gaan.
