---
title: Agenda
area: calendar
summary: De komende week op één plek: afspraken, to-do's met deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 970b39054ae39543
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- afspraken uit de agenda's die je hebt gekoppeld,
- to-do's met die dag als deadline en gesnoozede to-do's op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit boekings- en ticketmails.

Een afspraak die in twee agenda's staat, wordt één keer getoond. Een agenda die iemand met je heeft gedeeld, toont de afspraken van die persoon gedimd, met diens voornaam. Die afspraken maken nooit een to-do aan. Afspraken die de hele dag duren of meerdere dagen beslaan, worden op elke dag waarop ze vallen als hele-dagafspraak getoond. Een reis staat in Agenda op elke dag bovenaan. In Week en Maand staat hij als één balk over de dagen, bijvoorbeeld 'Reis naar Lissabon'.

Een gezamenlijk plan is één belofte, met 'Met' en de naam van de ander erbij. Een belofte over een afspraak die dag met dezelfde persoon staat op de rij van die afspraak.

**Te laat** staat bovenaan. Bij een afspraak met een open to-do staat de status: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die voltooid lijkt, omdat je al hebt geantwoord of omdat de uitvoering heeft vastgesteld dat hij klaar is, wordt niet als **Deadline** getoond.

## Agenda, week of maand

- **Agenda** toont elke dag. Scroll omlaag voor latere dagen, of omhoog (of kies **Eerdere dagen tonen**) voor eerdere dagen. Je kunt terug tot een week vóór je je agenda koppelde. Bovenaan staat vanaf welke dag de agenda wordt getoond. Zodra de [geschiedenis](history.md) is ingeladen, kun je ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik op een dag om de afspraken te bekijken.

Met **Vandaag**, ‹ en › bovenaan ga je naar een andere week of maand. De weergave die je kiest, wordt op dat apparaat onthouden.

In het weekraster staan afspraken op hetzelfde tijdstip naast elkaar, zodat ze leesbaar blijven. De rest wordt weergegeven als **+N**. Daarmee open je die dag in Agenda.

## Iets openen

Klik op een rij om de chat van de to-do, de belofte, de reis of het evenement, of de afspraak te openen. Bij een afspraak die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een afspraak met gasten, zie je de details: wanneer, waar en wie. Iemand die je Graph kent, en de organisaties en projecten waar de afspraak bij hoort, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de afspraak daar. Alleen bekijken verandert niets.

Een vergaderruimte die bij een afspraak is geboekt, staat bij Waar. Die wordt nooit als persoon of in je Graph getoond.

Een link naar een vergadering wordt weergegeven met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de afspraak om deel te nemen.

## Reizen en evenementen

Wanneer een boeking voor een vlucht, hotel, trein, bus, veerboot of huurauto in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar: de heenreis, het hotel en de terugreis. De reis wordt als één balk over de dagen getoond. Open de reis voor de boekingscode, stoel en het ticket van elke boeking, op volgorde van tijd.

Tickets voor een concert, wedstrijd, festival of conferentie maken een evenement aan. Er is één evenement per activiteit, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat via je werkmailbox is geboekt, is Werk. Anders is het Persoonlijk.

- Elke regel vermeldt van wie de boeking komt, bijvoorbeeld **Van Example Tickets**, en opent die mail.
- Als er een to-do uit de mail is gemaakt, bijvoorbeeld om de tickets te betalen, toont **De to-do openen** die to-do.
- Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.

Je Machine leest de gegevens die luchtvaartmaatschappijen, hotels, boekingssites en ticketverkopers in hun bevestigingsmails zetten. Daarvoor gebruikt hij geen AI. Een mail zonder die gegevens levert niets op. Boekingsmails uit het jaar aan geschiedenis dat je Machine bewaart, worden op de achtergrond ingelezen zodra die [geschiedenis](history.md) is ingeladen.

## Aantekeningen en transcript van een afspraak

De details van een afspraak bestaan uit twee delen. **Notities** is de samenvatting met besluiten en actiepunten. **Transcript** is wat er woord voor woord is gezegd. Het transcript is standaard ingeklapt en toont hoelang het is; met **Tonen** open je het.

Als ze niet laden, probeert de app het ongeveer een halve minuut automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Je kunt voor elk onderdeel apart **Notities toevoegen** of **Transcript toevoegen** kiezen, een Markdown- of tekstbestand **Bestand uploaden**, **Bewerken** of **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een afspraak die je kunt wijzigen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities van die dienst onder Notities en het transcript onder Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide beschikbaar zijn, worden ze allebei getoond.

