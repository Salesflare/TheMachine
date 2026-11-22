---
title: Instellingen
area: settings
summary: Waar je alle instellingen vindt, van lichte modus tot beveiliging en je account.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Open **Instellingen** via het tandwiel bovenaan. De tabbladen:

- **Account**: bovenaan vind je **Je adressen** (de adressen die als die van jou tellen) en **Uitloggen**. Op een gehoste Machine vind je hier ook je abonnement, facturen, Fleet, vrienden, inloggegevens en gegevens, met helemaal onderaan **Abonnement opzeggen** en **Account verwijderen**. Op een Machine op je eigen computer die is gekoppeld aan het Network vind je hier je Fleet, gebruikersnaam, vrienden en inloggegevens, elk met een link naar dat deel van je account (log daar in), en onderaan **Account verwijderen**. Nog niet gekoppeld? Bovenaan staat **Word lid van het Network**. Zie [Abonnementen en facturering](plans-and-billing.md).
- **Algemeen**: taal en regio, dit apparaat, spraakinvoer, de browser van je Machine, je Fleet, exporteren en importeren, en de versie die erop draait. Als er geen tabblad Account is, staat **Word lid van het Network** onderaan.
- **Beveiliging**: Standaard of Voorzichtig. Zie [Beveiligingsniveaus](security-levels.md). Ook **Toegang voor support**, zolang die is ingeschakeld: zie [Support krijgen](get-support.md#support-access).
- **Activiteit**: alles wat The Machine voor je heeft gedaan, met het nieuwste bovenaan. Zie [Activiteit](activity.md).
- **Meldingen**: welke meldingen je waar ontvangt, en je werkuren. Zie [Meldingen](notifications.md) en [Werkuren](work-hours.md).
- **Schrijven**: handtekeningen en je schrijfstijl. Zie [Schrijven](writing.md).
- **Skills**: handleidingen die je Machine volgt. Zie [Skills](skills.md).
- **Apps**: eerst de apps van The Machine voor je telefoon en computer, daarna Claude, ChatGPT en andere AI's die je hebt gekoppeld, en wat elke app mag doen. Zie [De mobiele app](mobile-app.md) en [Andere AI's koppelen](ai-connections.md).
- **Model**: de AI die je berichten leest en concepten schrijft, en de beperkingen ervan. Zie [Model](model.md). Ook **Codex en Claude Code**: zie [Overdragen aan Claude Code of Codex](hand-to-agent.md). En hieronder **Zoeken op betekenis**.

Een tabblad zonder inhoud is verborgen.

## Algemeen

- **Taal en regio**: met **Regio** bepaal je hoe datums, tijden en getallen worden weergegeven (24 okt of okt 24). Met **Tijdnotatie** kies je voor 12-uursnotatie (2:05 PM) of 24-uursnotatie (14:05). To-do's, Telegram, het overzicht en Fleet-berichten volgen beide instellingen. Een gehoste Machine gebruikt standaard de tijdzone die je bij het aanmelden hebt gekozen.
- **Taal**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 of Русский. Standaard wordt de taal van je browser gebruikt. Het dashboard, Help, meldingen, Telegram, het wekelijkse overzicht en de to-do's die je Machine schrijft, veranderen zodra je een taal kiest. Oudere teksten blijven zoals ze waren. Je teamgenoten krijgen vragen uit de Fleet en de Familie in hun eigen taal. Concepten voor anderen blijven in de taal van hun gesprek.
- **Dit apparaat**: **App installeren**, **Meldingen** met **Test versturen** en **Lichte modus**, alleen voor deze browser of telefoon. Zie [De app installeren en meldingen inschakelen](phone-app.md). Op [Omarchy](omarchy.md) staat ook **Omarchy-thema**.
- **Spraakinvoer**: hoe je gesproken woorden worden omgezet in tekst, en welke stem Live praten gebruikt. Zie [Spraakinvoer](voice-input.md) en [Live praten](talk-live.md).
- **De browser van je Machine openen ↗**: de browser die je Machine gebruikt voor sites zoals LinkedIn.
- **Fleet-regels**: zie [Deelregels](sharing-rules.md).
- **Exporteren**:
  - **Alles**: alles wat je Machine weet, in één versleuteld bestand om te verplaatsen of te bewaren, en **Importeren** om een bestand te importeren. Zie [Verplaatsen naar een andere computer](moving.md).
  - **Kennis voor een andere AI**: wat je Machine heeft geleerd, in bestanden die elke AI kan lezen. Zie [Kennis voor een andere AI](knowledge-export.md).

