---
title: Agenda
area: calendar
summary: De komende week in één overzicht: meetings, to-do’s met een deadline, gesnoozede to-do’s en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9f38e3718f3e8639
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- meetings uit de agenda’s die je hebt gekoppeld,
- to-do’s met een deadline op die dag en gesnoozede to-do’s op de dag waarop ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een meeting die in twee agenda’s staat, wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedempt en met diens voornaam. Die leiden nooit tot een to-do. Afspraken die de hele dag duren en afspraken over meerdere dagen worden elke dag waarop ze vallen als dagvullend getoond. Een reis staat in Agenda op elke dag als eerste, en in Week en Maand als één balk over de dagen, bijvoorbeeld ‘Reis naar Lissabon’.

Een gezamenlijk plan is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een meeting met die persoon op die dag staat op de rij van die meeting.

**Te laat** staat bovenaan. Bij een meeting met een open to-do zie je: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die afgerond lijkt, omdat je al hebt geantwoord of omdat de uitvoering heeft vastgesteld dat hij klaar is, wordt niet als **Deadline** getoond.

## Agenda, week of maand

- **Agenda** toont elke dag. Scrol omlaag voor latere dagen of omhoog (of tik op **Eerdere dagen tonen**) voor eerdere dagen. Je kunt terug tot een week voordat je je agenda koppelde. Bovenaan staat vanaf welke dag. Zodra je [geschiedenis](history.md) is ingeladen, kun je ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen; tik op een dag om de items te bekijken.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De gekozen weergave wordt op dit apparaat onthouden.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat ze leesbaar blijven. De rest wordt weergegeven als **+N**. Tik daarop om die dag in de agenda te openen.

## Iets openen

Klik op een rij om de chat van de to-do, de belofte, de reis of het evenement, of de meeting te openen. Bij een meeting die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een meeting met gasten, zie je de details: wanneer, waar en wie. Iemand die je Graph kent, en de organisaties en projecten waaraan de meeting is gekoppeld, linken naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) open je de meeting daar. Alleen kijken verandert niets.

Een meetingruimte die bij een meeting is geboekt, staat onder de locatie. Hij wordt nooit als persoon of in je Graph weergegeven.

Een link naar een meeting wordt getoond met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de meeting om deel te nemen.

## Reizen en evenementen

Wanneer een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen bij elkaar, uit al je mailboxen: de trein naar het vliegveld, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden samengevoegd als de dagen elkaar overlappen of de ene aansluit op de andere.

De reis wordt als één balk over de dagen getoond. Open de reis om alle boekingen op tijdsvolgorde te zien, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken een evenement aan, één per evenement, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat in je werkmailbox is geboekt, is Werk; anders is het Persoonlijk. Tickets voor iets dat tijdens een reis plaatsvindt, worden aan de reis toegevoegd.

Bij een reis die nog moet plaatsvinden, geeft je Machine aan wat er ontbreekt, bijvoorbeeld **Geen verblijf geboekt voor 2 nachten** of dat er niets is geboekt van het vliegveld naar je hotel. Die regels zijn gedempt en hebben het label **Geen boeking**. Bij een reis zonder verblijf wordt niets over overnachtingen vermeld.

- Elke regel vermeldt van wie de boeking afkomstig is, bijvoorbeeld **Van Example Tickets**, en opent die mail.
- Komt er een to-do uit de mail, bijvoorbeeld om voor de tickets te betalen, dan toont **De to-do openen** die to-do.
- Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar jou is doorgestuurd, komt niet bij je reizen te staan.

De meeste bevestigingen bevatten de boekingsgegevens in een vorm die je Machine zonder AI kan lezen. Bij bevestigingen die dat niet doen, zoals doorgestuurde mail of mail van een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Het wacht daarmee als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Meetingnotities en transcript

De details van een meeting bestaan uit twee delen. **Notities** is de samenvatting: beslissingen en actiepunten. **Transcript** is woord voor woord wat er is gezegd. Het staat eerst ingeklapt, met de duur erbij. Met **Tonen** open je het.

Als ze niet laden, probeert de app dat ongeveer een halve minuut vanzelf opnieuw. Tik daarna op **Opnieuw proberen**.

Je kunt voor elk onderdeel apart **Notities toevoegen** of **Transcript toevoegen**, een Markdown- of tekstbestand **Bestand uploaden**, en **Bewerken** of **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een meeting die je kunt wijzigen, open je de notities met **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, verschijnen de notities onder Notities en het transcript onder Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden ze allebei getoond.

