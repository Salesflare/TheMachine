---
title: Problemen op je computer
area: troubleshooting
summary: Je Machine leest de logboeken van zijn eigen computer en vertelt je over echte problemen, met de oorzaak en een oplossing. Een oplossing wordt pas uitgevoerd als je op **Doe het** tikt.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## Wat hij leest

Op Linux met systemd leest je Machine het logboek van je eigen gebruikerssessie: je eigen services en de crashmeldingen van je eigen programma's. Op Omarchy controleert hij ook Hyprland en de balk. Hij leest nooit het volledige systeemlogboek en vraagt nooit om meer toegang.

Hij leest welke service is gestopt, hoe dat is gebeurd en welk programma is vastgelopen. Hij leest nooit wat er in een logregel staat. Zo wordt er geen logtekst bewaard of van je computer verstuurd.

## Wat als een probleem telt

Een service die steeds opnieuw start, meerdere keren op een dag is mislukt of uit blijft, een service die geen geheugen meer had en een programma dat is vastgelopen. Op Omarchy gaat het ook om crashes van Hyprland of de balk en fouten in je Hyprland-instellingen.

Eén keer opnieuw starten of één mislukte uitvoering is normaal en blijft onopgemerkt. Dat geldt ook voor een service die een paar keer is mislukt en daarna weer gewoon draaide.

Browsers die door tests en agents worden aangestuurd (headless, Playwright, Puppeteer, CI) blijven buiten beeld. Dat geldt ook voor een programma dat stopt terwijl de bijbehorende service wordt gestopt of opnieuw gestart. Ontwikkelaarsactiviteiten blijven eveneens buiten beeld: wat een codeeragent uitvoert, tests en programma's die vanuit een tijdelijke map of cachemap worden gestart. Als een programma steeds opnieuw vastloopt, maakt The Machine één to-do met hoe vaak en wanneer dat gebeurde.

Een script wordt genoemd bij zijn eigen naam, zoals backup.py, niet als python3 of node.

## Wat je krijgt

Een to-do die in gewone woorden vertelt wat er is gebeurd, waarom het belangrijk is en wat je kunt doen. De opdrachten die laten zien waarom het gebeurde, staan onder **Meer weergeven**. Stel je vraag in de chat van de to-do en The Machine zoekt het uit. Alles wat hij wijzigt, gebeurt pas nadat je akkoord hebt gegeven, net als bij **Doe het**.

Als er een veilige oplossing is, staat **Doe het** op de to-do. Als een service van jou uit blijft, start hij die opnieuw. Op Omarchy zet hij de balk weer aan. **Doe het** voert alleen die opdracht uit. Het resultaat verschijnt in de chat van de to-do. Hij komt nooit aan de eigen services van The Machine of de OpenClaw Gateway.

Voor hetzelfde probleem krijg je hooguit één to-do per twee weken, en nooit zolang de bijbehorende to-do nog openstaat. Er komen maximaal twee nieuwe to-do's per dag bij. Een to-do over een service die uit staat, wordt vanzelf gesloten zodra de service weer draait of de melding is gewist.

## In een terminal

`assistant doctor` toont dezelfde problemen van de afgelopen dag.

## Andere computers

Op macOS, Windows en computers zonder systemd leest hij niets. Dat staat ook in `assistant doctor`.

Op een gehoste Machine zorgen wij ervoor dat de server blijft draaien. Problemen daarmee gaan naar het team van The Machine, niet naar jou als to-do's.

## Uitschakelen

Stel `"computer_logs": false` in config.json in en start de service opnieuw.
