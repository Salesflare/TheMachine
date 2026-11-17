---
title: Agenda
area: calendar
summary: De komende week op één plek: vergaderingen, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: c1941aa6ca09b134
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- vergaderingen uit de agenda's die je hebt gekoppeld,
- to-do's met een deadline op die dag en gesnoozede to-do's op de dag dat ze terugkomen,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [reizen en evenementen](calendar.md#trips-and-events) uit boekings- en ticketmails.

Een vergadering die in twee agenda's staat, zie je maar één keer. Een agenda die iemand met je deelt, toont diens afspraken gedimd en met diens voornaam. Die leiden nooit tot een to-do. Afspraken die de hele dag duren en meerdaagse afspraken worden op elke dag weergegeven als afspraken die de hele dag duren. Een reis staat in **Agenda** als eerste op elk van de reisdagen. In **Week** en **Maand** loopt er één balk over de reisdagen, bijvoorbeeld 'Reis naar Lissabon'.

Een plan dat jullie samen hebben gemaakt, is één belofte, met 'Met' en de naam van de ander erbij. Een belofte over een vergadering die dag met dezelfde persoon staat op de rij van die vergadering.

**Te laat** komt bovenaan. Bij een vergadering met een openstaande to-do zie je de status: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die afgerond lijkt, omdat je al hebt gereageerd of omdat de uitvoering ervan laat zien dat hij klaar is, wordt niet weergegeven als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen of omhoog, of kies **Eerdere dagen tonen**, voor eerdere dagen. Je kunt terug tot een week voordat je je agenda koppelde. Bovenaan staat vanaf welke dag de agenda begint. Zodra je [geschiedenis](history.md) is ingeladen, kun je ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op je telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op je telefoon zie je stippen. Tik op een dag om de afspraken van die dag te bekijken.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De weergave die je kiest, wordt op dat apparaat onthouden.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat ze leesbaar blijven. De overige afspraken verschijnen als **+N**. Daarmee open je die dag in de agendaweergave.

## Iets openen

Klik op een rij om de chat van de to-do, de belofte, de reis of het evenement, of de vergadering te openen. Bij een vergadering die je hier niet kunt wijzigen, zoals een vergadering van iemand anders of een vergadering met gasten, zie je de details: wanneer, waar en wie. Mensen die Graph kent, en de organisaties en projecten waaraan de vergadering is gekoppeld, linken naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) eronder open je de vergadering daar. Alleen bekijken brengt niets in beweging.

Een vergaderruimte die voor een vergadering is geboekt, staat bij de locatie. Je ziet die niet als persoon en ook niet in Graph.

Een link naar een vergadering wordt weergegeven met de naam van de dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de vergadering om deel te nemen.

## Reizen en evenementen

Als een boeking voor een vlucht, hotel, vakantiehuis, trein, bus, veerboot, huurauto, taxi of luchthavenparking in je mail binnenkomt, voegt je Machine die toe aan een reis. Boekingen voor één reis komen samen op één reis, uit al je mailboxen: de trein naar de luchthaven, de vluchten, de auto, het verblijf en de terugreis. Boekingen worden samengevoegd als hun data elkaar overlappen of als de ene eindigt waar de andere begint.

De reis verschijnt als één balk over de reisdagen. Open de reis om alle boekingen op tijdsvolgorde te zien, met de tijden, het adres, de boekingscode en de stoel.

Tickets voor een concert, wedstrijd, festival of conferentie maken één evenement per evenement aan, met de locatie, boekingscode, stoel en het aantal tickets. Een tweede bestelling voor hetzelfde evenement wordt aan hetzelfde evenement toegevoegd. Een evenement dat via je werkmailbox is geboekt, is Werk. Anders is het Persoonlijk. Tickets voor iets dat tijdens een reis plaatsvindt, worden aan de reis toegevoegd.

Voor een reis die nog moet plaatsvinden, laat je Machine zien wat er ontbreekt, zoals **Geen verblijf geboekt voor 2 nachten**, of dat er niets is geboekt van de luchthaven naar je hotel. Die regels zijn gedimd en hebben het label **Geen boeking**. Bij een reis zonder verblijf zie je geen informatie over overnachtingen.

- Op elke regel staat van wie de boeking komt, bijvoorbeeld **Van Example Tickets**. Klik erop om de mail te openen.
- Is er een to-do gemaakt op basis van de mail, bijvoorbeeld om voor de tickets te betalen, dan toont **De to-do openen** die to-do.
- Een gewijzigde boeking werkt de bijbehorende regel bij. Een geannuleerde boeking verdwijnt. Als alle boekingen zijn geannuleerd, verdwijnt ook de reis of het evenement.
- Een boeking voor iemand anders, zoals een vlucht van een collega die naar je is doorgestuurd, komt niet bij je reizen te staan.

In de meeste bevestigingen staan de details in een vorm die je Machine zonder AI kan lezen. Voor een bevestiging waarbij dat niet lukt, zoals een doorgestuurde mail of een boeking bij een kleine boekingssite, leest je [model](model.md) de mail op de achtergrond. Dat gebeurt met een paar mails tegelijk en wordt uitgesteld als je bijna aan je gebruikslimiet zit. Boekingsmails uit het jaar aan [geschiedenis](history.md) dat je Machine bijhoudt, worden op de achtergrond gelezen zodra die geschiedenis is ingeladen.

## Notities en transcript van een vergadering

