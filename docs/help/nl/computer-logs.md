---
title: Problemen op je computer
area: troubleshooting
summary: Je Machine leest de logboeken van je computer en vertelt je over echte problemen, met de oorzaak en een oplossing. Een oplossing wordt alleen uitgevoerd als je op Doe het tikt.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## Wat hij leest

Op Linux met systemd leest je Machine het logboek van je eigen gebruikerssessie: je eigen services en de crashrapporten van je eigen programma's. Op Omarchy controleert hij ook Hyprland en de balk. Hij leest nooit het logboek van het hele systeem en vraagt nooit om extra toegang.

Hij leest welke service is gestopt, hoe dat is gebeurd en welk programma is gecrasht. Hij leest nooit wat er in een logregel staat, zodat er geen logtekst wordt bewaard of van je computer wordt verstuurd.

## Wat als een probleem telt

Een service die steeds opnieuw start, een service die meerdere keren op een dag is mislukt of uitgevallen blijft, een service die geen geheugen meer had en een programma dat is gecrasht. Op Omarchy gaat het ook om een crash van Hyprland of de balk, en om fouten in je Hyprland-instellingen.

Eén keer opnieuw starten of één mislukte uitvoering is normaal en blijft buiten beeld. Dat geldt ook voor een service die een paar keer is mislukt en daarna weer goed draaide, en voor een mislukte service die door niets wordt gestart: hij staat niet ingeschakeld en geen andere service of timer start hem.

Browsers die door tests en agents worden aangestuurd (headless, Playwright, Puppeteer, CI) blijven buiten beeld. Dat geldt ook voor een programma dat stopt terwijl de bijbehorende service wordt gestopt of opnieuw gestart. Ontwikkelaarsprocessen blijven ook buiten beeld: wat een codeeragent uitvoert, tests en programma's die vanuit een tijdelijke map of cachemap worden gestart. Een programma dat steeds opnieuw crasht, maakt één to-do met hoe vaak en wanneer dat gebeurde.

Een script wordt bij de eigen naam genoemd, zoals backup.py, niet als python3 of node.

## Wat je krijgt

Een to-do die in gewone taal vertelt wat er is gebeurd, waarom dat belangrijk is en wat je kunt doen. De opdrachten die laten zien waarom, vind je onder **Meer tonen**. Vraag ernaar in de bijbehorende chat en The Machine onderzoekt het. Alles wat hij wil veranderen, wacht op je akkoord, net als bij **Doe het**.

Als er een veilige oplossing is, staat er **Doe het** bij de to-do. Voor een service van jou die uitgevallen blijft, start hij die opnieuw. Op Omarchy brengt hij ook de balk weer terug. **Doe het** voert alleen die opdracht uit en het resultaat verschijnt in de chat van de to-do. Hij raakt nooit de eigen services van The Machine of de OpenClaw Gateway aan.

Voor hetzelfde probleem krijg je hooguit eens per twee weken een to-do, en nooit zolang de bijbehorende to-do nog openstaat. Er komen hooguit twee nieuwe to-do's per dag bij. Een to-do over een uitgevallen service wordt vanzelf gesloten zodra die weer draait of het probleem is opgelost.

## In een terminal

`assistant doctor` toont dezelfde problemen van de afgelopen dag.

## Andere computers

Op macOS, Windows en computers zonder systemd leest hij niets en meldt hij dat in `assistant doctor`.

Bij een gehoste Machine zorgen wij ervoor dat de server blijft draaien. Problemen daarmee gaan naar het team van The Machine, niet naar jou als to-do's.

## Uitschakelen

Stel `"computer_logs": false` in config.json in en start de service opnieuw op.
