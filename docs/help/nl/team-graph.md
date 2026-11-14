---
title: Team Graph
area: fleet
summary: Experimenteel. Deel klantwerk met je Work Fleet, zoals in een CRM. Wat wordt gedeeld, wat nooit en hoe je iets privé houdt.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
In een Work Fleet kan je Machine klantwerk delen met de Machines van je teamgenoten, zoals in een gedeeld CRM. Dit is **Experimenteel** en staat standaard uit.

## Inschakelen

Een beheerder schakelt **De Graph delen in deze Fleet** in bij **Wat gedeeld wordt** en bevestigt dat het bedrijf deze mail mag delen en de medewerkers hierover heeft geïnformeerd. Iedereen kan zien of delen aanstaat.

Als je verplicht stelt dat iedereen zijn werkmail of agenda deelt, wordt delen ook ingeschakeld. Daarna kiest iedereen bij **Je koppelingen** wat er nog meer wordt gedeeld. De eerste keer dat een nieuwe teamgenoot iets deelt, gebeurt dat pas na een uur. Zo kan diegene het eerst privé houden.

## Je koppelingen

Bij **Wat gedeeld wordt** toont **Je koppelingen** elke koppeling met een schakelaar. Werkaccounts op het domein van je Fleet staan standaard aan. Accounts op het domein van een ander bedrijf staan standaard uit en hebben de melding ‘Ander bedrijf, niet gedeeld’. Persoonlijke accounts worden nooit gedeeld. Als je een koppeling uitzet, wordt wat die heeft gedeeld weer ingetrokken.

Een agenda van iemand anders die je via je eigen account bekijkt, wordt onder de eigen naam als persoonlijk weergegeven.

Ook binnen een ingeschakelde koppeling worden gesprekken afzonderlijk beoordeeld. De Slack van je eigen bedrijf telt alleen als communicatie met collega's. Alleen een Slack Connect-chat met een ander bedrijf kan klantwerk zijn. Persoonlijke gesprekken, gesprekken met alleen collega's, gevoelige gesprekken en geautomatiseerde gesprekken worden niet gedeeld, tenzij je er zelf een deelt.

## Vereist door de Fleet

Een beheerder kan bij **Vereist door de Fleet** instellen dat iedereen zijn **Werkmail** en **Werkagenda** op het domein van de Fleet deelt, nadat die heeft bevestigd dat het bedrijf de medewerkers hierover heeft geïnformeerd. Werkmail is eigendom van het bedrijf, net als in elk CRM. Bij verplichte koppelingen staat ‘Vereist door’ met de naam van je Fleet. Je kunt ze niet uitzetten. Gesprekken die je privé houdt, blijven privé.

## Wat het team te zien krijgt

