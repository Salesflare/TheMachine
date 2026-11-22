---
title: WhatsApp
area: connections
summary: Deine WhatsApp-Chats, gelesen wie auf einem verknüpften Gerät. Antworten erst nach deiner Freigabe.
covers: connector:whatsapp
code: onboarding.py, whatsapp_setup.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 130c64388a71b7d1
---
## Was gelesen wird

Deine WhatsApp-Chats, so wie auf einem mit dem WhatsApp deines Handys verknüpften Gerät, zum Beispiel auf einem Computer. Wenn du WhatsApp verbindest, sendet WhatsApp auch ältere Chats, oft mehrere Jahre zurück. Deine Machine behält alles, und nur Nachrichten aus den letzten 7 Tagen werden zu Aufgaben.

Ein Foto, eine Sprachnachricht oder eine Datei ohne Bildunterschrift wird als das angezeigt, was es ist, zum Beispiel als „Foto“ mit dem passenden Symbol. WhatsApps eigene Hinweise, etwa zum Verschlüsselungsstatus oder wenn jemand einer Gruppe beitritt, enthalten keinen Text und werden ausgelassen.

## Fotos lesen

Die Funktion ist deaktiviert, bis du sie einschaltest. Öffne unter **Verbindungen** WhatsApp und dann **Details**. Aktiviere **Fotos lesen**, damit The Machine Fotos aus deinen Arbeits-Chats liest: einen Beleg, einen Screenshot, ein Foto von einem Brief oder ein Formular. Mit **Auch in privaten Chats** werden auch Fotos aus deinen privaten Chats gelesen. Ob ein Chat beruflich oder privat ist, richtet sich danach, wie er geteilt wird. Ein Chat mit deiner Familie bleibt also privat.

The Machine lädt jedes Foto einmal herunter und speichert es auf deiner Machine wie einen E-Mail-Anhang: verschlüsselt, wenn der Nachrichtenschutz an ist, und gelöscht, sobald die zugehörige Nachricht gelöscht wird. Das eigene Modell von The Machine liest, was auf dem Foto zu sehen ist, und den darin enthaltenen Text. Beides gilt als Teil der Nachricht, niemals als Anweisung. Unterstützt werden JPEG, PNG und WebP bis zu 5 MB. Einmalcodes auf Fotos werden ausgelassen.

Die Aufgabe und die Nachricht zeigen das Foto. Tippe darauf, um es groß anzusehen.

## Was gesendet werden kann

Einen Text oder eine Datei mit optionaler Bildunterschrift in einen bestehenden Chat, und erst, nachdem du die Aufgabe freigegeben hast. Vor dem Senden zeigt die Aufgabe die Datei an, die du öffnen kannst. Dateien dürfen bis zu 18 MB groß sein. Eine Antwort auf die WhatsApp-Nachricht, aus der eine Aufgabe entstanden ist, zitiert die Nachricht, wenn danach noch weitere Nachrichten gesendet wurden oder sie in einer Gruppe steht. Im Entwurf steht **Als Antwort**.

Wenn eine Aufgabe per E-Mail eingegangen ist, du aber mit der Person über WhatsApp schreibst, erwähne das im Chat der Aufgabe. The Machine findet deinen bestehenden Chat mit der Person und stellt den Entwurf auf WhatsApp um, damit du ihn prüfen und senden kannst. The Machine beginnt nie einen neuen Chat.

WhatsApp bietet dafür keine offizielle Möglichkeit. Lesen und gelegentliche, von dir freigegebene Antworten verursachen sehr wahrscheinlich keine Probleme. Massenhaftes oder automatisiertes Senden kann dazu führen, dass ein Konto gesperrt wird.

## WhatsApp verbinden

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle WhatsApp aus.
2. Tippe auf **QR-Code zeigen**.
3. Öffne WhatsApp auf deinem Handy, gehe zu Einstellungen, Verknüpfte Geräte und Gerät verknüpfen, und scanne den QR-Code.
4. WhatsApp wird innerhalb einer Minute als verbunden angezeigt. Danach wird dein Chatverlauf weiter geladen. Währenddessen zeigt die Karte die Anzahl der Nachrichten an.
   Dauert das Verbinden zu lange, wird das nach ein paar Minuten angezeigt. Tippe auf **Erneut versuchen**, um dort weiterzumachen, wo der Vorgang angehalten wurde.

Richtest du WhatsApp auf deinem Handy ein und hast keinen zweiten Bildschirm zum Scannen? Öffne **Am Handy? Stattdessen mit einem Code verknüpfen**, gib deine Nummer ein und tippe auf **Code holen**. WhatsApp fragt dich dann nach dem Code.

Auf deinem eigenen Computer: Öffne **Verbindungen**, dann **Chat**, wähle WhatsApp aus, gib deine Telefonnummer mit Landesvorwahl ein und tippe auf **Verbinden**. Ein Code wird angezeigt. Öffne WhatsApp auf deinem Handy, gehe zu Einstellungen, Verknüpfte Geräte, Gerät verknüpfen und dann **Stattdessen mit Telefonnummer verknüpfen**. Gib den Code ein.

Oder führe `assistant connect whatsapp` aus und scanne den Code, der im Terminal angezeigt wird. Beim ersten Mal wird angeboten, den WhatsApp-Connector zu installieren. Dabei handelt es sich um einen festgelegten Build, der anhand seiner Prüfsumme überprüft wird ([Quellcode](https://github.com/Salesflare/wacli)).

Unter „Verknüpfte Geräte“ wird The Machine angezeigt. Eine Machine, die schon einmal verknüpft wurde, behält dort ihren alten Namen, bis du sie erneut verknüpfst.

Wenn WhatsApp deine Machine abmeldet, steht auf der Karte **WhatsApp hat die Verknüpfung mit dieser Machine aufgehoben**. Tippe auf **Neu verbinden** und verknüpfe sie erneut: Gib deine Telefonnummer und den Code ein, der in WhatsApp unter „Verknüpfte Geräte“ und **Stattdessen mit Telefonnummer verknüpfen** angezeigt wird. Die Verknüpfung wird am selben Ort wie zuvor eingerichtet, deine Chats bleiben also erhalten. Wenn du einen eigenen Dienst eingerichtet hast, der WhatsApp synchron hält, wird er während der Verknüpfung angehalten und danach wieder gestartet.

Wenn WhatsApp zu lange für eine Antwort braucht, wird das während der Einrichtung angezeigt. Tippe eine Minute später auf **Erneut versuchen**, um einen neuen Code anzufordern.

## Profilbilder

The Machine fragt WhatsApp über die Synchronisierung, die WhatsApp aktuell hält, nach Profilbildern für Personen in deinem Graph, bei denen noch keins vorhanden ist. Es werden höchstens 50 Bilder pro Tag angefragt. An diese Personen wird nichts gesendet. Wer sein Bild vor dir verbirgt, hat weiterhin keins.

## WhatsApp entfernen

- Auf einer gehosteten Machine: Tippe auf der Einrichtungsseite neben WhatsApp auf **Entfernen**. Deine Machine hebt die Verknüpfung auf und löscht die gespeicherten WhatsApp-Daten.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, dann WhatsApp und **Details**, und tippe auf **Trennen**. Hebe die Verknüpfung anschließend auch auf deinem Handy auf.

## Verknüpfung in WhatsApp aufheben

Öffne WhatsApp auf deinem Handy, gehe zu Einstellungen und Verknüpfte Geräte, tippe auf deine Machine und melde sie ab.
