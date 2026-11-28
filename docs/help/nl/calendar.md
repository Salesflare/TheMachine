---
title: Agenda
area: calendar
summary: De week vooruit op één plek: meetings, to-do’s met een deadline, gesnoozede to-do’s en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 7f9f9d9e9a502b7d
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda’s die je hebt gekoppeld,
- to-do’s met die dag als deadline en gesnoozede to-do’s op de dag dat ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een meeting in twee agenda’s wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd, met de voornaam van die persoon. Die leveren nooit een to-do op. Afspraken die de hele dag of meerdere dagen duren, worden voor elke dag waarop ze plaatsvinden als dagvullend getoond. Een reis staat in Agenda op elke dag als eerste, en in Week en Maand als één balk over de dagen heen, zoals ‘Reis naar Lissabon’.

Een plan dat jullie samen hebben gemaakt, is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een meeting die die dag plaatsvindt met diezelfde persoon, staat op de regel van die meeting.

**Te laat** komt bovenaan. Bij een meeting met een open to-do zie je: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die klaar lijkt (je hebt al geantwoord, of de uitvoering heeft vastgesteld dat hij klaar is), wordt niet als **Deadline** getoond.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scrol omlaag voor latere dagen, of omhoog (of tik op **Eerdere dagen tonen**) voor eerdere dagen. De weergave gaat terug tot een week vóór je je agenda hebt gekoppeld. Bovenaan staat vanaf welke dag. Zodra de [geschiedenis](history.md) is ingeladen, gaat de weergave ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie afspraken per dag. Op een telefoon zie je stippen. Tik erop om de afspraken van die dag te zien.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De weergave die je kiest, wordt onthouden op dat apparaat.

In het weekraster staan afspraken op hetzelfde tijdstip naast elkaar, zodat ze leesbaar blijven. De rest wordt als **+N** getoond. Tik erop om die dag in Agenda te openen.

## Iets openen

Klik op een regel om de chat van de to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een meeting met gasten, zie je de details: wanneer, waar en met wie. Iemand die je Graph kent, en de organisaties en projecten waartoe de meeting behoort, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de meeting daar. Alleen kijken verandert niets.

Een vergaderruimte die bij een meeting is geboekt, staat onder de locatie. De ruimte wordt nooit als persoon of in je Graph getoond.

Een meetinglink wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Zodra een boeking voor een vlucht, hotel, vakantiewoning, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden gecombineerd als hun data overlappen of als de ene aansluit op de andere.

De reis wordt als één balk over de reisdata getoond. Open de reis om alle boekingen op tijdsvolgorde te zien, met hun tijden, adres, boekingscode en stoelnummer.

Tickets voor een concert, wedstrijd, festival of conferentie maken een evenement aan, één per evenement. Je ziet waar het is, de boekingscode, het stoelnummer en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat je via je werkmail hebt geboekt, is Werk. Anders is het Persoonlijk. Tickets voor iets tijdens een reis worden aan de reis toegevoegd.

Voor een reis die nog moet plaatsvinden, laat je Machine zien wat er ontbreekt, zoals **Geen verblijf geboekt voor 2 nachten**, of dat er niets is geboekt van de luchthaven naar je hotel. Deze regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder overnachtingen wordt niets over nachten getoond.

- Op elke regel staat van wie de boeking komt, zoals **Van Example Tickets**. Open de regel om de mail te bekijken.
- Als er een to-do uit de mail is gemaakt, bijvoorbeeld om voor de tickets te betalen, zie je die met **De to-do openen**.
- Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals de vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

De meeste bevestigingen bevatten details in een formaat dat je Machine zonder AI kan uitlezen. Voor een bevestiging die dat niet heeft, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Je Machine wacht daarmee als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar dat je Machine bewaart in de [geschiedenis](history.md), worden op de achtergrond uitgelezen zodra die geschiedenis is ingeladen.

## Meetingnotities en transcript

De details van een meeting bestaan uit twee delen. **Notities** is de samenvatting: besluiten en actiepunten. **Transcript** is woord voor woord wat er is gezegd. Het transcript is in eerste instantie ingeklapt en toont hoelang het duurt. Met **Tonen** open je het.

Als de gegevens niet laden, probeert de app het ongeveer een halve minuut automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Voor elk onderdeel zijn er aparte knoppen: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een meeting die je kunt wijzigen, open je de notities met **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities bij Notities en het transcript bij Transcript. Ze krijgen het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden beide getoond.

