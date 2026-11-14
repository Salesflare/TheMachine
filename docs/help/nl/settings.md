---
title: Instellingen
area: settings
summary: Waar je elke instelling vindt, van de lichte modus tot beveiliging en je account.
covers: settings:general
code: dashboard.html
order: 1
translated: 00e42f9aeb395d21
---
Open **Instellingen** via het tandwiel bovenaan. De tabbladen:

- **Account**: bovenaan vind je **Je adressen** (de adressen die als jou tellen) en **Uitloggen**. Op een gehoste Machine staan hier ook je abonnement, facturen, Fleet, vrienden, aanmeldgegevens en gegevens, met helemaal onderaan **Abonnement opzeggen** en **Account verwijderen**. Op een Machine op je eigen computer die aan het Network is gekoppeld, staan hier je Fleet, gebruikersnaam, vrienden en aanmeldgegevens. Elk onderdeel heeft een link naar dat deel van je account, waar je je kunt aanmelden. Onderaan staat **Account verwijderen**. Nog niet gekoppeld? Bovenaan staat **Word lid van het Network**. Zie [Abonnementen en facturering](plans-and-billing.md).
- **Algemeen**: taal en regio, dit apparaat, spraakinvoer, de browser van je Machine, je Fleet, exporteren en importeren, en de versie die erop draait. Als er geen tabblad Account is, staat **Word lid van het Network** onderaan.
- **Beveiliging**: Standaard of Voorzichtig. Zie [Beveiligingsniveaus](security-levels.md). Ook **Toegang voor support**, zolang die aanstaat. Zie [Support krijgen](get-support.md#support-access).
- **Activiteit**: alles wat The Machine voor je heeft gedaan, nieuwste eerst. Zie [Activiteit](activity.md).
- **Meldingen**: wat je waar ontvangt, en je werkuren. Zie [Meldingen](notifications.md) en [Werkuren](work-hours.md).
- **Schrijven**: handtekeningen en hoe je schrijft. Zie [Schrijven](writing.md).
- **Skills**: handleidingen die je Machine volgt. Zie [Skills](skills.md).
- **Apps**: de apps van The Machine voor je telefoon en computer, daarna Claude, ChatGPT en andere AI's die je hebt gekoppeld, en wat ze mogen doen. Zie [De mobiele app](mobile-app.md) en [Andere AI's koppelen](ai-connections.md).
- **Model**: de AI die je mail leest en concepten maakt, en de beperkingen ervan. Zie [Model](model.md). Ook **Codex en Claude Code**: zie [Overdragen aan Claude Code of Codex](hand-to-agent.md). En **Zoeken op betekenis**, hieronder.

Een tabblad zonder inhoud wordt verborgen.

## Algemeen

- **Taal en regio**: met **Regio** stel je in hoe datums, tijden en getallen worden weergegeven (Oct 24 of 24 Oct). Met **Tijdnotatie** kies je voor 12-uursnotatie (2:05 PM) of 24-uursnotatie (14:05). To-do's, Telegram, het overzicht en Fleet-berichten volgen beide instellingen. Een gehoste Machine gebruikt standaard de tijdzone die je bij het aanmelden hebt gekozen.
- **Taal**: English, Nederlands, Français, Deutsch, Español, Italiano of Português (Brasil). Standaard wordt de taal van je browser gebruikt. Het dashboard, Help, meldingen, Telegram, het wekelijkse overzicht en de to-do's die je Machine schrijft, veranderen zodra je een taal kiest. Oudere tekst blijft ongewijzigd. Teamgenoten krijgen Fleet- en Family-vragen in hun eigen taal, en concepten voor anderen blijven in de taal van het gesprek.
- **Dit apparaat**: **App installeren**, **Meldingen** met **Stuur een test**, en **Lichte modus**, alleen voor deze browser of telefoon. Zie [De app installeren en meldingen inschakelen](phone-app.md). Op [Omarchy](omarchy.md) staat ook **Omarchy-thema**.
- **Spraakinvoer**: hoe wat je zegt wordt omgezet in tekst, en de stem van Talk live. Zie [Spraakinvoer](voice-input.md) en [Talk live](talk-live.md).
- **De browser van je Machine openen ↗**: de browser die je Machine gebruikt voor sites zoals LinkedIn.
- **Fleet-regels**: zie [Deelregels](sharing-rules.md).
- **Exporteren**:
  - **Alles**: alles wat je Machine weet in één versleuteld bestand, om te verplaatsen of te bewaren. Met **Importeren** kun je een bestand importeren. Zie [Verplaatsen naar een andere computer](moving.md).
  - **Kennis voor een andere AI**: wat je Machine heeft geleerd, in bestanden die elke AI kan lezen. Zie [Kennis voor een andere AI](knowledge-export.md).

