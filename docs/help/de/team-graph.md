---
title: Team Graph
area: fleet
summary: Experimentell. Teile Kundenarbeit mit deiner Work Fleet, wie in einem CRM. Erfahre, was geteilt wird und was nicht, und wie du Inhalte privat hältst.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: 9788be6d2d5e3fa6
---
In einer Work Fleet kann deine Machine Kundenarbeit mit den Machines deiner Teammitglieder teilen, ähnlich wie ein gemeinsames CRM. Die Funktion ist **Experimentell** und standardmäßig ausgeschaltet.

## Aktivieren

Ein Admin aktiviert **Den Graph in dieser Fleet teilen** unter **Was geteilt wird** und bestätigt, dass das Unternehmen diese E-Mails teilen darf und die Mitarbeitenden darüber informiert hat. Alle sehen, ob die Funktion aktiviert ist.

Wenn die Fleet die Arbeits-E-Mail oder den Arbeitskalender aller voraussetzt, wird die Funktion ebenfalls aktiviert. Anschließend wählt jede Person unter **Deine Verbindungen** aus, was noch geteilt wird. Die erste Freigabe eines neuen Teammitglieds erfolgt erst nach einer Stunde. So bleibt Zeit, zuerst Inhalte privat zu halten.

## Deine Verbindungen

Unter **Deine Verbindungen** auf **Was geteilt wird** wird jede Verbindung mit einem Schalter aufgeführt. Arbeitsverbindungen mit der Domain deiner Fleet sind standardmäßig aktiviert. Verbindungen mit der Domain eines anderen Unternehmens sind standardmäßig deaktiviert und mit „Anderes Unternehmen, nicht geteilt“ gekennzeichnet. Persönliche Verbindungen werden nie geteilt. Wenn du eine Verbindung ausschaltest, werden die darüber geteilten Inhalte zurückgenommen.

Der Kalender einer anderen Person, den du über deine eigene Anmeldung liest, wird unter seinem eigenen Namen als persönlich angezeigt.

Auch innerhalb einer aktivierten Verbindung wird jeder Nachrichtenverlauf einzeln eingestuft. Der Slack deines Unternehmens zählt nur als Austausch mit Kollegen. Nur ein Slack Connect-Chat mit einem anderen Unternehmen kann Kundenarbeit sein. Persönliche, nur unter Kollegen geführte, sensible und automatisierte Nachrichtenverläufe bleiben außen vor, sofern du sie nicht selbst teilst.

## Von der Fleet verlangt

Ein Admin kann unter **Von der Fleet verlangt** die **Arbeits-E-Mail** und den **Arbeitskalender** aller mit der Domain der Fleet voraussetzen, nachdem bestätigt wurde, dass das Unternehmen die Mitarbeitenden informiert hat. Arbeits-E-Mails gehören dem Unternehmen, wie bei jedem CRM. Erforderliche Verbindungen sind als „Von deiner Fleet verlangt“ gekennzeichnet und lassen sich nicht ausschalten. Nachrichtenverläufe, die du privat hältst, bleiben privat.

## Was das Team sieht

