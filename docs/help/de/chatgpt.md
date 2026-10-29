---
title: ChatGPT
area: connections
summary: Melde dich mit ChatGPT an, um deine Machine über deinen ChatGPT-Tarif laufen zu lassen, und importiere deine ChatGPT-Skills.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## Wofür es da ist

ChatGPT ist das Modell, das für dich liest und Entwürfe schreibt, über deinen eigenen ChatGPT-Tarif. The Machine hat keine eigene KI. Die Anfragen deiner Machine gehen direkt an OpenAI, unter deinem Konto und deren Bedingungen.

## Anmelden

Auf einer gehosteten Machine tippst du auf deiner Einrichtungsseite auf **Mit ChatGPT anmelden** und gibst den angezeigten Code bei ChatGPT ein. Später abgemeldet? Tippe auf **ChatGPT neu verbinden**.

OpenAI lehnt den Code ab? Öffne deine [ChatGPT-Sicherheitseinstellungen](https://chatgpt.com/settings/security), scrolle ganz nach unten und schalte "Enable device code sign-in for Codex, Excel, PowerPoint, and Word" ein. Gib den Code dann noch einmal ein.

Nicht da? Bei einem Arbeitskonto (Business, Enterprise oder Edu) schaltet ein Admin des Workspace es unter [Permissions & roles](https://chatgpt.com/admin/permissions) ein, bei "Codex and Work Local". Ein Schalter gilt für beide Codes: Hat der Code für dein Modell funktioniert, funktioniert auch der für Codex.

Auf deinem eigenen Computer meldest du OpenClaw mit `openclaw models auth login` bei ChatGPT an.

## Nutzungslimits

Ein ChatGPT-Tarif hat ein 5-Stunden-Limit und ein Wochenlimit. **Einstellungen**, dann **Modell** zeigt, wie viel davon verbraucht ist und wann es zurückgesetzt wird. Hintergrundarbeit stoppt deutlich vor einem Limit, damit Platz für deine eigenen Chats bleibt. Ist ein Limit erreicht, steht oben im Dashboard, welches und wann es zurückgesetzt wird. Danach geht die Arbeit weiter. Siehe [Modell](model.md).

## Deine ChatGPT-Skills importieren

Tippe in **Einstellungen**, **Skills** auf **Importieren**, wähle **Aus ChatGPT** und tippe auf **Meine Skills finden**. Es liest die Skills, die du erstellt hast, im Browser deiner Machine. Nur Anweisungen werden übernommen. Siehe [Skills](skills.md).

## Entfernen

Wähle auf deiner Einrichtungsseite ein anderes Modell, oder melde OpenClaw bei einem anderen Anbieter an. Um den Zugriff auf Seiten von OpenAI zu beenden, meldest du die Sitzung in deinen ChatGPT-Sicherheitseinstellungen ab.