## Versie

De release waarop je Machine draait. Updates worden automatisch geïnstalleerd. Als er een nieuwere versie klaarstaat op een gehoste Machine, installeert **Nu bijwerken** die meteen. Dat duurt een paar minuten en je gegevens blijven behouden.

Op je eigen computer installeert een dagelijkse timer elke nieuwe ondertekende release op Linux. Zie [Draaien op je eigen computer](self-hosted-setup.md).

## Zoeken op betekenis

In **Instellingen**, onder **Model**. Hiermee vind je e-mails, berichten en notities op basis van hun onderwerp, niet alleen op basis van de gebruikte woorden. Op een gehoste Machine doet een kleine AI op de Machine zelf dit werk, en er wordt niets ergens naartoe gestuurd. Deze functie staat aan vanaf 8 GB geheugen. Op 4 GB kun je de functie inschakelen met de schakelaar. De functie gebruikt ongeveer een halve gigabyte, dus een drukke Machine kan trager worden.

Op je eigen computer is dit het blok `embeddings` in `config.json`. Start de Machine opnieuw op nadat je iets hebt gewijzigd.

## Op deze Machine

Als je Machine op je eigen computer draait, worden een paar dingen daar uitgevoerd, in een terminal:

- Het instellingenbestand, `config.json`: alle instellingen op één plek. Start de Machine opnieuw op nadat je iets hebt gewijzigd.
- `assistant connect`: voeg een bron toe, zoals `assistant connect gmail` of `assistant connect outlook`.
- `assistant telegram on` of `off`: berichten op Telegram. Zie [Telegram](telegram.md).
- `assistant doctor`: controleert alles en geeft voor elk probleem een oplossing.

## Je adressen

Alle adressen van jou die de Machine heeft gevonden: je accounts, aliassen van Gmail of Outlook, je agenda en je Slack- en Intercom-profielen. E-mails en afspraken van al deze adressen tellen als die van jou. Kies **Verwijderen** voor een adres dat niet van jou is.

Een gedeeld adres, zoals info@ of een Google Group, telt nooit automatisch mee. Een adres waarover de Machine twijfelt, staat onder **Misschien van jou**. Kies een optie:

- **Van mij: alleen ik beantwoord het**: het telt als adres van jou. E-mails hiernaartoe kunnen je to-do's worden.
- **Van het team: anderen beantwoorden het ook**: het is niet van jou. E-mails die alleen naar dit adres zijn gestuurd, leveren geen to-do's of concepten voor jou op. De e-mails vullen wel de Graph aan.
- **Niet van mij**: het telt niet als adres van jou.

Kies op basis van wie het adres nu beantwoordt. Een teaminbox zoals support@ is van het team. Een adres zoals partnerships@ dat alleen jij beantwoordt, is van jou. Wijzig de keuze zodra anderen het ook beantwoorden.

Met **Wijzigen** op de bijbehorende regel kun je de keuze later aanpassen. Je eigen aanmeldadres is altijd van jou.

### Domeinen van je bedrijf

De domeinen van je eigen adressen tellen als domeinen van je bedrijf. Gebruik je daarnaast nog een ander domein, zoals acme.co naast acme.com? Typ het onder **Domeinen van je bedrijf** en druk op **Toevoegen**.

Mensen met zo'n domein zijn dan collega's, geen klanten: hun gesprekken komen niet in de Team Graph en er wordt geen organisatie voor aangemaakt. Met **Verwijderen** haal je het domein er weer uit. Gratis e-maildomeinen zoals gmail.com kun je niet toevoegen.

Een Gmail-alias van jou kan ook als **Van**-adres voor een concept worden gebruikt, als Gmail bevestigt dat je ermee kunt verzenden. Zie [Gmail](gmail.md#what-it-can-send).