De details van een vergadering bestaan uit twee delen. **Notities** is de samenvatting, met beslissingen en actiepunten. **Transcript** is wat er woord voor woord is gezegd. Het transcript is standaard ingeklapt en toont hoe lang het duurt. Met **Tonen** open je het.

Als ze niet laden, probeert de app het ongeveer een halve minuut lang vanzelf opnieuw. Tik daarna op **Opnieuw proberen**.

Voor elk onderdeel zijn er aparte knoppen: **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je bij het ene onderdeel toevoegt, blijft daar staan. Bij een vergadering die je kunt wijzigen, open je de notities met **Notities** onder het formulier.

Als je [Zoom](zoom.md), [Google Meet](google-meet.md) of [Granola](granola.md) hebt gekoppeld, verschijnen de notities bij Notities en het transcript bij Transcript, met het label **Van Zoom**, **Van Google Meet** of **Van Granola**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, zie je ze allebei.

Notities kunnen ook in de agenda-afspraak zelf staan, nadat de vergadering is begonnen zijn toegevoegd, of per mail van Zoom of Gemini komen. Na afloop van de vergadering maakt The Machine er alleen to-do's van als er duidelijke vervolgstappen in staan. Als dezelfde notities op twee manieren binnenkomen, ontstaat er één to-do, met de vergadering als bron: 'Bron: notities van' de vergadering.

Bij een vergadering met een transcript maar zonder notities staat **Notities maken**. The Machine maakt notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met de verantwoordelijke personen, in de taal van de vergadering.

Je ziet **Notities schrijven…**. De app gaat door als je de vergadering sluit. Bij een lange vergadering duurt dit een paar minuten en wordt je eigen model gebruikt. De notities krijgen het label **Geschreven door The Machine** en vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan de notities ook toevoegen. Vraag dat in een to-do, bijvoorbeeld: 'voeg dit transcript toe aan de vergadering van vandaag over het bord'. Een transcript komt bij Transcript te staan en een samenvatting bij Notities. Bij een vergadering met notities of een transcript zie je in de agenda **Notities** of **Transcript**.

The Machine gebruikt beide voor de vervolgacties van de vergadering. Die zijn Werk of Persoonlijk, net als de vergadering, en worden alleen met je team gedeeld als de vergadering ook met je team wordt gedeeld.

Je kunt een vergadering met deze details openen vanaf elke plek waar je die vindt: op een tijdlijn, in een berichtzoekopdracht of als bron van een to-do. Met **Originele uitnodiging** onderaan zie je de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook en andere agenda's zijn alleen-lezen. Met **Nieuwe afspraak** voeg je een afspraak toe. Op je telefoon vind je die onder **+** in de bovenbalk. Kies de agenda, een titel en het tijdstip. Klik op een afspraak zonder gasten in die agenda om die te wijzigen of **Verwijderen** om die te verwijderen (tik twee keer).

**Waar** stelt locaties voor terwijl je typt: eerst eerder gebruikte locaties en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om ze op te zoeken. Kies een locatie of behoud je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat hoeveel mensen je uitnodigt, bijvoorbeeld **Toevoegen en 2 uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten krijgt niemand een uitnodiging of update.

Een to-do kan ook een wijziging voorstellen, zoals een ophaalafspraak toevoegen. Je ziet precies wat er verandert. Alleen met **Toevoegen**, **Opslaan** of **Verwijderen** voer je de wijziging door.

Nog geen vergaderingen? Als je geen agenda hebt, opent **Koppel je agenda** de Koppelingen. Koppel [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Overlap met je andere agenda

Als een werkvergadering overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de nieuwste van de twee afspraken. The Machine kan een kort conceptbericht maken om de afspraak te verzetten, of voorstellen om die af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Afspraken die de hele dag duren, vrije afspraken en voorlopige afspraken tellen niet mee. Elke overlap komt maar één keer voor. Een Werk-to-do vermeldt alleen dat er een conflict is. Zo ziet je team de persoonlijke afspraak nooit. Alleen jij ziet waarmee die afspraak overlapt.

## Klaargezet voor je vergaderingen

Voor een vergadering met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de vergadering. Het is een korte briefing:

- **Wie:** wie ze zijn, volgens je Graph.
- **Laatste contact:** je laatste uitwisseling met hen. Dat bericht is na de vergadering de bron van de to-do.
- **Openstaande beloftes:** wat jij of zij nog moeten doen.
- **Open vragen:** wat nog onbeantwoord is.
- **Beslissen of meenemen:** wat je nog moet afspreken of meenemen.

De to-do verschijnt op de ochtend van een werkdag: op de dag van de vergadering als die 's middags plaatsvindt, anders op de werkdag ervoor. De briefing gebruikt alleen informatie die al op je Machine staat. Je kunt er alleen informatie in lezen. Markeer de to-do als **Gedaan** zodra je die hebt gelezen. Een belofte of vraag waar actie voor nodig is, krijgt een eigen to-do.

Zonder bruikbare geschiedenis verschijnt er geen to-do. Terugkerende, interne en persoonlijke vergaderingen, en vergaderingen die zijn geweigerd, krijgen er geen. Als een vergadering wordt verzet, blijft de to-do behouden en verschijnt die op het nieuwe tijdstip. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde vergadering wordt vanzelf gesloten.

De details van de vergadering tonen de to-do onder **To-do**, één tik verwijderd van de chat.
