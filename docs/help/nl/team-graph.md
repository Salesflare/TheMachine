---
title: Graph voor teams
area: fleet
summary: Experimenteel. Deel klantwerk met je Work Fleet, zoals in een CRM. Wat er wordt gedeeld, wat nooit wordt gedeeld en hoe je iets privé houdt.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
In een Work Fleet kan je Machine klantwerk delen met de Machines van je teamgenoten, zoals in een gedeeld CRM. Dit is **Experimenteel** en staat standaard uit.

## Inschakelen

Een beheerder schakelt **De Graph delen in deze Fleet** in bij **Wat gedeeld wordt** en bevestigt dat het bedrijf deze e-mail mag delen en dit aan de medewerkers heeft laten weten. Iedereen kan zien of delen aanstaat.

Als de werkmail of werkagenda van iedereen verplicht wordt gesteld, wordt delen ook ingeschakeld. Daarna kiest iedereen bij **Je koppelingen** wat er nog meer wordt gedeeld. Het eerste deelmoment van een nieuwe teamgenoot vindt pas na een uur plaats, zodat die eerst iets privé kan houden.

## Je koppelingen

Bij **Wat gedeeld wordt** staat onder **Je koppelingen** elke koppeling met een schakelaar. Werkgerelateerde koppelingen op het domein van je Fleet staan standaard aan. Koppelingen op het domein van een ander bedrijf staan uit en hebben de melding 'Ander bedrijf, niet gedeeld'. Persoonlijke koppelingen worden nooit gedeeld. Als je een koppeling uitzet, wordt ingetrokken wat ermee gedeeld is.

Een agenda van iemand anders die je via je eigen account bekijkt, staat onder de eigen naam als persoonlijk.

Ook binnen een ingeschakelde koppeling worden gesprekken nog steeds afzonderlijk beoordeeld. De Slack van je eigen bedrijf telt alleen als communicatie met collega's. Alleen een Slack Connect-chat met een ander bedrijf kan klantwerk zijn. Persoonlijke gesprekken, gesprekken met alleen collega's, gevoelige gesprekken en geautomatiseerde gesprekken worden niet gedeeld, tenzij je er zelf een deelt.

## Vereist door de Fleet

Een beheerder kan bij **Vereist door de Fleet** de **Werkmail** en **Werkagenda** van iedereen op het domein van de Fleet verplicht stellen, nadat die heeft bevestigd dat het bedrijf dit aan de medewerkers heeft laten weten. Werkmail is eigendom van het bedrijf, net als in elk CRM. Bij verplichte koppelingen staat 'Vereist door' met de naam van je Fleet. Je kunt ze niet uitzetten. Gesprekken die je privé houdt, blijven privé.

## Wat met het team wordt gedeeld