Notities kunnen ook in de agenda-afspraak zelf staan, nadat de meeting is begonnen zijn toegevoegd, of per mail van Zoom of Gemini binnenkomen. Na afloop van de meeting maakt The Machine daar alleen to-do’s van als er duidelijke vervolgstappen in staan. Als dezelfde notities op twee manieren binnenkomen, ontstaat er één to-do, met de meeting als bron: ‘Bron: notities van’ de meeting.

Bij een meeting met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met erbij wie ze uitvoert, in de taal van de meeting.

Je ziet **Notities schrijven…**. Het schrijven gaat door als je de meeting sluit. Een lange meeting kan een paar minuten duren en gebruikt je eigen model. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag dat in een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de boardmeeting van vandaag’. Een transcript komt onder Transcript, een samenvatting onder Notities. Bij een meeting met notities of een transcript staat in de agenda **Notities** of **Transcript**.

The Machine leest beide om de vervolgacties van de meeting te bepalen. Die zijn Werk of Persoonlijk, net als de meeting, en worden alleen met je team gedeeld als de meeting dat ook wordt.

Je kunt de details van een meeting overal openen waar je die tegenkomt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. **Originele uitnodiging** onderaan toont de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je kunt je eigen Google-agenda hier wijzigen. Outlook en andere agenda’s zijn alleen-lezen. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze onder **+** in de bovenste balk): kies de agenda, een titel en een tijd. Klik op een afspraak zonder gasten in die agenda om deze te wijzigen of **Verwijderen** (tik twee keer).

**Waar** stelt tijdens het typen locaties voor: eerst plekken die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om ze op te zoeken. Kies een suggestie of houd je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie staat alleen bij je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat hoeveel mensen je uitnodigt: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen als je erop tikt, niet eerder. Zonder gasten wordt niemand uitgenodigd en krijgt niemand een update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld een ophaalmoment om toe te voegen. Je ziet precies wat er verandert. Alleen met **Toevoegen**, **Opslaan** of **Verwijderen** voer je de wijziging door.

Nog geen meetings? Zonder agenda opent **Koppel je agenda** de Koppelingen: koppel [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een werkmeeting overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de nieuwste van de twee. Hij kan een kort bericht opstellen om de afspraak te verzetten of voorstellen om de uitnodiging af te wijzen. Er wordt niets verstuurd voordat je het goedkeurt.

Afspraken die de hele dag duren, als vrij zijn gemarkeerd of voorlopig zijn, tellen nooit mee. Elk conflict wordt één keer getoond. Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak conflicteert.

## Goed voorbereid op je meetings

Voor een meeting met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de meeting. Dat is een korte briefing:

- **Wie:** wie ze zijn, op basis van je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet dat relevant is voor de meeting.
- **Tot nu toe:** wat je hebt besproken, gevraagd en aangeboden, en wat de stand van zaken is. Die berichten zijn na de meeting de bronnen van de to-do.
- **Open beloftes:** wat jij of de ander nog moet doen, op basis van de beloftes op je Machine.
- **Open vragen:** wat nog onbeantwoord is.
- **Beslissen of meenemen:** wat je moet beslissen of meenemen, en wat voor hen waarschijnlijk belangrijk is.

De to-do verschijnt op de ochtend van een werkdag: op de dag van de meeting zelf als die ’s middags plaatsvindt, anders op de werkdag ervoor. Je kunt hem alleen lezen. Tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag uit de briefing waar iets mee moet gebeuren, krijgt een eigen to-do.

De briefing gebruikt informatie die al op je Machine staat. Voor een eerste meeting met iemand bij een bedrijf zoekt The Machine ook kort op het web naar de naam en het bedrijf, en toont een link naast de gevonden informatie. Alleen de openbare naam, bedrijfsnaam en website van die persoon worden meegestuurd voor de zoekopdracht, nooit je berichten. Een zoekopdracht wordt 30 dagen hergebruikt. Als **Werkcontacten opzoeken** uitstaat (Instellingen, Beveiliging), wordt er niet gezocht.

Zonder bruikbare geschiedenis wordt er geen to-do gemaakt. Terugkerende, interne, persoonlijke en afgewezen meetings krijgen er geen. Als een meeting wordt verzet, blijft de ene to-do behouden en krijgt die de nieuwe tijd. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde meeting wordt vanzelf gesloten.

Als een wijziging de inhoud van een briefing verandert, worden briefings voor toekomstige meetings één keer opnieuw opgesteld. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft zoals die is. Dat geldt ook voor een briefing van een meeting die binnen een paar minuten begint.

In de details van de meeting staat de to-do onder **To-do**, één tik verwijderd van de chat.
