---
title: Team Graph
area: fleet
summary: Experimentell. Teile Kundenarbeit mit deiner Work Fleet, wie in einem CRM. Was mitgeht, was nie, und wie du etwas privat hältst.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
In einer Work Fleet kann deine Machine deine Kundenarbeit mit den Machines deiner Teammitglieder teilen, wie ein gemeinsames CRM. Das ist **Experimentell** und anfangs aus.

## Einschalten

Ein Admin schaltet **Den Graph in dieser Fleet teilen** unter **Was geteilt wird** ein und bestätigt, dass die Firma diese Mails teilen darf und ihre Leute informiert hat. Alle sehen, ob es an ist.

Verlangt die Fleet die Arbeits-E-Mail oder den Arbeitskalender aller, schaltet das es ebenfalls ein. Jede Person wählt dann unter **Deine Verbindungen**, was sonst noch mitgeht. Das erste Teilen eines neuen Teammitglieds wartet eine Stunde, damit es vorher noch etwas privat halten kann.

## Deine Verbindungen

**Deine Verbindungen** unter **Was geteilt wird** listet jede Verbindung mit einem Schalter. Arbeitsverbindungen mit der Domain deiner Fleet sind anfangs an. Verbindungen mit der Domain einer anderen Firma sind anfangs aus, dort steht „Andere Firma, nicht geteilt“. Private gehen nie mit. Schaltest du eine aus, wird zurückgenommen, was sie geteilt hat.

Der Kalender einer anderen Person, den du über deine eigene Anmeldung liest, erscheint unter eigenem Namen, als private Verbindung.

Innerhalb einer eingeschalteten Verbindung wird jeder Thread trotzdem einsortiert. Das eigene Slack deiner Firma gilt als nur unter Kolleginnen und Kollegen. Nur eine Slack-Connect-Unterhaltung mit einer anderen Firma kann Kundenarbeit sein. Private, sensible und automatische Threads sowie solche nur unter Kolleginnen und Kollegen bleiben draußen, außer du teilst einen selbst.

## Von der Fleet verlangt

Ein Admin kann unter **Von der Fleet verlangt** die **Arbeits-E-Mail** und den **Arbeitskalender** aller mit der eigenen Domain der Fleet verlangen, nachdem er bestätigt hat, dass die Firma ihre Leute informiert hat. Arbeitsmails gehören der Firma, wie in jedem CRM. Verlangte Verbindungen zeigen „Verlangt von“ deiner Fleet und lassen sich nicht ausschalten. Threads, die du privat hältst, bleiben privat.

## Was ans Team geht