- Nachrichtenverläufe mit Kunden: Arbeits-E-Mails mit Personen außerhalb deines Unternehmens, einschließlich Anhängen.
- Berufliche Kontakte, Unternehmen und Projekte mit einem kurzen Verlauf. Auf der **Verlauf**-Seite zeigt **Team** jedes Ereignis einmal an. Wenn die Machine eines Teammitglieds es so verfasst hat, erscheint es in deiner Sprache und mit allen Beteiligten: „über Sam, Kim und Lee“.
- Eine kleine Kopie des Logos eines Unternehmens und des Arbeitsfotos einer Person. Die Bilder stammen aus einer Suche, aus Slack, LinkedIn, X, Salesflare oder Microsoft. Bilder aus Google Kontakte, WhatsApp, Telegram oder Facebook werden nie geteilt. Auch Bilder, die du geändert oder entfernt hast, bleiben außen vor.
- Auf einem Team-Board: die Besprechungen eines Projekts, Zoom-Notizen, Intercom-Unterhaltungen und Chats. Sensible Inhalte wie Geschäfte und Chats nur unter Kollegen bleiben außen vor.
- Anzahl und Daten der [Team-Briefings](fleet.md#brief-requests) eines Teammitglieds.
- Antworten, wenn ein Teammitglied fragt, wer jemanden kennt oder Kontext zu einer Besprechung braucht. Siehe [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Erkenntnisse des Teams](fleet.md#team-learnings): wie das Team arbeitet, ohne Namen oder Kundendetails.

## Nicht automatisch geteilt

- Sensible Nachrichtenverläufe: über den Kauf oder Verkauf eines Unternehmens, Investitionen, Verhandlungen, Personal und Einstellungen, Rechtliches, Gesundheit, Geld und Sicherheit. Nicht einmal, dass es sie gibt.
- Automatisierte E-Mails: Belege, Rechnungen, Benachrichtigungen, Newsletter und Rechnungen von Lieferanten.
- Nachrichtenverläufe nur unter Kollegen, persönliche E-Mails und alles von einem persönlichen Konto. Persönliche Inhalte werden nie geteilt, auch nicht, wenn du auf Team tippst.
- Alles, was du mit **Privat halten** markiert hast, sowie Boards und Projekte, die auf „Nur du“ gesetzt sind.
- Personen, die für dich persönlich sind, etwa Familie oder Freunde, und deren E-Mails. Ein Projekt, an dem sie beteiligt sind, wird trotzdem mit seinem Board geteilt, nur ohne sie.

Jeder Nachrichtenverlauf wird nach seinem Inhalt eingestuft. Das kann falsch sein. Prüfe, was geteilt würde, und korrigiere die Einstufung mit **Privat halten**. Wenn du einen Nachrichtenverlauf selbst mit dem Team oder bestimmten Personen teilst, hat das Vorrang vor einer Einstufung als sensibel. Prüfe also, wer Zugriff erhält.

## Ein Board mit ausgewählten Personen teilen

Tippe im Menü **⋯** eines Boards auf **Board teilen…** und wähle Teammitglieder aus. Nur sie erhalten die Projekte des Boards mit vollständigem Verlauf: E-Mails, Besprechungen und Zoom-Notizen, Intercom-Unterhaltungen, Chats, Aufgaben und Änderungen. Auch sensible Inhalte wie Geschäfte werden geteilt.

Persönliche und nur unter Kollegen geführte Nachrichtenverläufe bleiben außen vor. Das gilt auch für deine Familie und Freunde, automatisierte E-Mails und Verbindungen, die du nicht ausgewählt hast.

- Ein Projekt, das später zum Board hinzugefügt wird, wird ebenfalls geteilt. Wird es vom Board entfernt, wird die Freigabe zurückgenommen.
- Entferne eine Person oder wähle niemanden aus, wird der Inhalt aus der Machine dieser Person zurückgenommen.
- Um einen Nachrichtenverlauf mit ausgewählten Personen zu teilen, tippe auf seine Kennzeichnung und dann auf **Teilen mit…**. So kannst du sensible oder automatisierte Arbeits-E-Mails teilen, aber nie persönliche oder nur unter Kollegen geführte Nachrichtenverläufe.

## Unsicher? Dann wartet es

Wenn deine Machine unsicher ist, teilt sie nichts. Solche Nachrichtenverläufe warten unter **Diese teilen?**. Sie sind nach Themen gruppiert, etwa „Austausch mit Partnern und Inseraten“, und für jede Gruppe gibt es einen Vorschlag:

- **Mit Team teilen**: mit allen in der Fleet.
- **Teilen mit…**: nur mit den Teammitgliedern, die du auswählst, etwa einem Board-Mitglied für Gespräche mit Investoren.
- **Privat halten**: der Inhalt bleibt bei dir.

Mit einem Tippen entscheidest du für eine ganze Gruppe. Öffne eine Gruppe, um einzelne Nachrichtenverläufe abzuwählen und separat zu entscheiden.

Gespräche über den Kauf, Verkauf oder die Investition in ein Unternehmen sowie Angelegenheiten des Boards sind sensibel. Sie werden deshalb hier nicht angezeigt. Die tägliche Zusammenarbeit mit einem Partnerunternehmen zählt als Kundenarbeit.

## Vor der ersten Freigabe

Eine Stunde nachdem deine Machine dich informiert hat, wird deine erste Freigabe automatisch geteilt. Öffne in dieser Stunde **„Fleet“** und dann **Was geteilt wird**, um die Kundenverläufe zu sehen, die nach Unternehmen geteilt würden. Tippe bei einzelnen Verläufen auf **Privat halten** oder auf **Jetzt teilen**, um sie sofort zu teilen. Admins sehen, wer noch nichts geteilt hat.

## Was geteilt wird

Unter **„Fleet“** › **Was geteilt wird** siehst du alles: die Anzahl pro Kategorie, jeden geteilten Nachrichtenverlauf und den Grund für die Freigabe, die Einträge unter **Diese teilen?** und alles, was du privat hältst. Tippe auf einen Betreff, um ihn zu lesen. Auch **Einstellungen** und die Kennzeichnung jedes Nachrichtenverlaufs führen hierher.

Ein neuer Nachrichtenverlauf mit einem Kunden wartet eine Stunde, bevor er geteilt wird. So hast du Zeit, deine Entscheidung zu ändern. Danach wird er innerhalb einer halben Stunde geteilt. Das Zurücknehmen einer Freigabe und **Privat halten** werden deinem Team innerhalb von 5 Minuten angezeigt.

## Freigabe zurücknehmen

Tippe bei einem Nachrichtenverlauf auf die Kennzeichnung **Team** und dann auf **Nicht mehr teilen**. Die Machine jedes Teammitglieds löscht den Nachrichtenverlauf, seine Anhänge und die dazugehörigen Verlaufseinträge. Ist eine Machine offline, werden die Inhalte gelöscht, sobald sie wieder online ist. Jemand könnte sie bereits gelesen haben.

Mit **Privat halten** bei einer Person, einem Unternehmen oder einem Projekt nimmst du alle dazugehörigen Freigaben zurück.

Wenn du zwei Nachrichtenverläufe desselben Unternehmens privat hältst, fragt deine Machine einmal, ob du dieses Unternehmen immer privat halten möchtest.

## Wer sieht die Inhalte?

Nur die Machines deiner Teammitglieder. Die Inhalte sind Ende-zu-Ende verschlüsselt. The Machine Network leitet sie weiter, kann sie aber nicht lesen.

## Beitritt und neue Geräte

Ein Admin lässt jede Person einmalig zur Fleet zu. Die Anfrage wird bei allen Admins unter **Aufgaben** angezeigt. Die erste Antwort zählt. Danach ist für das Teilen keine weitere Bestätigung nötig.

Bis dahin zeigen der Graph und die Fleet der neuen Person an, auf welche Admins sie noch wartet. **Meine** und **Team** werden wenige Sekunden nach der Bestätigung angezeigt, ohne dass du neu laden musst.

Eine neue Machine einer Person, die bereits dabei ist, erhält den Graph des Teams nach 24 Stunden. Bis dahin können Admins auf **Nicht von der Person** tippen, damit er nicht geteilt wird.

## Wenn jemand geht

Ab diesem Zeitpunkt erhält die Person nichts Neues mehr. Was sie geteilt hat, bleibt beim Team. Ein Admin kann die Person außerdem mit **Herausnehmen** entfernen und später wieder **Erneut teilen**.

## Teilen für alle ausschalten

Ein Admin deaktiviert **Den Graph in dieser Fleet teilen** unter **Was geteilt wird**. Danach wird nichts Neues geteilt.

**Ausschalten** lässt die Inhalte auf den Machines der Teammitglieder. Mit **Ausschalten und geteilte Daten entfernen** werden sie von jeder Machine gelöscht. Wird das Teilen wieder aktiviert, prüft jede Person die Inhalte vorher erneut.

## Eigene Arbeit nicht mehr teilen

Schalte deine Verbindungen unter **Deine Verbindungen** aus, sofern die Fleet sie nicht voraussetzt. Die darüber geteilten Inhalte werden zurückgenommen.

Siehe auch [Fleets](fleet.md) und [Sicherheit und Datenschutz](security-and-privacy.md).
