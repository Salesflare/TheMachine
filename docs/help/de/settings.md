---
title: Einstellungen
area: settings
summary: Hier findest du alle Einstellungen, vom hellen Modus über Sicherheit bis zu deinem Konto.
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
Öffne **Einstellungen** über das Zahnradsymbol oben. Die Tabs:

- **Konto**: Oben findest du **Deine Adressen** (die Adressen, die als deine gelten) und **Abmelden**. Auf einer gehosteten Machine findest du hier außerdem deinen Tarif, Rechnungen, Fleet, Freund:innen, Anmeldung und Daten sowie ganz unten **Tarif kündigen** und **Konto löschen**. Auf einer Machine auf deinem eigenen Computer, die mit dem Network verbunden ist, findest du hier deine Fleet, deinen Benutzernamen, Freund:innen und die Anmeldung. Jeder Punkt hat einen Link, der den entsprechenden Bereich deines Kontos öffnet (melde dich dort an). Ganz unten findest du **Konto löschen**. Noch nicht verbunden? Oben findest du **Dem Network beitreten**. Siehe [Tarife und Abrechnung](plans-and-billing.md).
- **Allgemein**: Sprache und Region, dieses Gerät, Spracheingabe, der Browser deiner Machine, deine Fleet, Export und Import sowie die Version, die sie ausführt. Ohne Konto-Tab findest du **Dem Network beitreten** ganz unten.
- **Sicherheit**: Standard oder Vorsichtig. Siehe [Sicherheitsstufen](security-levels.md). Außerdem **Support-Zugriff**, solange er aktiviert ist: siehe [Support kontaktieren](get-support.md#support-access).
- **Aktivität**: Alles, was The Machine für dich getan hat, beginnend mit dem Neuesten. Siehe [Aktivität](activity.md).
- **Benachrichtigungen**: Was du wo erhältst und deine Arbeitszeiten. Siehe [Benachrichtigungen](notifications.md) und [Arbeitszeiten](work-hours.md).
- **Schreiben**: Signaturen und deine Schreibweise. Siehe [Schreiben](writing.md).
- **Skills**: Anleitungen, an die sich deine Machine hält. Siehe [Skills](skills.md).
- **Apps**: Die Apps von The Machine für dein Handy und deinen Computer, dann Claude, ChatGPT und andere KI-Systeme, die du verbunden hast, und was sie jeweils tun dürfen. Siehe [Die mobile App](mobile-app.md) und [Andere KIs verbinden](ai-connections.md).
- **Modell**: Die KI, die für dich liest und Entwürfe schreibt, und ihre Grenzen. Siehe [Modell](model.md). Außerdem **Codex und Claude Code**: siehe [Aufgabe an Claude Code oder Codex übergeben](hand-to-agent.md). Und weiter unten **Suche nach Bedeutung**.

Ein Tab ohne Inhalte wird ausgeblendet.

## Allgemein

- **Sprache und Region**: Unter **Region** legst du fest, wie Datumsangaben, Uhrzeiten und Zahlen angezeigt werden (24. Okt. oder 24. Okt.). Mit **Zeitformat** wählst du zwischen 12-Stunden-Format (2:05 PM) und 24-Stunden-Format (14:05). Aufgaben, Telegram, die Zusammenfassung und Fleet-Nachrichten richten sich nach diesen beiden Einstellungen. Bei einer gehosteten Machine wird zunächst die Zeitzone verwendet, die du bei der Anmeldung ausgewählt hast.
- **Sprache**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 oder Русский. Zunächst wird die Sprache deines Browsers verwendet. Das Dashboard, die Hilfe, Benachrichtigungen, Telegram, die wöchentliche Zusammenfassung und die Aufgaben, die deine Machine schreibt, wechseln zu der Sprache, die du auswählst. Ältere Texte bleiben unverändert. Deine Teamkolleg:innen erhalten Fleet- und Family-Fragen in ihrer eigenen Sprache. Entwürfe für andere bleiben in der Sprache ihres Gesprächs.
- **Dieses Gerät**: **App installieren**, **Benachrichtigungen** mit **Test senden** und **Heller Modus** gelten nur für diesen Browser oder dieses Handy. Siehe [App installieren und Benachrichtigungen einschalten](phone-app.md). Auf [Omarchy](omarchy.md) gibt es außerdem **Omarchy-Theme**.
- **Spracheingabe**: Wie deine gesprochenen Worte zu Text werden und welche Stimme Talk live verwendet. Siehe [Spracheingabe](voice-input.md) und [Live sprechen](talk-live.md).
- **Browser der Machine öffnen ↗**: Der Browser, den deine Machine für Websites wie LinkedIn verwendet.
- **Fleet-Regeln**: Siehe [Freigaberegeln](sharing-rules.md).
- **Exportieren**:
  - **Alles**: Alles, was deine Machine weiß, in einer verschlüsselten Datei, zum Übertragen oder Aufbewahren. Mit **Importieren** kannst du eine Datei importieren. Siehe [Auf einen anderen Computer umziehen](moving.md).
  - **Wissen für eine andere KI**: Was deine Machine gelernt hat, in Dateien, die jede KI lesen kann. Siehe [Wissen für eine andere KI](knowledge-export.md).

## Version

Die Version, die deine Machine ausführt. Updates werden automatisch installiert. Wenn eine neuere Version für eine gehostete Machine bereitsteht, installierst du sie mit **Jetzt aktualisieren** sofort. Das dauert ein paar Minuten, und deine Daten bleiben erhalten.

Auf deinem eigenen Computer installiert ein täglicher Timer jedes neue signierte Release unter Linux. Siehe [Auf deinem eigenen Computer ausführen](self-hosted-setup.md).

## Suche nach Bedeutung

Unter **Einstellungen** findest du die Option **Modell**. Damit findest du E-Mails, Nachrichten und Notizen anhand ihres Inhalts, nicht nur anhand ihrer Wörter. Auf einer gehosteten Machine übernimmt das eine kleine KI direkt auf der Machine. Es wird nichts weitergegeben. Ab 8 GB Arbeitsspeicher ist die Funktion aktiviert. Bei 4 GB kannst du sie mit dem Schalter aktivieren. Sie benötigt etwa ein halbes Gigabyte Arbeitsspeicher und kann eine stark ausgelastete Machine verlangsamen. Ist sie ausgeschaltet, sucht die Vorbereitung einer Aufgabe weiterhin anhand von Wörtern nach passenden Nachrichten.

Auf deinem eigenen Computer findest du die Funktion im Block `embeddings` in `config.json`. Starte die Machine nach einer Änderung neu.

## Auf dieser Machine

Wenn deine Machine auf deinem eigenen Computer läuft, erledigst du ein paar Dinge dort in einem Terminal:

- Die Einstellungsdatei `config.json`: Alle Einstellungen an einem Ort. Starte die Machine nach einer Änderung neu.
- `assistant connect`: Eine Quelle hinzufügen, zum Beispiel `assistant connect gmail` oder `assistant connect outlook`.
- `assistant telegram on` oder `off`: Nachrichten auf Telegram. Siehe [Telegram](telegram.md).
- `assistant doctor`: Überprüft alles und gibt für jedes Problem eine Lösung aus.

## Deine Adressen

Hier findest du alle Adressen von dir, die deine Machine gefunden hat: deine Konten, Gmail- oder Outlook-Aliasse, deinen Kalender sowie deine Slack- und Intercom-Profile. E-Mails und Termine von jeder dieser Adressen gelten als deine. Wähle **Entfernen** für eine Adresse, die nicht dir gehört.

Eine gemeinsam genutzte Adresse wie info@ oder eine Google Group gilt nie automatisch als deine. Bei Adressen, bei denen sich deine Machine nicht sicher ist, findest du sie unter **Vielleicht deine**. Wähle eine Option:

- **Meine: Nur ich beantworte sie**: Die Adresse gilt als deine. E-Mails an sie können zu deinen Aufgaben werden.
- **Vom Team: Andere beantworten sie auch**: Die Adresse gilt nicht als deine. E-Mails, die nur an diese Adresse gingen, erstellen keine Aufgaben oder Entwürfe für dich. Sie fließen aber weiterhin in den Graph ein.
- **Nicht meine**: Die Adresse gilt nicht als deine.

Entscheide danach, wer die Adresse aktuell beantwortet. Ein Team-Postfach wie support@ gehört dem Team. Eine Adresse wie partnerships@, die nur du beantwortest, gehört dir. Ändere die Einstellung, sobald auch andere darauf antworten.

Mit **Ändern** in der jeweiligen Zeile kannst du die Einstellung später ändern. Deine eigene Anmeldeadresse gilt immer als deine.

### Domains deiner Firma

Die Domains deiner eigenen Adressen gelten als Domains deiner Firma. Verwendest du noch eine andere, zum Beispiel acme.co zusätzlich zu acme.com? Gib sie unter **Domains deiner Firma** ein und wähle **Hinzufügen**.

Personen mit diesen Domains gelten dann als Kolleg:innen, nicht als Kund:innen: Ihre Threads erscheinen nicht im Team Graph und es wird keine Organisation für sie erstellt. Mit **Entfernen** kannst du eine Domain wieder löschen. Kostenlose E-Mail-Domains wie gmail.com lassen sich nicht hinzufügen.

Ein Gmail-Alias von dir kann auch als **From** eines Entwurfs verwendet werden, wenn Gmail bestätigt, dass du damit senden kannst. Siehe [Gmail](gmail.md#what-it-can-send).
