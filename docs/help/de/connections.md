---
title: Verbindungen
area: connections
summary: Deine Quellen an einem Ort: ihr Status, neue Quellen hinzufügen oder Verbindungen trennen.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 9f2a2162fe015e0b
---
## Ihr Status

Auf dem Tab **Verbindungen** sind deine Quellen nach Kategorie aufgeführt. **Anmeldungen** und **Prüfungen** stehen unter einer Trennlinie. Auf dem Smartphone tippst du auf eine Kategorie, um sie zu öffnen, und auf **Verbindungen**, um zurückzugehen. Eine Kategorie mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle wird als Zeile angezeigt: mit ihrem Status (Verbunden, Wartet auf den ersten Abgleich, Verbindet sich automatisch erneut oder Braucht deine Hilfe) und den zuletzt eingegangenen Daten. Tippe darauf, um die Karte und **Details** zu öffnen.

Ein fehlgeschlagener Abgleich, der durch einen späteren ausgeglichen wurde, wird grau angezeigt. Nur ein Fehler, der weiterhin der letzte ist, wird als Problem angezeigt, mit dem Zeitpunkt des nächsten Versuchs.

Die Zahlen zeigen alles, was die Quelle eingebracht hat, einschließlich des [Verlaufs](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender werden die Termine gezählt.

Jede Quelle ist nach ihrem Konto benannt, so wie der Dienst es benennt: nach deiner Adresse, einem X-Profil, einem Slack-Arbeitsbereich oder danach, wem das Signal- oder Telegram-Konto gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat**, außerdem die Adresse oder der Benutzername, falls der Name das noch nicht erkennen lässt. Haben zwei Quellen derselben Kategorie denselben Namen, wird zusätzlich angezeigt, woran du sie unterscheiden kannst, zum Beispiel Slack oder X oder die Adresse des Arbeitsbereichs.

Jede Quelle erklärt außerdem in einer Zeile, was sie einbringt und, falls sie Aktionen ausführen kann, dass sie das erst tut, wenn du auf **Senden** drückst oder die Aktion bestätigst.

## Quelle hinzufügen

Öffne eine Kategorie (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Wenn noch keine verbunden ist, findest du sie unter der Liste. Am Ende steht jeweils eine allgemeine Option: **Andere E-Mail** unter E-Mail sowie **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Termine und steht deshalb unter Kalender.

**Vorgeschlagen für dich** erscheint oben in **Verbindungen**, wenn deine Machine einen Grund für eine Quelle erkennt. Der Grund wird in einer Zeile genannt: etwa E-Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt auch in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** markiert. Deine Machine ermittelt diese Vorschläge direkt auf deinem Gerät. Nichts davon wird nach außen übertragen. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams wird zweimal angezeigt: unter **Chat** für Chats und unter **Meetings** als **Teams-Meetings** für Meetingnotizen. Beide verwenden dieselbe Microsoft-Anmeldung. Wenn du eine verbindest, wird also auch die andere verbunden.

Eine Quelle, die du bereits verbunden hast, ist in der Liste mit ihrem Konto gekennzeichnet. Wähle sie aus, um eine weitere daneben hinzuzufügen. Das Formular weist darauf hin und verlinkt auf die vorhandene Quelle.

Gib die erforderlichen Angaben ein, zum Beispiel einen Schlüssel oder eine Adresse, wähle **Arbeit** mit dem Namen deines Unternehmens oder **Privat** und drücke auf **Verbinden**. Bei E-Mail und Kalender wirst du nur gefragt, wenn sich die Auswahl nicht an der Adresse erkennen lässt. Bei Websites wie LinkedIn oder X öffnet sich die Anmeldung im Browser deiner Machine und der Vorgang wird automatisch fortgesetzt, sobald du angemeldet bist. Für GitHub, WhatsApp und Codex wird ein Code zum Eingeben angezeigt, für Telegram-Chats und Signal-Chats ein QR-Code zum Scannen.

Mit **Abbrechen** wird das Hinzufügen beendet. Hast du den Vorgang vorher verlassen? Öffne **Verbindungen** einfach auf einem beliebigen Gerät erneut. Der Vorgang wird dort fortgesetzt, wo du aufgehört hast. Sobald die Quelle verbunden ist, liest deine Machine sie sofort aus und zeigt den Status des ersten Abgleichs an.

Auf einer gehosteten Machine kannst du dich für Quellen mit eigener Anmeldung direkt hier anmelden: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und drücke auf die Anmeldeschaltfläche, zum Beispiel **Mit Google anmelden**. Du kehrst zu diesem Formular zurück, das den Status anzeigt. Auch für GitHub, WhatsApp, Codex, Telegram-Chats und dein Android-Smartphone wird der Code hier angezeigt.

Auf deinem eigenen Computer meldest du dich bei denselben Quellen an, sobald deine Machine mit deinem Konto verbunden ist. Drücke beim ersten Mal auf **Diese Machine verbinden**. Bei manchen Quellen gibt es auch eine andere Möglichkeit, zum Beispiel mit deiner eigenen App oder einem Schlüssel.

Mit **Neu verbinden** bei einer Quelle oder unter **Braucht dich** öffnest du dasselbe Formular. Auf deinem eigenen Computer geht das auch mit `assistant connect` in einem Terminal.

## Arbeit oder privat

Jede Quelle gilt als beruflich, also für ein Unternehmen, das du angibst, oder als privat. Du kannst das unter **Details** ändern. **Geschätzt** bedeutet, dass deine Machine die Zuordnung anhand der Adresse vorgenommen hat. Aufgaben für die Arbeit warten auf deine Arbeitstage.

Bei E-Mails und Kalendern von Google und Microsoft wird die Zuordnung anhand der Adresse vorgenommen, wenn sie eindeutig ist: Ein E-Mail-Anbieter wie Gmail oder Outlook.com gilt als privat, die Domain deines Teams als beruflich. Andernfalls wirst du direkt nach der Anmeldung einmal gefragt. Mit **Ändern** kannst du die Zuordnung selbst festlegen. Wenn deine E-Mails später auf die andere Zuordnung hindeuten, fragt dich die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du sie ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen, aus denen Aufgaben entstehen, Aktionen für deine Aufgaben ausführen, zum Beispiel ein Dokument lesen oder nach deiner Bestätigung etwas senden, beantworten oder ändern, oder beides. Wenn sie beides kann, gibt es unter **Details** jeweils einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Einer der beiden Schalter bleibt immer eingeschaltet. Um beides zu beenden, musst du die Verbindung trennen. Bei einem Chat gibt es nur **Kann Dinge tun**.

Ist **Bringt Signale** ausgeschaltet, wird kein Abgleich durchgeführt. Ist **Kann Dinge tun** ausgeschaltet, liest, entwirft oder ändert deine Machine nichts mit dieser Quelle.

## Quelle entfernen

Öffne die Quelle und dann **Details** und tippe auf **Trennen**. Deine Machine hört auf, sie auszulesen. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine wird bei Quellen, deren Anmeldung über deine Einrichtungsseite verwaltet wird (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** siehst du die Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten, die du in den letzten 30 Tagen entfernt hast, einschließlich des Zeitpunkts. Solange der Dienst die Trennung noch nicht bestätigt hat, wird „Ausstehend“ angezeigt und es werden weitere Versuche unternommen. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Google Docs eine eigene Anmeldung hatte. Jedes Konto steht unter seiner jeweiligen Kategorie: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Bei Websites wie LinkedIn oder X kannst du beim Anmelden **Für nächstes Mal speichern** aktivieren. Unter **Anmeldungen** werden sie dann aufgelistet. Wenn eine Website deine Machine abmeldet, meldet sie sich mit einem Fingertipp wieder an. Passwörter bleiben auf deiner Machine verschlüsselt. Mit **Vergessen** entfernst du eine Anmeldung.

Bei einer Website können mehrere Konten hinterlegt sein, zum Beispiel **Arbeit** und **Privat**. **Speichern unter** übernimmt zunächst die Zuordnung der Aufgabe. Mit **Anderer Name …** kannst du einen eigenen Namen festlegen. Eine Aufgabe meldet sich mit dem passenden Konto an. Ist nicht klar, welches Konto passt, fragt der Dialog einmal nach und merkt sich deine Auswahl für diese Aufgabe.

Unter **Anmeldungen** wird jede Website einmal mit den zugehörigen Konten darunter angezeigt: dem Benutzernamen und einem Menü mit der Zuordnung. Du kannst die Zuordnung jederzeit dort ändern. Bei Anmeldungen, die gespeichert wurden, bevor es Konten gab, wird **Arbeit oder privat?** angezeigt, bis du eine Zuordnung auswählst. Ändere die Zuordnung einer Anmeldung, wählt eine Aufgabe, die sie verwendet hat, erneut ein Konto aus.

Mit **Importieren** kannst du Anmeldungen aus einem Passwortmanager übernehmen: aus einem CSV-Export von 1Password, LastPass, Bitwarden oder Chrome oder direkt aus 1Password und LastPass über deren Kommandozeilenprogramme, wenn du auf diesem Computer dort angemeldet bist. Du wählst aus, welche Anmeldungen du behalten möchtest. Deine Machine meldet sich nie bei deinem Passwortmanager an und fragt nie nach dessen Master-Passwort. Lösche die Exportdatei, sobald du fertig bist.

Eine gespeicherte Anmeldung wird nur für ihre eigene Webadresse verwendet: dieselbe Website, `https` und derselbe Port. Nicht für eine ähnlich aussehende Adresse und nicht für eine andere Subdomain.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Inhalte prüft: die letzten Prüfungen und was sie jeweils ergeben haben. Siehe [Keine neuen Aufgaben](reviews-paused.md).

Zu jeder Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin erfährst du, was sie ausliest und was sie senden kann.
