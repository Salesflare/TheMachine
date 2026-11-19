---
title: Nachfassen
area: graph
summary: Lass automatisch nachfassen, wenn jemand nicht antwortet, für ein ganzes Board oder ein einzelnes Projekt. Standardmäßig fragt The Machine vorher nach.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 76bea8f586963be1
---
Wenn jemand auf einem Board nicht mehr antwortet, erstellt deine Machine einen Entwurf für eine Nachfassnachricht in deinem Stil und im selben Gespräch. Die Funktion ist ausgeschaltet, bis du sie aktivierst. Wenn ein Skill zu dem Board passt, orientieren sich die Entwürfe daran, auch bei der Reihenfolge der Inhalte in der E-Mail.

## Aktivieren

Tippe auf einem Board auf **⋯** und dann auf **Nachfassen…**. Aktiviere **Nachfassen, wenn keine Antwort kommt**. Das gilt für alle Projekte auf dem Board. Du kannst auch unter dem Namen des Boards auf **Nachfassen aus** tippen oder in einer Phase mit Projekten, auf die seit mindestens 10 Tagen keine Antwort kam, auf **Bei ihnen nachfassen**.

Für ein einzelnes Projekt findest du **Nachfassen…** im Menü **⋯** auf dem Board oder auf der Projektseite. Unter **Für dieses Projekt** kannst du **An**, **Aus** oder die Einstellung des Boards auswählen. Die Einstellung eines Projekts hat Vorrang vor der des Boards.

## Einstellungen

- Standardmäßig wird 3 bis 7 Tage auf eine Antwort gewartet. Die Nachfassnachricht wird nach der kürzesten Wartezeit als Entwurf erstellt und spätestens nach der längsten Wartezeit gesendet, auch wenn du dein Nutzungslimit fast erreicht hast.
- **Nur an Arbeitstagen**: An deinen freien Tagen werden keine Entwürfe erstellt oder gesendet. Deine freien Tage legst du unter **Einstellungen** > **Benachrichtigungen** > **Arbeitszeiten** fest. Was an einem freien Tag fällig wird, wartet bis zum nächsten Arbeitsmorgen. Für Arbeit ist die Option aktiviert, für Persönlich deaktiviert.
- Standardmäßig wird 1 bis 3 Mal nachgefasst. Die minimale Anzahl wird immer gesendet, für die restlichen Nachrichten werden Entwürfe erstellt. Wenn The Machine meint, dass du besser aufhören solltest, steht im Entwurf der Grund dafür ("The Machine würde hier aufhören: 9 unbeantwortete E-Mails seit August"). Der Entwurf ist dann nicht angehakt: Du kannst ihn senden, überspringen oder **Nachfassen hier beenden** auswählen. Die Höchstzahl wird nie überschritten.
- **Phasen**: Standardmäßig sind **Alle offenen Phasen** ausgewählt. Die letzte Phase des Boards sowie „Ins Stocken geraten oder abgelehnt“ sind ausgenommen. Mit **Anpassen** kannst du Phasen ein- oder ausschalten und für eine Phase eine eigene Wartezeit festlegen.
- **Kanäle**: Hier siehst du die verbundenen Kanäle, über die Nachrichten gesendet werden können. Eine Nachfassnachricht wird über denselben Kanal wie die letzte Nachricht gesendet. Mit **Kanal wechseln, wenn keine Antwort kommt** wird der nächste erlaubte Kanal ausprobiert.
- **Nach dem letzten nach „Ins Stocken geraten oder abgelehnt“ verschieben**: Ist aktiviert, wenn das Board diese Phase hat.

## Vor dem Senden fragen oder automatisch senden

**Vor dem Senden fragen** ist die Standardeinstellung: Entwürfe warten in deinen Aufgaben. **Ohne Nachfrage senden** gilt als dauerhafte Zustimmung für das Board oder Projekt. Bei ungewöhnlichen Problemen oder Fehlern wartet die Nachricht trotzdem auf dich. Bei der Sorgfaltsstufe „Sorgfältig“ wird immer nachgefragt. Eine Nachfassnachricht wird nie zweimal gesendet. Nachfassnachrichten lösen keine Push- oder E-Mail-Benachrichtigungen aus. Die Entwürfe warten in deiner Liste und in der morgendlichen Zusammenfassung.

