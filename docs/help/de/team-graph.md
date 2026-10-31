---
title: Team-Graph
area: fleet
summary: Experimentell. Teile Kundenarbeit mit deiner Work Fleet, wie in einem CRM. Was mitgeht, was nie, und wie du etwas privat hältst.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
---
In einer Work Fleet kann deine Machine deine Kundenarbeit mit den Machines deiner Teammitglieder teilen, wie ein gemeinsames CRM. Das ist **Experimentell**: neu und noch in Bewegung, deshalb ist es anfangs aus.

## Einschalten

Ein Admin schaltet **Graph in dieser Fleet teilen** unter **Was geteilt wird** ein und bestätigt, dass die Firma diese Mails teilen darf und ihre Leute informiert hat. Alle sehen, ob es an ist. Eine Fleet, die schon vorher geteilt hat, bleibt an. Dann sieht jede Person durch, was mitgehen würde, und tippt auf **Jetzt starten**. Vorher geht nichts raus.

## Deine Verbindungen

**Deine Verbindungen** unter **Was geteilt wird** listet jede mit einem Schalter. Arbeitsverbindungen mit der eigenen Domain deiner Fleet starten an. Eine mit der Domain einer anderen Firma startet aus, auch wenn es ein Arbeitskonto ist: Dort steht „Andere Firma, nicht geteilt“. Du kannst sie einschalten. Private gehen nie mit. Schaltest du eine aus, wird zurückgenommen, was sie geteilt hat.

Der Kalender einer anderen Person, den du über deine eigene Anmeldung liest, erscheint unter eigenem Namen, als private Verbindung.

Innerhalb einer eingeschalteten Verbindung wird jeder Thread trotzdem einsortiert. Das eigene Slack deiner Firma gilt als nur unter Kolleginnen und Kollegen, auch Direktnachrichten: Nur eine Slack-Connect-Unterhaltung mit einer anderen Firma kann ein Kunden-Thread sein. Private Threads und solche nur unter Kolleginnen und Kollegen bleiben draußen. Sensible und automatische Mails bleiben beim automatischen Teilen draußen. Deine ausdrücklichen Entscheidungen zum Teilen können diese Einstufungen überstimmen.

## Von der Fleet verlangt

Ein Admin kann unter **Von der Fleet verlangt** die **Arbeits-E-Mail** und den **Arbeitskalender** aller mit der eigenen Domain der Fleet verlangen, nachdem er bestätigt hat, dass die Firma ihre Leute informiert hat. Arbeitsmails gehören der Firma, wie in jedem CRM. Diese zeigen dann „Verlangt von“ deiner Fleet und lassen sich nicht ausschalten. Threads, die du privat hältst, bleiben privat.

## Was ans Team geht

- Kunden-Threads: E-Mails mit Personen außerhalb deiner Firma über Arbeit, mit ihren Anhängen.
- Arbeitskontakte, Organisationen und Projekte, mit einem kurzen Verlauf.
- Auf einem Team-Board auch die Meetings, Zoom-Notizen, Intercom-Unterhaltungen und Chats eines Projekts, weil sie auf dem Board sind. Sensible, etwa Deals, bleiben draußen, ebenso Chats nur unter Kollegen.

## Bleibt beim automatischen Teilen draußen

- Sensible Threads: Kauf oder Verkauf einer Firma, Investitionen, Bewertungen, Verhandlungen über Deals, HR, Einstellungen und Recruiter, Recht, Gesundheit, Geld, Sicherheit. Nicht einmal, dass es sie gibt.
- Automatische Mails: Quittungen, Rechnungen, Warnungen, Newsletter und die eigenen Rechnungen deiner Firma mit ihren Lieferanten.
- Interne Threads (nur unter Kolleginnen und Kollegen), private Mails und alles aus einem privaten Konto. Privates geht nie mit, auch nicht, wenn du auf Team tippst.
- Alles, was du mit **Privat halten** markiert hast, und Boards und Projekte, die auf Nur du stehen.

Jeder Thread wird für sich beurteilt, danach, worum es geht. Die Einstufung kann falsch sein: Prüfe, was mitgehen würde, und korrigiere es mit Privat halten. Deine ausdrückliche Wahl von Team oder ein Teilen mit bestimmten Teammitgliedern kann eine sensible Einstufung überstimmen. Prüfe die Empfänger, bevor du teilst.

## Ein Board mit ausgewählten Personen teilen

Tippe im Menü **⋯** eines Boards auf **Board teilen…** und wähle Teammitglieder. Nur sie bekommen seine Projekte mit dem vollständigen Verlauf: E-Mail-Threads, Meetings und ihre Zoom-Notizen, Intercom-Unterhaltungen, Chats, Aufgaben und Bewegungen. Auch sensible gehen mit, etwa Deals.

Private Threads und solche nur unter Kolleginnen und Kollegen bleiben draußen, ebenso Personen aus deiner Familie oder deinen Freunden und automatische Mails, wenn nur das Board geteilt wird. Verbindungen, die du nicht ausgewählt hast, bleiben ebenfalls draußen.

