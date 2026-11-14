---
title: Verbindungen
area: connections
summary: Alle deine Quellen an einem Ort: Sieh, wie es ihnen geht, füge neue hinzu oder trenne eine Verbindung.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 60304f2504ee5676
---
## So geht es ihnen

Im Tab **Verbindungen** sind deine Quellen nach Art sortiert. Darunter findest du **Anmeldungen** und **Prüfungen**, jeweils durch eine Linie getrennt. Auf dem Handy tippst du auf eine Art, um sie zu öffnen, und auf **Verbindungen**, um zurückzugehen. Eine Art mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle wird als Zeile angezeigt: mit ihrem Status (Verbunden, Wartet auf erste Synchronisierung, Verbindet sich automatisch neu oder Braucht deine Hilfe) und den zuletzt eingegangenen Inhalten. Tippe auf die Zeile, um die Karte und **Details** zu öffnen.

Ein fehlgeschlagener Abgleich, den ein späterer ausgeglichen hat, wird grau angezeigt. Nur ein Fehler, der noch aktuell ist, wird als Problem angezeigt, zusammen mit dem Zeitpunkt des nächsten Versuchs.

Die Anzahl umfasst alles, was die Quelle eingebracht hat, auch ihre [Verlaufseinträge](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender werden die Termine gezählt.

Jede Quelle ist nach ihrem Konto benannt, so wie es der jeweilige Dienst nennt: nach deiner Adresse, einem X-Profil, einem Slack-Arbeitsbereich oder danach, wem das Signal- oder Telegram-Konto gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat**, außerdem die Adresse oder der Benutzername, falls sie nicht bereits im Namen vorkommen. Haben zwei Quellen derselben Art denselben Namen, steht auch dabei, woran du sie unterscheiden kannst, zum Beispiel Slack oder X, oder die Adresse des Arbeitsbereichs.

Bei jeder Quelle steht außerdem in einer Zeile, was sie einbringt und, falls sie Aktionen ausführen kann, dass sie erst handelt, wenn du **Senden** drückst oder deine Zustimmung gibst.

## Quelle hinzufügen

Öffne eine Art (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Wenn noch keine verbunden ist, findest du die Auswahl unter der Liste. Als letzte Möglichkeit gibt es **Andere E-Mail** unter E-Mail sowie **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Meetings und ist deshalb unter Kalender zu finden.

**Vorgeschlagen für dich** wird oben in **Verbindungen** angezeigt, wenn deine Machine einen Grund für eine Quelle erkennt. Der Grund steht in einer Zeile, zum Beispiel E-Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt auch in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** markiert. Deine Machine zählt diese Vorschläge auf deiner Machine. Nichts davon verlässt sie. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams wird zweimal angezeigt: unter **Chat** für die Chats und unter **Meetings** als **Teams-Meetings** für die Meeting-Notizen. Beide verwenden dieselbe Microsoft-Anmeldung. Wenn du eine verbindest, wird auch die andere verbunden.

Eine Quelle, die du bereits verbunden hast, ist in der Liste mit ihrem Konto gekennzeichnet. Wähle sie aus, um eine weitere neben ihr hinzuzufügen. Im Formular steht, dass es um ein weiteres Konto geht, und es gibt einen Link zu deinem bereits verbundenen Konto.

Gib die erforderlichen Angaben ein, zum Beispiel einen Schlüssel oder eine Adresse. Wähle **Arbeit** mit dem Namen des Unternehmens oder **Privat**. Bei E-Mail und Kalender wirst du nur gefragt, wenn sich die Kategorie nicht aus der Adresse ergibt. Drücke dann **Verbinden**. Bei einer Website wie LinkedIn oder X wird die Anmeldung im Browser deiner Machine geöffnet. Sobald du angemeldet bist, geht es automatisch weiter. Bei GitHub, WhatsApp und Codex wird ein Code angezeigt, den du eingeben musst. Bei Telegram-Chats und Signal-Chats wird ein QR-Code zum Scannen angezeigt.

Mit **Abbrechen** brichst du das Hinzufügen ab. Hast du den Vorgang verlassen, bevor er abgeschlossen war? Öffne **Verbindungen** erneut, auf einem beliebigen Gerät. Der Vorgang wird beim selben Schritt fortgesetzt. Sobald die Verbindung hergestellt ist, beginnt deine Machine sofort, die Quelle zu lesen, und zeigt dir den Fortschritt der ersten Synchronisierung.

Auf einer gehosteten Machine kannst du dich hier bei Quellen anmelden, die eine eigene Anmeldung haben: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und drücke auf die Anmeldeschaltfläche, zum Beispiel **Mit Google anmelden**. Du kehrst zu diesem Formular zurück, das dir das Ergebnis anzeigt. Bei GitHub, WhatsApp, Codex, Telegram-Chats und deinem Android-Handy wird der Code ebenfalls hier angezeigt.

Auf deinem eigenen Computer meldest du dich bei denselben Quellen an, sobald deine Machine mit deinem Konto verbunden ist. Drücke beim ersten Mal auf **Diese Machine verbinden**. Für einige Quellen gibt es auch eine andere Möglichkeit, zum Beispiel eine eigene App oder einen Schlüssel.

Mit **Neu verbinden** bei einer Quelle oder unter **Braucht dich** öffnest du dasselbe Formular. Auf deinem eigenen Computer macht `assistant connect` dasselbe in einem Terminal.

## Beruflich oder privat

Jede Quelle ist entweder beruflich, für ein Unternehmen, das du angibst, oder privat. Du kannst die Einstellung unter **Details** ändern. **Geschätzt** bedeutet, dass deine Machine die Kategorie anhand der Adresse ausgewählt hat. Aufgaben für die Arbeit warten auf deine Arbeitstage.

Bei Google- und Microsoft-E-Mails und -Kalendern wird die Kategorie anhand der Adresse festgelegt, wenn sie eindeutig ist: Ein E-Mail-Anbieter wie Gmail oder Outlook.com bedeutet **Privat**, die Domain deines Teams bedeutet **Arbeit**. Andernfalls wirst du direkt nach der Anmeldung einmal gefragt. Mit **Ändern** legst du die Kategorie selbst fest. Wenn deine E-Mails später auf die andere Kategorie hindeuten, fragt dich die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du sie ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen, aus denen Aufgaben werden, Aktionen für deine Aufgaben ausführen, zum Beispiel ein Dokument lesen oder nach deiner Zustimmung etwas senden, beantworten oder ändern, oder beides. Wenn sie beides kann, findest du unter **Details** für jede Funktion einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Eine Funktion muss eingeschaltet bleiben. Um beide auszuschalten, trenne die Verbindung. Bei einem Chat gibt es nur **Kann Dinge tun**.

Wenn **Bringt Signale** ausgeschaltet ist, wird die Quelle nicht synchronisiert. Wenn **Kann Dinge tun** ausgeschaltet ist, liest, entwirft oder ändert deine Machine damit nichts.

## Quelle entfernen

Öffne die Quelle und wähle **Details** und dann **Trennen**. Sie wird nicht mehr gelesen. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine wird bei Quellen, deren Anmeldung auf deiner Einrichtungsseite verwaltet wird (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** findest du die Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten, die du in den letzten 30 Tagen entfernt hast, sowie den Zeitpunkt der Entfernung. Bis der Dienst die Trennung bestätigt, steht dort „Ausstehend“ und es wird weiter versucht. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Docs eine eigene Anmeldung hatte. Jedes Konto wird unter seiner eigenen Art angezeigt: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Bei Websites wie LinkedIn oder X kannst du bei der Anmeldung **Für nächstes Mal speichern** aktivieren. Unter **Anmeldungen** werden sie dann aufgelistet. Wenn eine Website deine Machine abmeldet, kannst du sie mit einem Tippen wieder anmelden. Passwörter bleiben auf deiner Machine verschlüsselt. Mit **Vergessen** entfernst du eine gespeicherte Anmeldung.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Inhalte liest: die letzten Prüfungen und was bei jeder davon gefunden wurde. Siehe [Keine neuen Aufgaben](reviews-paused.md).

Zu jeder Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin steht, was sie liest und was sie senden kann.