Kurz vor dem Senden wird der Verlauf noch einmal geprüft. Wenn seit dem Entwurf jemand geschrieben hat, wird die Nachricht nicht gesendet: „Nicht gesendet: neue Nachricht im Verlauf“. Die Aufgabe zeigt die Nachricht, wer sie geschrieben hat und wann, sowie **Lesen** und **Für diese Nachricht neu machen**. Damit wird ein neuer Entwurf angefordert, der die Nachricht berücksichtigt.

## Nachfassnachrichten prüfen

Die Nachfassnachrichten eines Boards erscheinen zusammen in einer Aufgabe, nicht als einzelne Aufgaben pro E-Mail. Während die Entwürfe erstellt werden, steht dort „3 Nachfassnachrichten werden geschrieben …“, danach „8 Nachfassnachrichten für Alpha testers bereit“.

Mit **Prüfen** siehst du die Nachrichten untereinander und vollständig, sodass du sie alle durchscrollen kannst. Für die aktuelle Nachricht werden **Senden**, **Bearbeiten** und **Überspringen** angezeigt. Mit j und k oder den Pfeiltasten kannst du navigieren. Enter sendet, e bearbeitet, s überspringt oder macht das Überspringen rückgängig, x markiert oder demarkiert und c ändert den Text. **Alle ausgewählten senden** sendet die weiterhin angehakten Nachrichten.

Zu jeder Nachfassnachricht gehört ein Entwurf. Wenn sich keine schreiben lässt, steht dort, was dafür fehlt („Kein Entwurf. Zuerst benötigt: der Empfänger.“), und sie ist nicht angehakt. Mit **Schreib es** kannst du trotzdem einen Entwurf anfordern. Wenn mehr als ein möglicher Empfänger für einen Entwurf infrage kommt, steht dort „Empfänger auswählen: bei Senden auswählen“. Wenn du auf **Senden** tippst, wirst du aufgefordert, einen Empfänger auszuwählen.

Mit **Überspringen** wird ein Entwurf abgewählt und ans Ende verschoben. Er ist als „Übersprungen“ markiert und hat eine Option **Rückgängig**. Wenn du die Prüfung schließt, wird er endgültig übersprungen. Du kannst einen übersprungenen Entwurf mit **Zurückholen** in den Nachfassnachrichten des Projekts oder in der Aufgabe unter Erledigt wiederherstellen, solange keine neuere Nachfassnachricht hinzugekommen ist. Für ein einzelnes Projekt ist die Nachfassnachricht eine normale Aufgabe.

Mit **Änderungen anfragen…** werden alle ausgewählten Entwürfe oder nur der aktuelle nach deinen Vorgaben neu geschrieben. Dabei wird nichts gesendet. Mit **Änderung rückgängig machen** kannst du den alten Text wiederherstellen. Solange das Eingabefeld geöffnet ist oder ein Entwurf neu geschrieben wird, kann nichts gesendet werden. Ein geänderter Entwurf wird noch einmal angezeigt, bevor er gesendet werden kann.

Wenn mehrere Nachrichten nacheinander gesendet werden, auch mit „Ohne Nachfrage senden“, verschickt jedes Postfach alle 30 bis 45 Sekunden eine Nachricht. Die Aufgabe zeigt den Fortschritt an: „3 von 8 werden gesendet …“. Mit **Senden stoppen** werden die übrigen Nachrichten angehalten. Eine Nachricht, die bereits unterwegs ist, wird noch gesendet. Die anderen werden als Entwürfe wieder in die Prüfung aufgenommen und können später gesendet werden („Angehalten. 1 gesendet, 11 als Entwürfe behalten.“).