- Gesprekken met klanten: werkmail met mensen buiten je bedrijf, inclusief bijlagen.
- Werkcontacten, organisaties en projecten, met een korte tijdlijn. Op de **Tijdlijn** van een pagina toont **Team** elke gebeurtenis één keer, in jouw taal als de Machine van een teamgenoot die zo heeft opgesteld, en met iedereen van wie de gebeurtenis afkomstig is: ‘via Sam, Kim en Lee’.
- Een kleine kopie van het logo van een organisatie en de werkfoto van iemand. Die kan afkomstig zijn uit een zoekopdracht, Slack, LinkedIn, X, Salesflare of Microsoft. Nooit uit Google-contacten, WhatsApp, Telegram of een Facebook-foto, en ook nooit een foto die je hebt aangepast of verwijderd.
- Op een Teambord: de vergaderingen, Zoom-notities, Intercom-gesprekken en chats van een project. Gevoelige gesprekken, zoals deals, en chats met alleen collega's worden niet gedeeld.
- Aantallen en datums uit de [teambrief](fleet.md#brief-requests) van een teamgenoot.
- Antwoorden op vragen van een teamgenoot over wie iemand kent of voor context bij een vergadering. Zie [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Teaminzichten](fleet.md#team-learnings): hoe het team werkt, zonder namen of klantgegevens.

## Wordt niet automatisch gedeeld

- Gevoelige gesprekken: over het kopen of verkopen van een bedrijf, investeringen, onderhandelingen over deals, HR en werving, juridische zaken, gezondheid, geld en beveiliging. Zelfs niet dat ze bestaan.
- Geautomatiseerde mail: ontvangstbewijzen, facturen, meldingen, nieuwsbrieven en leveranciersfacturen.
- Gesprekken met alleen collega's, persoonlijke mail en alles van een persoonlijk account. Persoonlijke gegevens worden nooit gedeeld, ook niet als je op Team tikt.
- Alles wat je hebt gemarkeerd met **Privé houden**, en borden en projecten die zijn ingesteld op ‘Alleen jij’.
- Iemand die voor jou persoonlijk is, zoals je familie of vrienden, en hun mail. Een project waar diegene aan werkt, wordt wel met het bord gedeeld, maar zonder die persoon.

Elk gesprek wordt beoordeeld op basis van de inhoud. Dat kan misgaan. Controleer wat er gedeeld zou worden en gebruik **Privé houden** om dit aan te passen. Als je zelf een gesprek deelt met het team of met specifieke personen, wordt een gevoelig label genegeerd. Controleer dus wie het te zien krijgt.

## Een bord delen met specifieke mensen

Tik in het menu **⋯** van een bord op **Bord delen…** en kies teamgenoten. Alleen zij krijgen de projecten op het bord, met de volledige tijdlijn: mail, vergaderingen en Zoom-notities, Intercom-gesprekken, chats, to-do's en wijzigingen. Ook gevoelige gesprekken, zoals deals, worden gedeeld.

Persoonlijke gesprekken en gesprekken met alleen collega's worden niet gedeeld. Hetzelfde geldt voor je familie en vrienden, geautomatiseerde mail en koppelingen die je niet hebt geselecteerd.

- Een project dat later aan het bord wordt toegevoegd, wordt ook gedeeld. Wordt het van het bord verwijderd, dan wordt de toegang ingetrokken.
- Als je iemand verwijdert of niemand selecteert, wordt het project verwijderd van de Machine van die persoon.
- Wil je één gesprek delen met specifieke mensen? Tik op het label en daarna op **Delen met…**. Dit kan ook gevoelige of geautomatiseerde werkmail zijn, maar nooit persoonlijke gesprekken of gesprekken met alleen collega's.

## Twijfel? Dan wacht het

Als je Machine twijfelt, deelt hij niets. Die gesprekken verschijnen bij **Deze delen?**, gegroepeerd op soort, bijvoorbeeld ‘Uitwisselingen met partners en over plaatsingen’. Bij elke groep staat een suggestie:

- **Delen met team**: iedereen in de Fleet.
- **Delen met…**: alleen de teamgenoten die je kiest, bijvoorbeeld een bestuurslid voor gesprekken met investeerders.
- **Privé houden**: het blijft alleen voor jou zichtbaar.

Met één tik beslis je voor een hele groep. Open een groep om gesprekken uit te vinken waarover je afzonderlijk wilt beslissen.

Gesprekken over het kopen, verkopen of financieren van een bedrijf en bestuurszaken zijn gevoelig. Ze verschijnen daarom niet hier. Gewoon werk met een partnerbedrijf geldt als klantwerk.

## Voordat je voor het eerst deelt

Een uur nadat je Machine je dit heeft laten weten, deelt hij automatisch je eerste gegevens. Open in dat uur **Fleet** en daarna **Wat gedeeld wordt** om per organisatie te zien welke klantgesprekken worden gedeeld. Tik bij gesprekken die je niet wilt delen op **Privé houden**, of tik op **Nu delen** om meteen te delen. Beheerders kunnen zien wie nog niets heeft gedeeld.

## Wat gedeeld wordt

Bij **Fleet** › **Wat gedeeld wordt** zie je alles: aantallen per soort, elk gedeeld gesprek met de reden waarom het is gedeeld, de gesprekken onder **Deze delen?** en wat je privé houdt. Tik op een onderwerp om het te lezen. Je vindt hier ook **Instellingen** en de labels van afzonderlijke gesprekken.

Nieuwe gesprekken met klanten worden pas na een uur gedeeld. Zo heb je tijd om van gedachten te veranderen.

## Delen ongedaan maken

Tik op het label **Team** van een gesprek en daarna op **Niet meer delen**. De Machine van elke teamgenoot verwijdert het gesprek, de bijlagen en de regels op de tijdlijn. Is een Machine offline, dan gebeurt dit zodra hij weer online is. Iemand kan het gesprek al gelezen hebben.

Als je bij een persoon, organisatie of project op **Privé houden** tikt, wordt alles daarvan niet meer gedeeld.

Houd twee gesprekken met hetzelfde bedrijf privé en je Machine vraagt één keer of je dat bedrijf voortaan altijd privé wilt houden.

## Wie kan het zien?

Alleen de Machines van je teamgenoten. De gegevens zijn end-to-end versleuteld. The Machine Network geeft ze door, maar kan ze niet lezen.

## Lid worden en nieuwe apparaten

Een beheerder geeft iedereen één keer toegang. Het verzoek staat bij **To-do's** van alle beheerders. Het eerste antwoord telt. Daarna zijn geen nieuwe toestemmingen nodig om te delen.

Tot die tijd zie je in de Graph en Fleet van de nieuwe persoon op welke beheerders diegene wacht. **Van mij** en **Team** verschijnen een paar seconden na de toestemming, zonder dat je de pagina opnieuw hoeft te laden.

Een nieuwe Machine van iemand die al lid is, krijgt de Graph van het team na 24 uur. In de tussentijd kunnen beheerders op **Niet van hen** tikken om te zorgen dat die niet wordt toegevoegd.

## Als iemand vertrekt

Vanaf dat moment krijgt diegene niets nieuws. Wat diegene heeft gedeeld, blijft bij het team. Een beheerder kan iemand ook **Eruit halen** en diegene later **Opnieuw delen**.

## Delen voor iedereen uitzetten

Een beheerder zet **De Graph delen in deze Fleet** uit bij **Wat gedeeld wordt**. Er wordt niets nieuws meer gedeeld.

Met **Uitzetten** behoud je wat teamgenoten al hebben. Met **Uitzetten en gedeelde gegevens verwijderen** verwijdert elke Machine die gegevens. Als delen weer wordt ingeschakeld, bekijkt iedereen eerst opnieuw wat er wordt gedeeld.

## Stoppen met je eigen werk delen

Zet je koppelingen uit bij **Je koppelingen**, tenzij de Fleet ze verplicht stelt. Wat ze hebben gedeeld, wordt ingetrokken.

Zie ook [Fleets](fleet.md) en [Beveiliging en privacy](security-and-privacy.md).
