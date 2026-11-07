---
title: Einstellungen
area: settings
summary: Wo du jede Einstellung findest, vom hellen Modus bis zu Sicherheit und deinem Konto.
covers: settings:general
code: dashboard.html
order: 1
---
Öffne **Einstellungen** über das Zahnrad oben. Die Tabs:

- **Konto**: **Deine Adressen**, die als du zählen, jeweils mit Herkunft, und **Abmelden**. Auf einer gehosteten Machine auch dein Tarif, Rechnungen, Machine, Fleet, Adresse, Freunde, Anmeldung und Daten, jeweils mit Button. Siehe [Tarife und Abrechnung](plans-and-billing.md). **Abmelden** steht oben, **Tarif kündigen** und **Konto löschen** ganz unten. Auf einer Machine auf deinem eigenen Computer, mit dem Network gekoppelt: deine Fleet, Benutzername, Freunde und Anmeldung, jeweils mit einem Link, der diesen Teil deines Kontos öffnet (dort anmelden), und **Konto löschen** ganz unten.
- **Allgemein**: Sprache und Region, Spracheingabe, dieses Gerät, der Browser deiner Machine, deine Fleet, Export und Import und dein Konto.
- **Sicherheit**: Standard oder Vorsichtig und die Einstellungen, die sie festlegen. Siehe [Sicherheitsstufen](security-levels.md). Auch **Support-Zugriff**, solange er an ist: siehe [Support bekommen](get-support.md#support-access).
- **Aktivität**: alles, was The Machine für dich getan hat, das Neueste zuerst. Siehe [Aktivität](activity.md).
- **Benachrichtigungen**: was dich wo erreicht, und deine Arbeitszeiten. Siehe [Benachrichtigungen](notifications.md) und [Arbeitszeiten](work-hours.md).
- **Schreiben**: Signaturen und wie du schreibst. Siehe [Schreiben](writing.md).
- **Skills**: Anleitungen, denen deine Machine folgt. Siehe [Skills](skills.md).
- **Apps**: die Apps von The Machine für Handy und Computer, dann Claude, ChatGPT und andere KIs, die du verbunden hast, und was jede darf. Siehe [Die mobile App](mobile-app.md) und [Andere KIs verbinden](ai-connections.md).
- **Modell**: was für dich antwortet, und seine Limits. Siehe [Modell](model.md). Auch **Codex und Claude Code**: siehe [An Claude Code oder Codex übergeben](hand-to-agent.md).

Ein Tab ohne Inhalt wird ausgeblendet.

## Allgemein

- **Sprache und Region**: Deine **Region** legt fest, wie Daten aussehen (24. Okt. oder Oct 24), und die übliche Uhr. **Zeitformat** wählt stattdessen 12 Stunden (2:05 PM) oder 24 Stunden (14:05). Aufgaben, Telegram, die Zusammenfassung und Nachrichten aus der Fleet folgen dem. Eine gehostete Machine startet mit dem Land der Zeitzone, die du bei der Registrierung gewählt hast. Angaben wie „vor 3 Stunden“ und Zahlen folgen dem ebenfalls.
- **Sprache**: English, Nederlands, Français, Deutsch, Español, Italiano oder Português (Brasil). Beim ersten Öffnen des Dashboards wird die Sprache deines Browsers gewählt, wenn sie eine davon ist (Portugiesisch aus Portugal bekommt vorerst brasilianisches Portugiesisch). Das Dashboard, Datumsangaben, Telegram-Nachrichten, Benachrichtigungen, der Wochenrückblick sowie die Notizen und Aufgabentitel, die deine Machine für dich schreibt, folgen ihr ab dem Moment, in dem du sie wählst. Was schon geschrieben ist, bleibt, wie es war. Fragen aus Fleet und Familie erscheinen in der eigenen Sprache jedes Teammitglieds. Entwürfe an andere Personen bleiben in der Sprache ihrer Unterhaltung. Auch die Hilfe und ihre Seiten folgen ihr.
- **Dieses Gerät**: die App (**App installieren**), **Benachrichtigungen** mit **Test senden** und **Heller Modus**, nur für diesen Browser oder dieses Handy. Siehe [App installieren und Benachrichtigungen einschalten](phone-app.md).
- **Spracheingabe**: wie aus dem, was du sagst, Text wird, und die Stimme von Live sprechen. Siehe [Spracheingabe](voice-input.md) und [Live sprechen](talk-live.md).
- **Browser der Machine öffnen ↗**: der Browser, den deine Machine für Websites wie LinkedIn nutzt.
- **Fleet-Regeln**: siehe [Freigaberegeln](sharing-rules.md).
- **Exportieren**:
  - **Alles**: alles, was deine Machine weiß, in einer verschlüsselten Datei, zum Umziehen oder Aufbewahren, und **Importieren**, um einen hereinzuholen. Siehe [Auf einen anderen Computer umziehen](moving.md).
  - **Wissen für eine andere KI**: was deine Machine gelernt hat, in Dateien, die jede KI lesen kann. Siehe [Wissen für eine andere KI](knowledge-export.md).

## Auf dieser Machine

Ein paar Einstellungen liegen auf dem Computer, auf dem deine Machine läuft, nicht in der App:

- `config.json`: jede Einstellung, in einer Datei. Starte die Machine nach einer Änderung neu.
- `assistant connect`: eine Quelle hinzufügen, etwa `assistant connect gmail` oder `assistant connect outlook`.
- `assistant telegram on` oder `off`: Nachrichten über Telegram. Siehe [Telegram](telegram.md).
- `assistant doctor`: prüft alles und zeigt für jedes Problem eine Lösung.

## Deine Adressen

Jede deiner Adressen, die die Machine gefunden hat: deine Konten, Aliasse in Gmail oder Outlook, dein Kalender, dein Profil in Slack und Intercom. Mails und Meetings von jeder davon erscheinen als du. **Entferne** eine, die nicht deine ist.

Eine geteilte Adresse wie info@ oder eine Google Group zählt nie von selbst. Eine, bei der sich die Machine nicht sicher ist, steht unter **Vielleicht deine**, und nichts wird für dich ausgewählt. Wähle eins:

- **Meine: Nur ich beantworte sie**: Sie zählt als deine. Mails an sie können deine Aufgaben werden.
- **Vom Team: Andere beantworten sie auch**: Sie ist nicht du. Mails nur an diese Adresse machen dir keine Aufgaben und keine Entwürfe. Sie füllt weiter den Graph, mit deinem Team geteilt wie bisher.
- **Nicht meine**: Sie zählt nicht als deine.

Wähle danach, wer sie heute beantwortet. Ein Team-Postfach wie support@ ist vom Team. Eine Adresse wie partnerships@, die gerade nur du beantwortest, ist deine; stell sie auf Team um, sobald andere sie auch beantworten.

**Ändern** in ihrer Zeile stellt es später um. Deine eigene Anmeldeadresse ist immer deine.

### Domains deiner Firma

Die Domains deiner eigenen Adressen zählen als die deiner Firma. Nutzt sie noch eine weitere, etwa acme.co neben acme.com, gib sie unter **Domains deiner Firma** ein und drücke **Hinzufügen**.

Leute dort sind dann deine Kollegen, nie Kunden: Ihre Threads bleiben aus dem Team Graph wie jeder Thread nur unter Kollegen, und es entsteht keine Organisation dafür. **Entfernen** nimmt sie wieder raus. Eine kostenlose E-Mail-Domain wie gmail.com geht nicht.

Ein Gmail-Alias von dir kann auch **Von** eines Entwurfs sein, wenn Gmail bestätigt, dass du als dieser Alias senden kannst. Siehe [Gmail](gmail.md#what-it-can-send).
