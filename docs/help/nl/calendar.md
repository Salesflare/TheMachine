---
title: Agenda
area: calendar
summary: De komende week op één plek: meetings, to-do’s met een deadline, gesnoozede to-do’s en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: f3f41306aad03084
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda’s die je hebt gekoppeld,
- to-do’s met een deadline op die dag en gesnoozede to-do’s op de dag waarop ze terugkomen,
- opvolging van werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een meeting in twee agenda’s wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd en met de voornaam erbij. Daaruit ontstaan nooit to-do’s. Afspraken die de hele dag of meerdere dagen duren, worden op elke dag waarop ze vallen als afspraken voor de hele dag getoond. Een reis staat in Agenda op elke dag als eerste, en in Week en Maand als één balk over de reisdagen, bijvoorbeeld ‘Reis naar Lissabon’.

Een afspraak die jullie samen hebben gemaakt, is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een meeting met diezelfde persoon op die dag staat bij die meeting.

**Te laat** staat bovenaan. Bij een meeting met een open to-do zie je die to-do: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die afgehandeld lijkt, omdat je al hebt geantwoord of omdat de uitvoering liet zien dat hij klaar was, wordt niet als **Deadline** getoond.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen, of omhoog (of kies **Eerdere dagen tonen**) voor eerdere dagen. Je kunt terug tot een week vóór je je agenda hebt gekoppeld. Bovenaan staat vanaf welke dag je agenda wordt getoond. Zodra je [geschiedenis](history.md) is ingeladen, kun je ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik erop om de items van die dag te zien.

Met **Vandaag**, ‹ en › bovenaan blader je door weken of maanden. De weergave die je kiest, wordt op dat apparaat onthouden.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat ze leesbaar blijven. De overige afspraken worden getoond als **+N**. Daarmee open je die dag in de agendaweergave.

## Iets openen

Klik op een rij om de chat van de to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt wijzigen, zoals die van iemand anders of een meeting met gasten, zie je de details: wanneer, waar en met wie. Iemand die je Graph kent, en de organisaties en projecten die bij de meeting horen, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de meeting daar. Alleen kijken brengt niets teweeg.

Een meetingruimte die bij een meeting is geboekt, staat onder ‘Waar’, nooit als persoon of in je Graph.

Een link naar een meeting wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Zodra een boeking voor een vlucht, hotel, vakantiewoning, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden gecombineerd als hun datums overlappen of als de ene eindigt wanneer de andere begint.

De reis wordt als één balk over de reisdagen getoond. Open de reis om alle boekingen op volgorde te zien, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken één evenement per evenement aan, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat je via je werkmail hebt geboekt, is Werk. Anders is het Persoonlijk. Tickets voor iets tijdens een reis worden aan de reis toegevoegd.

Bij een reis die nog moet plaatsvinden, geeft je Machine aan wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten** of dat er niets is geboekt voor de rit van de luchthaven naar je hotel. Die regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder overnachtingen wordt niets over nachten vermeld.

- Elke regel vermeldt van wie de boeking komt, bijvoorbeeld **Van Example Tickets**, en opent die mail.
- Als er vanuit de mail een to-do is aangemaakt, bijvoorbeeld om voor de tickets te betalen, zie je die via **De to-do openen**.
- Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

De meeste bevestigingen bevatten de details in een vorm die je Machine zonder AI kan lezen. Bij bevestigingen waarbij dat niet kan, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Het wacht daarmee als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar dat je Machine bewaart als [geschiedenis](history.md), worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Meetingnotities en transcript

De details van een meeting bestaan uit twee delen. **Notities** is de samenvatting met besluiten en actiepunten. **Transcript** bevat precies wat er is gezegd. Het transcript is eerst ingeklapt en toont de duur. Met **Tonen** open je het.

Als de gegevens niet laden, probeert de app het ongeveer een halve minuut lang vanzelf opnieuw. Tik daarna op **Opnieuw proberen**.

Voor elk onderdeel zijn er aparte opties: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een meeting die je kunt wijzigen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities bij Notities en het transcript bij Transcript. Ze hebben het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, zie je ze allebei.

Notities kunnen ook in de agenda-afspraak van de meeting zelf staan, nadat de meeting is begonnen zijn toegevoegd, of per mail van Zoom of Gemini binnenkomen. Na afloop van de meeting maakt The Machine daar alleen to-do’s van als er duidelijke vervolgstappen zijn. Als dezelfde notities op twee manieren binnenkomen, ontstaat er maar één to-do, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities zie je **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, besluiten en actiepunten met erbij wie ze uitvoert, in de taal van de meeting.

De melding **Notities schrijven…** blijft staan terwijl The Machine verderwerkt, ook als je de meeting sluit. Een lange meeting verwerken kan een paar minuten duren en gebruikt je eigen model. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag het in een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de meeting van vandaag over het bord’. Een transcript komt bij Transcript, een samenvatting bij Notities. Bij een meeting met notities of een transcript zie je in Agenda **Notities** of **Transcript**.

The Machine leest beide om de vervolgstappen van de meeting te vinden. Ze zijn Werk of Persoonlijk, net als de meeting, en worden alleen met je team gedeeld als de meeting dat ook is.

Een meeting opent met deze details, waar je hem ook vindt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Onderaan toont **Originele uitnodiging** de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook-agenda’s en andere agenda’s zijn alleen zichtbaar. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze optie onder **+** in de bovenbalk): kies de agenda, een titel en een tijdstip. Klik op een afspraak zonder gasten in die agenda om deze te wijzigen, of **Verwijderen** (tik twee keer).

