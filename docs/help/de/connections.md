---
title: Verbindungen
area: connections
summary: Deine Quellen an einem Ort: So geht es jeder einzelnen, wie du eine neue hinzufügst oder eine trennst.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 38d682b69cab758d
---
## So geht es ihnen

Im Tab **Verbindungen** werden deine Quellen nach Kategorien aufgeführt. Darunter findest du **Anmeldungen** und **Prüfungen**. Auf dem Smartphone tippst du auf eine Kategorie, um sie zu öffnen, und auf **Verbindungen**, um zurückzugehen. Eine Kategorie mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle erscheint in einer Zeile: mit ihrem Status (Verbunden, Wartet auf den ersten Abgleich, Verbindet sich automatisch neu oder Braucht deine Hilfe) und den zuletzt eingegangenen Daten. Tippe auf die Quelle, um ihre Karte und **Details** zu öffnen.

Ein fehlgeschlagener Abgleich, der bei einem späteren Abgleich nachgeholt wurde, wird grau angezeigt. Nur ein Fehler, der weiterhin der letzte Abgleich ist, wird als Problem angezeigt, zusammen mit dem Zeitpunkt des nächsten Versuchs.

Die Anzahl zeigt alles, was die Quelle eingebracht hat, einschließlich des [Verlaufs](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender werden die Termine gezählt.

Jede Quelle trägt den Namen ihres Kontos, so wie der Dienst es benennt: deine Adresse, ein X-Profil, ein Slack-Arbeitsbereich oder die Person, der das Signal- oder Telegram-Konto gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat** und außerdem die Adresse oder der Benutzername, falls der Name das noch nicht verrät. Haben zwei Quellen derselben Kategorie denselben Namen, steht zusätzlich dabei, woran du sie unterscheiden kannst, zum Beispiel Slack oder X oder die Adresse des Arbeitsbereichs.

Jede Quelle beschreibt außerdem in einer Zeile, was sie einbringt und, falls sie Aktionen ausführen kann, dass sie erst nach deinem Tippen auf **Senden** oder deiner Bestätigung handelt.

## Quelle hinzufügen

Öffne eine Kategorie (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Wenn noch keine verbunden ist, findest du die Auswahl unter der Liste. Zuletzt kommt jeweils eine Auffangkategorie: **Andere E-Mail** unter E-Mail sowie **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Meetings und steht deshalb unter Kalender.

**Vorgeschlagen für dich** erscheint oben in **Verbindungen**, wenn deine Machine einen Grund für eine Quelle erkennt. Der Grund steht in einer Zeile: E-Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt auch in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** markiert. Diese Vorschläge werden auf deiner Machine ermittelt. Nichts davon verlässt sie. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams wird zweimal angezeigt: unter **Chat** für Chats und unter **Meetings** als **Teams-Meetings** für Meeting-Notizen. Beide verwenden dieselbe Microsoft-Anmeldung. Wenn du die eine verbindest, wird also auch die andere verbunden.

Eine bereits verbundene Quelle ist in der Liste mit ihrem Konto gekennzeichnet. Wähle sie aus, um eine weitere daneben hinzuzufügen. Im Formular steht das ebenfalls, und es verlinkt auf die bereits verbundene Quelle.

Gib die erforderlichen Angaben ein, zum Beispiel einen Schlüssel oder eine Adresse, wähle **Arbeit** mit dem Namen deines Unternehmens oder **Privat** aus (bei E-Mail und Kalender wirst du nur gefragt, wenn die Adresse keine eindeutige Zuordnung erlaubt) und tippe auf **Verbinden**. Bei Websites wie LinkedIn oder X öffnet sich die Anmeldung im Browser deiner Machine. Sobald du angemeldet bist, wird der Vorgang automatisch fortgesetzt. GitHub, WhatsApp und Codex zeigen einen Code an, den du eingeben musst. Für Telegram-Chats und Signal-Chats wird ein QR-Code zum Scannen angezeigt.

Mit **Abbrechen** wird das Hinzufügen beendet. Hast du die Seite verlassen, bevor der Vorgang abgeschlossen war? Öffne **Verbindungen** einfach wieder, auf einem beliebigen Gerät. Der Vorgang wird an derselben Stelle fortgesetzt. Sobald die Quelle verbunden ist, beginnt deine Machine sofort, sie auszulesen, und zeigt den Status des ersten Abgleichs an.

Auf einer gehosteten Machine meldest du dich für Quellen mit eigener Anmeldung direkt hier an: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und tippe auf die Schaltfläche zur Anmeldung, zum Beispiel **Mit Google anmelden**. Du kehrst zu diesem Formular zurück, wo du siehst, ob die Anmeldung geklappt hat. Auch GitHub, WhatsApp, Codex, Telegram-Chats und dein Android-Smartphone zeigen ihren Code hier an.

Auf deinem eigenen Computer meldest du dich bei denselben Quellen an, sobald deine Machine mit deinem Konto gekoppelt ist. Tippe beim ersten Mal auf **Diese Machine verbinden**. Bei manchen gibt es auch eine andere Möglichkeit, etwa über deine eigene App oder einen Schlüssel.

**Neu verbinden** bei einer Quelle und unter **Braucht dich** öffnet dasselbe Formular. Auf deinem eigenen Computer macht `assistant connect` dasselbe in einem Terminal.

## Arbeit oder privat

Jede Quelle wird als Arbeit (für ein Unternehmen, das du angibst) oder privat eingestuft. Du kannst die Zuordnung unter **Details** ändern. **Geschätzt** bedeutet, dass deine Machine die Zuordnung anhand der Adresse vorgenommen hat. Aufgaben für die Arbeit warten bis zu deinen Arbeitstagen.

Bei Google- und Microsoft-E-Mails und -Kalendern wird die Zuordnung anhand der Adresse vorgenommen, wenn sie eindeutig ist: Ein E-Mail-Anbieter wie Gmail oder Outlook.com bedeutet „Privat“, die Domain deines Teams bedeutet „Arbeit“. Andernfalls wirst du direkt nach der Anmeldung einmal gefragt. Mit **Ändern** legst du die Zuordnung selbst fest. Wenn die E-Mails später auf das jeweils andere hindeuten, fragt dich die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du die Zuordnung ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen (Eingänge werden zu Aufgaben), Aktionen für deine Aufgaben ausführen (ein Dokument lesen oder nach deiner Bestätigung etwas senden, beantworten oder ändern) oder beides. Wenn sie beides kann, findest du unter **Details** für jede Funktion einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Eine der beiden Funktionen bleibt immer eingeschaltet. Um beide zu beenden, musst du die Quelle trennen. Bei einem Chat gibt es nur **Kann Dinge tun**.

Wenn **Bringt Signale** ausgeschaltet ist, wird die Quelle nicht abgeglichen. Wenn **Kann Dinge tun** ausgeschaltet ist, liest, entwirft oder ändert deine Machine damit nichts.

## Quelle entfernen

Öffne die Quelle und dann **Details**. Tippe anschließend auf **Trennen**. Die Quelle wird nicht mehr ausgelesen. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine wird bei Quellen, deren Anmeldung auf deiner Einrichtungsseite verwaltet wird (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** werden Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten angezeigt, die du in den letzten 30 Tagen entfernt hast, einschließlich des Zeitpunkts. Solange der Dienst die Trennung noch nicht bestätigt hat, steht dort „Ausstehend“, und deine Machine versucht es weiter. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Docs eine eigene Anmeldung hatten. Jedes Konto erscheint unter seiner eigenen Kategorie: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Wenn du dich bei Websites wie LinkedIn oder X anmeldest, setze ein Häkchen bei **Für nächstes Mal speichern**. Die Anmeldung erscheint dann unter **Anmeldungen**. Wenn eine Website deine Machine abmeldet, meldet sie sich mit einem Tippen wieder an. Passwörter bleiben verschlüsselt auf deiner Machine. Mit **Vergessen** entfernst du eine Anmeldung.

Eine Website kann mehrere Konten haben, zum Beispiel **Arbeit** und **Privat**. **Speichern unter** beginnt mit der Zuordnung der Aufgabe. Mit **Anderer Name …** kannst du einen eigenen Namen vergeben. Eine Aufgabe meldet sich mit dem passenden Konto an. Wenn das nicht eindeutig ist, fragt der Dialog einmal, welches Konto verwendet werden soll, und merkt sich deine Auswahl für diese Aufgabe.

Unter **Anmeldungen** wird jede Website einmal aufgeführt, mit ihren Konten darunter: dem Benutzernamen und einem Menü mit der jeweiligen Zuordnung. Du kannst die Zuordnung dort jederzeit ändern. Bei Anmeldungen, die gespeichert wurden, bevor es Konten gab, wird **Arbeit oder privat?** angezeigt, bis du eine Zuordnung auswählst. Wenn du die Zuordnung änderst, wählt eine Aufgabe, die diese Anmeldung verwendet hat, erneut ein Konto aus.

Mit **Importieren** kannst du Anmeldungen aus einem Passwortmanager übernehmen. Wähle einen aus:

- **LastPass**, **Bitwarden** oder **Google Passwortmanager**: Die Exportseite öffnet sich im Browser deiner Machine. Melde dich dort an. Deine Machine navigiert dann zum Export. In einer Zeile steht, was du noch tun musst, zum Beispiel dein Master-Passwort eingeben. Auf einem Smartphone wird die Ansicht auf das Eingabefeld vergrößert. Sieht die Seite anders aus als erwartet, werden stattdessen die Schritte zum manuellen Abschließen angezeigt. Deine Machine übernimmt die Datei, liest sie einmal aus und löscht sie.
- **1Password**: Exportiere eine CSV-Datei aus der 1Password-App auf einem Computer und wähle sie anschließend aus. Wenn `op` von 1Password auf deiner Machine angemeldet ist, liest sie die Daten stattdessen von dort aus (bei `lpass` von LastPass ebenso).
- **Aus einer Exportdatei**: eine CSV-Datei von 1Password, LastPass, Bitwarden oder Chrome. Lösche die Datei anschließend.

Setze danach ein Häkchen bei den Anmeldungen, die du behalten möchtest. Deine Machine meldet sich nie für dich bei deinem Passwortmanager an, gibt dein Master-Passwort nie ein und liest es nie aus. Außerdem zeigt sie der Assistentin nie die Seite an. Du gibst das Passwort selbst auf der Seite ein.

Eine gespeicherte Anmeldung wird nur für ihre eigene Webadresse verwendet: dieselbe Website, `https` und derselbe Port. Nicht für eine ähnlich aussehende Adresse und nicht für eine andere Subdomain.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Daten ausliest: die letzten Prüfungen und was dabei gefunden wurde. Weitere Informationen findest du unter [Keine neuen Aufgaben](reviews-paused.md).

Für jede Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin erfährst du, was die Verbindung ausliest und was sie senden kann.
