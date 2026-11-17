---
title: Agenda
area: calendar
summary: De komende week op één plek: afspraken, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 24033419578a8c8f
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- afspraken uit de agenda's die je hebt gekoppeld,
- to-do's met een deadline op die dag en gesnoozede to-do's op de dag dat ze terugkomen,
- opvolging van werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit je boekings- en ticketmails.

Een afspraak in twee agenda's wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd, met diens voornaam. Die leveren nooit een to-do op. Afspraken die de hele dag of meerdere dagen duren, worden op elke dag waarop ze vallen als afspraken voor de hele dag getoond. Een reis staat in **Agenda** bovenaan op elk van de reisdagen, en in **Week** en **Maand** als één balk over die dagen, bijvoorbeeld 'Reis naar Lissabon'.

Een gezamenlijk gemaakt plan is één belofte, met 'Met' en de naam van de ander erbij. Een belofte over een afspraak met diezelfde persoon staat op de regel van die afspraak.

**Te laat** staat bovenaan. Bij een afspraak met een open to-do zie je de status: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die voltooid lijkt, omdat je al hebt gereageerd of omdat de uitvoering heeft uitgewezen dat die klaar is, wordt niet als **Deadline** getoond.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen of omhoog (of tik op **Eerdere dagen tonen**) voor eerdere dagen. De agenda gaat terug tot een week voordat je je agenda koppelde. Bovenaan staat vanaf welke dag hij begint. Zodra je [geschiedenis](history.md) is ingeladen, gaat hij ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik op een dag om de items te bekijken.

Met **Vandaag**, ‹ en › bovenaan blader je door weken of maanden. De gekozen weergave wordt op dat apparaat onthouden.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat ze leesbaar blijven. De overige afspraken worden weergegeven als **+N**. Daarmee open je die dag in de agendaweergave.

## Iets openen

Klik op een regel om de chat van de to-do, de belofte, de reis of het evenement, of de afspraak te openen. Bij een afspraak die je hier niet kunt wijzigen, bijvoorbeeld omdat die van iemand anders is of gasten heeft, zie je de details: wanneer, waar en wie. Personen die je Graph kent, en de organisaties en projecten bij de afspraak, zijn links naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) open je de afspraak daar. Alleen bekijken brengt niets in beweging.

Een vergaderruimte die bij een afspraak is geboekt, staat bij de locatie. Hij wordt nooit als persoon of in je Graph getoond.

Een link naar een afspraak wordt weergegeven met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de afspraak om deel te nemen.

## Reizen en evenementen

Wanneer een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of parkeerplaats bij het vliegveld in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen samen op één reis, uit al je mailboxen: de trein naar het vliegveld, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden gecombineerd als hun datums elkaar overlappen of als de ene eindigt op de dag waarop de andere begint.

De reis wordt als één balk over de reisdagen getoond. Open de reis om alle boekingen op volgorde te bekijken, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken een evenement aan, één per evenement, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat via je werkmailbox is geboekt, is Werk. Anders is het Persoonlijk. Tickets voor iets tijdens een reis worden aan de reis toegevoegd.

Voor een reis die nog moet plaatsvinden, laat je Machine zien wat er ontbreekt, zoals **Geen verblijf geboekt voor 2 nachten**, of dat er niets is geboekt van het vliegveld naar je hotel. Die regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder verblijf wordt niets over overnachtingen vermeld.

- Op elke regel staat van wie de boeking afkomstig is, bijvoorbeeld **Van Example Tickets**. Klik erop om de mail te openen.
- Als er vanuit de mail een to-do is gemaakt, bijvoorbeeld om voor de tickets te betalen, kun je die openen met **De to-do openen**.
- Een gewijzigde boeking werkt de regel bij. Een geannuleerde boeking wordt verwijderd. Als alle boekingen zijn geannuleerd, wordt ook de reis of het evenement verwijderd.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

In de meeste bevestigingen staan de gegevens in een formaat dat je Machine zonder AI kan lezen. Bij bevestigingen in een ander formaat, zoals een doorgestuurde mail of een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond, een paar tegelijk. Dat gebeurt pas weer als je niet dicht bij je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bewaart, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Aantekeningen en transcript van afspraken

De details van een afspraak bestaan uit twee delen. **Notities** is de samenvatting: beslissingen en actiepunten. **Transcript** is alles wat er woord voor woord is gezegd. Het transcript is ingeklapt en toont hoe lang het is. Met **Tonen** open je het.

Als de inhoud niet laadt, probeert de app het ongeveer een halve minuut lang automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Voor beide onderdelen zijn er aparte opties: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een afspraak die je kunt wijzigen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) is gekoppeld, staan de notities bij Notities en het transcript bij Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden ze allebei getoond.