**Waar** stelt tijdens het typen locaties voor: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om de locaties op te zoeken. Kies een suggestie of gebruik je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop staat wie een uitnodiging krijgt. Op de knop staat hoeveel mensen je uitnodigt: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten wordt niemand uitgenodigd en krijgt niemand een update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld een ophaalafspraak toevoegen. Je ziet precies wat er verandert. Pas als je **Toevoegen**, **Opslaan** of **Verwijderen** kiest, wordt de wijziging doorgevoerd.

Nog geen meetings? Als je nog geen agenda hebt, opent **Koppel je agenda** Koppelingen. Daar kun je [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md) koppelen.

## Conflicten met je andere agenda

Als een werkmeeting overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de meest recente van de twee afspraken. The Machine kan een kort bericht opstellen om de afspraak te verplaatsen, of voorstellen om de afspraak af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Afspraken die de hele dag duren, als vrij gemarkeerd zijn of voorlopig zijn, tellen niet mee. Elk conflict wordt maar één keer gemeld. Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak botst.

## Voorbereid naar je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do aan: **Voorbereiden op** de meeting. Dat is een korte briefing:

- **Wie:** wie ze zijn, op basis van je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet, voor wie en tegen welke prijs, als dat relevant is voor de meeting.
- **Tot nu toe:** wat jullie hebben besproken, gevraagd en aangeboden, en wat de stand van zaken is. Na de meeting staan die berichten als bron bij de to-do.
- **Eerder afgesproken:**, **Sindsdien gewijzigd:** en **Nog open:** wat er uit eerdere meetings met dezelfde mensen is gekomen, met bij elke regel de meeting of het bericht waar die vandaan komt.
- **Open beloftes:** wat jij of de ander nog moet doen, op basis van de beloftes op je Machine.
- **Open vragen:** wat nog geen antwoord heeft.
- **Beslissen of meenemen:** wat je moet bespreken of meenemen, en wat voor de ander waarschijnlijk belangrijk is.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de meeting als die in de middag plaatsvindt, anders op de werkdag ervoor. De briefing is alleen bedoeld om te lezen. Als je hem hebt gelezen, kies je **Gedaan**. Een belofte of vraag waarvoor actie nodig is, krijgt een eigen to-do.

Eerdere meetings tellen mee als er iemand van buiten bij allebei aanwezig is, ongeacht de naam van de meeting of het e-mailadres dat die persoon gebruikte. The Machine leest de notities die je Machine heeft: jouw notities, die van je meeting-app of notities die per mail naar je zijn gestuurd. Anders leest hij het transcript of de notities in de agenda-afspraak. De nieuwste informatie weegt het zwaarst. Een punt dat later is afgehandeld, wordt niet meer als open getoond.

Notities en berichten uit [Geschiedenis](history.md) tellen ook mee. Zo bevat een briefing ook informatie over meetings van voordat je begon.

Een werkbriefing leest geen persoonlijke notities en ook niets van de Machine van iemand anders. De tekst blijft van jou: bij een overdracht gaat hij niet mee en je kunt hem niet ter controle versturen. Als er geen notities zijn, worden die regels niet getoond.

De briefing gebruikt informatie die al op je Machine staat. Voor een eerste meeting met iemand van een bedrijf leest The Machine ook de startpagina van de website van het bedrijf.

Als webzoekopdrachten zijn ingesteld op je Machine, zoekt The Machine ook kort op hun naam en bedrijf. Een gehoste Machine heeft deze functie niet. Op je eigen computer kun je die instellen in OpenClaw. Bij de gevonden informatie staat een link. Alleen hun openbare naam, bedrijfsnaam en website worden meegestuurd voor de zoekopdracht, nooit je berichten. De resultaten worden 30 dagen hergebruikt.

Zo kan een briefing klaarstaan voor een eerste meeting waarvoor je hebt bevestigd, nog voordat je met de ander hebt gesproken. Je ziet wat hun bedrijf doet, wat dat voor jou betekent en, als het bekend is, wie ze zijn. Als alleen de voornaam bekend is, bewaart The Machine de zoekresultaten alleen als die naar één persoon verwijzen. Als **Werkcontacten opzoeken** is uitgeschakeld (Instellingen, Beveiliging), zoekt The Machine niets op.

Een terugkerende meeting krijgt alleen een briefing als er sinds de vorige keer iets is gebeurd: een bericht, notities of een belofte. De briefing vermeldt wat nieuw is, niet wat er in de vorige briefing stond. De briefing komt pas nadat de vorige meeting is afgelopen. Voor maximaal twee terugkerende meetings per dag.

Als er niets nuttigs te melden is, maakt The Machine geen to-do aan. Voor interne, persoonlijke en afgewezen meetings komen er geen to-do’s. Als een meeting wordt verplaatst, blijft de bestaande to-do behouden en wordt het tijdstip aangepast. Een afgewezen meeting komt niet terug. De to-do van een geannuleerde meeting wordt vanzelf gesloten.

Als een update de inhoud van een briefing verandert, worden open briefings voor meetings die nog moeten plaatsvinden één keer opnieuw geschreven met de bijgewerkte informatie. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft zoals die is. Dat geldt ook voor een briefing van een meeting die binnen een paar minuten begint.

Bij de details van de meeting staat de bijbehorende to-do onder **To-do**. Met één tik open je de chat.
