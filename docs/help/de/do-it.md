---
title: Ausführen und was gesendet wird
area: cards
summary: Mit Ausführen wird die Arbeit vorbereitet. Gesendet, bezahlt oder geändert wird erst, wenn du den jeweiligen Schritt bestätigst.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: f6078d1de97851ae
---
## Was Ausführen macht

**Ausführen** fordert deine Machine auf, die Aufgabe vorzubereiten: eine Antwort entwerfen, etwas nachschlagen oder ein Formular ausfüllen. Sie verwendet dafür deine eigenen Konten und ihren eigenen Browser, so wie du selbst.

Während sie im Browser arbeitet, zeigen die Aufgabe und der zugehörige Chat diese Seite live, auch zwischen den einzelnen Schritten, bis sie dort fertig ist. Klicke auf das Bild, um den Browser zu öffnen. In der Aufgabe wird er größer angezeigt, zusammen mit **Stoppen**: Ein Klick beendet diesen Durchlauf sofort.

Vor einer Nachfassnachricht oder einer Übergabe prüft sie, ob neuere Antworten eingegangen sind, auch von einem Teammitglied. Wenn die Aufgabe schon erledigt ist, sagt sie das. Wenn sie ein Dokument oder eine Seite geändert hat, verlinkt die Aufgabe darauf.

Wenn eine schwierige Aufgabe auf einer Website oder in einem Workflow klappt, speichert deine Machine die Schritte als Skill, ohne die persönlichen Angaben anderer. Spätere Aufgaben auf dieser Website erhalten sie als Anleitung, aber niemals als Erlaubnis: Zum Senden oder Bezahlen brauchst du weiterhin deine Zustimmung. Du findest sie unter **Einstellungen > Skills** mit der Kennzeichnung **Aus einer Aufgabe gelernt**.

Wenn die Schritte eines solchen Skills bei drei Aufgaben hintereinander nicht funktionieren, deaktiviert deine Machine ihn. Das bleibt so, bis eine spätere Aufgabe zeigt, was jetzt funktioniert, oder du ihn wieder aktivierst.

## Nichts wird ohne dein Ja gesendet

- Eine Antwort wird als Entwurf bereitgestellt. Mit **Prüfen und senden** öffnest du ihn und kannst ihn bearbeiten. Er wird erst gesendet, wenn du auf **Jetzt senden** klickst.
- Bei zwei oder mehr E-Mails in einer Aufgabe kannst du sie alle über eine Schaltfläche im Chat der Aufgabe prüfen. Jede E-Mail wird nacheinander angezeigt. Mit **Weiter** kommst du zur nächsten. Im letzten Schritt werden sie alle gesendet. Jede E-Mail wird erst dann als gesendet angezeigt, wenn sie tatsächlich rausgegangen ist.
- Eine E-Mail wird so angezeigt, wie sie aussehen wird, einschließlich Fettschrift, Listen und Links. Eine Slack- oder Chat-Nachricht ist reiner Text.
- Mit **Änderungen anfragen** kannst du im selben Fenster sagen, was geändert werden soll. Deine Machine erstellt den Entwurf dann neu.
- Eine Antwort bezieht sich auf die neueste E-Mail im Thread. Über die Quelle der Aufgabe öffnest du diese E-Mail.
- Bei einem Schritt, der etwas verbindlich macht, etwa beim Absenden, Bezahlen oder Buchen, wartet deine Machine auf deine Bestätigung oder darauf, dass du im Chat darum bittest. Wenn du einen Schritt bestätigst, bleiben die anderen weiterhin offen. Die Aufgabe wird erst geschlossen, wenn alle Schritte erledigt sind.
- Die Aufgabe und ihr Chat zeigen dir vor dem Antippen, was bei einem solchen Schritt gesendet wird. Bei einer Kalendereinladung siehst du den Titel, die Uhrzeit, die Gäste und ob ein Besprechungslink hinzugefügt wird.
- Verbundene Kalender werden bei der Suche nach einem Termin berücksichtigt: Deine Machine prüft deine Besprechungen für die jeweiligen Tage, bevor sie dir Termine vorschlägt.
- Ein Entwurf im Chat einer Aufgabe wird nie in derselben Nachricht gesendet, in der er erstellt wurde.
- Bis du zustimmst, wartet die Aufgabe unter **Für dich** als **Vorbereitet**. In der Liste steht einmal, dass nichts gesendet wird, bis du zustimmst. **Vorbereitet** bedeutet, dass ein Entwurf oder Ergebnis zur Freigabe bereit ist. Wenn die Arbeit ohne Entwurf oder Ergebnis endet, weil deine Machine etwas von dir braucht, etwa eine Entscheidung, eine fehlende Angabe, eine Anmeldung oder eine Auswahl, wird stattdessen **Braucht dich** angezeigt, zusammen mit einem Hinweis darauf, was fehlt. Das gilt auch, wenn sie nur geantwortet oder etwas erklärt hat („Beantwortet. Noch nichts erledigt.“). In diesem Fall steht **Ausführen** an erster Stelle. Dasselbe gilt für die Benachrichtigung und die morgendliche Zusammenfassung. Ein Entwurf wird erst dann als gesendet angezeigt, wenn er tatsächlich rausgegangen ist.
- Bei einem langen Entwurf werden die ersten drei Zeilen angezeigt. Mit **Mehr anzeigen** oder durch Antippen des Textes öffnest du den Rest. Unter **Prüfen und senden** wird immer der gesamte Entwurf angezeigt.

