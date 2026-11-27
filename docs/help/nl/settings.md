---
title: Instellingen
area: settings
summary: Waar je elke instelling vindt, van lichte modus tot beveiliging en je account.
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
Open **Instellingen** met het tandwiel bovenaan. De tabbladen:

- **Account**: bovenaan vind je **Je adressen** (adressen die als van jou gelden) en **Uitloggen**. Op een gehoste Machine vind je ook je abonnement, facturen, Fleet, vrienden, inloggen en gegevens, met helemaal onderaan **Abonnement opzeggen** en **Account verwijderen**. Op een Machine op je eigen computer die gekoppeld is aan het Network vind je je Fleet, gebruikersnaam, vrienden en inloggen. Bij elk staat een link naar dat onderdeel van je account (log daar in), met onderaan **Account verwijderen**. Nog niet gekoppeld? Bovenaan staat **Word lid van het Network**. Zie [Abonnementen en facturatie](plans-and-billing.md).
- **Algemeen**: taal en regio, dit apparaat, spraakinvoer, de browser van je Machine, je Fleet, exporteren en importeren, en de versie die erop draait. Zonder tabblad Account staat **Word lid van het Network** onderaan.
- **Beveiliging**: Standaard of Voorzichtig. Zie [Beveiligingsniveaus](security-levels.md). Ook **Toegang voor support**, zolang die aanstaat: zie [Hulp krijgen](get-support.md#support-access).
- **Activiteit**: alles wat The Machine voor je heeft gedaan, met het nieuwste bovenaan. Zie [Activiteit](activity.md).
- **Meldingen**: waar je meldingen ontvangt en je werkuren. Zie [Meldingen](notifications.md) en [Werkuren](work-hours.md).
- **Schrijven**: handtekeningen en hoe je schrijft. Zie [Schrijven](writing.md).
- **Skills**: handleidingen die je Machine volgt. Zie [Skills](skills.md).
- **Apps**: de apps van The Machine voor je telefoon en computer, daarna Claude, ChatGPT en andere AI's die je hebt gekoppeld, en wat ze mogen doen. Op een computer staan de desktop-apps voor Windows, Mac en Linux vermeld, met **Downloaden** bij elke app. De app voor **Deze computer** is gemarkeerd. Zie [De mobiele app](mobile-app.md), [De desktopapp](desktop-app.md) en [Andere AI's koppelen](ai-connections.md).
- **Model**: de AI die voor je leest en concepten opstelt, en de beperkingen ervan. Zie [Model](model.md). Ook **Codex en Claude Code**: zie [Overdragen aan Claude Code of Codex](hand-to-agent.md). En **Zoeken op betekenis**, hieronder.

Een tabblad zonder inhoud is verborgen.

## Algemeen

- **Taal en regio**: met **Regio** bepaal je hoe datums, tijden en getallen worden weergegeven (24 okt of 24 oktober). Met **Tijdnotatie** kies je voor 12-uursnotatie (2:05 PM) of 24-uursnotatie (14:05). To-do's, Telegram, het overzicht en Fleet-berichten gebruiken beide instellingen. Een gehoste Machine gebruikt standaard de tijdzone die je bij het aanmelden hebt gekozen.
- **Taal**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 of Русский. De taal is standaard die van je browser. Het dashboard, Help, meldingen, Telegram, het wekelijkse overzicht en de to-do's die je Machine schrijft, schakelen over zodra je een taal kiest. Oudere tekst blijft ongewijzigd. Teamgenoten krijgen Fleet- en Family-vragen in hun eigen taal. Concepten voor anderen blijven in de taal van het gesprek.
- **Dit apparaat**: **App installeren**, **Meldingen** met **Test versturen** en **Lichte modus**, alleen voor deze browser of telefoon. Zie [De app installeren en meldingen aanzetten](phone-app.md). Op [Omarchy](omarchy.md) staat ook **Omarchy-thema**.
- **Spraakinvoer**: hoe je gesproken woorden worden omgezet in tekst en welke stem Talk live gebruikt. Zie [Spraakinvoer](voice-input.md) en [Live praten](talk-live.md).
- **De browser van je Machine openen ↗**: de browser die je Machine gebruikt voor sites zoals LinkedIn.
- **Fleet-regels**: zie [Deelregels](sharing-rules.md).
- **Exporteren**:
  - **Alles**: alles wat je Machine weet in één versleuteld bestand, om mee te nemen of te bewaren. Met **Importeren** importeer je een bestand. Zie [Verplaatsen naar een andere computer](moving.md).
  - **Kennis voor een andere AI**: wat je Machine heeft geleerd, in bestanden die elke AI kan lezen. Zie [Kennis voor een andere AI](knowledge-export.md).

