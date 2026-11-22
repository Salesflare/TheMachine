---
title: Einstellungen
area: settings
summary: Wo du die einzelnen Einstellungen findest, von hellem Modus bis zu Sicherheit und Konto.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Öffne **Einstellungen** über das Zahnrad oben. Die Tabs:

- **Konto**: Oben findest du **Deine Adressen** (Adressen, die als deine gelten) und **Abmelden**. Bei einer gehosteten Machine außerdem deinen Tarif, Rechnungen, Fleet, Freunde, Anmeldung und Daten. Ganz unten findest du **Tarif kündigen** und **Konto löschen**. Bei einer Machine auf deinem eigenen Computer, die mit dem Network verbunden ist: Fleet, Benutzername, Freunde und Anmeldung, jeweils mit einem Link zu diesem Bereich deines Kontos (melde dich dort an), sowie ganz unten **Konto löschen**. Noch nicht verbunden? Oben findest du **Dem Network beitreten**. Weitere Informationen findest du unter [Tarife und Abrechnung](plans-and-billing.md).
- **Allgemein**: Sprache und Region, dieses Gerät, Spracheingabe, der Browser deiner Machine, deine Fleet, Export und Import sowie die Version, die sie ausführt. Wenn es keinen Tab „Konto“ gibt, findest du **Dem Network beitreten** ganz unten.
- **Sicherheit**: Standard oder Vorsichtig. Weitere Informationen findest du unter [Sicherheitsstufen](security-levels.md). Außerdem **Support-Zugriff**, solange er aktiviert ist: siehe [Support kontaktieren](get-support.md#support-access).
- **Aktivität**: Alles, was The Machine für dich getan hat, neueste Einträge zuerst. Weitere Informationen findest du unter [Aktivität](activity.md).
- **Benachrichtigungen**: Welche Benachrichtigungen dich wo erreichen und deine Arbeitszeiten. Weitere Informationen findest du unter [Benachrichtigungen](notifications.md) und [Arbeitszeiten](work-hours.md).
- **Schreiben**: Signaturen und dein Schreibstil. Weitere Informationen findest du unter [Schreiben](writing.md).
- **Skills**: Anleitungen, an die sich deine Machine hält. Weitere Informationen findest du unter [Skills](skills.md).
- **Apps**: Zuerst die Apps von The Machine für dein Handy und deinen Computer, dann Claude, ChatGPT und andere KIs, die du verbunden hast, und was sie jeweils tun dürfen. Weitere Informationen findest du unter [Die mobile App](mobile-app.md) und [Andere KIs verbinden](ai-connections.md).
- **Modell**: Die KI, die für dich liest und Entwürfe erstellt, und ihre Grenzen. Weitere Informationen findest du unter [Modell](model.md). Außerdem **Codex und Claude Code**: siehe [An Claude Code oder Codex übergeben](hand-to-agent.md). Und weiter unten **Suche nach Bedeutung**.

Ein Tab ohne Inhalte wird ausgeblendet.

## Allgemein

- **Sprache und Region**: Mit **Region** legst du fest, wie Datumsangaben, Uhrzeiten und Zahlen angezeigt werden (Oct 24 oder 24. Okt.). Unter **Zeitformat** wählst du zwischen 12-Stunden-Format (2:05 PM) und 24-Stunden-Format (14:05). Aufgaben, Telegram, die Zusammenfassung und Fleet-Nachrichten richten sich nach beiden Einstellungen. Bei einer gehosteten Machine wird zunächst die Zeitzone verwendet, die du bei der Anmeldung ausgewählt hast.
- **Sprache**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 oder Русский. Standardmäßig wird die Sprache deines Browsers verwendet. Das Dashboard, die Hilfe, Benachrichtigungen, Telegram, der Wochenrückblick und die Aufgaben, die deine Machine erstellt, wechseln ab dem Zeitpunkt deiner Auswahl zur neuen Sprache. Ältere Texte bleiben unverändert. Deine Teammitglieder erhalten Fleet- und Family-Anfragen in ihrer eigenen Sprache. Entwürfe an andere bleiben in der Sprache des jeweiligen Gesprächs.
- **Dieses Gerät**: **App installieren**, **Benachrichtigungen** mit **Test senden** und **Heller Modus**, nur für diesen Browser oder dieses Handy. Weitere Informationen findest du unter [App installieren und Benachrichtigungen einschalten](phone-app.md). Unter [Omarchy](omarchy.md) gibt es außerdem **Omarchy-Theme**.
- **Spracheingabe**: Wie deine gesprochenen Worte zu Text werden und wie Talk live klingt. Weitere Informationen findest du unter [Spracheingabe](voice-input.md) und [Talk live](talk-live.md).
- **Browser der Machine öffnen ↗**: Der Browser, den deine Machine für Websites wie LinkedIn verwendet.
- **Fleet-Regeln**: Weitere Informationen findest du unter [Freigaberegeln](sharing-rules.md).
- **Exportieren**:
  - **Alles**: Alles, was deine Machine weiß, in einer verschlüsselten Datei, zum Übertragen oder Aufbewahren. Mit **Importieren** kannst du eine Datei importieren. Weitere Informationen findest du unter [Auf einen anderen Computer umziehen](moving.md).
  - **Wissen für eine andere KI**: Was deine Machine gelernt hat, in Dateien, die jede KI lesen kann. Weitere Informationen findest du unter [Wissen für eine andere KI](knowledge-export.md).

## Version

Die Version, die deine Machine ausführt. Updates werden automatisch installiert. Wenn auf einer gehosteten Machine eine neuere Version bereitsteht, wird sie mit **Jetzt aktualisieren** sofort installiert. Das dauert ein paar Minuten. Deine Daten bleiben erhalten.

Auf deinem eigenen Computer installiert ein täglicher Timer jede neue signierte Version unter Linux. Weitere Informationen findest du unter [Auf dem eigenen Computer ausführen](self-hosted-setup.md).

## Suche nach Bedeutung

Unter **Einstellungen** > **Modell**. Damit findest du E-Mails, Nachrichten und Notizen nach ihrem Thema, nicht nur nach ihren Wörtern. Auf einer gehosteten Machine erledigt das eine kleine KI direkt auf der Machine. Dabei werden keine Daten irgendwohin gesendet. Ab 8 GB Arbeitsspeicher ist die Funktion aktiviert. Bei 4 GB kannst du sie über den Schalter aktivieren. Sie belegt etwa ein halbes Gigabyte. Bei hoher Auslastung kann deine Machine dadurch langsamer werden.

Auf deinem eigenen Computer findest du dafür den Block `embeddings` in `config.json`. Starte die Machine nach einer Änderung neu.

## Auf dieser Machine

Wenn deine Machine auf deinem eigenen Computer läuft, werden einige Dinge dort in einem Terminal erledigt:

- Die Einstellungsdatei `config.json`: alle Einstellungen an einem Ort. Starte die Machine nach einer Änderung neu.
- `assistant connect`: eine Quelle hinzufügen, zum Beispiel `assistant connect gmail` oder `assistant connect outlook`.
- `assistant telegram on` oder `off`: Nachrichten auf Telegram. Weitere Informationen findest du unter [Telegram](telegram.md).
- `assistant doctor`: überprüft alles und gibt für jedes Problem eine Lösung aus.

## Deine Adressen

Alle Adressen von dir, die The Machine gefunden hat: deine Konten, Gmail- oder Outlook-Aliasse, dein Kalender sowie deine Slack- und Intercom-Profile. E-Mails und Besprechungen von all diesen Adressen gelten als deine. Mit **Entfernen** kannst du eine Adresse löschen, die nicht dir gehört.

Eine geteilte Adresse wie info@ oder eine Google Group gilt nie von selbst als deine. Adressen, bei denen sich The Machine nicht sicher ist, warten unter **Vielleicht deine**. Wähle eine Option:

- **Meine: Nur ich beantworte sie**: Die Adresse gilt als deine. E-Mails an diese Adresse können zu deinen Aufgaben werden.
- **Vom Team: Andere beantworten sie auch**: Die Adresse gehört nicht dir. E-Mails, die nur an diese Adresse gesendet wurden, erstellen keine Aufgaben und Entwürfe für dich. Sie fließen aber weiterhin in den Graph ein.
- **Nicht meine**: Die Adresse gilt nicht als deine.

Entscheide danach, wer die Adresse heute beantwortet. Ein gemeinsamer Posteingang wie support@ gehört dem Team. Eine Adresse wie partnerships@, die nur du beantwortest, gehört dir. Ändere die Einstellung, sobald auch andere darauf antworten.

Mit **Ändern** in der jeweiligen Zeile kannst du die Einstellung später ändern. Deine eigene Anmeldeadresse gehört immer dir.

### Domains deiner Firma

Die Domains deiner eigenen Adressen gelten als Domains deiner Firma. Verwendest du noch eine weitere, zum Beispiel acme.co neben acme.com? Gib sie unter **Domains deiner Firma** ein und klicke auf **Hinzufügen**.

Personen mit diesen Domains gelten dann als Kolleginnen und Kollegen, nicht als Kundinnen und Kunden: Ihre Unterhaltungen erscheinen nicht im Team Graph und es wird keine Organisation dafür erstellt. Mit **Entfernen** kannst du eine Domain wieder löschen. Kostenlose E-Mail-Domains wie gmail.com lassen sich nicht hinzufügen.

Ein Gmail-Alias von dir kann auch als **Von** für einen Entwurf verwendet werden, wenn Gmail bestätigt, dass du über diesen Alias senden kannst. Weitere Informationen findest du unter [Gmail](gmail.md#what-it-can-send).
