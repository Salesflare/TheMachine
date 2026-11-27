---
title: Einstellungen
area: settings
summary: Hier findest du alle Einstellungen, von hellem Modus über Sicherheit bis zu deinem Konto.
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
Öffne die **Einstellungen** über das Zahnradsymbol oben. Die Tabs:

- **Konto**: Oben findest du **Deine Adressen** (Adressen, die als deine gelten) und **Abmelden**. Bei einer gehosteten Machine außerdem deinen Tarif, Rechnungen, Fleet, Freunde, Anmeldung und Daten. Ganz unten findest du **Tarif kündigen** und **Konto löschen**. Bei einer Machine auf deinem eigenen Computer, die mit dem Network verbunden ist: deine Fleet, deinen Nutzernamen, Freunde und Anmeldung. Jeder Punkt hat einen Link zum entsprechenden Bereich deines Kontos, in dem du dich anmeldest. **Konto löschen** findest du unten. Noch nicht verbunden? Oben findest du **Dem Network beitreten**. Siehe [Tarife und Abrechnung](plans-and-billing.md).
- **Allgemein**: Sprache und Region, dieses Gerät, Spracheingabe, der Browser deiner Machine, deine Fleet, Export und Import sowie die ausgeführte Version. Wenn es keinen Tab „Konto“ gibt, findest du **Dem Network beitreten** ganz unten.
- **Sicherheit**: Standard oder Vorsichtig. Siehe [Sicherheitsstufen](security-levels.md). Außerdem **Support-Zugriff**, solange er aktiviert ist: siehe [Support kontaktieren](get-support.md#support-access).
- **Aktivität**: Alles, was The Machine für dich getan hat, neuestes zuerst. Siehe [Aktivität](activity.md).
- **Benachrichtigungen**: Was dich wo erreicht und deine Arbeitszeiten. Siehe [Benachrichtigungen](notifications.md) und [Arbeitszeiten](work-hours.md).
- **Schreiben**: Signaturen und dein Schreibstil. Siehe [Schreiben](writing.md).
- **Skills**: Anleitungen, an die sich deine Machine hält. Siehe [Skills](skills.md).
- **Apps**: Die Apps von The Machine für dein Handy und deinen Computer, dann Claude, ChatGPT und andere verbundene KIs und was jede davon tun darf. Auf einem Computer werden außerdem die Desktop-Apps für Windows, Mac und Linux aufgeführt. Für jede gibt es **Herunterladen**, und die App für **Dieser Computer** ist gekennzeichnet. Siehe [Die mobile App](mobile-app.md), [Die Desktop-App](desktop-app.md) und [Andere KIs verbinden](ai-connections.md).
- **Modell**: Die KI, die für dich liest und Entwürfe schreibt, und ihre Grenzen. Siehe [Modell](model.md). Außerdem **Codex und Claude Code**: siehe [Aufgabe an Claude Code oder Codex übergeben](hand-to-agent.md). Und weiter unten **Suche nach Bedeutung**.

Tabs ohne Inhalte werden ausgeblendet.

## Allgemein

- **Sprache und Region**: Mit **Region** legst du fest, wie Datumsangaben, Uhrzeiten und Zahlen angezeigt werden (Oct 24 oder 24 Oct). Unter **Zeitformat** wählst du zwischen 12-Stunden-Format (2:05 PM) und 24-Stunden-Format (14:05). Aufgaben, Telegram, die Zusammenfassung und Fleet-Nachrichten richten sich nach beidem. Eine gehostete Machine verwendet zunächst die Zeitzone, die du bei der Anmeldung ausgewählt hast.
- **Sprache**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 oder Русский. Die Sprache richtet sich zunächst nach der Sprache deines Browsers. Das Dashboard, die Hilfe, Benachrichtigungen, Telegram, die wöchentliche Zusammenfassung und die Aufgaben, die deine Machine schreibt, wechseln sofort nach deiner Auswahl die Sprache. Ältere Texte bleiben unverändert. Teammitglieder erhalten Fragen zu Fleet und Family in ihrer eigenen Sprache. Entwürfe für andere bleiben in der Sprache des jeweiligen Gesprächs.
- **Dieses Gerät**: **App installieren**, **Benachrichtigungen** mit **Test senden** und **Heller Modus**, nur für diesen Browser oder dieses Handy. Siehe [App installieren und Benachrichtigungen einschalten](phone-app.md). Auf [Omarchy](omarchy.md) gibt es außerdem **Omarchy-Theme**.
- **Spracheingabe**: Wie deine gesprochenen Worte zu Text werden und welche Stimme Talk live verwendet. Siehe [Spracheingabe](voice-input.md) und [Live sprechen](talk-live.md).
- **Browser der Machine öffnen ↗**: Der Browser, den deine Machine für Websites wie LinkedIn verwendet.
- **Fleet-Regeln**: Siehe [Freigaberegeln](sharing-rules.md).
- **Exportieren**:
  - **Alles**: Alles, was deine Machine weiß, in einer verschlüsselten Datei, zum Übertragen oder Aufbewahren. Mit **Importieren** kannst du eine Datei hinzufügen. Siehe [Auf einen anderen Computer umziehen](moving.md).
  - **Wissen für eine andere KI**: Was deine Machine gelernt hat, in Dateien, die jede KI lesen kann. Siehe [Wissen für eine andere KI](knowledge-export.md).

## Version

Die Version, die auf deiner Machine läuft. Updates werden automatisch installiert. Wenn auf einer gehosteten Machine eine neuere Version bereitsteht, installiert **Jetzt aktualisieren** sie sofort. Das dauert ein paar Minuten. Deine Daten bleiben erhalten.

Auf deinem eigenen Computer installiert ein täglicher Timer jede neue, signierte Version unter Linux. Siehe [Auf deinem eigenen Computer ausführen](self-hosted-setup.md).

## Suche nach Bedeutung

Unter **Einstellungen** findest du die Option **Modell**. Damit findest du E-Mails, Nachrichten und Notizen nach ihrem Inhalt, nicht nur nach ihren Wörtern. Auf einer gehosteten Machine übernimmt das eine kleine KI direkt auf der Machine. Dabei wird nichts irgendwohin gesendet. Ab 8 GB Arbeitsspeicher ist die Funktion aktiviert. Bei 4 GB kannst du sie mit dem Schalter aktivieren. Sie belegt etwa ein halbes Gigabyte. Auf einer ausgelasteten Machine kann sie daher alles verlangsamen. Ist sie ausgeschaltet, sucht die Vorbereitung einer Aufgabe weiterhin anhand von Wörtern nach passenden Nachrichten.

Auf deinem eigenen Computer ist das der Block `embeddings` in `config.json`. Starte die Machine nach einer Änderung neu.

## Auf dieser Machine

Wenn deine Machine auf deinem eigenen Computer läuft, werden einige Aufgaben dort in einem Terminal erledigt:

- Die Einstellungsdatei `config.json`: alle Einstellungen an einem Ort. Starte die Machine nach einer Änderung neu.
- `assistant connect`: eine Quelle hinzufügen, zum Beispiel `assistant connect gmail` oder `assistant connect outlook`.
- `assistant telegram on` oder `off`: Nachrichten auf Telegram. Siehe [Telegram](telegram.md).
- `assistant doctor`: prüft alles und gibt für jedes Problem eine Lösung aus.

## Deine Adressen

Alle deine Adressen, die deine Machine gefunden hat: deine Konten, Gmail- oder Outlook-Aliasse, dein Kalender sowie deine Slack- und Intercom-Profile. E-Mails und Besprechungen von all diesen Adressen gelten als deine. Wähle **Entfernen** bei einer Adresse, die nicht dir gehört.

Eine geteilte Adresse wie info@ oder eine Google Group gilt niemals automatisch als deine. Bei Adressen, bei denen sich deine Machine nicht sicher ist, findest du sie unter **Vielleicht deine**. Wähle eine Option:

- **Meine: Nur ich beantworte sie**: Die Adresse gilt als deine. E-Mails an sie können zu deinen Aufgaben werden.
- **Vom Team: Andere beantworten sie auch**: Die Adresse gehört nicht zu dir. E-Mails, die nur an diese Adresse gingen, erzeugen keine Aufgaben und Entwürfe für dich. Sie fließen aber weiterhin in den Graph ein.
- **Nicht meine**: Die Adresse gilt nicht als deine.

Entscheide danach, wer die Adresse heute beantwortet. Ein gemeinsames Postfach wie support@ gehört dem Team. Eine Adresse wie partnerships@, die nur du beantwortest, gehört dir. Ändere die Auswahl, sobald auch andere darauf antworten.

Mit **Ändern** in der Zeile kannst du die Auswahl später ändern. Deine eigene Anmeldeadresse gehört immer dir.

### Domains deiner Firma

Die Domains deiner eigenen Adressen gelten als Domains deiner Firma. Verwendest du noch eine weitere, zum Beispiel acme.co neben acme.com? Gib sie unter **Domains deiner Firma** ein und wähle **Hinzufügen**.

Personen mit diesen Domains gelten dann als Kollegen, niemals als Kunden. Ihre Threads erscheinen nicht im Team Graph, und dafür wird keine Organisation angelegt. Mit **Entfernen** kannst du eine Domain wieder löschen. Kostenlose E-Mail-Domains wie gmail.com lassen sich nicht hinzufügen.

Ein Gmail-Alias von dir kann auch als **Von** für einen Entwurf verwendet werden, wenn Gmail bestätigt, dass du unter dieser Adresse senden kannst. Siehe [Gmail](gmail.md#what-it-can-send).
