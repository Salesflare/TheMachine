---
title: Intercom
area: connections
summary: Kundengespräche in deinem Intercom-Workspace. Es antwortet erst, nachdem du sendest, in deinem Namen.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
---
## Was es liest

Kundenunterhaltungen in deinem Intercom-Workspace: die letzten 7 Tage beim Verbinden, danach neue, sobald sie reinkommen. Es liest auch, zu welchem Workspace und welchem Admin die Anmeldung gehört.

## Was es tun kann

Es liest Gespräche. Mit deinem eigenen **Mit Intercom anmelden** kann es auch in einem Gespräch in deinem Namen antworten, erst nachdem du für genau diesen Text auf **Senden** tippst. Es weist nie zu, schließt nie, vergibt keine Tags und schreibt keine Notizen. Ein Intercom, das über deine Fleet mit dir geteilt ist, liest nur.

## Aufgaben aus Intercom

Eine Aufgabe aus einem Intercom-Gespräch zeigt, woher sie kommt: **Nachricht lesen** öffnet das Gespräch, mit einem Link dorthin in Intercom, und der Kunde steht auf der Aufgabe. Ihre Antwort ist eine Intercom-Antwort in diesem Gespräch, außer du bittest um eine E-Mail.

Kann Intercom nicht von deiner Machine aus antworten (nur zum Lesen mit dir geteilt, Antworten nicht eingeschaltet oder nicht verbunden), geht der Entwurf per E-Mail. Die Aufgabe sagt warum, und ihre Prüfung fragt **Stattdessen per E-Mail senden?** Um selbst in Intercom zu antworten, tippe auf der Aufgabe auf **Eigenes Intercom verbinden** und melde dich an. Nichts geht raus, bevor du es sendest.

## Verbinden

1. Im Dashboard: **Verbindungen**, **+ Hinzufügen**, Intercom. Oder auf der Einrichtungsseite einer gehosteten Machine unter app.themachine.computer/setup: **Weitere Quellen**, Intercom. Auf deinem eigenen Computer koppelst du ihn zuerst mit deinem Konto.
2. Tippe auf **Mit Intercom anmelden**.
3. Erlaube The Machine in Intercom. Sie wird von Salesflare gemacht. Danach bist du wieder dort, wo du angefangen hast.

Eine Anmeldung bei einem anderen Workspace fügt ein zweites Intercom-Konto hinzu.

Intercom zählt immer als Arbeit, für die Firma, die sein Workspace nennt.

## Entfernen

- Im Dashboard: **Verbindungen**, Intercom öffnen, **Details**, dann **Trennen**. Es hört auf zu lesen. Was es schon reingebracht hat, bleibt.
- Auf einer gehosteten Machine kannst du auch auf deiner Einrichtungsseite daneben auf **Entfernen** tippen.

## Bei Intercom deinstallieren

Öffne in Intercom Settings, Apps, Installed apps und entferne The Machine.
