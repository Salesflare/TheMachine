---
title: Team Graph
area: fleet
summary: Experimentell. Teile Kundenarbeit mit deiner Work Fleet, ähnlich wie bei einem CRM. Was geteilt wird, was privat bleibt und wie du etwas für dich behältst.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
In einer Work Fleet kann deine Machine Kundenarbeit mit den Machines deiner Teammitglieder teilen, ähnlich wie bei einem gemeinsamen CRM. Die Funktion ist **Experimentell** und standardmäßig ausgeschaltet.

## Einschalten

Ein Admin schaltet **Den Graph in dieser Fleet teilen** unter **Was geteilt wird** ein und bestätigt, dass das Unternehmen diese E-Mail teilen darf und seine Mitarbeitenden darüber informiert hat. Alle sehen, ob die Funktion eingeschaltet ist.

Wenn die Work-E-Mail oder der Arbeitskalender aller Personen verlangt wird, wird die Funktion ebenfalls eingeschaltet. Danach wählt jede Person unter **Deine Verbindungen** aus, was sonst noch geteilt wird. Die erste Freigabe eines neuen Teammitglieds erfolgt erst nach einer Stunde. So kann die Person vorher Dinge privat halten.

## Deine Verbindungen

Unter **Was geteilt wird** listet **Deine Verbindungen** jede Verbindung mit einem Schalter auf. Arbeitsverbindungen mit der Domain deiner Fleet sind standardmäßig eingeschaltet. Verbindungen mit der Domain eines anderen Unternehmens sind standardmäßig ausgeschaltet und mit „Anderes Unternehmen, nicht geteilt“ gekennzeichnet. Private Verbindungen werden nie geteilt. Wenn du eine Verbindung ausschaltest, werden die darüber geteilten Inhalte wieder entfernt.

Ein Kalender, den du über deine eigene Anmeldung mitliest, wird unter seinem eigenen Namen als privat angezeigt.

Auch bei einer eingeschalteten Verbindung wird jeder Thread einzeln bewertet. Der Slack deines Unternehmens zählt nur als Kommunikation mit Kolleginnen und Kollegen. Nur ein Slack-Connect-Chat mit einem anderen Unternehmen kann Kundenarbeit sein. Private Threads, Threads nur mit Kolleginnen und Kollegen, sensible Threads und automatisierte Threads werden nicht geteilt, außer du teilst einen davon selbst.

## Von der Fleet verlangt

Ein Admin kann unter **Von der Fleet verlangt** die **Arbeits-E-Mail** und den **Arbeitskalender** aller Personen mit der Domain der Fleet verlangen, nachdem er bestätigt hat, dass das Unternehmen seine Mitarbeitenden darüber informiert hat. Arbeits-E-Mails gehören dem Unternehmen, wie bei jedem CRM. Erforderliche Verbindungen sind mit „Von der Fleet verlangt“ gekennzeichnet und lassen sich nicht ausschalten. Threads, die du privat hältst, bleiben privat.

## Was das Team sieht

