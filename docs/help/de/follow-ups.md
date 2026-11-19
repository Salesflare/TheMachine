---
title: Nachfassen
area: graph
summary: Automatisches Nachfassen, wenn jemand nicht antwortet, für ein ganzes Board oder ein einzelnes Projekt. Vor dem Senden wirst du gefragt, sofern du nichts anderes festlegst.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 0e7bdfb2c9b2deb5
---
Wenn jemand auf einem Board nicht mehr antwortet, erstellt deine Machine einen Entwurf für die Nachfassnachricht, in deinem Stil und im selben Gespräch. Die Funktion ist aus, bis du sie einschaltest. Wenn ein Skill von dir zum Board passt, richten sich die Entwürfe danach, auch bei der Reihenfolge der Inhalte in der E-Mail.

## Einschalten

Tippe auf einem Board auf **⋯** und dann auf **Nachfassen…**. Aktiviere anschließend **Nachfassen, wenn keine Antwort kommt**. Das gilt für alle Projekte auf diesem Board. Du kannst auch unter dem Boardnamen auf **Nachfassen aus** tippen oder in einer Phase mit Projekten, auf die seit mindestens 10 Tagen niemand geantwortet hat, auf **Bei ihnen nachfassen**.

Für ein einzelnes Projekt tippst du auf dem Board oder auf der Projektseite in **⋯** auf **Nachfassen…**. Mit **Für dieses Projekt** wählst du **An**, **Aus** oder die Einstellung des Boards. Die Einstellung eines Projekts hat Vorrang vor der des Boards.

## Einstellungen

- Standardmäßig wird nach 3 bis 7 Tagen ohne Antwort nachgefasst. Nach der kürzesten Wartezeit wird ein Entwurf erstellt und spätestens nach der längsten Wartezeit verschickt, auch wenn dein Nutzungslimit knapp ist.
- **Nur an Arbeitstagen**: An deinen freien Tagen wird nichts erstellt oder gesendet. Deine Arbeitstage findest du unter **Einstellungen** > **Benachrichtigungen** > **Arbeitszeiten**. Was an einem freien Tag fällig wäre, wartet bis zum nächsten Arbeitsmorgen. Bei „Arbeit“ ist die Option an, bei „Persönlich“ aus.
- Standardmäßig wird 1 bis 3 Mal nachgefasst. Die Mindestanzahl wird immer gesendet, für alles Weitere werden Entwürfe erstellt. Wenn die Machine meint, dass du besser aufhören solltest, steht der Grund im Entwurf („The Machine würde hier aufhören: 9 unbeantwortete E-Mails seit August“). Der Entwurf ist nicht angekreuzt. Du kannst ihn senden, überspringen oder **Nachfassen hier beenden** auswählen. Die Höchstzahl wird nie überschritten.
- **Phasen**: Standardmäßig sind **Alle offenen Phasen** ausgewählt. Die letzte Phase des Boards und „Ins Stocken geraten oder abgelehnt“ sind also ausgenommen. Mit **Anpassen** kannst du Phasen ein- oder ausschalten und für jede Phase eine eigene Wartezeit festlegen.
- **Kanäle**: Hier siehst du die verbundenen Kanäle, über die Nachrichten gesendet werden können. Eine Nachfassnachricht wird über denselben Kanal wie die letzte Nachricht gesendet. **Kanal wechseln, wenn keine Antwort kommt** versucht den nächsten zugelassenen Kanal.
- **Nach dem letzten nach „Ins Stocken geraten oder abgelehnt“ verschieben**: Ist aktiviert, wenn das Board diese Phase hat.

## Erst fragen oder automatisch senden

**Vor dem Senden fragen** ist die Standardeinstellung: Entwürfe warten in deinen Aufgaben. **Ohne Nachfrage senden** bedeutet, dass du für dieses Board oder Projekt dauerhaft zustimmst. Ungewöhnliche Fälle und Fehler warten trotzdem auf dich. Bei der Stufe „Sorgfältig“ wird immer gefragt. Eine Nachfassnachricht wird nie zweimal gesendet. Nachfassnachrichten lösen keine Benachrichtigungen per Push oder E-Mail aus. Die Entwürfe warten in deiner Liste und in der morgendlichen Zusammenfassung.

Unmittelbar vor dem Senden wird der Gesprächsverlauf noch einmal geprüft. Wenn seit dem Entwurf jemand geschrieben hat, wird er nicht gesendet: „Nicht gesendet: neue Nachricht im Gespräch“. Die Aufgabe zeigt die Nachricht, wer sie geschrieben hat und wann. Dort findest du **Lesen** und **Für diese Nachricht neu machen**. Damit wird ein neuer Entwurf angefordert, der die Nachricht berücksichtigt.

## Entwürfe prüfen

Die Nachfassnachrichten eines Boards erscheinen gesammelt in einer Aufgabe, nicht als einzelne Aufgabe pro E-Mail. Während die Entwürfe erstellt werden, steht dort „3 Nachfassnachrichten werden geschrieben …“. Danach steht dort zum Beispiel „8 Nachfassnachrichten für Alpha testers bereit“.

Unter **Prüfen** werden die Entwürfe untereinander und vollständig angezeigt, sodass du sie alle mit einem einzigen Scrollen lesen kannst. Beim aktuellen Entwurf werden **Senden**, **Bearbeiten** und **Überspringen** angezeigt. Mit j und k oder den Pfeiltasten wechselst du zwischen den Entwürfen. Mit der Eingabetaste sendest du, mit e bearbeitest du, mit s überspringst du. Drücke s erneut, um das rückgängig zu machen. Mit x markierst du Entwürfe oder hebst die Markierung auf, mit c forderst du Änderungen an. **Alle markierten senden** sendet die Entwürfe, die noch markiert sind.

