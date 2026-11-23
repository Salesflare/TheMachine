---
title: Instellingen
area: settings
summary: Waar je elke instelling vindt, van lichte modus tot beveiliging en je account.
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
Open **Instellingen** via het tandwiel bovenaan. De tabbladen:

- **Account**: bovenaan vind je **Je adressen** (adressen die als jou tellen) en **Uitloggen**. Op een gehoste Machine staan ook je abonnement, facturen, Fleet, vrienden, login en gegevens hier, met **Abonnement opzeggen** en **Account verwijderen** helemaal onderaan. Op een Machine op je eigen computer die aan het Network is gekoppeld, vind je hier je Fleet, gebruikersnaam, vrienden en login, elk met een link naar dat deel van je account (log daar in), en onderaan **Account verwijderen**. Nog niet gekoppeld? Bovenaan staat **Word lid van het Network**. Zie [Abonnementen en facturatie](plans-and-billing.md).
- **Algemeen**: taal en regio, dit apparaat, spraakinvoer, de browser van je Machine, je Fleet, exporteren en importeren, en de versie die erop draait. Zonder tabblad Account staat **Word lid van het Network** onderaan.
- **Beveiliging**: Standaard of Voorzichtig. Zie [Beveiligingsniveaus](security-levels.md). Ook **Toegang voor support**, zolang die aanstaat: zie [Hulp krijgen](get-support.md#support-access).
- **Activiteit**: alles wat The Machine voor je heeft gedaan, met het nieuwste bovenaan. Zie [Activiteit](activity.md).
- **Meldingen**: waar je meldingen ontvangt en wanneer, en je werkuren. Zie [Meldingen](notifications.md) en [Werkuren](work-hours.md).
- **Schrijven**: handtekeningen en hoe je schrijft. Zie [Schrijven](writing.md).
- **Skills**: handleidingen die je Machine volgt. Zie [Skills](skills.md).
- **Apps**: de apps van The Machine voor je telefoon en computer, daarna Claude, ChatGPT en andere AI's die je hebt gekoppeld, en wat ze mogen doen. Zie [De mobiele app](mobile-app.md) en [Andere AI’s koppelen](ai-connections.md).
- **Model**: de AI die voor je leest en concepten opstelt, en de beperkingen ervan. Zie [Model](model.md). Ook **Codex en Claude Code**: zie [Overdragen aan Claude Code of Codex](hand-to-agent.md). En **Zoeken op betekenis**, hieronder.

Een tabblad zonder inhoud is verborgen.

## Algemeen

- **Taal en regio**: met **Regio** stel je in hoe datums, tijden en getallen worden weergegeven (24 okt of 24 oktober). Met **Tijdnotatie** kies je een 12-uursnotatie (2:05 PM) of 24-uursnotatie (14:05). To-do's, Telegram, het overzicht en Fleet-berichten gebruiken beide instellingen. Een gehoste Machine neemt de tijdzone over die je bij het aanmelden hebt gekozen.
- **Taal**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 of Русский. De taal is standaard die van je browser. Het dashboard, Help, meldingen, Telegram, de wekelijkse terugblik en de to-do's die je Machine schrijft, schakelen over zodra je een taal kiest. Oudere tekst blijft zoals die was. Teamgenoten krijgen Fleet- en Familievragen in hun eigen taal. Concepten voor anderen blijven in de taal van hun gesprek.
- **Dit apparaat**: **App installeren**, **Meldingen** met **Test versturen**, en **Lichte modus**, alleen voor deze browser of telefoon. Zie [De app installeren en meldingen aanzetten](phone-app.md). Op [Omarchy](omarchy.md) staat ook **Omarchy-thema**.
- **Spraakinvoer**: hoe wat je zegt tekst wordt, en welke stem Talk live gebruikt. Zie [Spraakinvoer](voice-input.md) en [Live praten](talk-live.md).
- **De browser van je Machine openen ↗**: de browser die je Machine gebruikt voor sites zoals LinkedIn.
- **Fleet-regels**: zie [Deelregels](sharing-rules.md).
- **Exporteren**:
  - **Alles**: alles wat je Machine weet, in één versleuteld bestand om te bewaren of over te zetten, en **Importeren** om een bestand te importeren. Zie [Verplaatsen naar een andere computer](moving.md).
  - **Kennis voor een andere AI**: wat je Machine heeft geleerd, in bestanden die elke AI kan lezen. Zie [Kennis voor een andere AI](knowledge-export.md).

## Versie

De versie die je Machine gebruikt. Updates worden automatisch geïnstalleerd. Als er een nieuwere versie klaarstaat op een gehoste Machine, installeert **Nu bijwerken** die meteen. Dat duurt een paar minuten en je gegevens blijven behouden.

Op je eigen computer installeert een dagelijkse timer elke nieuwe, ondertekende release op Linux. Zie [Op je eigen computer draaien](self-hosted-setup.md).

## Zoeken op betekenis

Onder **Instellingen**, **Model**. Hiermee vind je e-mails, berichten en notities op basis van waar ze over gaan, niet alleen op basis van de woorden. Op een gehoste Machine doet een kleine AI dit op de Machine zelf. Er wordt niets ergens anders naartoe gestuurd. De functie staat aan vanaf 8 GB geheugen. Op 4 GB kun je die aanzetten met de schakelaar. De functie gebruikt ongeveer een halve gigabyte, dus een drukke Machine kan trager worden. Als de functie uitstaat, zoekt de voorbereiding van een to-do nog steeds naar verwante berichten op basis van woorden.

Op je eigen computer is dit het `embeddings`-blok in `config.json`. Start de Machine opnieuw op nadat je iets hebt gewijzigd.

## Op deze Machine

Als je Machine op je eigen computer draait, gebeuren een paar dingen daar in een terminal:

- Het instellingenbestand, `config.json`: alle instellingen op één plek. Start de Machine opnieuw op nadat je iets hebt gewijzigd.
- `assistant connect`: een bron toevoegen, zoals `assistant connect gmail` of `assistant connect outlook`.
- `assistant telegram on` of `off`: berichten op Telegram. Zie [Telegram](telegram.md).
- `assistant doctor`: controleert alles en geeft voor elk probleem een oplossing.

## Je adressen

Alle adressen van jou die je Machine heeft gevonden: je accounts, aliassen voor Gmail of Outlook, je agenda en je Slack- en Intercom-profielen. E-mails en meetings van al deze adressen tellen als van jou. Kies **Verwijderen** voor een adres dat niet van jou is.

Een gedeeld adres, zoals info@ of een Google Group, telt nooit vanzelf mee. Een adres waarover je Machine twijfelt, staat bij **Misschien van jou**. Kies een optie:

- **Van mij: alleen ik beantwoord het**: het telt als van jou. E-mails aan dit adres kunnen je to-do's worden.
- **Van het team: anderen beantwoorden het ook**: het is niet van jou. E-mails die alleen naar dit adres zijn gestuurd, leveren geen to-do's of concepten voor je op. Ze vullen de Graph nog wel aan.
- **Niet van mij**: het telt niet als van jou.

Kies op basis van wie het adres vandaag beantwoordt. Een teaminbox zoals support@ is van het team. Een adres zoals partnerships@ dat alleen jij beantwoordt, is van jou. Wijzig dit zodra anderen het ook beantwoorden.

Met **Wijzigen** op de rij kun je dit later aanpassen. Je eigen loginadres is altijd van jou.

### Domeinen van je bedrijf

De domeinen van je eigen adressen tellen als domeinen van je bedrijf. Gebruik je ook een ander domein, zoals acme.co naast acme.com? Typ het onder **Domeinen van je bedrijf** en klik op **Toevoegen**.

Mensen met zo'n domein zijn dan collega's, nooit klanten. Hun gesprekken komen niet in de Team-Graph en er wordt geen organisatie voor aangemaakt. Met **Verwijderen** haal je het domein er weer uit. Gratis e-maildomeinen zoals gmail.com kun je niet toevoegen.

Een alias van je Gmail-account kan ook als **Van**-adres van een concept worden gebruikt, als Gmail bevestigt dat je ermee kunt versturen. Zie [Gmail](gmail.md#what-it-can-send).