## Versie

De versie die op je Machine draait. Updates worden automatisch geïnstalleerd. Staat er een nieuwere versie klaar op een gehoste Machine, dan installeert **Nu bijwerken** die meteen. Dat duurt een paar minuten en je gegevens blijven behouden.

Op je eigen computer installeert een dagelijkse timer elke nieuwe, ondertekende versie op Linux. Zie [Op je eigen computer draaien](self-hosted-setup.md).

## Zoeken op betekenis

In **Instellingen**, onder **Model**. Hiermee vind je e-mails, berichten en notities op basis van waar ze over gaan, niet alleen op basis van de gebruikte woorden. Op een gehoste Machine doet een kleine AI op de Machine zelf dit werk. Er wordt niets naar een andere plek verstuurd. Vanaf 8 GB geheugen staat dit aan. Op een Machine met 4 GB kun je het inschakelen met de schakelaar. Het gebruikt ongeveer een halve gigabyte, dus een drukke Machine kan trager worden. Staat het uit, dan zoekt de voorbereiding van een to-do nog steeds naar gerelateerde berichten, op basis van woorden.

Op je eigen computer is dit het blok `embeddings` in `config.json`. Start de Machine opnieuw op nadat je iets hebt gewijzigd.

## Op deze Machine

Als je Machine op je eigen computer draait, voer je een paar dingen daar uit, in een terminal:

- Het instellingenbestand, `config.json`: alle instellingen op één plek. Start de Machine opnieuw op nadat je iets hebt gewijzigd.
- `assistant connect`: een bron toevoegen, zoals `assistant connect gmail` of `assistant connect outlook`.
- `assistant telegram on` of `off`: berichten op Telegram. Zie [Telegram](telegram.md).
- `assistant doctor`: controleert alles en geeft voor elk probleem een oplossing weer.

## Je adressen

Alle adressen van jou die je Machine heeft gevonden: je accounts, Gmail- of Outlook-aliassen, je agenda en je Slack- en Intercom-profielen. E-mail en meetings van al deze adressen gelden als van jou. **Verwijderen** een adres dat niet van jou is.

Een gedeeld adres, zoals info@ of een Google Group, geldt nooit vanzelf als van jou. Een adres waarover je Machine twijfelt, staat onder **Misschien van jou**. Kies een optie:

- **Van mij: alleen ik beantwoord het**: het adres geldt als van jou. E-mail die ernaartoe wordt gestuurd, kan je to-do's opleveren.
- **Van het team: anderen beantwoorden het ook**: het adres geldt niet als van jou. E-mail die alleen naar dit adres is gestuurd, levert geen to-do's of concepten voor je op. De e-mail vult wel de Graph aan.
- **Niet van mij**: het adres geldt niet als van jou.

Kies op basis van wie het adres nu beantwoordt. Een teaminbox zoals support@ is van het team. Een adres zoals partnerships@ dat alleen jij beantwoordt, is van jou. Wijzig dit zodra anderen het ook beantwoorden.

Met **Wijzigen** op de regel pas je dit later aan. Je eigen inlogadres geldt altijd als van jou.

### Domeinen van je bedrijf

De domeinen van je eigen adressen gelden als domeinen van je bedrijf. Gebruik je ook een ander domein, zoals acme.co naast acme.com? Typ het onder **Domeinen van je bedrijf** en druk op **Toevoegen**.

Mensen met die domeinen gelden dan als collega's, nooit als klanten. Hun gesprekken komen niet in de Team-Graph en er wordt geen organisatie voor aangemaakt. Met **Verwijderen** haal je een domein weer weg. Gratis e-maildomeinen zoals gmail.com kun je niet toevoegen.

Een Gmail-alias van jou kan ook als **Van**-adres voor een concept worden gebruikt, als Gmail bevestigt dat je ermee kunt versturen. Zie [Gmail](gmail.md#what-it-can-send).