Zu jeder Nachfassnachricht gehört ein Entwurf. Wenn sich einer nicht erstellen lässt, steht dort, was zuerst benötigt wird („Kein Entwurf. Zuerst benötigt: Empfänger“). Er ist nicht markiert. Mit **Schreib es** forderst du trotzdem einen Entwurf an. Wenn für einen Entwurf mehrere Empfänger infrage kommen, steht dort „Empfänger beim Senden auswählen“. Wenn du auf **Senden** tippst, kannst du den Empfänger auswählen.

Mit **Überspringen** hebst du die Markierung eines Entwurfs auf und verschiebst ihn ans Ende. Er wird als „Übersprungen“ markiert und mit **Rückgängig** versehen. Sobald du die Prüfung schließt, ist er endgültig übersprungen. Einen übersprungenen Entwurf kannst du mit **Zurückholen** in den Nachfassnachrichten des Projekts oder in der Aufgabe unter Erledigt wiederherstellen, sofern kein neueres Follow-up hinzugekommen ist. Das Follow-up für ein einzelnes Projekt ist eine normale Aufgabe.

Mit **Änderungen anfragen…** werden alle markierten Entwürfe oder nur der aktuelle so umgeschrieben, wie du es vorgibst. Es wird nichts gesendet. Mit **Änderung rückgängig machen** stellst du den alten Text wieder her. Solange das Eingabefeld geöffnet ist oder ein Entwurf umgeschrieben wird, kann nichts gesendet werden. Ein geänderter Entwurf wird noch einmal angezeigt, bevor er gesendet werden kann.

Wenn mehrere Nachrichten nacheinander gesendet werden, auch mit **Ohne Nachfrage senden**, verschickt jedes Postfach alle 30 bis 45 Sekunden eine Nachricht. In der Aufgabe siehst du den Fortschritt: „3 von 8 werden gesendet …“. Mit **Senden stoppen** hältst du die übrigen an. Eine Nachricht, die bereits unterwegs ist, wird trotzdem gesendet. Die anderen erscheinen wieder als Entwürfe in der Prüfung und können später gesendet werden („Gestoppt. 1 gesendet, 11 als Entwürfe behalten.“).

## E-Mails, die vor deiner Machine gesendet wurden

Auch E-Mails, die du in einer anderen App gesendet hast, bevor deine Machine das Postfach gelesen hat, werden gezählt. Deine Machine liest den Gesprächsverlauf selbst. Wenn das nicht möglich ist, liest sie die früheren E-Mails, die in deiner letzten zitiert wurden. Drei E-Mails ohne Antwort zählen also als drei. Auch „Keine Antwort seit“ zählt ab der ersten E-Mail. Wenn du die Höchstzahl bereits erreicht hast, wird kein weiterer Entwurf erstellt.

## Wann das Nachfassen endet

Das Nachfassen endet, wenn die Person antwortet, das Projekt gewonnen, verloren oder archiviert wird oder in eine geschlossene Phase verschoben wird. Es endet auch, wenn du eine Aufgabe zurückstellst oder überspringst. Bevor ein Entwurf erstellt wird, prüft deine Machine den Gesprächsverlauf auf neue Nachrichten, damit sie niemanden nervt, der schon woanders geantwortet hat.

Mit **Pausieren** unter **Nachfassen…** hältst du das Nachfassen für ein Board oder Projekt an, ohne es auszuschalten. Es werden keine Entwürfe erstellt oder gesendet, keine Runde endet und offene Nachfassaufgaben bleiben offen. Wähle einen Tag für die Fortsetzung oder tippe auf **Fortsetzen**, wenn du so weit bist. Die Wartezeit läuft dort weiter, wo sie unterbrochen wurde. Fällige Nachrichten werden nacheinander bearbeitet. Bis dahin wird **Pausiert** angezeigt.

Wenn nach dem letzten Follow-up keine Antwort kommt, wird beim Projekt „Keine Antwort nach 3 Nachfassnachrichten“ angezeigt. Ist die entsprechende Option aktiviert, wird das Projekt nach „Ins Stocken geraten oder abgelehnt“ verschoben. Wurde das Nachfassen beendet, bevor etwas gesendet wurde, steht dort „Nachfassen beendet“ und das Projekt bleibt in seiner Phase.

Wenn die E-Mail-Adresse der Person einen Zustellfehler verursacht und eine andere Adresse vorhanden ist, wird das Follow-up stattdessen dorthin gesendet („Zustellung fehlgeschlagen, jetzt an <address>“). Wenn die Adresse eines Entwurfs vor dem Senden einen Zustellfehler verursacht, wird er zurückgehalten: „Nicht gesendet: <address> hat einen Zustellfehler verursacht“. Er wird der anderen Adresse zugeordnet und wartet dort darauf, dass du auf **Senden** tippst.

Wenn keine andere Adresse vorhanden ist, wird das Follow-up zu LinkedIn oder WhatsApp verschoben, sofern das erlaubt ist und du dort mit der Person kommunizierst. Andernfalls endet es mit „E-Mail nicht zugestellt“. Wenn das Projekt wichtig ist, erhältst du eine Aufgabe, eine neue Adresse zu finden.

## Wo du es siehst

Im Boardkopf steht „Nachfassen an, nächstes Follow-up: Do.“ Bei einem Projekt auf dem Board wird das nächste Follow-up angezeigt oder dass eines bereit ist. Auf der Projektseite siehst du alle gesendeten Nachrichten, auch die automatisch gesendeten.

Nachfassnachrichten warten, wenn deine Machine beschäftigt ist oder sich deinem Nutzungslimit nähert, und werden später nachgeholt. Auf einem geteilten Board fasst nur die Machine der Person nach, der das Projekt gehört.
