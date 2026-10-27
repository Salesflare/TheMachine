---
title: Instellingen
area: settings
summary: Waar je elke instelling vindt, van de lichte modus tot beveiliging en je account.
covers: settings:general
code: dashboard.html
order: 1
---
Open **Instellingen** met het tandwiel bovenaan. De tabbladen:

- **Account**: **Je adressen**, de adressen die als jou tellen, met waar elk vandaan komt. Je abonnement in het kort, knoppen naar je accountpagina's, en **Uitloggen**. Zie [Abonnementen en facturatie](plans-and-billing.md).
- **Algemeen**: taal en regio, dit apparaat, de browser van je Machine, je Fleet en je account.
- **Beveiliging**: Standaard of Voorzichtig, en de instellingen die ze bepalen. Zie [Beveiligingsniveaus](security-levels.md). Ook **Toegang voor support**, zolang het aanstaat: zie [Hulp krijgen](get-support.md#support-access).
- **Meldingen**: wat je waar bereikt, en je werkuren. Zie [Meldingen](notifications.md) en [Werkuren](work-hours.md).
- **Schrijven**: handtekeningen en hoe je schrijft. Zie [Schrijven](writing.md).
- **Skills**: handleidingen die je Machine volgt. Zie [Skills](skills.md).
- **Model**: wat voor je antwoordt, en de limieten. Zie [Model](model.md). Ook **Codex en Claude Code**: zie [Overdragen aan Claude Code of Codex](hand-to-agent.md).

Een tabblad zonder inhoud wordt verborgen.

## Algemeen

- **Taal en regio**: je **Regio** bepaalt hoe datums eruitzien (Oct 24 of 24 okt) en de gebruikelijke klok. **Tijdnotatie** kiest in plaats daarvan 12 uur (2:05 PM) of 24 uur (14:05). To-do's, Telegram, het overzicht en berichten in de Fleet volgen die. Een gehoste Machine begint met het land van de tijdzone die je bij het aanmelden koos. Tijden zoals "3 uur geleden" en getallen volgen die ook.
- **Taal**: English, Nederlands, Français, Deutsch, Español, Italiano of Português (Brasil). De eerste keer dat je het dashboard opent, kiest het de taal van je browser, als het een van deze is (Portugees uit Portugal krijgt voorlopig Braziliaans Portugees). Het dashboard, datums, Telegram-berichten, meldingen, het weekoverzicht en de notities en titels van to-do's die je Machine voor je schrijft, volgen die vanaf het moment dat je hem kiest; wat al geschreven was, blijft zoals het was. Vragen in de Fleet en de Familie verschijnen in de eigen taal van elke teamgenoot. Concepten aan anderen blijven in de taal van hun gesprek. Help en de helppagina’s volgen ze ook.
- **Dit apparaat**: de app (**App installeren**), **Meldingen** met **Stuur een test**, en **Lichte modus**, alleen voor deze browser of telefoon. Zie [De app installeren en meldingen aanzetten](phone-app.md).
- **De browser van je Machine openen ↗**: de browser die je Machine gebruikt voor sites zoals LinkedIn.
- **Fleet-regels**: zie [Deelregels](sharing-rules.md).
- **Account**: **Account openen** en **Uitloggen**, op een gehoste Machine.

## Op deze Machine

Een paar instellingen staan op de computer waarop je Machine draait, niet in de app:

- `config.json`: elke instelling, in één bestand. Herstart de Machine na een wijziging.
- `assistant connect`: een bron toevoegen, zoals `assistant connect gmail` of `assistant connect outlook`.
- `assistant telegram on` of `off`: berichten op Telegram. Zie [Telegram](telegram.md).
- `assistant doctor`: controleert alles en toont een oplossing voor elk probleem.

## Je adressen

Elk adres van jou dat de Machine vond: je accounts, aliassen in Gmail of Outlook, je agenda, je profiel in Slack en Intercom. Mail en afspraken van elk ervan tonen als jou. **Verwijder** er een dat niet van jou is.

Een gedeeld adres, zoals info@ of een Google Group, telt nooit vanzelf mee. Een adres waarover de Machine niet zeker is, staat onder **Misschien van jou**, en er wordt niets voor je gekozen. Kies er een:

- **Van mij: ik behandel het**: het telt als van jou. Mail eraan kan je to-do's worden.
- **Van het team: anderen nemen het ook op**: het is niet jij. Mail die alleen daarheen ging, maakt geen to-do's en geen concepten voor je. Het vult nog steeds de Graph aan, gedeeld met je team zoals voorheen.
- **Niet van mij**: het telt niet als van jou.

**Wijzigen** op de rij zet het later om. Je eigen inlogadres is altijd van jou.