Notities kunnen ook worden toegevoegd aan de agenda-afspraak zelf nadat die is begonnen, of per mail van Zoom of Gemini binnenkomen. Na afloop van de afspraak maakt The Machine daar alleen to-do's van voor duidelijke vervolgstappen. Als dezelfde notities op twee manieren binnenkomen, wordt er één to-do gemaakt, met de afspraak als bron: 'Bron: notities van' de afspraak.

Bij een afspraak met een transcript maar zonder notities staat **Notities maken**. The Machine maakt dan notities op basis van het transcript: een korte samenvatting, besluiten en actiepunten met de naam van degene die ze uitvoert, in de taal van de afspraak.

Je ziet **Notities schrijven…**. Het schrijven gaat door als je de afspraak sluit. Een lange afspraak kan een paar minuten duren en gebruikt je eigen model. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

Je kunt The Machine ook vragen om ze toe te voegen. Vraag het in een to-do, bijvoorbeeld: 'voeg dit transcript toe aan de teamvergadering van vandaag'. Een transcript komt onder Transcript te staan, een samenvatting onder Notities. Bij een afspraak met notities of een transcript staat **Notities** of **Transcript** in de Agenda.

The Machine leest beide om de vervolgacties van de afspraak te vinden. Die zijn Werk of Persoonlijk, net als de afspraak, en worden alleen met je team gedeeld als de afspraak dat ook wordt.

Je kunt een afspraak met deze details openen vanaf elke plek waar je die vindt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Met **Originele uitnodiging** onderaan bekijk je de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je kunt je eigen Google-agenda hier wijzigen. Outlook en andere agenda's zijn alleen zichtbaar. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze onder **+** in de bovenbalk): kies de agenda, een titel en het tijdstip. Klik op een afspraak zonder gasten in die agenda om die te wijzigen of **Verwijderen** te kiezen (tik twee keer).

**Waar** geeft suggesties terwijl je typt: eerst plaatsen die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om te zoeken. Kies een suggestie of houd je eigen tekst aan.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat om hoeveel mensen het gaat: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas wanneer je erop tikt. Zonder gasten wordt niemand uitgenodigd en krijgt niemand een update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld om een ophaalmoment toe te voegen. Je ziet precies wat er verandert. De wijziging wordt pas doorgevoerd als je **Toevoegen**, **Opslaan** of **Verwijderen** kiest.

Nog geen afspraken? Als je geen agenda hebt, opent **Koppel je agenda** de Koppelingen. Koppel [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Botsingen met je andere agenda

Als een werkafspraak overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de nieuwste van de twee afspraken. Hij kan een kort bericht opstellen om de afspraak te verzetten of voorstellen om die af te wijzen. Er wordt pas iets verstuurd nadat je het hebt goedgekeurd.

Afspraken die de hele dag duren, als vrij gemarkeerd zijn of voorlopig zijn, tellen niet mee. Elke botsing wordt één keer gemeld. Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak botst.

## Voorbereid op je afspraken

Voor een afspraak met mensen van buiten je bedrijf maakt The Machine één to-do aan: **Voorbereiden op** de afspraak. Dat is een korte briefing:

- **Wie:** wie ze zijn, op basis van je Graph.
- **Laatste contact:** je laatste gesprek met ze. Dat bericht is na de afspraak de bron van de to-do.
- **Open beloftes:** wat jij of zij nog moeten doen.
- **Open vragen:** wat nog niet is beantwoord.
- **Beslissen of meenemen:** wat je moet bespreken of meenemen.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de afspraak als die in de middag is, anders op de werkdag ervoor. Hij gebruikt alleen informatie die al op je Machine staat. De briefing is alleen bedoeld om te lezen. Kies **Gedaan** als je hem hebt gelezen. Een belofte of vraag die actie vereist, krijgt een eigen to-do.

Zonder bruikbare geschiedenis wordt er geen to-do gemaakt. Terugkerende, interne, persoonlijke en afgewezen afspraken krijgen er geen. Als een afspraak wordt verzet, blijft dezelfde to-do staan, nu op het nieuwe tijdstip. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde afspraak wordt automatisch gesloten.

De details van de afspraak tonen de bijbehorende to-do onder **To-do**, één tik verwijderd van de chat.
