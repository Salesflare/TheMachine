---
title: Verbindungen
area: connections
summary: Alle deine Quellen an einem Ort: Sieh, wie es ihnen geht, füge eine neue hinzu oder trenne eine Verbindung.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: ec53596a1636fee7
---
## So geht es deinen Quellen

Im Tab **Verbindungen** sind deine Quellen nach Typ aufgelistet. Darunter findest du **Anmeldungen** und **Prüfungen**. Auf dem Smartphone tippst du auf einen Typ, um ihn zu öffnen, und auf **Verbindungen**, um zurückzugehen. Ein Typ mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle hat eine eigene Zeile mit ihrem Status (Verbunden, Wartet auf erste Synchronisierung, Verbindet automatisch neu oder Deine Hilfe erforderlich) und den zuletzt eingegangenen Daten. Tippe auf eine Quelle, um ihre Karte und **Details** zu öffnen.

Ein fehlgeschlagener Abgleich, der bei einem späteren Versuch nachgeholt wurde, wird grau angezeigt. Nur ein Fehler, der weiterhin der letzte ist, wird als Problem angezeigt, zusammen mit dem Zeitpunkt des nächsten Versuchs.

Die Zahlen zeigen alles, was die Quelle eingebracht hat, einschließlich des [Verlaufs](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender werden die Termine gezählt.

Jede Quelle ist nach ihrem Konto benannt, so wie der jeweilige Dienst es benennt: nach deiner Adresse, einem X-Profil, einem Slack-Arbeitsbereich oder danach, zu wem das Signal oder Telegram gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat**, dazu die Adresse oder der Benutzername, falls der Name das nicht schon erkennen lässt. Haben zwei Quellen desselben Typs denselben Namen, steht auch dabei, woran du sie unterscheiden kannst, etwa Slack oder X, oder die Adresse des Arbeitsbereichs.

Bei jeder Quelle steht außerdem in einer Zeile, was sie einbringt und, falls sie Aktionen ausführen kann, dass sie das nur tut, wenn du auf **Senden** tippst oder die Aktion bestätigst.

## Quelle hinzufügen

Öffne einen Typ (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Wenn noch keine verbunden ist, kannst du sie auch unter der Liste auswählen. Am Ende findest du eine allgemeine Option: **Andere E-Mail** unter E-Mail sowie **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Besprechungen und ist deshalb unter Kalender zu finden.

Wenn deine Machine einen Grund für eine Quelle erkennt, wird oben in **Verbindungen** der Bereich **Vorgeschlagen für dich** angezeigt. Der Grund steht in einer Zeile, zum Beispiel E-Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt auch in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** gekennzeichnet. Diese Hinweise werden auf deiner Machine ermittelt. Es wird nichts von ihr übertragen. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams wird zweimal angezeigt: unter **Chat** für Chats und unter **Meetings** als **Teams-Meetings** für Besprechungsnotizen. Beide verwenden dieselbe Microsoft-Anmeldung. Wenn du eine verbindest, wird auch die andere verbunden.

In der Liste steht bei einer Quelle, die du schon verbunden hast, dass sie verbunden ist, sowie das zugehörige Konto. Wähle sie aus, um daneben ein weiteres Konto hinzuzufügen. Im Formular steht, dass du ein weiteres Konto hinzufügst, und es gibt einen Link zum bereits verbundenen Konto.

Gib die erforderlichen Angaben ein, etwa einen Schlüssel oder eine Adresse, wähle **Arbeit** und den zugehörigen Firmennamen oder **Privat** und tippe auf **Verbinden**. Bei Diensten wie LinkedIn oder X öffnet sich die Anmeldeseite im Browser deiner Machine. Sobald du angemeldet bist, geht es automatisch weiter. GitHub, WhatsApp und Codex zeigen einen Code an, den du eingeben musst. Für Telegram-Chats und Signal-Chats wird ein QR-Code zum Scannen angezeigt.

Mit **Abbrechen** brichst du das Hinzufügen ab. Hast du aufgehört, bevor der Vorgang abgeschlossen war? Öffne **Verbindungen** erneut, auf einem beliebigen Gerät. Der Vorgang wird an derselben Stelle fortgesetzt. Sobald die Quelle verbunden ist, beginnt deine Machine sofort, sie auszulesen, und zeigt dir den Status der ersten Synchronisierung.

Auf einer gehosteten Machine meldest du dich direkt hier bei Quellen an, für die eine eigene Anmeldung erforderlich ist: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und tippe auf die Schaltfläche zum Anmelden, zum Beispiel **Mit Google anmelden**. Danach kehrst du zu diesem Formular zurück, in dem der Status angezeigt wird. Für GitHub, WhatsApp, Codex, Telegram-Chats und dein Android-Smartphone wird der Code ebenfalls hier angezeigt.

Auf deinem eigenen Computer meldest du dich bei denselben Quellen an, sobald deine Machine mit deinem Konto verbunden ist. Tippe beim ersten Mal auf **Diese Machine verbinden**. Bei manchen Quellen gibt es noch eine andere Möglichkeit, zum Beispiel über deine eigene App oder einen Schlüssel.

Über **Neu verbinden** bei einer Quelle oder unter **Braucht dich** öffnest du dasselbe Formular. Auf deinem eigenen Computer bewirkt `assistant connect` dasselbe im Terminal.

## Arbeit oder privat

Jede Quelle ist entweder beruflich, also für ein von dir benanntes Unternehmen, oder privat. Du kannst das unter **Details** ändern. **Automatisch erkannt** bedeutet, dass deine Machine die Zuordnung anhand der Adresse vorgenommen hat. Aufgaben für die Arbeit werden an deinen Arbeitstagen fällig.

Bei Google- und Microsoft-E-Mails und -Kalendern wird die Zuordnung anhand der Adresse festgelegt, wenn sie eindeutig ist: Ein E-Mail-Anbieter wie Gmail oder Outlook.com gilt als privat, die Domain deines Teams als beruflich. Andernfalls wirst du direkt nach der Anmeldung einmal gefragt. Mit **Ändern** legst du die Zuordnung selbst fest. Falls eine spätere E-Mail auf die andere Zuordnung hindeutet, wirst du einmal über die Aufgabe **Hol mehr aus The Machine heraus** gefragt, ob du sie ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen, aus denen Aufgaben entstehen, Aktionen für deine Aufgaben ausführen, etwa ein Dokument lesen oder nach deiner Bestätigung etwas senden, beantworten oder ändern, oder beides. Wenn sie beides kann, findest du unter **Details** jeweils einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Einer der beiden Schalter muss eingeschaltet bleiben. Wenn du beide Funktionen beenden möchtest, trenne die Verbindung. Bei einem Chat gibt es nur **Kann Dinge tun**.

Wenn **Bringt Signale** ausgeschaltet ist, wird nichts synchronisiert. Wenn **Kann Dinge tun** ausgeschaltet ist, liest, entwirft oder ändert deine Machine damit nichts.

## Quelle entfernen

Öffne die Quelle und gehe zu **Details**. Tippe dann auf **Trennen**. Die Quelle wird nicht mehr ausgelesen. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine wird bei Quellen, deren Anmeldedaten auf deiner Einrichtungsseite hinterlegt sind (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** werden die Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten aufgeführt, die du in den letzten 30 Tagen entfernt hast, jeweils mit dem Zeitpunkt. Bis der Dienst die Trennung bestätigt, wird „Ausstehend“ angezeigt und der Vorgang weiter versucht. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Docs eine eigene Anmeldung hatte. Jedes Konto erscheint unter seinem eigenen Typ: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Wenn du dich bei Websites wie LinkedIn oder X anmeldest, aktiviere **Für nächstes Mal speichern**. Anschließend werden die Anmeldungen unter **Anmeldungen** aufgeführt. Wenn eine Website deine Machine abmeldet, kann sie sich mit einem Tipp wieder anmelden. Passwörter bleiben auf deiner Machine verschlüsselt. Mit **Vergessen** entfernst du eine Anmeldung.

Bei einer Website können mehrere Konten gespeichert sein, zum Beispiel **Arbeit** und **Privat**. **Speichern unter** wählt standardmäßig die Kategorie der Aufgabe aus. Über **Anderer Name …** kannst du einen eigenen Namen vergeben. Eine Aufgabe meldet sich mit dem passenden Konto an. Ist nicht klar, welches Konto passt, fragt der Dialog einmal nach und merkt sich deine Auswahl für diese Aufgabe.

Unter **Anmeldungen** wird jede Website einmal mit den zugehörigen Konten darunter aufgeführt. Anmeldungen, die gespeichert wurden, bevor es Konten gab, werden als **Standard** angezeigt, bis du ihnen dort eine Kategorie zuweist.

Mit **Importieren** kannst du Anmeldungen aus einem Passwortmanager übernehmen: über einen CSV-Export aus 1Password, LastPass, Bitwarden oder Chrome oder direkt aus 1Password und LastPass über deren Befehlszeilentools, wenn du auf diesem Computer dort angemeldet bist. Du wählst aus, welche Anmeldungen du behalten möchtest. Deine Machine meldet sich nie bei deinem Passwortmanager an und fragt nie nach seinem Master-Passwort. Lösche die Exportdatei, wenn du fertig bist.

Eine gespeicherte Anmeldung wird nur für die zugehörige Webadresse verwendet: dieselbe Website, `https` und derselbe Port. Nicht für eine ähnlich aussehende Adresse und nicht für eine andere Subdomain.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Daten ausliest: die letzten Prüfungen und was dabei gefunden wurde. Weitere Informationen findest du unter [Keine neuen Aufgaben](reviews-paused.md).

Für jede Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin erfährst du, was sie ausliest und was sie senden kann.
