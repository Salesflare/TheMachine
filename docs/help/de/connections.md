---
title: Verbindungen
area: connections
summary: Alle deine Quellen an einem Ort: Status prüfen, neue Quellen hinzufügen oder Verbindungen trennen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 809547189ccfa026
---
## So läuft es

Auf dem Tab **Verbindungen** sind deine Quellen nach Art sortiert. Darunter stehen **Anmeldungen** und **Prüfungen**, abgetrennt durch eine Linie. Auf dem Smartphone tippst du auf eine Art, um sie zu öffnen, und auf **Verbindungen**, um zurückzugehen. Eine Art mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle wird als Zeile angezeigt: mit ihrem Status (Verbunden, Erster Sync steht aus, Verbindung wird automatisch wiederhergestellt oder Deine Hilfe ist erforderlich) und den zuletzt eingegangenen Daten. Tippe auf die Zeile, um die Karte und **Details** zu öffnen.

Ein fehlgeschlagener Sync, der durch einen späteren ausgeglichen wurde, wird grau angezeigt. Nur ein Fehler, der weiterhin der neueste ist, wird als Problem angezeigt, zusammen mit dem Zeitpunkt des nächsten Versuchs.

Die Zähler zeigen alles, was die Quelle eingebracht hat, einschließlich des [Verlaufs](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender werden die Termine gezählt.

Jede Quelle wird nach dem Konto benannt, so wie der Dienst es nennt: deine Adresse, ein X-Profil, ein Slack-Arbeitsbereich oder die Person, zu der das Signal- oder Telegram-Konto gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat** sowie die Adresse oder der Benutzername, sofern das nicht schon aus dem Namen hervorgeht. Haben zwei Quellen derselben Art denselben Namen, steht zusätzlich dabei, woran du sie unterscheiden kannst, zum Beispiel Slack oder X oder die Adresse des Arbeitsbereichs.

Bei jeder Quelle steht außerdem in einer Zeile, was sie einbringt. Wenn sie auch Aktionen ausführen kann, steht dort, dass sie erst nach deinem Klick auf **Senden** oder deiner Bestätigung mit OK handelt.

## Quelle hinzufügen

Öffne eine Art (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Wenn noch keine verbunden ist, findest du die Auswahl unter der Liste. Am Ende steht jeweils eine allgemeine Option: **Andere E-Mail** unter E-Mail, **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Termine aus und steht deshalb unter Kalender.

**Vorgeschlagen für dich** erscheint oben auf **Verbindungen**, wenn deine Machine einen Grund für eine Quelle erkennt. Der Grund wird in einer Zeile genannt: E-Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt auch in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** markiert. Diese Vorschläge werden auf deiner Machine ermittelt. Dabei wird nichts von deiner Machine übertragen. Eine bereits verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams wird zweimal angezeigt: unter **Chat** für die Chats und unter **Meetings** als **Teams-Meetings** für die Besprechungsnotizen. Für beide wird dieselbe Microsoft-Anmeldung verwendet. Wenn du eine verbindest, wird die andere ebenfalls verbunden.

Bei einer Quelle, die du bereits verbunden hast, steht das samt Konto in der Liste. Wähle sie aus, um eine weitere Quelle daneben hinzuzufügen. Das Formular weist darauf hin und verlinkt auf die bereits verbundene Quelle.

Gib die erforderlichen Angaben ein, zum Beispiel einen Schlüssel oder eine Adresse, wähle **Arbeit** mit dem Namen deines Unternehmens oder **Privat** und klicke auf **Verbinden**. Bei Mail und Kalender wirst du nur gefragt, wenn sich die Auswahl nicht aus der Adresse ergibt. Bei einer Website wie LinkedIn oder X öffnet sich die Anmeldung im Browser deiner Machine. Sobald du angemeldet bist, geht es automatisch weiter. Bei GitHub, WhatsApp und Codex wird ein Code angezeigt, den du eingeben musst. Für Telegram- und Signal-Chats wird ein QR-Code zum Scannen angezeigt.

Mit **Abbrechen** wird der Vorgang beendet. Hast du das Formular geschlossen, bevor der Vorgang abgeschlossen war? Öffne **Verbindungen** erneut, auf einem beliebigen Gerät, und du kannst an derselben Stelle weitermachen. Sobald die Quelle verbunden ist, beginnt deine Machine sofort mit dem Lesen und zeigt dir den Status des ersten Syncs.

Auf einer gehosteten Machine meldest du dich direkt hier bei Quellen an, die eine eigene Anmeldung haben: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und klicke auf die Anmeldeschaltfläche, zum Beispiel **Mit Google anmelden**. Du kehrst zu diesem Formular zurück, wo du siehst, ob die Anmeldung geklappt hat. Auch für GitHub, WhatsApp, Codex, Telegram-Chats und dein Android-Smartphone wird der Code hier angezeigt.

Auf deinem eigenen Computer meldest du dich bei denselben Quellen an, sobald deine Machine mit deinem Konto gekoppelt ist. Klicke beim ersten Mal auf **Diese Machine verbinden**. Bei manchen Quellen gibt es auch eine andere Möglichkeit, zum Beispiel eine eigene App oder einen Schlüssel.

Mit **Neu verbinden** bei einer Quelle oder unter **Braucht dich** öffnest du dasselbe Formular. Auf deinem eigenen Computer erledigt `assistant connect` dasselbe im Terminal.

## Arbeit oder privat

Jede Quelle ist entweder beruflich, für ein von dir angegebenes Unternehmen, oder privat. Ändere die Einstellung unter **Details**. **Geschätzt** bedeutet, dass deine Machine die Zuordnung anhand der Adresse vorgenommen hat. Aufgaben für die Arbeit warten auf deine Arbeitstage.

Bei Google- und Microsoft-Mailkonten und -Kalendern wird die Zuordnung anhand der Adresse festgelegt, wenn sie eindeutig ist: Ein Mailanbieter wie Gmail oder Outlook.com bedeutet „Privat“, die Domain deines Teams bedeutet „Arbeit“. Andernfalls wirst du direkt nach der Anmeldung einmal gefragt. Mit **Ändern** legst du die Zuordnung selbst fest. Wenn eine spätere E-Mail auf die andere Zuordnung hindeutet, fragt die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du sie ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen, aus denen Aufgaben entstehen, Aktionen für deine Aufgaben ausführen, zum Beispiel ein Dokument lesen oder nach deiner Bestätigung etwas senden, beantworten oder ändern, oder beides. Wenn sie beides kann, gibt es unter **Details** jeweils einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Einer davon muss eingeschaltet bleiben. Um beide Funktionen zu beenden, trenne die Verbindung. Bei einem Chat gibt es nur **Kann Dinge tun**.

Wenn **Bringt Signale** ausgeschaltet ist, wird nichts synchronisiert. Wenn **Kann Dinge tun** ausgeschaltet ist, liest, entwirft oder ändert deine Machine damit nichts.

## Quelle entfernen

Öffne die Quelle und dann **Details** und klicke auf **Trennen**. Sie wird dann nicht mehr gelesen. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine wird bei Quellen, deren Anmeldung auf deiner Einrichtungsseite verwaltet wird (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** stehen die Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten, die du in den letzten 30 Tagen entfernt hast, samt Zeitpunkt. Bis der Dienst die Trennung bestätigt, wird „Ausstehend“ angezeigt und es werden weitere Versuche unternommen. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Docs eine eigene Anmeldung hatte. Jedes Konto erscheint unter seiner eigenen Art: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Melde dich bei Websites wie LinkedIn oder X an und aktiviere **Für nächstes Mal speichern**. Unter **Anmeldungen** werden die Websites dann aufgelistet. Wenn eine Website deine Machine abmeldet, meldet sie sich mit einem Tippen wieder an. Passwörter bleiben verschlüsselt auf deiner Machine. Mit **Vergessen** entfernst du eine Anmeldung.

Bei einer Website können mehrere Konten gespeichert sein, zum Beispiel **Arbeit** und **Privat**. **Speichern unter** wählt standardmäßig die Zuordnung der Aufgabe. Mit **Anderer Name …** kannst du einen eigenen Namen vergeben. Eine Aufgabe meldet sich mit dem passenden Konto an. Wenn nicht klar ist, welches Konto passt, fragt ein Dialog einmal nach und merkt sich deine Auswahl für diese Aufgabe.

Unter **Anmeldungen** wird jede Website einmal mit den zugehörigen Konten darunter angezeigt: dem Benutzernamen und einem Menü mit der jeweiligen Zuordnung. Du kannst die Zuordnung dort jederzeit ändern. Bei Anmeldungen, die gespeichert wurden, bevor Konten unterstützt wurden, wird **Arbeit oder privat?** angezeigt, bis du eine Zuordnung auswählst. Wenn du die Zuordnung änderst, wählt eine Aufgabe, die diese Anmeldung verwendet hat, das Konto erneut aus.

Mit **Importieren** kannst du Anmeldungen aus einem Passwortmanager importieren. Wähle einen aus:

- **LastPass**, **Bitwarden** oder **Google Passwortmanager**: Die Exportseite wird im Browser deiner Machine geöffnet. Melde dich dort an und exportiere deine Daten. Die Schritte werden daneben angezeigt. Deine Machine findet die Datei, liest sie einmal ein und löscht sie.
- **1Password**: Exportiere eine CSV-Datei über die 1Password-App auf einem Computer und wähle dann die Datei aus. Wenn `op` von 1Password auf deiner Machine angemeldet ist, werden die Daten stattdessen von dort eingelesen. Das gilt auch für `lpass` von LastPass.
- **Aus einer Exportdatei**: Wähle eine CSV-Datei aus 1Password, LastPass, Bitwarden oder Chrome aus. Lösche sie anschließend.

Wähle dann aus, welche Anmeldungen du behalten möchtest. Deine Machine meldet sich nie für dich bei deinem Passwortmanager an und fragt nie nach deinem Masterpasswort. Du gibst es selbst auf der Seite ein.

Eine gespeicherte Anmeldung wird nur für die zugehörige Webadresse verwendet: dieselbe Website, `https` und derselbe Port. Nicht für eine ähnlich aussehende Adresse und nicht für eine andere Subdomain.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Daten liest: die letzten Prüfungen und was dabei gefunden wurde. Siehe [Keine neuen Aufgaben](reviews-paused.md).

Für jede Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin steht, was sie liest und was sie senden kann.
