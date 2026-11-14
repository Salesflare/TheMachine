---
title: Einstellungen
area: settings
summary: Hier findest du alle Einstellungen, vom hellen Modus bis zu Sicherheit und Konto.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Öffne **Einstellungen** über das Zahnrad oben. Die Tabs:

- **Konto**: Oben findest du **Deine Adressen** (Adressen, die als deine gelten) und **Abmelden**. Bei einer gehosteten Machine findest du hier außerdem deinen Tarif, Rechnungen, Fleet, Freunde, Anmeldung und Daten sowie ganz unten **Tarif kündigen** und **Konto löschen**. Bei einer Machine auf deinem eigenen Computer, die mit dem Network verbunden ist, findest du hier Fleet, deinen Benutzernamen, Freunde und Anmeldung. Jeder Punkt hat einen Link, der den entsprechenden Bereich deines Kontos öffnet (melde dich dort an). Ganz unten findest du **Konto löschen**. Noch nicht verbunden? Oben findest du **Dem Network beitreten**. Mehr dazu unter [Tarife und Abrechnung](plans-and-billing.md).
- **Allgemein**: Sprache und Region, dieses Gerät, Spracheingabe, der Browser deiner Machine, Fleet, Export und Import sowie die installierte Version. Wenn es keinen Tab „Konto“ gibt, findest du **Dem Network beitreten** ganz am Ende.
- **Sicherheit**: Standard oder Vorsichtig. Mehr dazu unter [Sicherheitsstufen](security-levels.md). Außerdem **Support-Zugriff**, solange er aktiviert ist: siehe [Support erhalten](get-support.md#support-access).
- **Aktivität**: alles, was The Machine für dich getan hat, neuestes zuerst. Mehr dazu unter [Aktivität](activity.md).
- **Benachrichtigungen**: welche Benachrichtigungen dich wo erreichen und deine Arbeitszeiten. Mehr dazu unter [Benachrichtigungen](notifications.md) und [Arbeitszeiten](work-hours.md).
- **Schreiben**: Signaturen und deine Schreibweise. Mehr dazu unter [Schreiben](writing.md).
- **Skills**: Anleitungen, an die sich deine Machine hält. Mehr dazu unter [Skills](skills.md).
- **Apps**: zuerst die Apps von The Machine für dein Smartphone und deinen Computer, dann Claude, ChatGPT und andere KI-Assistenten, die du verbunden hast, und was sie jeweils tun dürfen. Mehr dazu unter [Die mobile App](mobile-app.md) und [Andere KIs verbinden](ai-connections.md).
- **Modell**: die KI, die für dich liest und Entwürfe schreibt, und ihre Grenzen. Mehr dazu unter [Modell](model.md). Außerdem **Codex und Claude Code**: siehe [An Claude Code oder Codex übergeben](hand-to-agent.md). Und **Suche nach Bedeutung**, weiter unten.

Tabs ohne Inhalte werden ausgeblendet.

## Allgemein

- **Sprache und Region**: Unter **Region** legst du fest, wie Datumsangaben, Uhrzeiten und Zahlen angezeigt werden (24. Okt. oder 24. Okt.). **Zeitformat** bestimmt, ob die Uhrzeit im 12-Stunden-Format (2:05 PM) oder im 24-Stunden-Format (14:05) angezeigt wird. Aufgaben, Telegram, die Zusammenfassung und Fleet-Nachrichten richten sich nach diesen beiden Einstellungen. Bei einer gehosteten Machine wird die Zeitzone verwendet, die du bei der Anmeldung ausgewählt hast.
- **Sprache**: Englisch, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 oder Русский. Standardmäßig wird die Sprache deines Browsers verwendet. Das Dashboard, die Hilfe, Benachrichtigungen, Telegram, der Wochenrückblick und die Aufgaben, die deine Machine schreibt, wechseln sofort nach deiner Auswahl die Sprache. Ältere Texte bleiben unverändert. Teammitglieder erhalten Fleet- und Family-Fragen in ihrer eigenen Sprache. Entwürfe für andere bleiben in der Sprache des jeweiligen Gesprächs.
- **Dieses Gerät**: **App installieren**, **Benachrichtigungen** mit **Test senden** und **Heller Modus**. Diese Einstellungen gelten nur für diesen Browser oder dieses Smartphone. Mehr dazu unter [App installieren und Benachrichtigungen aktivieren](phone-app.md). Unter [Omarchy](omarchy.md) gibt es außerdem **Omarchy-Theme**.
- **Spracheingabe**: wie deine gesprochenen Worte in Text umgewandelt werden und welche Stimme Talk live verwendet. Mehr dazu unter [Spracheingabe](voice-input.md) und [Talk live](talk-live.md).
- **Browser der Machine öffnen ↗**: der Browser, den deine Machine für Websites wie LinkedIn verwendet.
- **Fleet-Regeln**: siehe [Freigaberegeln](sharing-rules.md).
- **Exportieren**:
  - **Alles**: alles, was deine Machine weiß, in einer verschlüsselten Datei, zum Übertragen oder Aufbewahren. Mit **Importieren** kannst du eine Datei importieren. Mehr dazu unter [Auf einen anderen Computer umziehen](moving.md).
  - **Wissen für eine andere KI**: was deine Machine gelernt hat, in Dateien, die jede KI lesen kann. Mehr dazu unter [Wissen für eine andere KI](knowledge-export.md).

## Version

Die Version, die auf deiner Machine läuft. Updates werden automatisch installiert. Wenn bei einer gehosteten Machine eine neuere Version bereitsteht, wird sie mit **Jetzt aktualisieren** sofort installiert. Das dauert ein paar Minuten. Deine Daten bleiben erhalten.

Auf deinem eigenen Computer installiert ein täglicher Timer jede neue, signierte Version für Linux. Mehr dazu unter [Auf deinem eigenen Computer ausführen](self-hosted-setup.md).

## Suche nach Bedeutung

Unter **Einstellungen** und **Modell**. Damit findest du E-Mails, Nachrichten und Notizen nach ihrem Inhalt, nicht nur nach ihren Wörtern. Bei einer gehosteten Machine übernimmt eine kleine KI direkt auf der Machine die Suche. Dabei werden keine Daten irgendwohin gesendet. Ab 8 GB Arbeitsspeicher ist die Funktion aktiviert. Bei 4 GB kannst du sie mit dem Schalter aktivieren. Sie benötigt etwa ein halbes Gigabyte Arbeitsspeicher und kann eine ausgelastete Machine deshalb verlangsamen.

Auf deinem eigenen Computer findest du die Funktion im Block `embeddings` in `config.json`. Starte die Machine nach einer Änderung neu.

## Auf dieser Machine

Wenn deine Machine auf deinem eigenen Computer läuft, werden einige Dinge dort in einem Terminal erledigt:

- Die Einstellungsdatei `config.json`: alle Einstellungen an einem Ort. Starte die Machine nach einer Änderung neu.
- `assistant connect`: fügt eine Quelle hinzu, zum Beispiel `assistant connect gmail` oder `assistant connect outlook`.
- `assistant telegram on` oder `off`: Nachrichten auf Telegram. Mehr dazu unter [Telegram](telegram.md).
- `assistant doctor`: prüft alles und gibt für jedes Problem eine Lösung aus.

## Deine Adressen

Alle Adressen von dir, die deine Machine gefunden hat: deine Konten, Gmail- oder Outlook-Aliasse, dein Kalender sowie deine Slack- und Intercom-Profile. E-Mails und Termine von all diesen Adressen gelten als deine. Mit **Entfernen** kannst du Adressen löschen, die nicht dir gehören.

Eine gemeinsam genutzte Adresse wie info@ oder eine Google Group gilt nie automatisch als deine. Bei Adressen, bei denen sich deine Machine nicht sicher ist, findest du sie unter **Vielleicht deine**. Wähle eine Option:

- **Meine: Nur ich beantworte sie**: Die Adresse gilt als deine. E-Mails an sie können zu deinen Aufgaben werden.
- **Vom Team: Andere beantworten sie auch**: Die Adresse gilt nicht als deine. E-Mails, die nur an sie gesendet wurden, erzeugen keine Aufgaben oder Entwürfe für dich. Sie fließen aber weiterhin in den Graph ein.
- **Nicht meine**: Die Adresse gilt nicht als deine.

Entscheide danach, wer die Adresse heute beantwortet. Ein Team-Postfach wie support@ gehört dem Team. Eine Adresse wie partnerships@, die nur du beantwortest, gehört dir. Ändere die Einstellung, wenn auch andere die Adresse beantworten.

Mit **Ändern** in der Zeile kannst du die Auswahl später ändern. Deine eigene Anmeldeadresse gilt immer als deine.

### Domains deiner Firma

Die Domains deiner eigenen Adressen gelten als Domains deiner Firma. Nutzt du noch eine andere, zum Beispiel acme.co neben acme.com? Gib sie unter **Domains deiner Firma** ein und klicke auf **Hinzufügen**.

Personen unter diesen Domains gelten dann als Kolleginnen und Kollegen, nie als Kundinnen oder Kunden: Ihre Unterhaltungen erscheinen nicht im Team-Graph, und dafür wird keine Organisation erstellt. Mit **Entfernen** kannst du eine Domain wieder löschen. Kostenlose E-Mail-Domains wie gmail.com lassen sich nicht hinzufügen.

Ein Gmail-Alias von dir kann auch als **Von** für einen Entwurf verwendet werden, wenn Gmail bestätigt, dass du damit E-Mails senden kannst. Mehr dazu unter [Gmail](gmail.md#what-it-can-send).
