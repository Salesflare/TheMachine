---
title: Einstellungen
area: settings
summary: Hier findest du alle Einstellungen, von hellem Modus bis zu Sicherheit und Konto.
covers: settings:general
code: dashboard.html
order: 1
translated: 00e42f9aeb395d21
---
Öffne **Einstellungen** über das Zahnrad oben. Die Tabs:

- **Konto**: Oben findest du **Deine Adressen** (Adressen, die dir zugerechnet werden) und **Abmelden**. Bei einer gehosteten Machine findest du hier außerdem deinen Tarif, Rechnungen, Fleet, Freunde, Anmeldung und Daten. Ganz unten stehen **Tarif kündigen** und **Konto löschen**. Bei einer Machine auf deinem eigenen Computer, die mit dem Network verbunden ist, findest du hier Fleet, Benutzername, Freunde und Anmeldung. Jeder Punkt enthält einen Link, der den entsprechenden Bereich deines Kontos öffnet (melde dich dort an). Ganz unten steht **Konto löschen**. Noch nicht verbunden? Oben findest du **Dem Network beitreten**. Weitere Informationen findest du unter [Tarife und Abrechnung](plans-and-billing.md).
- **Allgemein**: Sprache und Region, dieses Gerät, Spracheingabe, der Browser deiner Machine, Fleet, Export und Import sowie die Version, die sie verwendet. Ohne Konto-Tab steht **Dem Network beitreten** ganz unten.
- **Sicherheit**: Standard oder Vorsichtig. Weitere Informationen findest du unter [Sicherheitsstufen](security-levels.md). Außerdem findest du hier **Support-Zugriff**, solange er aktiviert ist. Weitere Informationen findest du unter [Support erhalten](get-support.md#support-access).
- **Aktivität**: Alles, was The Machine für dich getan hat, beginnend mit dem Neuesten. Weitere Informationen findest du unter [Aktivität](activity.md).
- **Benachrichtigungen**: Was dich wo erreicht und deine Arbeitszeiten. Weitere Informationen findest du unter [Benachrichtigungen](notifications.md) und [Arbeitszeiten](work-hours.md).
- **Schreiben**: Signaturen und deine Schreibweise. Weitere Informationen findest du unter [Schreiben](writing.md).
- **Skills**: Anleitungen, an die sich deine Machine hält. Weitere Informationen findest du unter [Skills](skills.md).
- **Apps**: Zuerst die Apps von The Machine für dein Smartphone und deinen Computer, dann Claude, ChatGPT und andere verbundene KIs sowie die Möglichkeiten der einzelnen Apps. Weitere Informationen findest du unter [Die mobile App](mobile-app.md) und [Andere KIs verbinden](ai-connections.md).
- **Modell**: Die KI, die deine E-Mails liest und Entwürfe schreibt, und ihre Grenzen. Weitere Informationen findest du unter [Modell](model.md). Außerdem **Codex und Claude Code**: Weitere Informationen findest du unter [An Claude Code oder Codex übergeben](hand-to-agent.md). Und weiter unten **Suche nach Bedeutung**.

Tabs ohne Inhalte werden ausgeblendet.

## Allgemein

- **Sprache und Region**: Über **Region** legst du fest, wie Datumsangaben, Uhrzeiten und Zahlen angezeigt werden (24. Okt. oder 24. Okt.). Unter **Zeitformat** wählst du das 12-Stunden-Format (2:05 PM) oder das 24-Stunden-Format (14:05). Aufgaben, Telegram, die Zusammenfassung und Fleet-Nachrichten richten sich nach beiden Einstellungen. Bei einer gehosteten Machine wird zunächst die Zeitzone verwendet, die du bei der Anmeldung ausgewählt hast.
- **Sprache**: Englisch, Nederlands, Français, Deutsch, Español, Italiano oder Português (Brasil). Standardmäßig wird die Sprache deines Browsers verwendet. Das Dashboard, die Hilfe, Benachrichtigungen, Telegram, die wöchentliche Zusammenfassung und die Aufgaben, die deine Machine schreibt, wechseln sofort nach deiner Auswahl zur neuen Sprache. Ältere Texte bleiben unverändert. Teammitglieder erhalten Fleet- und Family-Fragen in ihrer eigenen Sprache. Entwürfe an andere Personen bleiben in der Sprache ihres Gesprächs.
- **Dieses Gerät**: **App installieren**, **Benachrichtigungen** mit **Test senden** und **Heller Modus**, nur für diesen Browser oder dieses Smartphone. Weitere Informationen findest du unter [App installieren und Benachrichtigungen aktivieren](phone-app.md). Unter [Omarchy](omarchy.md) gibt es außerdem **Omarchy-Theme**.
- **Spracheingabe**: Wie deine gesprochenen Worte in Text umgewandelt werden und welche Stimme Talk live verwendet. Weitere Informationen findest du unter [Spracheingabe](voice-input.md) und [Talk live](talk-live.md).
- **Browser der Machine öffnen ↗**: Der Browser, den deine Machine für Websites wie LinkedIn verwendet.
- **Fleet-Regeln**: Weitere Informationen findest du unter [Freigaberegeln](sharing-rules.md).
- **Exportieren**:
  - **Alles**: Alles, was deine Machine weiß, in einer verschlüsselten Datei, zum Übertragen oder Aufbewahren. Mit **Importieren** kannst du eine Datei importieren. Weitere Informationen findest du unter [Auf einen anderen Computer umziehen](moving.md).
  - **Wissen für eine andere KI**: Was deine Machine gelernt hat, in Dateien, die jede KI lesen kann. Weitere Informationen findest du unter [Wissen für eine andere KI](knowledge-export.md).

## Version

Die Version, die auf deiner Machine läuft. Updates werden automatisch installiert. Sobald eine neuere Version für eine gehostete Machine verfügbar ist, kannst du sie mit **Jetzt aktualisieren** sofort installieren. Das dauert ein paar Minuten. Deine Daten bleiben erhalten.

Auf deinem eigenen Computer installiert unter Linux ein täglicher Timer jede neue signierte Version. Weitere Informationen findest du unter [Auf dem eigenen Computer ausführen](self-hosted-setup.md).

## Suche nach Bedeutung

Unter **Einstellungen** findest du die Option **Modell**. Damit findest du E-Mails, Nachrichten und Notizen anhand ihres Inhalts, nicht nur anhand ihrer Wörter. Auf einer gehosteten Machine übernimmt das eine kleine KI direkt auf der Machine. Dabei werden keine Daten an andere Stellen gesendet. Ab 8 GB Arbeitsspeicher ist die Funktion aktiviert. Bei 4 GB kannst du sie mit dem Schalter aktivieren. Sie benötigt etwa ein halbes Gigabyte Arbeitsspeicher. Eine stark ausgelastete Machine kann dadurch langsamer werden.

Auf deinem eigenen Computer ist es der Block `embeddings` in `config.json`. Starte die Machine nach einer Änderung neu.

## Auf dieser Machine

Wenn deine Machine auf deinem eigenen Computer läuft, werden einige Dinge dort in einem Terminal erledigt:

- Die Einstellungsdatei `config.json`: alle Einstellungen an einem Ort. Starte die Machine nach einer Änderung neu.
- `assistant connect`: eine Quelle hinzufügen, zum Beispiel `assistant connect gmail` oder `assistant connect outlook`.
- `assistant telegram on` oder `off`: Nachrichten auf Telegram. Weitere Informationen findest du unter [Telegram](telegram.md).
- `assistant doctor`: überprüft alles und gibt für jedes Problem eine Lösung aus.

## Deine Adressen

Alle deine Adressen, die die Machine gefunden hat: deine Konten, Gmail- oder Outlook-Aliasse, dein Kalender sowie deine Slack- und Intercom-Profile. E-Mails und Termine von all diesen Adressen werden dir zugerechnet. Über **Entfernen** kannst du eine Adresse löschen, die nicht dir gehört.

Eine gemeinsam genutzte Adresse wie info@ oder eine Google Group wird nie automatisch dir zugerechnet. Bei Adressen, bei denen sich die Machine nicht sicher ist, findest du sie unter **Vielleicht deine**. Wähle eine Option:

- **Meine: Nur ich beantworte sie**: Die Adresse wird dir zugerechnet. E-Mails an sie können zu deinen Aufgaben werden.
- **Vom Team: Andere beantworten sie auch**: Die Adresse gehört nicht dir. E-Mails, die nur an diese Adresse gingen, führen bei dir weder zu Aufgaben noch zu Entwürfen. Sie fließen aber weiterhin in den Graph ein.
- **Nicht meine**: Die Adresse wird dir nicht zugerechnet.

Entscheide danach, wer heute darauf antwortet. Ein gemeinsames Postfach wie support@ gehört dem Team. Eine Adresse wie partnerships@, auf die nur du antwortest, gehört dir. Ändere die Einstellung, sobald auch andere darauf antworten.

Über **Ändern** in der Zeile kannst du die Einstellung später ändern. Deine eigene Anmeldeadresse gehört immer dir.

### Domains deiner Firma

Die Domains deiner eigenen Adressen gelten als Domains deiner Firma. Verwendest du noch eine andere, zum Beispiel acme.co zusätzlich zu acme.com? Gib sie unter **Domains deiner Firma** ein und klicke auf **Hinzufügen**.

Personen mit diesen Domains gelten dann als Kolleginnen und Kollegen, nicht als Kundinnen oder Kunden. Ihre Unterhaltungen erscheinen nicht im Team-Graph, und es wird keine Organisation dafür erstellt. Über **Entfernen** kannst du eine Domain wieder löschen. Kostenlose E-Mail-Domains wie gmail.com können nicht hinzugefügt werden.

Ein Gmail-Alias von dir kann auch als **Von** für einen Entwurf verwendet werden, wenn Gmail bestätigt, dass du damit E-Mails senden kannst. Weitere Informationen findest du unter [Gmail](gmail.md#what-it-can-send).