Je nach Quelle kann deine Machine eine E-Mail, eine Slack-Direktnachricht oder eine Nachricht über WhatsApp, Telegram, LinkedIn oder X senden. Im Artikel zu jeder Verbindung steht, was sie senden kann.

## Eine E-Mail bearbeiten

- Nutze die Schaltflächen über dem Text oder `Ctrl B` für Fettschrift, `Ctrl I` für Kursivschrift und `Ctrl K` für einen Link (`⌘` auf einem Mac). Außerdem gibt es Schaltflächen für Aufzählungen und nummerierte Listen.
- Ein Link braucht eine Adresse, die mit https:// beginnt. Eingefügter Text wird ohne Farben und Bilder übernommen.
- Formatierungen, die eine E-Mail nicht unterstützt, werden zuerst entfernt. Die Nachricht zeigt dir dann, wie sie aussehen wird. Klicke noch einmal auf **Jetzt senden**, um sie zu senden.
- Die E-Mail wird genau so gesendet, wie sie angezeigt wird. Dazu wird eine Nur-Text-Version für Mail-Apps erstellt, die keine Formatierungen anzeigen.

## Wenn es nicht klappt

- „Das kann von hier aus nicht gesendet werden.“ bedeutet, dass du den Entwurf mit **Entwurf kopieren** kopierst und selbst sendest.
- Bei **Braucht dich** und einer Aufgabe, bei der nichts gesendet, geöffnet oder gelesen werden muss, wird zuerst **Antworten** angezeigt. Sag, was gebraucht wird, und deine Machine macht weiter. Wenn du einen Schritt selbst erledigen musst, etwa eine Zahlung bei deiner Bank, wird zuerst **Als erledigt markieren** angezeigt.
- **Braucht deine Hilfe** bedeutet, dass eine Frage offen ist: Tippe auf **Antworten**. **Hängt fest** bedeutet, dass die Aufgabe ohne offene Frage abgebrochen wurde. In der Aufgabe steht warum.
- Hast du mehr als eine Frage gestellt? Jede Frage hat eigene Auswahlmöglichkeiten oder ein kurzes Eingabefeld, das manchmal bereits mit deiner letzten Antwort ausgefüllt ist. Mit **Antworten** sendest du alle Antworten auf einmal.
- Bittet dich jemand um Informationen oder Dateien? Deine Machine entwirft eine Antwort mit den gefundenen Informationen und fragt dich nur nach dem Rest.
- Fehlt etwas, das nur du hast? Deine Machine fragt danach und entwirft nur den Teil, der auch ohne diese Angabe gesendet werden kann, etwa eine Antwort, die einen Termin bestätigt. Sie entwirft keine Antwort, die nur sagt, dass noch etwas kommt.
- Mit **Erneut versuchen** wird die Aufgabe noch einmal ausgeführt. Mit **Änderungen anfragen** kannst du um etwas anderes bitten. Bei einer festgefahrenen Aufgabe wird **Erneut versuchen** zuerst angezeigt. Unter **Details** siehst du, was deine Machine versucht hat.
- Ist die Aufgabe fehlgeschlagen, weil der Durchlauf selbst nicht funktioniert hat? Nachdem deine Machine aktualisiert wurde, versucht sie die Aufgabe automatisch noch einmal.
- Einen fehlgeschlagenen Durchlauf versucht deine Machine höchstens zweimal automatisch erneut. Danach wartet sie auf etwas Neues, zum Beispiel eine neue Nachricht, eine Nachricht von dir im Chat oder auf **Erneut versuchen**.
- Während der Vorbereitung steht in der Aufgabe in einer kurzen Zeile, was deine Machine gerade macht, etwa „Liest die E-Mail“, „Liest das PDF“ oder „Schreibt den Entwurf“. Die einzelnen Schritte stehen im Chat der Aufgabe.
- Eine Aufgabe mit der Kennzeichnung **Wird vorbereitet…** beginnt innerhalb weniger Sekunden. Wenn sie warten muss, steht dort warum und ungefähr wie lange, etwa „Beginnt nach der aktuellen Aufgabe“.
- Eine Aufgabe, die deine Machine vorbereitet, bevor du sie darum bittest, kann warten, während deine Machine Nutzung spart. **Ausführen** wird trotzdem angezeigt. Tippe darauf, um die Aufgabe sofort und vor den anderen zu starten. Nichts wird ohne dein Ja gesendet. Wenn das Nutzungslimit deines KI-Tarifs erreicht ist, wird das bei Ausführen angezeigt. Die Aufgabe beginnt, sobald das Limit zurückgesetzt wurde.
- Möchte eine Website, dass du dich anmeldest? Tippe auf **Anmelden** oder auf **Browser öffnen** und melde dich dort an. Deine Machine macht dann automatisch weiter. Falls nicht, tippe auf **Weiter**.
- Ein Code, der an dein Handy gesendet wird, oder eine fehlende Berechtigung hält die Aufgabe auf. In der Aufgabe steht, was gebraucht wird. Tippe dann auf **Weiter** oder **Erneut versuchen**. Wenn eine Quelle nicht verbunden ist, zum Beispiel Slack, wird in der Aufgabe **Slack verbinden** angezeigt. Sobald Slack verbunden ist, macht deine Machine automatisch weiter.
