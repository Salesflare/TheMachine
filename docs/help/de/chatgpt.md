---
title: ChatGPT
area: connections
summary: Melde dich mit ChatGPT an, damit deine Machine mit deinem ChatGPT-Tarif läuft, und importiere deine ChatGPT-Skills.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## Wofür es gedacht ist

Melde dich bei ChatGPT an. Deine Machine nutzt ChatGPT, um damit zu lesen und Entwürfe zu erstellen, und zwar über deinen eigenen ChatGPT-Tarif. The Machine hat keine eigene KI: Anfragen gehen direkt an OpenAI, über dein Konto und gemäß deren Nutzungsbedingungen.

## Anmelden

Klicke auf einer gehosteten Machine auf deiner Einrichtungsseite auf **Mit ChatGPT anmelden** und gib den Code, den ChatGPT anzeigt, dort ein. Später abgemeldet? Klicke auf **ChatGPT erneut verbinden**.

Lehnt OpenAI den Code ab? Öffne deine [ChatGPT-Sicherheitseinstellungen](https://chatgpt.com/settings/security), scrolle ganz nach unten und aktiviere den Schalter „Gerätecode-Anmeldung für Codex, Excel, PowerPoint und Word aktivieren“. Gib den Code anschließend noch einmal ein.

Du siehst den Schalter nicht? Bei einem Arbeitskonto (Business, Enterprise oder Edu) muss dein ChatGPT-Admin ihn unter [Berechtigungen und Rollen](https://chatgpt.com/admin/permissions) unter „Codex and Work Local“ aktivieren.

Führe auf deinem eigenen Computer `openclaw models auth login` in einem Terminal aus.

## Nutzungslimits

Ein ChatGPT-Tarif hat ein 5-Stunden-Limit und ein Wochenlimit. Unter **Einstellungen** > **Modell** siehst du, wie viel von beiden Limits verbraucht ist und wann sie zurückgesetzt werden. Hintergrundaufgaben werden schon lange vor Erreichen eines Limits angehalten, damit genug Spielraum für deine eigenen Chats bleibt. Wenn ein Limit erreicht ist, wird oben im Dashboard angezeigt, wann es zurückgesetzt wird. Weitere Informationen findest du unter [Modell](model.md).

## ChatGPT-Skills importieren

Klicke unter **Einstellungen** > **Skills** auf **Importieren**, wähle **Aus ChatGPT** und klicke auf **Meine Skills finden**. Es werden nur die Anweisungen importiert. Weitere Informationen findest du unter [Skills](skills.md).

## Entfernen

Wähle auf deiner Einrichtungsseite ein anderes Modell aus. (Auf deinem eigenen Computer kannst du dich genauso bei einem anderen Anbieter anmelden.) Um den Zugriff auf OpenAI-Seite zu entziehen, melde dich in deinen ChatGPT-Sicherheitseinstellungen von der Sitzung ab.