## Versie

De versie die je Machine gebruikt. Updates worden automatisch geïnstalleerd. Als er een nieuwere versie klaarstaat op een gehoste Machine, installeert **Nu bijwerken** die meteen. Dit duurt een paar minuten en je gegevens blijven behouden.

Op je eigen computer installeert een dagelijkse timer elke nieuwe, ondertekende release op Linux. Zie [Draaien op je eigen computer](self-hosted-setup.md).

## Zoeken op betekenis

Ga in **Instellingen** naar **Model**. Hiermee vind je e-mails, berichten en notities op basis van waar ze over gaan, niet alleen op basis van de woorden. Op een gehoste Machine doet een kleine AI op de Machine zelf dit werk. Er wordt niets ergens naartoe gestuurd. De functie staat aan vanaf 8 GB geheugen. Op een Machine met 4 GB kun je die inschakelen met de schakelaar. De functie gebruikt ongeveer een halve gigabyte, dus een drukke Machine kan trager worden.

Op je eigen computer vind je de instelling in het blok `embeddings` van `config.json`. Start de Machine opnieuw op nadat je iets hebt gewijzigd.

## Op deze Machine

Als je Machine op je eigen computer draait, doe je een paar dingen daar in een terminal:

- Het instellingenbestand, `config.json`: alle instellingen op één plek. Start de Machine opnieuw op nadat je iets hebt gewijzigd.
- `assistant connect`: voeg een bron toe, zoals `assistant connect gmail` of `assistant connect outlook`.
- `assistant telegram on` of `off`: berichten op Telegram. Zie [Telegram](telegram.md).
- `assistant doctor`: controleert alles en geeft voor elk probleem een oplossing.

## Je adressen

Alle adressen van jou die The Machine heeft gevonden: je accounts, Gmail- of Outlook-aliassen, je agenda, je Slack- en Intercom-profielen. E-mail en meetings van al deze adressen tellen als die van jou. Met **Verwijderen** haal je een adres weg dat niet van jou is.

Een gedeeld adres, zoals info@ of een Google Group, telt nooit vanzelf mee. Een adres waarover The Machine twijfelt, staat onder **Misschien van jou**. Kies een van deze opties:

- **Van mij: alleen ik beantwoord het**: het adres telt als van jou. E-mail hiernaartoe kan je to-do's opleveren.
- **Van het team: anderen beantwoorden het ook**: het adres is niet van jou. E-mail die alleen hiernaartoe is gestuurd, levert geen to-do's of concepten voor jou op. De e-mail wordt wel meegenomen in de Graph.
- **Niet van mij**: het adres telt niet als van jou.

Kies op basis van wie het adres nu beantwoordt. Een teaminbox zoals support@ is van het team. Een adres zoals partnerships@ dat alleen jij beantwoordt, is van jou. Wijzig de instelling zodra anderen het adres ook beantwoorden.

Met **Wijzigen** op de bijbehorende rij kun je dit later aanpassen. Je eigen inlogadres is altijd van jou.

### Domeinen van je bedrijf

De domeinen van je eigen adressen tellen als domeinen van je bedrijf. Gebruik je ook een ander domein, zoals acme.co naast acme.com? Typ het onder **Domeinen van je bedrijf** en klik op **Toevoegen**.

Mensen met die domeinen zijn dan collega's, geen klanten: hun gesprekken komen niet in de Team-Graph en er wordt geen organisatie voor aangemaakt. Met **Verwijderen** haal je een domein weer weg. Gratis e-maildomeinen zoals gmail.com kun je niet toevoegen.

Een Gmail-alias van jou kan ook als **Van**-adres voor een concept worden gebruikt, als Gmail bevestigt dat je namens dat adres kunt versturen. Zie [Gmail](gmail.md#what-it-can-send).