## E-Mails, die vor deiner Machine gesendet wurden

Auch E-Mails, die du in einer anderen App gesendet hast, bevor deine Machine das Postfach gelesen hat, werden mitgezählt. The Machine liest den Gesprächsverlauf selbst. Wenn das nicht möglich ist, berücksichtigt sie die früheren E-Mails, die in deiner letzten Nachricht zitiert wurden. Drei E-Mails ohne Antwort zählen also als drei, und die Zeit ohne Antwort wird ab der ersten E-Mail berechnet. Wenn du die Höchstzahl bereits erreicht hast, wird kein weiterer Entwurf erstellt.

## Wann das Nachfassen endet

Das Nachfassen endet, wenn die Person antwortet, das Projekt gewonnen, verloren oder archiviert wird, in eine geschlossene Phase verschoben wird oder du eine Nachricht zurückstellst oder überspringst. Vor dem Erstellen eines Entwurfs prüft deine Machine den Gesprächsverlauf auf neue Nachrichten, damit niemand mehrmals gefragt wird, wenn die Person bereits anderswo geantwortet hat.

Eine Nachfassnachricht wird auch geschlossen, wenn jemand im selben Gespräch bereits wieder geschrieben hat. Nachfassnachrichten eines anderen Projekts zählen nicht. Wenn The Machine aus einem anderen Grund meint, dass eine Nachricht nicht nötig ist, bleibt die Aufgabe offen und der Grund wird angezeigt. Du entscheidest.

Mit **Pausieren** unter **Nachfassen…** kannst du ein Board oder Projekt pausieren, ohne das Nachfassen auszuschalten. Es werden keine Entwürfe erstellt oder gesendet, keine Runde endet und offene Nachfassaufgaben bleiben offen. Wähle einen Tag aus, an dem das Nachfassen fortgesetzt werden soll, oder tippe auf **Fortsetzen**, wenn du bereit bist. Die Wartezeit wird dort fortgesetzt, wo sie unterbrochen wurde. Fällige Nachrichten werden nacheinander bearbeitet. In der Zwischenzeit wird **Pausiert** angezeigt.

Wenn nach der letzten Nachfassnachricht keine Antwort kommt, zeigt das Projekt „Keine Antwort nach 3 Nachfassnachrichten“ an und wird in „Ins Stocken geraten oder abgelehnt“ verschoben, wenn diese Option aktiviert ist. Wenn das Nachfassen beendet wird, bevor eine Nachricht gesendet wurde, steht dort „Nachfassen beendet“ und das Projekt bleibt in seiner Phase.

Wenn eine E-Mail zurückkommt und die Person eine andere Adresse hat, wird die Nachfassnachricht stattdessen dorthin gesendet („Zurückgekommen, jetzt an <address>“). Wenn eine Adresse zurückkommt, bevor ein Entwurf gesendet wird, wird er zurückgehalten: „Nicht gesendet: <address> ist zurückgekommen“. Er wird der anderen Adresse zugeordnet und wartet auf deine Freigabe zum Senden.

Wenn es keine andere Adresse gibt, wird auf LinkedIn oder WhatsApp gewechselt, sofern das erlaubt ist und du dort mit der Person sprichst. Andernfalls endet das Nachfassen mit „E-Mail zurückgekommen“. Wenn das Projekt wichtig ist, erhältst du eine Aufgabe, eine neue Adresse zu finden.

## Wo du die Nachfassnachrichten siehst

Im Board-Header steht „Nachfassen an, nächste Nachricht Do.“ Bei einem Projekt auf dem Board wird die nächste Nachfassnachricht oder der Status „Bereit“ angezeigt. Auf der Projektseite sind alle gesendeten Nachrichten aufgeführt, auch die automatisch gesendeten.

Nachfassnachrichten warten, während deine Machine beschäftigt ist oder sich dem Nutzungslimit nähert, und werden später nachgeholt. Auf einem geteilten Board fasst nur die Machine der Person nach, der das Projekt gehört.
