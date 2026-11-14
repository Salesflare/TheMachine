---
title: Verbindungen
area: connections
summary: Deine Quellen an einem Ort: wie es jeder geht, eine neue hinzufügen oder eine trennen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Wie es ihnen geht

Der Tab **Verbindungen** listet deine Quellen nach Art (**E-Mail**, **Kalender**, **Chat** und mehr), unter einer Linie **Anmeldungen** und **Prüfungen**. Auf dem Handy öffnet ein Tipp eine Art, **Verbindungen** führt zurück. Jede Quelle ist eine Zeile; ein Tipp öffnet ihre Karte. Jede zeigt, wie es ihr geht: Verbunden, Wartet auf die erste Synchronisierung, Verbindet sich automatisch neu oder Braucht deine Hilfe. Öffne **Details** für **Letzte Syncs**, wo ihre Synchronisierung in einfachen Worten steht (etwa „Auf dem neuesten Stand“ oder „Erstes Lesen“), und was zu tun ist.

Ein fehlgeschlagener Sync, den ein späterer ausgeglichen hat, steht in Grau; nur ein Fehler, der noch der letzte ist, steht als Problem da, mit dem Zeitpunkt des nächsten Versuchs.

Ihre Zahlen zeigen alles, was sie hereingeholt hat, auch ihren [Verlauf](history.md), was in den letzten 24 Std. dazukam und was noch nicht geprüft ist. Ein Kalender zählt Termine: alle, die der nächsten 7 Tage und der letzten 24 Std.

Jede Quelle heißt wie ihr Konto, so wie der Dienst es nennt: deine Adresse, ein X-Profil, ein Slack-Workspace oder wem das Signal oder Telegram gehört. Darunter steht **Arbeit** oder **Privat**, dazu die Adresse oder der Handle, wenn der Name sie noch nicht nennt. Haben zwei Quellen auf einem Tab denselben Namen, steht bei jeder auch, was sie unterscheidet, etwa Slack oder X oder die Adresse des Workspace.

Unter dem Status sagt jede Quelle in einer Zeile, was sie hereinholt, und wenn sie etwas tun kann, dass sie es erst tut, wenn du auf **Senden** drückst oder zustimmst.

## Eine hinzufügen

Öffne ihre Art und wähle eine Quelle unter **Weitere hinzufügen**, oder unter der Liste, wenn noch keine verbunden ist. Sie zeigt ein kurzes Formular, wie auf deiner Einrichtungsseite: was sie braucht (einen Schlüssel, eine Adresse), und **Arbeit** mit ihrer Firma oder **Privat**. Tippe auf **Verbinden**. Eine Quelle mit Anmeldung, etwa LinkedIn oder X, öffnet ihre Anmeldung auf deiner Machine und macht von selbst weiter, sobald du drin bist. GitHub, WhatsApp und Codex zeigen einen Code zum Eingeben, und Telegram-Chats einen QR-Code zum Scannen.

Die Liste ist gruppiert (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**), von A bis Z in jeder Gruppe. Ein Sammeleintrag wie **Andere E-Mail** steht zuletzt in seiner Gruppe.

**Vorgeschlagen für dich** steht oben, wenn deine Machine einen Grund für eine Quelle sieht, mit diesem Grund in einer Zeile: Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine Einrichtung, die nicht abgeschlossen wurde. Die Quelle bleibt auch in ihrer eigenen Gruppe, als **Vorgeschlagen** markiert. Sie zählt das auf deiner Machine; nichts verlässt sie. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams steht zweimal da: unter **Chat** für die Chats und unter **Meetings** als **Teams-Meetings** für die Meeting-Notizen. Beide nutzen dieselbe Microsoft-Anmeldung, also verbindet eine auch die andere.

Eine Quelle, die du schon verbunden hast, zeigt das in der Liste, mit ihrem Konto. Wähl sie, um eine weitere daneben hinzuzufügen: ihr Formular sagt das und verlinkt die bestehende.