- Kunden-Threads: Arbeits-E-Mails mit Personen außerhalb deines Unternehmens, einschließlich Anhängen.
- Arbeitskontakte, Organisationen und Projekte mit einem kurzen Verlauf. Unter **Verlauf** auf einer Seite zeigt **Team** jedes Ereignis einmal an. Die Sprache richtet sich danach, in welcher Sprache die Machine eines Teammitglieds das Ereignis verfasst hat. Dazu wird angezeigt, von wem es stammt: „über Sam, Kim und Lee“.
- Eine kleine Kopie des Logos einer Organisation und des Arbeitsfotos einer Person, falls verfügbar: aus einer Suche, aus Slack, LinkedIn, X, Salesflare oder Microsoft. Nie ein Bild aus Google-Kontakten, WhatsApp, Telegram oder Facebook und nie ein Bild, das du geändert oder entfernt hast.
- Auf einem Team-Board: Meetings, Zoom-Notizen, Intercom-Unterhaltungen und Chats eines Projekts. Sensible Inhalte wie Deals und Threads nur mit Kolleginnen und Kollegen bleiben außen vor.
- Anzahl und Daten der [Team-Briefings](fleet.md#brief-requests) eines Teammitglieds.
- Antworten, wenn ein Teammitglied fragt, wer jemanden kennt, oder Kontext zu einem Meeting braucht. Siehe [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Team-Erkenntnisse](fleet.md#team-learnings): wie das Team arbeitet, ohne Namen oder Kundendetails.

## Wird nicht automatisch geteilt

- Sensible Threads: über den Kauf oder Verkauf eines Unternehmens, Investitionen, Verhandlungen über Deals, Personalwesen und Einstellungen, Rechtliches, Gesundheit, Geld und Sicherheit. Nicht einmal, dass es sie gibt.
- Automatisierte E-Mails: Belege, Rechnungen, Benachrichtigungen, Newsletter und Lieferantenrechnungen.
- Threads nur mit Kolleginnen und Kollegen, private E-Mails und alles von einem privaten Konto. Private Inhalte werden nie geteilt, auch nicht, wenn du auf Team tippst.
- Alles, was du mit **Privat halten** markiert hast, sowie Boards und Projekte, die auf „Nur du“ gesetzt sind.
- Personen, die für dich privat sind, etwa deine Familie oder Freunde, und deren E-Mails. Ein Projekt, an dem sie beteiligt sind, wird trotzdem mit seinem Board geteilt, aber ohne sie.

Jeder Thread wird nach seinem Inhalt beurteilt. Dabei kann es zu Fehlern kommen. Prüfe, was geteilt würde, und nutze „Privat halten“, um die Auswahl zu korrigieren. Wenn du selbst einen Thread mit dem Team oder bestimmten Personen teilst, wird eine Kennzeichnung als sensibel übergangen. Prüfe deshalb, wer Zugriff erhält.

## Ein Board mit ausgewählten Personen teilen

Tippe im Menü **⋯** eines Boards auf **Board teilen…** und wähle Teammitglieder aus. Nur sie erhalten die zugehörigen Projekte mit vollständigem Verlauf: E-Mails, Meetings und Zoom-Notizen, Intercom-Unterhaltungen, Chats, Aufgaben und Änderungen. Auch sensible Inhalte wie Deals werden geteilt.

Private Threads und Threads nur mit Kolleginnen und Kollegen bleiben außen vor. Das gilt auch für deine Familie und Freunde, automatisierte E-Mails und Verbindungen, die du nicht ausgewählt hast.

- Ein Projekt, das später zum Board hinzugefügt wird, wird ebenfalls geteilt. Wird es vom Board entfernt, wird es wieder entzogen.
- Wenn du jemanden entfernst oder niemanden auswählst, wird der Zugriff auf die Machine der betreffenden Person wieder entzogen.
- Um einen einzelnen Thread mit bestimmten Personen zu teilen, tippe auf seine Kennzeichnung und dann auf **Teilen mit…**. Dazu können sensible oder automatisierte Arbeits-E-Mails gehören, aber niemals private Threads oder Threads nur mit Kolleginnen und Kollegen.

## Noch unsicher? Es bleibt erst einmal offen

Wenn deine Machine unsicher ist, teilt sie nichts. Diese Threads warten unter **Diese teilen?** und sind nach Art gruppiert, zum Beispiel „Austausch mit Partnern und über Inserate“. Für jede Gruppe gibt es einen Vorschlag:

- **Mit Team teilen**: mit allen in der Fleet.
- **Teilen mit…**: nur mit den Teammitgliedern, die du auswählst, zum Beispiel einem Board-Mitglied für Gespräche mit Investorinnen und Investoren.
- **Privat halten**: Der Inhalt bleibt bei dir.

Mit einem Tippen entscheidest du für eine ganze Gruppe. Öffne eine Gruppe, um einzelne Threads abzuwählen und selbst zu entscheiden.

Gespräche über den Kauf, Verkauf oder die Investition in ein Unternehmen sowie Angelegenheiten des Boards sind sensibel und warten deshalb nicht hier. Gewöhnliche Arbeit mit einem Partnerunternehmen zählt als Kundenarbeit.

## Vor der ersten Freigabe

Eine Stunde nachdem deine Machine dich informiert hat, wird deine erste Freigabe automatisch geteilt. Öffne in dieser Stunde **Fleet** und dann **Was geteilt wird**, um die Kunden-Threads zu sehen, die nach Organisation geteilt würden. Tippe bei einzelnen Threads auf **Privat halten** oder auf **Jetzt teilen**, um sie sofort zu teilen. Admins sehen, wer noch nichts geteilt hat.

## Was geteilt wird

Unter **Fleet** › **Was geteilt wird** siehst du alles: die Anzahl je Art, jeden geteilten Thread mit dem Grund für die Freigabe, die Threads unter **Diese teilen?** und alles, was du privat hältst. Tippe auf einen Betreff, um ihn zu lesen. Auch **Einstellungen** und die Kennzeichnung jedes Threads führen hierher.

Ein neuer Kunden-Thread wartet eine Stunde, bevor er geteilt wird. So hast du Zeit, es dir anders zu überlegen.

## Freigabe aufheben

Tippe bei einem Thread auf die Kennzeichnung **Team** und dann auf **Nicht mehr teilen**. Die Machine jedes Teammitglieds löscht den Thread, seine Anhänge und die zugehörigen Verlaufszeilen. Ist sie gerade offline, geschieht das, sobald sie wieder online ist. Jemand könnte den Inhalt bereits gelesen haben.

Wenn du bei einer Person, Organisation oder einem Projekt auf **Privat halten** tippst, wird alles davon nicht mehr geteilt.

Wenn du zwei Threads mit demselben Unternehmen privat hältst, fragt deine Machine einmal, ob du dieses Unternehmen immer privat halten möchtest.

## Wer sieht die Inhalte?

Nur die Machines deiner Teammitglieder. Die Inhalte sind Ende-zu-Ende-verschlüsselt. The Machine Network leitet sie weiter, kann sie aber nicht lesen.

## Beitritt und neue Geräte

Ein Admin lässt jede Person einmalig zu. Die Anfrage erscheint bei jedem Admin unter **Aufgaben**. Die erste Antwort zählt. Danach sind für das Teilen keine weiteren Bestätigungen nötig.

Bis dahin zeigen der Graph und die Fleet der neuen Person an, auf welche Admins sie wartet. **Meine** und **Team** erscheinen wenige Sekunden nach der Bestätigung, ohne dass die Seite neu geladen werden muss.

Eine neue Machine einer bereits aufgenommenen Person erhält den Graph des Teams nach 24 Stunden. In der Zwischenzeit können Admins auf **Nicht von der Person** tippen, damit er nicht geteilt wird.

## Wenn jemand das Team verlässt

Ab diesem Zeitpunkt erhält die Person nichts Neues mehr. Was sie geteilt hat, bleibt beim Team. Ein Admin kann die Person auch **Herausnehmen** und später **Erneut teilen**.

## Teilen für alle ausschalten

Ein Admin schaltet **Den Graph in dieser Fleet teilen** unter **Was geteilt wird** aus. Danach werden keine neuen Inhalte geteilt.

**Ausschalten** lässt die Inhalte bestehen, die Teammitglieder bereits erhalten haben. **Ausschalten und geteilte Daten entfernen** löscht sie auf jeder Machine. Wird das Teilen wieder eingeschaltet, prüft jede Person die Inhalte zuerst erneut.

## Eigene Arbeit nicht mehr teilen

Schalte deine Verbindungen unter **Deine Verbindungen** aus, sofern die Fleet sie nicht verlangt. Die darüber geteilten Inhalte werden wieder entfernt.

Siehe auch [Fleets](fleet.md) und [Sicherheit und Datenschutz](security-and-privacy.md).