Notities kunnen ook in de agenda-afspraak zelf staan, nadat die is begonnen zijn toegevoegd, of per mail van Zoom of Gemini binnenkomen. Na afloop van de afspraak maakt The Machine er alleen to-do's van als er duidelijke vervolgstappen zijn. Als dezelfde notities op twee manieren binnenkomen, levert dat één to-do op, met de afspraak als bron: 'Bron: notities van' de afspraak.

Bij een afspraak met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met erbij wie ze uitvoert, in de taal van de afspraak.

Je ziet **Notities schrijven…**. Het schrijven gaat door als je de afspraak sluit. Bij een lange afspraak duurt het een paar minuten. Hiervoor wordt je eigen model gebruikt. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

Je kunt The Machine ook vragen ze toe te voegen, bijvoorbeeld via een to-do: 'voeg dit transcript toe aan de teamvergadering van vandaag'. Een transcript komt bij Transcript te staan en een samenvatting bij Notities. Bij een afspraak met notities of een transcript staat **Notities** of **Transcript** in de agenda.

The Machine leest beide om de vervolgacties van de afspraak te bepalen. Ze zijn Werk of Persoonlijk, net als de afspraak, en worden alleen met je team gedeeld als de afspraak ook met je team wordt gedeeld.

Een afspraak opent met deze details, waar je hem ook vindt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Met **Originele uitnodiging** onderaan bekijk je de uitnodiging zoals die is binnengekomen.

## Een evenement toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook en andere agenda's zijn alleen-lezen. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze optie onder **+** in de bovenbalk): kies de agenda, een titel en een tijd. Klik op een afspraak zonder gasten in die agenda om deze te wijzigen of **Verwijderen** om hem te verwijderen (tik twee keer).

**Waar** stelt tijdens het typen locaties voor: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om ze op te zoeken. Kies een suggestie of houd je eigen tekst aan.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar voor je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat hoeveel mensen je uitnodigt: **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten krijgt niemand een uitnodiging of update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld om een ophaalmoment toe te voegen. Je ziet precies wat er verandert. De wijziging wordt pas doorgevoerd als je op **Toevoegen**, **Opslaan** of **Verwijderen** klikt.

Nog geen afspraken? Zonder agenda opent **Koppel je agenda** Koppelingen, waar je [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md) kunt koppelen.

## Conflicten met je andere agenda

Als een werkafspraak overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de afspraak die later is toegevoegd. The Machine kan een kort bericht opstellen om de afspraak te verzetten, of voorstellen om die af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Afspraken die de hele dag duren, als vrij gemarkeerd zijn of voorlopig zijn, tellen niet mee. Elk conflict wordt maar één keer gemeld. Een Werk-to-do vermeldt alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak botst.

## Klaar voor je afspraken

Voor een afspraak met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de afspraak. Die bevat een korte briefing:

- **Wie:** wie ze zijn volgens je Graph, met informatie over hun achtergrond als die bekend is.
- **Organisatie:** wat hun bedrijf doet dat relevant is voor de afspraak.
- **Tot nu toe:** wat jullie hebben besproken, gevraagd en aangeboden, en wat de stand van zaken is. Na de afspraak zijn die berichten de bronnen van de to-do.
- **Openstaande beloftes:** wat jij of de ander nog moet doen.
- **Openstaande vragen:** wat nog niet is beantwoord.
- **Beslissen of meenemen:** wat je moet beslissen of meenemen, en wat waarschijnlijk belangrijk is voor de ander.

De briefing verschijnt op de ochtend van een werkdag: op de dag van de afspraak als die 's middags plaatsvindt, anders op de voorafgaande werkdag. Je kunt de briefing alleen lezen. Tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag waar iets mee moet gebeuren, krijgt een eigen to-do.

De briefing is gebaseerd op wat al op je Machine staat. Voor een eerste afspraak met iemand bij een bedrijf zoekt The Machine ook kort op het web naar diens naam en bedrijf. Naast de gevonden informatie staat een link. Alleen de openbare naam, bedrijfsnaam en website van die persoon worden voor de zoekopdracht gebruikt, nooit je berichten. Een zoekopdracht wordt 30 dagen hergebruikt. Als **Werkcontacten opzoeken** uitstaat (Instellingen, Beveiliging), wordt er niet gezocht.

Als er geen bruikbare geschiedenis is, wordt er geen to-do aangemaakt. Terugkerende, interne en persoonlijke afspraken, en afspraken die zijn afgewezen, krijgen geen to-do. Als een afspraak wordt verzet, blijft dezelfde to-do behouden, met de nieuwe tijd. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde afspraak wordt automatisch gesloten.

Als een update de inhoud van een briefing verandert, worden open briefings voor afspraken die nog moeten plaatsvinden één keer opnieuw opgesteld. De titel, bronnen en plek in je lijst blijven hetzelfde. Een briefing die je hebt gewijzigd, gesnoozed of gesloten, blijft zoals die is. Dat geldt ook voor een briefing van een afspraak die over een paar minuten begint.

Bij de afspraakdetails vind je de to-do onder **To-do**. Tik erop om de chat te openen.