- Gesprekken met klanten: werkmail met mensen buiten je bedrijf, inclusief bijlagen.
- Werkgerelateerde personen, organisaties en projecten, met een korte tijdlijn. Op de **Tijdlijn** van een pagina toont **Team** elke gebeurtenis één keer. Als de Machine van een teamgenoot de gebeurtenis in diens taal heeft vastgelegd, zie je die taal, samen met iedereen van wie de gebeurtenis afkomstig is: 'via Sam, Kim en Lee'.
- Een kleine kopie van het logo van een organisatie en de werkfoto van iemand. Deze komen uit een zoekresultaat, Slack, LinkedIn, X, Salesflare of Microsoft. Nooit uit Google Contacten, WhatsApp, Telegram of Facebook, en ook geen foto die je hebt gewijzigd of verwijderd.
- Op een Team-bord: vergaderingen van een project, Zoom-notities, Intercom-gesprekken en chats. Gevoelige gesprekken, zoals over deals, en chats met alleen collega's worden niet gedeeld.
- Aantallen en datums voor de [teambrief](fleet.md#brief-requests) van een teamgenoot.
- Antwoorden wanneer een teamgenoot vraagt wie iemand kent of context over een vergadering wil. Zie [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Team-inzichten](fleet.md#team-learnings): hoe het team werkt, zonder namen of klantgegevens.

## Wordt niet automatisch gedeeld

- Gevoelige gesprekken: over het kopen of verkopen van een bedrijf, investeringen, dealonderhandelingen, HR en werving, juridische zaken, gezondheid, geld en beveiliging. Zelfs het bestaan ervan wordt niet gedeeld.
- Geautomatiseerde e-mail: betalingsbewijzen, facturen, meldingen, nieuwsbrieven en facturen van leveranciers.
- Gesprekken met alleen collega's, persoonlijke e-mail en alles van een persoonlijk account. Persoonlijke gegevens worden nooit gedeeld, ook niet als je op Team tikt.
- Alles wat je **Privé houden** hebt gemarkeerd, en borden en projecten die op Alleen jij staan.
- Iemand die voor jou Persoonlijk is, zoals je Familie of Vrienden, en diens e-mail. Een project waar die persoon aan werkt, wordt wel met het bord gedeeld, maar zonder die persoon.

Elk gesprek wordt beoordeeld op het onderwerp. Dat kan verkeerd gaan. Controleer wat er wordt gedeeld en gebruik Privé houden om dit aan te passen. Als je zelf een gesprek deelt met het team of met specifieke mensen, gaat dat vóór een gevoeligheidslabel. Controleer dus met wie je het deelt.

## Een bord delen met gekozen mensen

Tik in het menu **⋯** van een bord op **Bord delen…** en kies teamgenoten. Alleen zij krijgen de projecten op het bord, met volledige tijdlijnen: e-mail, vergaderingen en Zoom-notities, Intercom-gesprekken, chats, to-do's en wijzigingen. Ook gevoelige projecten, zoals deals, worden gedeeld.

Persoonlijke gesprekken en gesprekken met alleen collega's worden niet gedeeld. Dat geldt ook voor je Familie en Vrienden, geautomatiseerde e-mail en koppelingen die je niet hebt geselecteerd.

- Een project dat later aan het bord wordt toegevoegd, wordt ook gedeeld. Een project dat van het bord wordt gehaald, wordt weer ingetrokken.
- Verwijder iemand of kies niemand, en de gedeelde gegevens worden weer van diens Machine verwijderd.
- Tik op het label van een gesprek en daarna op **Delen met…** om één gesprek met specifieke mensen te delen. Dit kan gevoelige of geautomatiseerde werkmail bevatten, maar nooit persoonlijke gesprekken of gesprekken met alleen collega's.

## Twijfel? Dan wacht het

Als je Machine het niet zeker weet, deelt hij niets. Die gesprekken wachten onder **Deze delen?**, gegroepeerd op soort, bijvoorbeeld 'Contacten met partners en advertenties'. Bij elke groep staat een suggestie:

- **Delen met team**: iedereen in de Fleet.
- **Delen met…**: alleen de teamgenoten die je kiest, bijvoorbeeld een bestuurslid voor gesprekken over investeerders.
- **Privé houden**: het blijft alleen voor jou zichtbaar.

Met één tik kies je voor een hele groep. Open een groep om gesprekken uit te vinken die je afzonderlijk wilt beoordelen.

Gesprekken over het kopen, verkopen of financieren van een bedrijf, en bestuurszaken, zijn gevoelig en wachten hier dus niet. Gewoon werk met een partnerbedrijf geldt als klantwerk.

## Voor het eerst delen

Je eerste deelmoment vindt automatisch plaats een uur nadat je Machine je hierover informeert. Open in dat uur **Fleet** en daarna **Wat gedeeld wordt** om per organisatie te zien welke gesprekken met klanten worden gedeeld. Tik bij een gesprek op **Privé houden**, of tik op **Nu delen** om het meteen te delen. Beheerders zien wie nog niets heeft gedeeld.

## Wat gedeeld wordt

Bij **Fleet** › **Wat gedeeld wordt** zie je alles: aantallen per soort, elk gedeeld gesprek en waarom het is gedeeld, de gesprekken onder **Deze delen?** en wat je privé houdt. Tik op een onderwerp om het te lezen. Je vindt hier ook links vanuit **Instellingen** en het label van elk gesprek.

Een nieuw gesprek met een klant wacht een uur voordat het wordt gedeeld, zodat je tijd hebt om van gedachten te veranderen.

## Delen ongedaan maken

Tik op het label **Team** van een gesprek en daarna op **Niet meer delen**. De Machine van elke teamgenoot verwijdert het gesprek, de bijlagen en de regels in de tijdlijn. Als de Machine offline is, gebeurt dit zodra hij weer online is. Iemand kan het gesprek al gelezen hebben.

Met **Privé houden** bij een persoon, organisatie of project maak je het delen van alle bijbehorende gegevens ongedaan.

Houd twee gesprekken met hetzelfde bedrijf privé en je Machine vraagt één keer of je dat bedrijf voortaan altijd privé wilt houden.

## Wie kan het zien

Alleen de Machines van je teamgenoten. De gegevens zijn end-to-end versleuteld. The Machine Network geeft ze door, maar kan ze niet lezen.

## Deelnemers en nieuwe apparaten

Een beheerder laat elke persoon één keer toe. Het verzoek verschijnt bij **To-do's** van alle beheerders. Het eerste antwoord telt. Daarna is voor delen geen toestemming meer nodig.

Tot die tijd laten de Graph en Fleet van de nieuwe persoon zien op welke beheerders die wacht. **Van mij** en **Team** verschijnen enkele seconden na de toestemming, zonder dat je de pagina opnieuw hoeft te laden.

Een nieuwe Machine van iemand die al is toegelaten, krijgt na 24 uur de Graph van het team. In de tussentijd kunnen beheerders op **Niet van hen** tikken om de Graph buiten die Machine te houden.

## Als iemand vertrekt

Vanaf dat moment krijgt die persoon niets nieuws meer. Wat die persoon heeft gedeeld, blijft bij het team. Een beheerder kan iemand ook **Eruit halen** en die persoon later **Opnieuw delen**.

## Delen voor iedereen uitzetten

Een beheerder schakelt **De Graph delen in deze Fleet** uit bij **Wat gedeeld wordt**. Er wordt dan niets nieuws meer gedeeld.

Met **Uitzetten** behouden teamgenoten wat ze al hebben. Met **Uitzetten en gedeelde gegevens verwijderen** verwijdert elke Machine de gedeelde gegevens. Als delen later weer wordt ingeschakeld, bekijkt iedereen de gegevens eerst opnieuw.

## Je eigen werk niet meer delen

Zet je koppelingen uit bij **Je koppelingen**, tenzij de Fleet ze verplicht stelt. Wat ermee gedeeld is, wordt weer ingetrokken.

Zie ook [Fleets](fleet.md) en [Beveiliging en privacy](security-and-privacy.md).
