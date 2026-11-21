---
title: Verbindungen
area: connections
summary: Alle deine Quellen an einem Ort: So geht es ihnen, wie du eine hinzufügst oder trennst.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 353fdfaa67678a1f
---
## So geht es ihnen

Auf dem Tab **Verbindungen** sind deine Quellen nach Typ sortiert. Darunter stehen **Anmeldungen** und **Prüfungen**, getrennt durch eine Linie. Auf dem Smartphone tippst du auf einen Typ, um ihn zu öffnen, und auf **Verbindungen**, um zurückzugehen. Ein Typ mit einer Quelle, die dich braucht, wird zuerst geöffnet. Jede Quelle steht in einer Zeile: mit ihrem Status (Verbunden, Wartet auf den ersten Abgleich, Stellt automatisch die Verbindung wieder her oder Braucht deine Hilfe) und den zuletzt eingegangenen Daten. Tippe darauf, um die Karte und **Details** zu öffnen.

Ein fehlgeschlagener Abgleich, den ein späterer ausgeglichen hat, wird grau angezeigt. Nur ein Fehler, der weiterhin der letzte ist, wird als Problem angezeigt, zusammen mit dem Zeitpunkt des nächsten Versuchs.

Die Zähler zeigen alles, was die Quelle eingebracht hat, auch den [Verlauf](history.md), was in den letzten 24 Stunden eingegangen ist und was noch nicht geprüft wurde. Bei einem Kalender werden die Termine gezählt.

Jede Quelle trägt den Namen ihres Kontos, so wie ihn der Dienst angibt: deine Adresse, ein X-Profil, ein Slack-Arbeitsbereich oder wem das Signal- oder Telegram-Konto gehört. Unter dem Namen steht zuerst **Arbeit** oder **Privat**, außerdem die Adresse oder der Benutzername, falls der Name das nicht bereits erkennen lässt. Gibt es zwei Quellen desselben Typs mit demselben Namen, steht auch dabei, woran du sie unterscheiden kannst, etwa Slack oder X, oder die Adresse des Arbeitsbereichs.

Bei jeder Quelle steht außerdem in einer Zeile, was sie einbringt und, falls sie Aktionen ausführen kann, dass sie das erst tut, wenn du **Senden** drückst oder die Aktion bestätigst.

## Quelle hinzufügen

Öffne einen Typ (**E-Mail**, **Kalender**, **Chat**, **Meetings**, **Dokumente und Dateien**, **Kunden**, **Projekte und Code**, **Andere**) und wähle unter **Weitere hinzufügen** eine Quelle aus. Falls noch keine verbunden ist, findest du die Auswahl unter der Liste. Die Sammeloptionen stehen ganz unten: **Andere E-Mail** unter E-Mail sowie **Kalenderlink (ICS)** und **Anderer Kalender** unter Kalender. Exchange Server liest Meetings und ist deshalb unter Kalender zu finden.

**Vorgeschlagen für dich** erscheint oben in **Verbindungen**, wenn deine Machine einen Grund für eine Quelle erkennt. Der Grund steht in einer Zeile, zum Beispiel Mails von Stripe, Zoom-Meetings in deinem Kalender, Nachrichten mit Links zu Google Docs oder eine nicht abgeschlossene Einrichtung. Die Quelle bleibt auch in ihrer eigenen Gruppe und ist dort als **Vorgeschlagen** markiert. Die Zählung erfolgt auf deiner Machine. Nichts wird von ihr übertragen. Eine verbundene Quelle wird nie vorgeschlagen.

Microsoft Teams erscheint zweimal: unter **Chat** für Chats und unter **Meetings** als **Teams-Meetings** für Besprechungsnotizen. Beide verwenden dieselbe Microsoft-Anmeldung. Wenn du eines verbindest, wird auch das andere verbunden.

In der Liste ist bei einer bereits verbundenen Quelle das Konto angegeben. Wähle sie aus, um eine weitere daneben hinzuzufügen. Das Formular weist darauf hin und verlinkt die vorhandene Quelle.