**Abbrechen** beendet das Hinzufügen. Vorher weggegangen? Öffne **Verbindungen** wieder, auf jedem Gerät, und es geht beim selben Schritt weiter. Sobald sie verbunden ist, liest deine Machine sie sofort und öffnet die neue Karte. Die zeigt, wie die erste Synchronisierung läuft.

Auf einer gehosteten Machine meldest du dich hier bei Google, Microsoft, Microsoft OneDrive, Zoom, Stripe und Intercom an: Wähle **Arbeit** oder **Privat**, tippe auf **Anmelden**, und du kommst zurück zu diesem Formular, das zeigt, wie das Verbinden läuft oder warum es nicht geklappt hat. GitHub, WhatsApp, Codex, Telegram-Chats und dein Android-Handy zeigen ihren Code direkt in diesem Formular. Die Kachel von Codex zeigt, ob Codex angemeldet ist.

**Neu verbinden** bei einer Quelle und in **Braucht dich** öffnet dasselbe Formular. Auf deinem eigenen Computer macht `assistant connect` dasselbe im Terminal.

## Arbeit oder privat

Jede Quelle zählt als Arbeit (für eine Firma, die du nennst) oder als privat. Das änderst du unter **Details**. Dort steht nur dann **Geraten**, wenn deine Machine es anhand der Adresse gewählt hat. Sobald du wählst, gilt deine Wahl. Arbeitsaufgaben warten auf deine Arbeitstage.

Mail und Kalender von Google und Microsoft richten sich nach ihrer Adresse, wenn sie eindeutig ist: ein Mailanbieter wie Gmail oder Outlook.com ist Privat, die Domain deines Teams ist Arbeit. Sonst fragt sie einmal, direkt nach der Anmeldung. Mit **Ändern** legst du es selbst fest. Sagt die Mail danach das Gegenteil, fragt die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du es ändern willst.

## Fähigkeiten

Eine Quelle kann Signale bringen (was hereinkommt, wird zu Aufgaben), Dinge für deine Aufgaben tun (ein Dokument lesen, wenn eine es braucht, oder nach deinem OK etwas senden, beantworten oder ändern) oder beides. Mit beidem hat **Details** für jede einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Einer bleibt an. Um beides zu stoppen, trenne die Quelle. Die Antworten eines Chats beziehen sich auf das, was er bringt, deshalb hat ein Chat nur **Kann Dinge tun**.

Mit **Bringt Signale** aus synchronisiert sie nicht, und ihre Karte zeigt keine Zahlen. Mit **Kann Dinge tun** aus liest deine Machine damit nie etwas auf Abruf, entwirft nichts und ändert nichts. Quellen von früher haben beides an.

## Eine entfernen

Öffne die Quelle, **Details**, dann **Trennen**. Sie hört auf zu lesen. Was sie schon reingebracht hat, bleibt. Auf einer gehosteten Machine zeigen Google, Microsoft, Microsoft OneDrive, Zoom und Stripe **Trennen ↗**, das deine Einrichtungsseite öffnet.

**Kürzlich getrennt** listet die Konten bei Google, Microsoft, Zoom, Slack, Stripe und Salesforce, die du in den letzten 30 Tagen entfernt hast, und wann. Ein Google-Konto steht nur einmal da, auch wenn Google Meet oder Docs eine eigene Anmeldung hatten. Jedes steht unter seiner eigenen Art: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Websites, die der Browser deiner Machine nutzt, etwa LinkedIn oder X, können eine Anmeldung speichern: Setz beim Anmelden ein Häkchen bei **Für nächstes Mal speichern**. Dann listet **Anmeldungen** sie auf. Wenn eine Website deine Machine abmeldet, meldet sie sich mit einem Tippen wieder an. Passwörter bleiben verschlüsselt auf deiner Machine. **Vergessen** entfernt eine gespeicherte Anmeldung.

## Prüfungen

**Prüfungen** zeigt, wie deine Machine liest, was reinkommt: letzte Durchläufe und was jeder gefunden hat. Siehe [Keine neuen Aufgaben](reviews-paused.md).

Jede Verbindung hat in diesem Bereich einen eigenen Artikel, mit dem, was sie liest und was sie senden kann.