Notities kunnen ook worden toegevoegd aan de agenda-afspraak van de meeting zelf, nadat die is begonnen, of via mail van Zoom of Gemini. Na afloop van de meeting maakt The Machine alleen to-do’s van duidelijke vervolgstappen. Als dezelfde notities op twee manieren binnenkomen, levert dat één to-do op, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities staat **Notities maken**. The Machine maakt dan notities op basis van het transcript: een korte samenvatting, besluiten en actiepunten, met erbij wie ze uitvoert. De notities zijn in de taal van de meeting.

Je ziet **Notities schrijven…**. The Machine gaat door als je de meeting sluit. Bij een lange meeting duurt het een paar minuten. Hiervoor gebruikt The Machine je eigen model. De notities krijgen het label **Geschreven door The Machine** en vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag dat in een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de vergadering van vandaag over het bord’. Een transcript wordt toegevoegd aan Transcript, een samenvatting aan Notities. Bij een meeting met notities of een transcript zie je in Agenda **Notities** of **Transcript**.

The Machine leest beide om de vervolgacties van de meeting te bepalen. Ze zijn Werk of Persoonlijk, net als de meeting, en worden alleen met je team gedeeld als de meeting dat ook wordt.

Overal waar je een meeting opent, zie je dezelfde details: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Met **Originele uitnodiging** onderaan bekijk je de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. In Outlook en andere agenda’s kun je alleen afspraken bekijken. Met **Nieuwe afspraak** voeg je er een toe (op een telefoon staat deze optie onder **+** in de bovenbalk): kies de agenda, een titel en het tijdstip. Klik op een afspraak zonder gasten in die agenda om die te wijzigen, of **Verwijderen** om die te verwijderen (tik twee keer).

Bij **Waar** verschijnen suggesties terwijl je typt: eerst plaatsen die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om te zoeken. Kies een suggestie of laat je eigen tekst staan.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat om hoeveel mensen het gaat: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten wordt niemand uitgenodigd of op de hoogte gebracht.

Een to-do kan ook een wijziging voorstellen, zoals een afspraak voor een ophaalmoment. Je ziet precies wat er verandert. Pas als je op **Toevoegen**, **Opslaan** of **Verwijderen** tikt, wordt de wijziging doorgevoerd.