Gib die erforderlichen Angaben ein, etwa einen Schlüssel oder eine Adresse, wähle **Arbeit** mit dem Namen deines Unternehmens oder **Privat** und drücke **Verbinden**. Bei E-Mail und Kalender wirst du nur dann gefragt, wenn sich die Auswahl nicht anhand der Adresse treffen lässt. Bei einer Website wie LinkedIn oder X öffnet sich die Anmeldung im Browser deiner Machine. Sobald du angemeldet bist, geht es automatisch weiter. Bei GitHub, WhatsApp und Codex wird ein Code angezeigt, den du eingeben musst. Für Telegram-Chats und Signal-Chats wird ein QR-Code zum Scannen angezeigt.

Mit **Abbrechen** brichst du das Hinzufügen ab. Hast du den Vorgang vor dem Abschluss verlassen? Öffne **Verbindungen** erneut, auf einem beliebigen Gerät. Der Vorgang wird an derselben Stelle fortgesetzt. Sobald die Quelle verbunden ist, liest deine Machine sie sofort aus und zeigt dir den Status des ersten Abgleichs.

Auf einer gehosteten Machine meldest du dich direkt hier bei Quellen an, die eine eigene Anmeldung haben: Google, Microsoft (Outlook, OneDrive und Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce und Trello.

Wähle **Arbeit** oder **Privat** und drücke die entsprechende Anmeldeschaltfläche, zum Beispiel **Mit Google anmelden**. Du kehrst zu diesem Formular zurück, wo du siehst, wie es gelaufen ist. Bei GitHub, WhatsApp, Codex, Telegram-Chats und deinem Android-Smartphone wird der Code ebenfalls hier angezeigt.

Auf deinem eigenen Computer melden sich dieselben Quellen an, sobald deine Machine mit deinem Konto verbunden ist. Drücke beim ersten Mal **Diese Machine verbinden**. Bei einigen Quellen gibt es auch eine andere Möglichkeit, zum Beispiel mit deiner eigenen App oder einem Schlüssel.

**Neu verbinden** bei einer Quelle oder unter **Braucht dich** öffnet dasselbe Formular. Auf deinem eigenen Computer macht `assistant connect` dasselbe in einem Terminal.

## Arbeit oder privat

Jede Quelle wird als Arbeit (für ein Unternehmen, das du angibst) oder privat eingestuft. Ändere die Einstellung unter **Details**. **Geschätzt** bedeutet, dass deine Machine die Auswahl anhand der Adresse getroffen hat. Aufgaben für die Arbeit warten, bis an deinen Arbeitstagen.

Bei Google- und Microsoft-E-Mail und -Kalendern wird die Auswahl anhand der Adresse getroffen, wenn sie eindeutig ist: Ein E-Mail-Anbieter wie Gmail oder Outlook.com steht für Privat, die Domain deines Teams für Arbeit. Andernfalls wirst du einmal direkt nach der Anmeldung gefragt. Mit **Ändern** legst du die Auswahl selbst fest. Wenn spätere E-Mails auf das Gegenteil hindeuten, fragt dich die Aufgabe **Hol mehr aus The Machine heraus** einmal, ob du die Auswahl ändern möchtest.

## Funktionen

Eine Quelle kann Signale einbringen (aus eingehenden Daten werden Aufgaben), Aktionen für deine Aufgaben ausführen (ein Dokument lesen oder nach deiner Bestätigung etwas senden, beantworten oder ändern) oder beides. Wenn sie beides kann, findest du unter **Details** je einen Schalter: **Bringt Signale** und **Kann Dinge tun**. Einer davon bleibt eingeschaltet. Wenn du beide ausschalten möchtest, musst du die Quelle trennen. Bei einem Chat gibt es nur **Kann Dinge tun**.

Wenn **Bringt Signale** ausgeschaltet ist, wird nichts abgeglichen. Wenn **Kann Dinge tun** ausgeschaltet ist, liest, entwirft oder ändert deine Machine damit nichts.

## Quelle entfernen

Öffne die Quelle und dann **Details** und **Trennen**. Sie wird nicht mehr ausgelesen. Was sie bereits eingebracht hat, bleibt erhalten. Auf einer gehosteten Machine wird bei Quellen, deren Anmeldung auf deiner Einrichtungsseite liegt (Google, Microsoft, Google Meet, Slack, Zoom, Stripe und Salesforce), **Trennen ↗** angezeigt. Damit öffnest du deine Einrichtungsseite.

Unter **Kürzlich getrennt** siehst du die Google-, Microsoft-, Zoom-, Slack-, Stripe- und Salesforce-Konten, die du in den letzten 30 Tagen entfernt hast, und wann du sie entfernt hast. Bis der Dienst die Trennung bestätigt, steht dort „Ausstehend“ und es wird weiter versucht. Ein Google-Konto wird nur einmal angezeigt, auch wenn Google Meet oder Docs eine eigene Anmeldung hatte. Jede Quelle steht unter ihrem jeweiligen Typ: ein Google- oder Microsoft-Konto unter **E-Mail**, Slack unter **Chat**.

## Gespeicherte Anmeldungen

Aktiviere bei der Anmeldung auf Websites wie LinkedIn oder X **Für nächstes Mal speichern**. Die Website erscheint dann unter **Anmeldungen**. Wenn sie deine Machine abmeldet, meldet sie sich mit einem Tippen wieder an. Passwörter bleiben auf deiner Machine verschlüsselt. Mit **Vergessen** entfernst du eine Anmeldung.

Auf einer Website können mehrere Konten gespeichert sein, zum Beispiel **Arbeit** und **Privat**. **Speichern unter** beginnt mit der Einstellung der Aufgabe, und mit **Anderer Name …** kannst du einen eigenen Namen festlegen. Eine Aufgabe meldet sich mit dem passenden Konto an. Ist nicht klar, welches das ist, fragt der Dialog einmal nach und merkt sich deine Auswahl für diese Aufgabe.

Unter **Anmeldungen** wird jede Website einmal mit den zugehörigen Konten darunter aufgeführt: mit dem Benutzernamen und einem Menü für die jeweilige Einstellung. Du kannst die Einstellung dort jederzeit ändern. Bei Anmeldungen, die gespeichert wurden, bevor es Konten gab, wird **Arbeit oder privat?** angezeigt, bis du eine Auswahl triffst. Eine Aufgabe, die eine Anmeldung verwendet hat, fragt erneut nach, wenn du deren Einstellung änderst.

Mit **Importieren** übernimmst du Anmeldungen aus einem Passwortmanager. Wähle einen aus:

- **LastPass**, **Bitwarden** oder **Google Passwortmanager**: Die Exportseite wird in einem Dialog direkt im Browser deiner Machine geöffnet, wie bei **Ausführen** für eine Aufgabe. Melde dich dort an. Deine Machine klickt sich dann bis zum Export durch. In einer Zeile steht, was du noch tun musst, zum Beispiel dein Masterpasswort eingeben. Auf einem Smartphone wird die Ansicht auf die Eingabestelle vergrößert. Wenn die Seite anders aussieht als erwartet, werden stattdessen die Schritte zum manuellen Abschließen angezeigt. Deine Machine übernimmt die Datei, liest sie einmal aus und löscht sie.
- **1Password**: Exportiere in der 1Password-App auf einem Computer eine CSV-Datei und wähle sie anschließend aus. Wenn `op` von 1Password auf deiner Machine angemeldet ist, werden die Daten stattdessen von dort ausgelesen. Das gilt auch für `lpass` von LastPass.
- **Aus einer Exportdatei**: eine CSV-Datei von 1Password, LastPass, Bitwarden oder Chrome. Lösche sie, wenn du fertig bist.

Wähle anschließend aus, welche Anmeldungen du behalten möchtest. Deine Machine meldet sich nie für dich bei deinem Passwortmanager an, gibt dein Masterpasswort weder ein noch liest sie es aus und zeigt der Assistentin nie die Seite. Du gibst das Passwort selbst auf der Seite ein.

Eine gespeicherte Anmeldung wird nur für die dazugehörige Webadresse verwendet: dieselbe Website, `https` und derselbe Port. Nicht für eine ähnlich aussehende Adresse und nicht für eine andere Subdomain.

## Prüfungen

Unter **Prüfungen** siehst du, wie deine Machine eingehende Daten ausliest: die letzten Prüfungen und was dabei gefunden wurde. Siehe [Keine neuen Aufgaben](reviews-paused.md).

Für jede Verbindung gibt es in diesem Abschnitt einen eigenen Artikel. Darin steht, was sie ausliest und was sie senden kann.
