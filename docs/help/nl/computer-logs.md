---
title: Problemen op je computer
area: troubleshooting
summary: Je Machine leest de eigen logs van zijn computer en meldt echte problemen, met de oorzaak en een oplossing. Een oplossing draait alleen als je op Do it tikt.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## Wat hij leest

Op Linux met systemd leest je Machine het log van je eigen gebruikerssessie: je eigen services en de crashrapporten van je eigen programma's. Op Omarchy kijkt hij ook naar Hyprland en de balk. Het log van het hele systeem leest hij nooit, en hij vraagt nooit om meer toegang.

Hij leest welke service stopte, hoe die eindigde en welk programma crashte. Nooit wat er in een logregel staat, dus er wordt geen logtekst bewaard en niets ervan verlaat je computer.

## Wat telt als probleem

Een service die blijft herstarten, een die op een dag een paar keer mislukte of eruit blijft liggen, een die geen geheugen meer had, en een programma dat crashte. Op Omarchy ook een crash van Hyprland of de balk, en fouten in je Hyprland-instellingen.

Een enkele herstart of een enkele mislukte run is normaal en blijft stil.

## Wat je krijgt

Een to-do die in gewone woorden zegt wat er gebeurde, waarom het telt en wat je kunt doen. De commando's die tonen waarom, staan onder Meer tonen. Vraag het in de chat ervan en The Machine zoekt het uit. Alles wat hij verandert, wacht op je OK, zoals bij Do it.

Is er een veilige oplossing, dan heeft de to-do Do it. Een dienst van jou die uit blijft, start het opnieuw, en op Omarchy brengt het de balk terug. Do it voert alleen dat commando uit, en het resultaat staat in de chat van de to-do. Het komt nooit aan de diensten van The Machine zelf of de OpenClaw Gateway.

Hetzelfde probleem geeft hooguit één to-do per twee weken, en nooit zolang die to-do nog openstaat. Hooguit twee nieuwe per dag.

## In een terminal

`assistant doctor` toont dezelfde problemen van de laatste dag.

## Andere computers

Op macOS, Windows en computers zonder systemd leest hij niets en zegt hij dat in `assistant doctor`.

## Uitzetten

Zet `"computer_logs": false` in config.json en herstart de service.
