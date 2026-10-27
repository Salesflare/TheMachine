---
title: Intercom
area: connections
summary: Kundengespräche in deinem Intercom-Workspace. Es antwortet erst, nachdem du sendest, in deinem Namen.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, Or paste an access token, Connect, More sources, Remove
---
## Was es liest

Kundenunterhaltungen in deinem Intercom-Workspace: die letzten 7 Tage beim Verbinden, danach neue, sobald sie reinkommen. Es liest auch, zu welchem Workspace und welchem Admin die Anmeldung gehört.

## Was es tun kann

Es liest Gespräche. Mit deinem eigenen **Mit Intercom anmelden** kann es auch in einem Gespräch in deinem Namen antworten, erst nachdem du für genau diesen Text auf **Senden** tippst. Es weist nie zu, schließt nie, vergibt keine Tags und schreibt keine Notizen. Ein Intercom, das über deine Fleet mit dir geteilt ist, liest nur.

## Aufgaben aus Intercom

Eine Aufgabe aus einem Intercom-Gespräch zeigt, woher sie kommt: **Nachricht lesen** öffnet das Gespräch, mit einem Link dorthin in Intercom, und der Kunde steht auf der Aufgabe. Ihre Antwort ist eine Intercom-Antwort in diesem Gespräch, außer du bittest um eine E-Mail.

Kann Intercom nicht von deiner Machine aus antworten (nur zum Lesen mit dir geteilt, Antworten nicht eingeschaltet oder nicht verbunden), geht der Entwurf per E-Mail. Die Aufgabe sagt warum, und ihre Prüfung fragt **Stattdessen per E-Mail senden?** Um selbst in Intercom zu antworten, tippe auf der Aufgabe auf **Eigenes Intercom verbinden** und melde dich an. Nichts geht raus, bevor du es sendest.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne deine Einrichtungsseite unter app.themachine.computer/setup und geh zu **Weitere Quellen**.
2. Öffne Intercom und tippe auf **Mit Intercom anmelden**.
3. Gib The Machine in Intercom frei. Es kommt von Salesflare.

Passt die Anmeldung nicht zu deinem Workspace, öffne stattdessen **Oder füge ein Zugriffstoken ein**, füge ein Token aus dem Developer Hub von Intercom ein und tippe auf **Verbinden**.

Auf deinem eigenen Computer:

1. Öffne im Developer Hub von Intercom deine App, dann Authentication, und kopiere ihr Zugriffstoken.
2. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle Intercom. Oder führe `assistant connect intercom` aus.
3. Füge das Token ein. Ein Token aus einem anderen Workspace wird zu einem zweiten Intercom-Konto.

Intercom zählt immer als Arbeit, für die Firma, die sein Workspace nennt.

## Entfernen

- Im Dashboard: **Verbindungen**, Intercom öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Intercom deinstallieren

- Mit Intercom angemeldet: Öffne in Intercom Settings, Apps, Installed apps und entferne The Machine.
- Ein eingefügtes Token: Lösche oder erneuere es im Developer Hub, oder lösche die App, in der du es erstellt hast.
