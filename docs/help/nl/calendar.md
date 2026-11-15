---
title: Agenda
area: calendar
summary: De komende week op één plek: afspraken, to-do's met een deadline, gesnoozede to-do's en beloftes.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: d85b3eff63ea503d
---
## Wat je ziet

Je dagen vanaf vandaag, met:

- afspraken uit de agenda's die je hebt gekoppeld,
- to-do's met die dag als deadline en to-do's die die dag terugkomen nadat ze zijn gesnoozed,
- check-ins over werk dat je hebt overgedragen,
- beloftes met een datum,
- [notities](notes.md) met datums, zoals een reis.

Een afspraak die in twee agenda's staat, wordt maar één keer getoond. Een agenda die iemand met je heeft gedeeld, toont diens afspraken gedimd, met de voornaam van die persoon. Die afspraken leiden nooit tot een to-do. Afspraken die de hele dag duren of meerdere dagen beslaan, worden elke dag waarop ze plaatsvinden als dagvullend getoond. Een reis staat in Agenda op elk van de dagen bovenaan en wordt in Week en Maand als één balk over die dagen getoond, bijvoorbeeld ‘Reis naar Lissabon’.

Een plan dat jullie samen hebben gemaakt, is één belofte, met ‘Met’ en de naam van de ander erbij. Een belofte over een afspraak met die persoon op die dag staat op de rij van die afspraak.

**Te laat** staat bovenaan. Bij een afspraak met een openstaande to-do zie je die to-do: **Voorbereiding klaar**, **Wordt voorbereid** of **To-do**. Een to-do die afgerond lijkt (je hebt al geantwoord of de uitvoering heeft vastgesteld dat hij klaar is), wordt niet getoond als **Deadline**.

## Agenda, week of maand

- **Agenda** toont elke dag apart. Scroll omlaag voor latere dagen of omhoog (of kies **Eerdere dagen tonen**) voor eerdere dagen. De agenda gaat terug tot een week voordat je je agenda koppelde. Bovenaan staat vanaf welke dag. Zodra de [geschiedenis](history.md) is ingeladen, gaat de agenda ongeveer een jaar terug.
- **Week** toont een raster van maandag tot en met zondag. Op een telefoon zie je drie dagen.
- **Maand** toont de hele maand. Op een computer zie je maximaal drie items per dag. Op een telefoon zie je stippen. Tik erop om de items van die dag te bekijken.

Met **Vandaag**, ‹ en › bovenaan blader je door de weken of maanden. De weergave die je kiest, wordt onthouden op dat apparaat.

In het weekraster staan afspraken die op hetzelfde moment plaatsvinden naast elkaar, zodat ze leesbaar blijven. De overige afspraken worden weergegeven als **+N**. Tik daarop om die dag in de agenda te openen.

## Iets openen

Klik op een rij om de chat van de to-do, de belofte, de notitie of de afspraak te openen. Bij een afspraak die je hier niet kunt wijzigen, bijvoorbeeld die van iemand anders of een afspraak met gasten, zie je de details: wanneer, waar en wie. Iemand die je Graph kent en de organisaties en projecten waarvoor de afspraak is, linken naar hun pagina. Met **Openen in Google Calendar** (of **Openen in Outlook**) open je de afspraak daar. Alleen bekijken verandert niets.

Een vergaderruimte die bij een afspraak is geboekt, staat bij de locatie. Die wordt nooit als persoon of in je Graph weergegeven.

Een vergaderlink wordt getoond als de bijbehorende dienst, zoals Zoom, Google Meet of Teams, of als **Videogesprek**. Open de afspraak om deel te nemen.

## Notities en transcript van een afspraak

De details van een afspraak bestaan uit twee delen. **Notities** is de samenvatting: beslissingen en actiepunten. **Transcript** is een woordelijke weergave van wat er is gezegd. Het transcript is eerst ingeklapt en toont hoe lang het is. Met **Tonen** open je het.

Als ze niet worden geladen, probeert The Machine het ongeveer een halve minuut automatisch opnieuw. Tik daarna op **Opnieuw proberen**.

Elk onderdeel heeft een eigen optie **Notities toevoegen** of **Transcript toevoegen**, **Bestand uploaden** voor een Markdown- of tekstbestand, **Bewerken** en **Verwijderen** (tik twee keer). Wat je aan het ene onderdeel toevoegt, blijft daar staan. Bij een afspraak die je kunt wijzigen, open je de notities via **Notities** onder het formulier.

Als [Zoom](zoom.md) of [Google Meet](google-meet.md) is gekoppeld, verschijnen de notities onder Notities en het transcript onder Transcript, met de aanduiding **Van Zoom** of **Van Google Meet**. Ze vervangen nooit wat je zelf hebt toegevoegd. Als beide aanwezig zijn, worden ze allebei getoond.

Notities kunnen ook afkomstig zijn uit het agenda-item zelf, als ze zijn toegevoegd nadat de afspraak begon, of uit een e-mail van Zoom of Gemini. Na afloop van de afspraak maakt The Machine daar alleen to-do's van als er duidelijke vervolgstappen zijn. Als dezelfde notities op twee manieren binnenkomen, wordt er één to-do van gemaakt, met de afspraak als bron: ‘Bron: notities van’ de afspraak.