- Ein Projekt, das später zum Board hinzukommt, geht auch mit. Eins, das vom Board genommen wird, wird zurückgenommen.
- Nimmst du jemanden heraus oder wählst niemanden, wird es von dessen Machine zurückgenommen.
- Auch ein einzelner Thread kann an ausgewählte Personen gehen: Tippe auf sein Label, dann **Teilen mit…**. Diese ausdrückliche Wahl kann sensible oder automatische Arbeitsmails einschließen. Private Threads und solche nur unter Kolleginnen und Kollegen lassen sich nicht teilen.

## Unsicher? Es wartet

Wenn deine Machine unsicher ist, teilt sie nicht. Diese Threads warten unter **Diese teilen?**, gruppiert nach dem, was sie sind (etwa „Partner- und Listing-Tausch“), jede Gruppe mit einer vorgeschlagenen Wahl:

- **Mit Team teilen** geht an alle in der Fleet.
- **Teilen mit…** geht nur an die Teammitglieder, die du wählst, zum Beispiel ein Mitglied des Boards für Gespräche mit Investoren. Der Rest des Teams bekommt es nicht.
- **Privat halten** behält es bei dir.

Ein Tippen entscheidet für eine ganze Gruppe. Öffne eine Gruppe, um ihre Threads zu sehen, und entferne den Haken bei denen, die du einzeln entscheiden willst.

Gespräche über Kauf, Verkauf oder Investitionen in eine Firma und Board-Themen gelten als sensibel und warten deshalb nicht hier. Listings, Integrationen und andere alltägliche Arbeit mit einer Partnerfirma sind Kundenarbeit.

## Vor dem ersten Teilen

Öffne **Fleet**, dann **Was geteilt wird**. Dort stehen die Kunden-Threads, die mitgehen würden, nach Organisation. Tippe bei beliebigen davon auf **Privat halten**, dann auf **Jetzt starten**.

Bis du startest, erinnert dich deine Machine alle paar Tage daran, während deiner Arbeitszeiten. Admins sehen, wer noch nicht gestartet hat.

## Was geteilt wird

**Fleet** › **Was geteilt wird** zeigt alles an einem Ort: Anzahlen pro Art, jeden geteilten Thread mit dem Grund, warum er mitging, die wartenden unter **Diese teilen?** und was du privat hältst. **Einstellungen** hat eine Abkürzung dorthin, ebenso das Label an jedem Thread. Tippe auf den Betreff eines Threads, um ihn zu lesen.

Ein neuer Kunden-Thread wartet eine Stunde, bevor er mitgeht, damit Zeit bleibt, es dir anders zu überlegen.

## Freigabe aufheben

Tippe bei einem Thread auf das Label **Team**, dann auf **Freigabe aufheben**. Deine Machine sagt es der Machine jedes Teammitglieds, und jede löscht den Thread, seine Anhänge und seine Zeilen im Verlauf. Eine Machine, die aus war, macht das, sobald sie wieder läuft. Vielleicht hat es jemand schon gelesen.

**Privat halten** bei einer Person, Organisation oder einem Projekt hebt auf dieselbe Weise die Freigabe für alles davon auf.

Hältst du zwei Threads mit derselben Firma privat, fragt deine Machine einmal: Threads dieser Firma immer privat halten?

## Wer es sieht

Nur die Machines deiner Teammitglieder. Alles ist Ende-zu-Ende verschlüsselt, versiegelt für die Machine jedes Teammitglieds. The Machine Network leitet es nur weiter und kann es nicht lesen.

## Beitritt und neue Geräte

Ein Admin lässt jede Person einmal in die Fleet. Danach braucht das Teilen mit ihr kein weiteres OK. Die Frage steht für jeden Admin unter **Vorschläge**, und die erste Antwort gilt für das ganze Team. Mitglieder bekommen sie nie.

Eine neue Machine einer Person, die schon dabei ist, bekommt den Graph des Teams nach 24 Stunden. Admins sehen sie in der Zwischenzeit und können auf **Nicht ihres** tippen, um sie draußen zu halten.

## Wenn jemand geht

Die Person bekommt ab diesem Moment nichts Neues mehr. Was sie geteilt hat, bleibt beim Team. Ein Admin kann jemanden auch **Herausnehmen** und später **Erneut teilen**.

## Für alle ausschalten

Ein Admin kann **Graph in dieser Fleet teilen** unter **Was geteilt wird** ausschalten. Alle sehen, ob es an ist. Ist es aus, geht nichts Neues raus.

**Ausschalten** behält, was schon auf den Machines der Teammitglieder ist. **Ausschalten und geteilte Daten entfernen** lässt jede Machine löschen, was sie bekommen hat. Wird das Teilen wieder eingeschaltet, sieht jede Person zuerst wieder durch.

## Deine eigene Arbeit nicht mehr teilen

Schalte deine Verbindungen unter **Deine Verbindungen** aus, außer die Fleet verlangt sie. Was sie geteilt haben, wird zurückgenommen.

Siehe auch [Fleets](fleet.md) und [Sicherheit und Datenschutz](security-and-privacy.md).
