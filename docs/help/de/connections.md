---
title: Verbindungen
area: connections
summary: Alle deine Quellen an einem Ort: Status prüfen, neue Quellen hinzufügen oder Verbindungen trennen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 0896d8f689ca9699
---
## Status deiner Quellen

Der Tab **Verbindungen** listet deine Quellen nach Art auf. Darunter findest du **Anmeldungen** und **Prüfungen**, abgetrennt durch eine Linie. Auf dem Handy tippst du auf eine Art, um sie zu öffnen, und auf **Verbindungen**, um zurückzugehen. Eine Art mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle wird als Zeile angezeigt: mit ihrem Status (Verbunden, wartet auf den ersten Sync, verbindet sich automatisch neu oder braucht deine Hilfe) und den zuletzt eingegangenen Daten. Tippe auf die Quelle, um ihre Karte und **Details** zu öffnen.

Ein fehlgeschlagener Sync, den ein späterer Sync ausgeglichen hat, wird grau angezeigt. Nur ein Fehler, der weiterhin der neueste ist, wird als Problem angezeigt, zusammen mit dem Zeitpunkt des nächsten Versuchs.

Die Zähler zeigen alles, was die Quelle eingebracht hat, auch ihren [Verlauf](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender zählen sie die Termine.

Jede Quelle trägt den Namen ihres Kontos, so wie der jeweilige Dienst ihn angibt: deine Adresse, ein X-Profil, ein Slack-Arbeitsbereich oder die Person, zu der Signal oder Telegram gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat**. Dazu kommt die Adresse oder der Benutzername, wenn der Name das noch nicht erkennen lässt. Haben zwei Quellen derselben Art denselben Namen, wird außerdem angezeigt, woran du sie unterscheiden kannst, zum Beispiel Slack oder X, oder die Adresse des Arbeitsbereichs.

Zu jeder Quelle steht außerdem in einer Zeile, was sie einbringt und, falls sie Aktionen ausführen kann, dass sie erst handelt, wenn du auf **Senden** tippst oder die Aktion bestätigst.

## Quelle hinzufügen

Öffne eine Art (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Wenn noch keine Quelle verbunden ist, findest du die Auswahl unter der Liste. Am Ende steht jeweils eine Option für weitere Quellen: **Andere E-Mail** unter E-Mail sowie **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Termine und ist deshalb unter Kalender aufgeführt.

Wenn deine Machine einen Grund für eine Quelle erkennt, wird oben in **Verbindungen** der Bereich **Für dich vorgeschlagen** angezeigt. Der Grund steht jeweils in einer Zeile: E-Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt außerdem in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** markiert. Diese Daten werden auf deiner Machine gezählt und verlassen sie nicht. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams wird zweimal angezeigt: unter **Chat** für Chats und unter **Meetings** als **Teams-Meetings** für Meeting-Notizen. Beide verwenden dieselbe Microsoft-Anmeldung. Wenn du eine verbindest, wird also auch die andere verbunden.

Eine bereits verbundene Quelle ist in der Liste mit ihrem Konto gekennzeichnet. Wähle sie aus, um eine weitere Quelle desselben Typs hinzuzufügen. Im Formular steht das ebenfalls und es enthält einen Link zur bereits verbundenen Quelle.

Gib die erforderlichen Daten ein, etwa einen Schlüssel oder eine Adresse, wähle **Arbeit** mit dem Namen deines Unternehmens oder **Privat** und tippe auf **Verbinden**. Bei E-Mail-Adressen und Kalendern wird nur dann gefragt, wenn sich die Auswahl nicht aus der Adresse ergibt. Bei Websites wie LinkedIn oder X wird die Anmeldung im Browser deiner Machine geöffnet. Sobald du angemeldet bist, geht es automatisch weiter. GitHub, WhatsApp und Codex zeigen einen Code zum Eingeben an, Telegram-Chats und Signal-Chats einen QR-Code zum Scannen.

Mit **Abbrechen** beendest du das Hinzufügen. Hast du den Vorgang vor dem Abschluss verlassen? Öffne **Verbindungen** einfach wieder auf einem beliebigen Gerät. Der Vorgang wird an derselben Stelle fortgesetzt. Sobald die Quelle verbunden ist, beginnt deine Machine sofort, sie auszulesen, und zeigt den Status des ersten Syncs an.

Auf einer gehosteten Machine meldest du dich direkt hier bei Quellen an, die eine eigene Anmeldung haben: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und tippe auf die Anmeldeschaltfläche, zum Beispiel **Mit Google anmelden**. Danach kehrst du zu diesem Formular zurück, das dir den Status anzeigt. GitHub, WhatsApp, Codex, Telegram-Chats und dein Android-Handy zeigen ihren Code ebenfalls hier an.

Auf deinem eigenen Computer meldest du dich bei denselben Quellen an, sobald deine Machine mit deinem Konto verbunden ist. Tippe beim ersten Mal auf **Diese Machine koppeln**. Bei einigen Quellen gibt es auch eine andere Möglichkeit, zum Beispiel eine eigene App oder einen Schlüssel.

**Neu verbinden** bei einer Quelle oder unter **Braucht dich** öffnet dasselbe Formular. Auf deinem eigenen Computer bewirkt `assistant connect` dasselbe in einem Terminal.

## Arbeit oder privat

Jede Quelle wird als Arbeit (für ein Unternehmen, das du angibst) oder privat eingestuft. Du kannst das unter **Details** ändern. **Abgeleitet** bedeutet, dass deine Machine die Einstufung anhand der Adresse vorgenommen hat. Aufgaben für die Arbeit warten bis zu deinen Arbeitstagen.

Bei E-Mails und Kalendern von Google und Microsoft ergibt sich die Einstufung automatisch aus der Adresse, wenn sie eindeutig ist: Ein E-Mail-Anbieter wie Gmail oder Outlook.com bedeutet Privat, die Domain deines Teams bedeutet Arbeit. Andernfalls wirst du einmal direkt nach der Anmeldung gefragt. Mit **Ändern** legst du die Einstufung selbst fest. Falls eine spätere E-Mail auf die andere Einstufung hindeutet, fragt dich die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du sie ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen, aus denen Aufgaben entstehen, Aktionen für deine Aufgaben ausführen (ein Dokument lesen oder nach deiner Bestätigung etwas senden, beantworten oder ändern) oder beides. Wenn beides möglich ist, gibt es unter **Details** jeweils einen Schalter: **Liefert Signale** und **Kann Dinge tun**. Einer der Schalter muss eingeschaltet bleiben. Wenn du beide ausschalten möchtest, trenne die Verbindung. Bei einem Chat gibt es nur **Kann Dinge tun**.

Wenn **Liefert Signale** ausgeschaltet ist, wird die Quelle nicht synchronisiert. Wenn **Kann Dinge tun** ausgeschaltet ist, liest, entwirft oder ändert deine Machine damit nichts.

## Quelle entfernen

Öffne die Quelle und dann **Details** und tippe auf **Trennen**. Die Quelle wird nicht mehr ausgelesen. Bereits eingegangene Daten bleiben erhalten. Auf einer gehosteten Machine wird bei einer Quelle, deren Anmeldung auf deiner Einrichtungsseite gespeichert ist (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** werden Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten aufgeführt, die du in den letzten 30 Tagen entfernt hast, zusammen mit dem jeweiligen Zeitpunkt. Bis der Dienst die Trennung bestätigt, steht dort „Ausstehend“ und es wird weiter versucht. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Docs eine eigene Anmeldung hatte. Jedes Konto erscheint unter seiner jeweiligen Art: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Bei Websites wie LinkedIn oder X kannst du bei der Anmeldung **Für nächstes Mal speichern** aktivieren. Unter **Anmeldungen** werden sie dann aufgeführt. Wenn eine Website deine Machine abmeldet, kann sie sich mit einem Tippen wieder anmelden. Passwörter bleiben auf deiner Machine verschlüsselt. Mit **Vergessen** entfernst du eine Anmeldung.

Eine Website kann mehrere Konten haben, zum Beispiel **Arbeit** und **Privat**. **Speichern unter** übernimmt zunächst die Einstufung der Aufgabe. Mit **Anderer Name …** kannst du einen eigenen Namen vergeben. Eine Aufgabe meldet sich mit dem passenden Konto an. Wenn nicht klar ist, welches Konto passt, fragt der Dialog einmal nach und merkt sich die Auswahl für diese Aufgabe.

Unter **Anmeldungen** wird jede Website einmal mit den zugehörigen Konten aufgeführt: mit dem Benutzernamen und einem Menü, in dem die Einstufung steht. Du kannst die Einstufung dort jederzeit ändern. Bei Anmeldungen, die gespeichert wurden, bevor es Konten gab, steht **Arbeit oder privat?**, bis du eine Auswahl triffst. Eine Aufgabe, die diese Anmeldung verwendet hat, wählt nach einer Änderung der Einstufung erneut ein Konto aus.

Mit **Importieren** importierst du Anmeldungen aus einem Passwortmanager. Wähle einen aus:

- **LastPass**, **Bitwarden** oder **Google Passwortmanager**: Die Exportseite des jeweiligen Dienstes wird im Browser deiner Machine geöffnet und direkt im Dialog angezeigt, wie bei **Ausführen** für eine Aufgabe. Melde dich dort an. Deine Machine klickt sich dann bis zum Export durch. In einer Zeile steht, was du noch tun musst, zum Beispiel dein Masterpasswort eingeben. LastPass schickt dir einen Link, um den Export zu bestätigen. Deine Machine startet den Export einmal und öffnet den Link selbst, wenn die E-Mail innerhalb von 10 Minuten in einem verbundenen Postfach ankommt. Andernfalls wirst du aufgefordert, den Export noch einmal zu bestätigen und zu starten. Auf einem Handy wird die Ansicht zu der Stelle vergrößert, an der du etwas eingeben musst. Sieht die Seite anders aus als erwartet, werden stattdessen die Schritte zum manuellen Abschluss angezeigt. Deine Machine übernimmt die Datei, liest sie einmal aus und löscht sie.
- **1Password**: Exportiere eine CSV-Datei aus der 1Password-App auf einem Computer und wähle die Datei aus. Wenn `op` von 1Password auf deiner Machine angemeldet ist, wird die Datei stattdessen von dort eingelesen (auch `lpass` von LastPass).
- **Aus einer Exportdatei**: eine CSV-Datei aus 1Password, LastPass, Bitwarden oder Chrome. Lösche sie, sobald du fertig bist.

Wähle anschließend aus, welche Anmeldungen du behalten möchtest. Deine Machine meldet sich nie für dich bei deinem Passwortmanager an, gibt dein Masterpasswort nie ein und liest es nie aus. Sie zeigt der Assistentin auch nie die Seite. Du gibst das Passwort selbst auf der Seite ein.

Eine gespeicherte Anmeldung wird nur für die zugehörige Webadresse verwendet: dieselbe Website, `https` und derselbe Port. Nicht für eine ähnlich aussehende Adresse und nicht für eine andere Subdomain.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Daten ausliest: die letzten Prüfungen und was dabei gefunden wurde. Siehe [Keine neue Aufgabe](reviews-paused.md).

Zu jeder Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin steht, was sie ausliest und was sie senden kann.