- Kunden-Threads: Arbeits-E-Mails mit Personen außerhalb deiner Firma, mit Anhängen.
- Arbeitskontakte, Organisationen und Projekte, mit einem kurzen Verlauf. Im **Verlauf** einer Seite zeigt **Team** jedes Ereignis einmal, in deiner Sprache, wenn die Machine eines Teammitglieds es so geschrieben hat, mit allen, von denen es kommt: „über Sam, Kim und Lee“.
- Eine kleine Kopie des Logos einer Organisation und des Arbeitsfotos einer Person: aus einer Suche, Slack, LinkedIn, X, Salesflare oder Microsoft. Nie ein Bild aus Google-Kontakten, WhatsApp, Telegram oder Facebook und nie ein Bild, das du geändert oder entfernt hast.
- Auf einem Team-Board die Meetings, Zoom-Notizen, Intercom-Unterhaltungen und Chats eines Projekts. Sensible, etwa Deals, bleiben draußen, ebenso Chats nur unter Kolleginnen und Kollegen.
- Anzahlen und Daten für das [Team-Briefing](fleet.md#brief-requests) eines Teammitglieds.
- Antworten, wenn ein Teammitglied fragt, wer jemanden kennt, oder Kontext zu einem Meeting braucht. Siehe [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Erkenntnisse des Teams](fleet.md#team-learnings): wie das Team arbeitet, ohne Namen oder Kundendetails.

## Bleibt beim automatischen Teilen draußen

- Sensible Threads: Kauf oder Verkauf einer Firma, Investitionen, Verhandlungen über Deals, HR und Einstellungen, Recht, Gesundheit, Geld, Sicherheit. Nicht einmal, dass es sie gibt.
- Automatische Mails: Quittungen, Rechnungen, Warnungen, Newsletter und Lieferantenrechnungen.
- Threads nur unter Kolleginnen und Kollegen, private Mails und alles aus einem privaten Konto. Privates geht nie mit, auch nicht, wenn du auf Team tippst.
- Alles, was du mit **Privat halten** markiert hast, und Boards und Projekte, die auf Nur du stehen.
- Jemand, der für dich Privat ist, etwa deine Familie oder Freunde, und deren Mail. Ein Projekt, bei dem die Person dabei ist, geht trotzdem mit seinem Board mit, ohne sie.

Jeder Thread wird danach beurteilt, worum es geht, und das kann falsch sein. Prüfe, was mitgehen würde, und korrigiere es mit Privat halten. Teilst du einen Thread selbst, mit dem Team oder mit bestimmten Personen, überstimmt das eine sensible Einstufung. Prüfe also, wer ihn bekommt.

## Ein Board mit ausgewählten Personen teilen

Tippe im Menü **⋯** eines Boards auf **Board teilen…** und wähle Teammitglieder. Nur sie bekommen seine Projekte mit dem vollständigen Verlauf: E-Mails, Meetings und Zoom-Notizen, Intercom-Unterhaltungen, Chats, Aufgaben und Bewegungen. Auch sensible gehen mit, etwa Deals.

Private Threads und solche nur unter Kolleginnen und Kollegen bleiben draußen, ebenso deine Familie und Freunde, automatische Mails und Verbindungen, die du nicht ausgewählt hast.

- Ein Projekt, das später zum Board hinzukommt, geht auch mit. Eins, das vom Board genommen wird, wird zurückgenommen.
- Nimmst du jemanden heraus oder wählst niemanden, wird es von dessen Machine zurückgenommen.
- Um einen einzelnen Thread mit ausgewählten Personen zu teilen, tippe auf sein Label, dann auf **Teilen mit…**. Das kann auch sensible oder automatische Arbeitsmails einschließen, nie aber private Threads oder solche nur unter Kolleginnen und Kollegen.

## Unsicher? Es wartet

Wenn deine Machine unsicher ist, teilt sie nicht. Diese Threads warten unter **Diese teilen?**, gruppiert nach Art (etwa „Partner- und Listing-Austausch“), jeweils mit einem Vorschlag:

- **Mit Team teilen**: alle in der Fleet.
- **Teilen mit…**: nur die Teammitglieder, die du wählst, zum Beispiel ein Board-Mitglied für Gespräche mit Investoren.
- **Privat halten**: Es bleibt bei dir.

Ein Tippen entscheidet für eine ganze Gruppe. Öffne eine Gruppe, um den Haken bei Threads zu entfernen, die du einzeln entscheiden willst.

Gespräche über Kauf, Verkauf oder Investitionen in eine Firma und Board-Themen gelten als sensibel und warten deshalb nicht hier. Alltägliche Arbeit mit einer Partnerfirma ist Kundenarbeit.

## Vor dem ersten Teilen

Dein erstes Teilen geht eine Stunde, nachdem deine Machine dir Bescheid gibt, von selbst raus. Öffne in dieser Stunde **Fleet**, dann **Was geteilt wird**: Dort stehen die Kunden-Threads, die mitgehen würden, nach Organisation. Tippe bei beliebigen davon auf **Privat halten** oder auf **Jetzt teilen**, um sofort zu senden. Admins sehen, wer noch nicht geteilt hat.

## Was geteilt wird

**Fleet** › **Was geteilt wird** zeigt alles: Anzahlen pro Art, jeden geteilten Thread und warum er mitging, die wartenden unter **Diese teilen?** und was du privat hältst. Tippe auf einen Betreff, um ihn zu lesen. Auch **Einstellungen** und das Label an jedem Thread führen hierher.

Ein neuer Kunden-Thread wartet eine Stunde, bevor er mitgeht, damit Zeit bleibt, es dir anders zu überlegen.

## Nicht mehr teilen

Tippe bei einem Thread auf das Label **Team**, dann auf **Nicht mehr teilen**. Die Machine jedes Teammitglieds löscht den Thread, seine Anhänge und seine Zeilen im Verlauf, oder tut das, sobald sie wieder online ist. Vielleicht hat es jemand schon gelesen.

**Privat halten** bei einer Person, Organisation oder einem Projekt nimmt alles davon zurück.

Hältst du zwei Threads mit derselben Firma privat, fragt deine Machine einmal, ob sie diese Firma immer privat halten soll.

## Wer es sieht

Nur die Machines deiner Teammitglieder. Alles ist Ende-zu-Ende verschlüsselt. The Machine Network leitet es nur weiter und kann es nicht lesen.

## Beitritt und neue Geräte

Ein Admin lässt jede Person einmal herein. Die Anfrage steht für jeden Admin unter **Aufgaben**, und die erste Antwort gilt. Danach braucht das Teilen kein weiteres OK.

Bis dahin zeigen Graph und Fleet der neuen Person, auf welche Admins sie wartet. **Meine** und **Team** erscheinen wenige Sekunden nach dem OK, ohne Neuladen.

Eine neue Machine einer Person, die schon dabei ist, bekommt den Graph des Teams nach 24 Stunden. In der Zwischenzeit können Admins auf **Nicht von der Person** tippen, um sie draußen zu halten.

## Wenn jemand geht

Die Person bekommt ab diesem Moment nichts Neues mehr. Was sie geteilt hat, bleibt beim Team. Ein Admin kann jemanden auch **Herausnehmen** und später **Erneut teilen**.

## Für alle ausschalten

Ein Admin kann **Den Graph in dieser Fleet teilen** unter **Was geteilt wird** ausschalten. Dann geht nichts Neues mehr raus.

**Ausschalten** behält, was die Teammitglieder schon haben. **Ausschalten und geteilte Daten entfernen** lässt jede Machine es löschen. Wird das Teilen wieder eingeschaltet, sieht jede Person zuerst noch einmal alles durch.

## Deine eigene Arbeit nicht mehr teilen

Schalte deine Verbindungen unter **Deine Verbindungen** aus, außer die Fleet verlangt sie. Was sie geteilt haben, wird zurückgenommen.

Siehe auch [Fleets](fleet.md) und [Sicherheit und Datenschutz](security-and-privacy.md).
