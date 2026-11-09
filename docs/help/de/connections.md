---
title: Verbindungen
area: connections
summary: Deine Quellen an einem Ort: wie es jeder geht, eine neue hinzufügen oder eine trennen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Wie es ihnen geht

Der Tab **Verbindungen** gruppiert deine Quellen in **Mail und Kalender**, **Chat** und **Andere Quellen**. Jede zeigt, wie es ihr geht: Verbunden, Wartet auf die erste Synchronisierung, Verbindet sich automatisch neu oder Braucht deine Hilfe. Öffne **Details** für **Letzte Syncs**, wo ihre Synchronisierung in einfachen Worten steht (etwa „Auf dem neuesten Stand“ oder „Erstes Lesen“), und was zu tun ist.

Ihre Zahlen zeigen, was sie hereingeholt hat, was in den letzten 24 Std. dazukam und was noch nicht geprüft ist. Ein Kalender zählt Termine: alle, die der nächsten 7 Tage und der letzten 24 Std.

Unter dem Status sagt jede Quelle in einer Zeile, was sie hereinholt, und wenn sie etwas tun kann, dass sie es erst tut, wenn du auf **Senden** drückst oder zustimmst.

## Eine hinzufügen

Öffne **+ Hinzufügen** und wähle eine Quelle. Sie zeigt ein kurzes Formular, wie auf deiner Einrichtungsseite: was sie braucht (einen Schlüssel, eine Adresse), und **Arbeit** mit ihrer Firma oder **Privat**. Tippe auf **Verbinden**. Eine Quelle mit Anmeldung, etwa LinkedIn oder X, öffnet ihre Anmeldung auf deiner Machine und macht von selbst weiter, sobald du drin bist. GitHub, WhatsApp und Codex zeigen einen Code zum Eingeben, und Telegram-Chats einen QR-Code zum Scannen.

Die Liste ist gruppiert (**Mail und Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**), von A bis Z in jeder Gruppe.

**Vorgeschlagen für dich** steht oben, wenn deine Machine einen Grund für eine Quelle sieht, mit diesem Grund in einer Zeile: Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine Einrichtung, die nicht abgeschlossen wurde. Sie zählt das auf deiner Machine; nichts verlässt sie. Kein Grund, kein Abschnitt. Eine verbundene Quelle wird nie vorgeschlagen.

Eine Quelle, die du schon verbunden hast, zeigt das in der Liste, mit ihrem Konto. Wähl sie, um eine weitere daneben hinzuzufügen: ihr Formular sagt das und verlinkt die bestehende.

**Abbrechen** beendet das Hinzufügen. Vorher weggegangen? Öffne **Verbindungen** wieder, auf jedem Gerät, und es geht beim selben Schritt weiter. Sobald sie verbunden ist, startet deine Machine neu, um sie zu lesen, und öffnet dann die neue Karte. Die zeigt, wie die erste Synchronisierung läuft.

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

**Kürzlich getrennt** listet Anmeldungen bei Google, Microsoft und Zoom, die du entfernt hast. **Entfernt, bestätigt** heißt, dass Google die Abmeldung bestätigt hat, oder bei Microsoft und Zoom, dass keine Kopie mehr übrig ist. **Ausstehend** sagt, warum, und deine Machine versucht es weiter.

## Gespeicherte Anmeldungen

Websites, die der Browser deiner Machine nutzt, etwa LinkedIn oder X, können eine Anmeldung speichern: Setz beim Anmelden ein Häkchen bei **Für nächstes Mal speichern**. Dann listet **Anmeldungen** sie auf. Wenn eine Website deine Machine abmeldet, meldet sie sich mit einem Tippen wieder an. Passwörter bleiben verschlüsselt auf deiner Machine. **Vergessen** entfernt eine gespeicherte Anmeldung.

## Prüfungen

**Prüfungen** zeigt, wie deine Machine liest, was reinkommt: letzte Durchläufe und was jeder gefunden hat. Siehe [Keine neuen Aufgaben](reviews-paused.md).

Jede Verbindung hat in diesem Bereich einen eigenen Artikel, mit dem, was sie liest und was sie senden kann.