Bij een afspraak met een transcript maar zonder notities staat **Notities maken**. The Machine maakt dan notities op basis van het transcript: een korte samenvatting, beslissingen en actiepunten met de verantwoordelijke persoon, in de taal van de afspraak.

The Machine toont **Notities schrijven…** en gaat door als je de afspraak sluit. Een lange afspraak kan een paar minuten duren. Hiervoor wordt je eigen model gebruikt. Bij de notities staat **Geschreven door The Machine**. Ze vervangen nooit notities die je zelf hebt toegevoegd.

The Machine kan ook notities toevoegen. Vraag dat in een chat over een to-do, bijvoorbeeld: ‘voeg dit transcript toe aan de teamvergadering van vandaag’. Een transcript komt onder Transcript te staan en een samenvatting onder Notities. Bij een afspraak met notities of een transcript staat in de Agenda **Notities** of **Transcript**.

The Machine leest beide om de vervolgacties van de afspraak te bepalen. Die zijn Werk of Persoonlijk, net als de afspraak, en komen alleen bij je team terecht als de afspraak ook voor je team is.

Je kunt de details van een afspraak overal openen waar je die tegenkomt: op een tijdlijn, in een zoekresultaat voor berichten of als bron van een to-do. Onderaan toont **Originele uitnodiging** de uitnodiging zoals die is binnengekomen.

## Een afspraak toevoegen of wijzigen

Je eigen Google-agenda kun je hier wijzigen. Outlook en andere agenda's kun je alleen bekijken. Met **Nieuwe afspraak** voeg je een afspraak toe (op een telefoon vind je deze onder **+** in de bovenbalk): kies de agenda, een titel en een tijdstip. Klik op een afspraak zonder gasten in die agenda om deze te wijzigen of te **Verwijderen** (tik twee keer).

**Waar** stelt locaties voor terwijl je typt: eerst locaties die je eerder hebt gebruikt en je organisaties, daarna adressen van [OpenStreetMap](https://www.openstreetmap.org), een gratis kaart. Alleen de woorden die je typt, worden verstuurd om locaties op te zoeken. Kies een suggestie of gebruik je eigen tekst.

Met **Uitnodigen** voeg je mensen uit je Graph of een e-mailadres toe. Deze optie is alleen beschikbaar in je eigen agenda. Boven de knop zie je wie een uitnodiging krijgt. Op de knop staat hoeveel mensen dat zijn: **Toevoegen en 2 personen uitnodigen**. Google verstuurt de uitnodigingen pas als je erop tikt. Zonder gasten wordt niemand uitgenodigd en krijgt niemand een update.

Een to-do kan ook een wijziging voorstellen, bijvoorbeeld om een ophaalmoment toe te voegen. Je ziet precies wat er verandert. Alleen als je op **Toevoegen**, **Opslaan** of **Verwijderen** tikt, wordt de wijziging doorgevoerd.

Nog geen afspraken? Als je geen agenda hebt gekoppeld, opent **Koppel je agenda** Koppelingen. Koppel daar [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) of [een andere agenda](other-calendars.md).

## Conflicten met je andere agenda

Als een werkafspraak overlapt met iets in je persoonlijke agenda, of andersom, maakt The Machine één to-do over de afspraak die het laatst is toegevoegd. The Machine kan een kort bericht opstellen om de afspraak te verzetten of voorstellen om deze af te zeggen. Er wordt niets verstuurd voordat je het goedkeurt.

Afspraken die de hele dag duren, als vrij staan of voorlopig zijn, tellen niet mee. Elk conflict komt maar één keer aan bod. Bij een Werk-to-do staat alleen dat er een conflict is, zodat je team de persoonlijke afspraak nooit ziet. Alleen jij ziet waarmee de afspraak botst.

## Klaargezet voor je afspraken

Voor een afspraak met mensen van buiten je bedrijf maakt The Machine één to-do: **Voorbereiden op** de afspraak. Dit is een korte briefing:

- **Wie:** wie ze zijn, volgens je Graph.
- **Laatste contact:** je laatste uitwisseling met hen. Na de afspraak is dat bericht de bron van de to-do.
- **Openstaande beloftes:** wat jij of zij nog moeten doen.
- **Open vragen:** wat nog geen antwoord heeft.
- **Beslissen of meenemen:** wat je moet afspreken of meenemen.

De to-do verschijnt op de ochtend van een werkdag: op de dag van de afspraak als die 's middags plaatsvindt, anders op de werkdag ervoor. The Machine gebruikt alleen informatie die al op je Machine staat. De to-do is alleen bedoeld om te lezen. Tik op **Gedaan** als je hem hebt gelezen. Een belofte of vraag erin die actie vereist, heeft een eigen to-do.

Zonder bruikbare geschiedenis wordt er geen to-do gemaakt. Terugkerende, interne en persoonlijke afspraken en afspraken die zijn afgewezen, krijgen geen to-do. Als een afspraak wordt verzet, blijft de bijbehorende to-do bestaan op het nieuwe tijdstip. Een afgewezen to-do komt niet terug. De to-do van een geannuleerde afspraak wordt automatisch gesloten.

In de details van de afspraak staat de to-do onder **To-do**. Tik erop om de chat te openen.