Nog geen meetings? Zonder agenda opent **Koppel je agenda** de pagina Koppelingen. Koppel [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Overlap met je andere agenda

Als een werkmeeting overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de meest recente van de twee. The Machine kan een kort bericht opstellen om de meeting te verplaatsen, of voorstellen om die af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Als een afspraak met meerdere andere afspraken overlapt, komt er één to-do voor die afspraak. Een nieuwe overlap wordt eraan toegevoegd zolang de to-do openstaat. Zodra de to-do is afgerond of afgewezen, zorgt alleen een later aangemaakte of gewijzigde meeting ervoor dat die terugkomt.

Afspraken die de hele dag duren, als vrij staan of voorlopig zijn, tellen nooit mee. Elke overlap wordt maar één keer gemeld. De werklocatie, focustijd en afwezigheidsmelding van Google tellen ook niet mee. Een blok in je agenda dat andere meetings bevat, zoals een kantoordag, telt evenmin mee. Alleen de meetings binnen dat blok kunnen overlappen. Een blok zonder anderen en zonder meetings, zoals een vlucht, overlapt wel met een afspraak waar anderen bij betrokken zijn.

Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee die overlapt: de eerste twee afspraken, en daarna hoeveel er nog meer zijn. Een to-do waar je niets mee hebt gedaan, wordt automatisch gesloten als de overlap bij een andere to-do hoort of toch geen overlap blijkt te zijn.

## Klaar voor je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de meeting. Dit is een korte briefing:

- **Wie:** wie de mensen zijn volgens je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet, voor wie en tegen welke prijs, als dat relevant is voor de meeting.
- **Tot nu toe:** wat je hebt besproken, gevraagd en aangeboden, en wat de stand van zaken is. Na de meeting zijn die berichten de bronnen van de to-do.
- **Eerder afgesproken:**, **Sindsdien gewijzigd:** en **Nog open:** wat er uit eerdere meetings met dezelfde mensen is gekomen. Elke regel verwijst naar de meeting of het bericht waar die vandaan komt.
- **Open beloftes:** wat jij of de anderen nog moeten doen, op basis van de beloftes op je Machine.
- **Open vragen:** wat nog niet is beantwoord.
- **Beslissen of meenemen:** wat je moet bespreken of meenemen, en waar de anderen waarschijnlijk belang aan hechten.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de meeting als die in de namiddag plaatsvindt, anders op de vorige werkdag. De briefing is bedoeld om te lezen. Als je hem hebt gelezen, wordt die **Gedaan**. Een belofte of vraag in de briefing die actie vereist, krijgt een eigen to-do.

Stel in de chat van de meeting een vraag of voeg informatie toe: The Machine geeft antwoord of verwerkt je notitie in de briefing, bijvoorbeeld onder **Beslissen of meenemen**, en leert ervan. Vanuit een briefing wordt niets verstuurd.

Eerdere meetings tellen mee als er bij beide iemand van buitenaf aanwezig is, ongeacht de naam van de meeting en het adres dat die persoon heeft gebruikt. The Machine leest de notities die op je Machine staan: je eigen notities, notities van je meetingapp of notities die je per mail hebt ontvangen. Als die er niet zijn, leest The Machine het transcript of de notities in de agenda-afspraak. De meest recente notities wegen het zwaarst. Een punt dat later is afgehandeld, wordt niet meer als open getoond.

Notities en berichten uit [Geschiedenis](history.md) tellen ook mee. Zo bevat een briefing informatie over meetings van voordat je bent begonnen.

Een werkbriefing leest geen persoonlijke notities en niets van de Machine van iemand anders. De tekst blijft bij jou: bij een overdracht gaat die nooit mee en je kunt die niet ter beoordeling versturen. Als er geen notities zijn, worden die regels niet getoond.

The Machine gebruikt informatie die al op je Machine staat. Voor een eerste meeting met iemand bij een bedrijf leest The Machine ook de homepage van de bedrijfswebsite.

The Machine zoekt ook kort op het web naar de naam en het bedrijf van de persoon. Op een gehoste Machine wordt daarvoor je eigen ChatGPT- of Claude-login gebruikt. De zoekopdracht gebruikt een klein deel van je abonnement. Op je eigen computer gebruikt The Machine de zoekprovider die je in OpenClaw hebt ingesteld, of je login zodra je dat inschakelt (`meeting_prep_signin_search` in `config.json`). Een provider die je zelf hebt ingesteld, krijgt altijd voorrang.

Alleen de openbare naam, bedrijfsnaam en website van de persoon worden naar de zoekopdracht gestuurd, nooit je berichten. De zoekresultaten bevatten een link en worden 30 dagen opnieuw gebruikt. Bij ChatGPT kiest het model de link. De link wordt niet gecontroleerd, dus open die voordat je op de informatie vertrouwt. In de chat van de to-do zie je **Zocht op het web**.

Zo kan een eerste meeting waarmee je hebt ingestemd al een briefing krijgen voordat je ook maar één woord hebt uitgewisseld: wat het bedrijf doet, wat dat voor jou betekent en, als die informatie bekend is, wie de persoon is. Als alleen de voornaam bekend is, gebruikt The Machine de zoekresultaten alleen als die naar één persoon verwijzen. Als **Werkcontacten opzoeken** is uitgeschakeld (Instellingen, Beveiliging), worden er geen contacten opgezocht en geen zoekopdrachten uitgevoerd.

Een terugkerende meeting krijgt alleen een briefing als er sinds de vorige keer iets is gebeurd: een bericht, notities of een belofte. De briefing vermeldt wat er nieuw is, niet wat er in de vorige briefing stond. Die verschijnt zodra de vorige meeting is afgelopen, voor maximaal twee terugkerende meetings per dag.

Een meeting met alleen je eigen team krijgt alleen een briefing als eerdere notities uit dezelfde reeks meetings (of met dezelfde titel en met iemand van het team erbij) een punt bevatten dat voor jou is: een open actiepunt voor jou, een vraag aan jou, een besluit dat nog genomen moet worden of een belofte die jij hebt gedaan. Actiepunten die alleen collega’s moeten uitvoeren, leiden niet tot een briefing. The Machine zoekt niets op over je collega’s. De briefing verschijnt zo mogelijk op de ochtend van de meeting zelf.

Als er niets nuttigs te melden is, wordt er geen to-do gemaakt. Persoonlijke en afgewezen meetings krijgen geen briefing. Als een meeting wordt verplaatst, blijft dezelfde to-do behouden, maar dan op het nieuwe tijdstip. Een afgewezen briefing komt niet terug. De to-do van een geannuleerde meeting wordt automatisch gesloten.

Als een wijziging de inhoud van een briefing aanpast, worden open briefings voor meetings die nog moeten plaatsvinden één keer opnieuw geschreven. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft zoals die is. Dat geldt ook voor een briefing van een meeting die over een paar minuten begint.

De details van de meeting tonen de bijbehorende to-do onder **To-do**. Tik erop om de chat te openen.
