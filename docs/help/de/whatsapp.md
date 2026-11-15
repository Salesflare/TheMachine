---
title: WhatsApp
area: connections
summary: Deine WhatsApp-Chats, gelesen über ein verknüpftes Gerät. Antworten werden erst nach deiner Freigabe gesendet.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 4ceded6544e535eb
---
## Was gelesen wird

Deine WhatsApp-Chats, als verknüpftes Gerät deines WhatsApp-Kontos auf dem Handy, ähnlich wie WhatsApp auf einem Computer. Wenn du die Verbindung herstellst, sendet WhatsApp auch ältere Chats, oft mehrere Jahre davon. Deine Machine speichert alles. Nur Nachrichten aus den letzten 7 Tagen werden zu Aufgaben.

Ein Foto, eine Sprachnachricht oder eine Datei ohne Beschriftung wird als das angezeigt, was es ist, zum Beispiel als „Foto“ mit dem entsprechenden Symbol. WhatsApps eigene Mitteilungen, etwa der Hinweis zur Verschlüsselung oder dass jemand einer Gruppe beigetreten ist, enthalten keinen Text und werden ausgelassen.

## Fotos lesen

Die Funktion ist deaktiviert, bis du sie einschaltest. Öffne unter **Verbindungen** WhatsApp und dann **Details**. Aktiviere **Fotos lesen**, damit The Machine die Fotos in deinen beruflichen Chats liest: einen Beleg, einen Screenshot, ein Foto von einem Brief oder einem Formular. Mit **Auch in privaten Chats** werden auch die Fotos in deinen privaten Chats gelesen. Ob ein Chat beruflich oder privat ist, richtet sich danach, wie er beim Teilen eingeordnet wird. Ein Chat mit der Familie bleibt also privat.

The Machine lädt jedes Foto einmal herunter und speichert es auf deiner Machine wie einen E-Mail-Anhang: Bei aktiviertem Nachrichtenschutz ist es verschlüsselt und wird gelöscht, sobald die zugehörige Nachricht gelöscht wird. Das eigene Modell von The Machine liest, was auf dem Foto zu sehen ist, und den darin enthaltenen Text. Beides gilt als Teil der Nachricht, niemals als Anweisung. JPEG, PNG und WebP bis zu 5 MB. Ein einmaliger Code auf einem Foto wird ausgelassen.

Die Aufgabe und die Nachricht zeigen das Foto. Tippe darauf, um es groß zu sehen.

## Was gesendet werden kann

Einen Text oder eine Datei mit optionaler Beschriftung an einen bestehenden Chat, aber erst, nachdem du die Aufgabe freigegeben hast. Bevor du etwas sendest, zeigt die Aufgabe die Datei an, die du öffnen kannst. Eine Datei darf bis zu 18 MB groß sein. Eine Antwort auf die WhatsApp-Nachricht, von der eine Aufgabe stammt, zitiert diese Nachricht, wenn danach noch etwas geschrieben wurde oder wenn sie in einer Gruppe gesendet wurde. Im Entwurf steht **Als Antwort**.

Wenn eine Aufgabe per E-Mail eingegangen ist, du aber mit der Person auf WhatsApp schreibst, sag das im Chat der Aufgabe. The Machine findet den bestehenden Chat mit der Person und stellt den Entwurf auf WhatsApp um, damit du ihn prüfen und senden kannst. Ein neuer Chat wird nie begonnen.

WhatsApp bietet dafür keine offizielle Möglichkeit. Lesen und gelegentliche, von dir freigegebene Antworten führen sehr wahrscheinlich zu keinen Problemen. Massenversand oder automatisiertes Senden kann dazu führen, dass ein Konto gesperrt wird.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle WhatsApp aus.
2. Tippe auf **QR-Code zeigen**.
3. Öffne auf deinem Handy in WhatsApp die Einstellungen, Verknüpfte Geräte und Gerät verknüpfen. Scanne dann den QR-Code.
4. WhatsApp wird innerhalb einer Minute als verbunden angezeigt. Danach wird weiterhin dein Chatverlauf geladen. Auf der zugehörigen Karte wird angezeigt, wie viele Nachrichten dabei verarbeitet wurden.
   Wenn das Verbinden zu lange dauert, wird das nach einigen Minuten angezeigt. Tippe auf **Erneut versuchen**, um dort weiterzumachen, wo der Vorgang angehalten wurde.

Richtest du WhatsApp auf deinem Handy ein und hast keinen zweiten Bildschirm zum Scannen? Öffne **Am Handy? Stattdessen mit einem Code verknüpfen**, gib deine Nummer ein und tippe auf **Code holen**. WhatsApp fragt dich dann nach dem Code.

Auf deinem eigenen Computer: Öffne **Verbindungen**, dann **Chat**, wähle WhatsApp aus, gib deine Telefonnummer mit Ländervorwahl ein und tippe auf **Verbinden**. Es wird ein Code angezeigt. Öffne auf deinem Handy in WhatsApp die Einstellungen, Verknüpfte Geräte und Gerät verknüpfen. Tippe dann auf **Stattdessen mit Telefonnummer verknüpfen** und gib den Code ein.

Oder führe `assistant connect whatsapp` aus und scanne den Code, der im Terminal angezeigt wird. Beim ersten Mal kannst du den WhatsApp-Connector installieren. Dabei handelt es sich um einen angehefteten Build, der anhand seiner Prüfsumme überprüft wurde ([Quelle](https://github.com/Salesflare/wacli)).

Unter „Verknüpfte Geräte“ wird The Machine angezeigt. Eine Machine, die schon einmal verknüpft war, behält dort ihren alten Namen, bis du sie erneut verknüpfst.

## Profilbilder

The Machine fragt WhatsApp über die Synchronisierung, die WhatsApp aktuell hält, nach den Profilbildern von Personen in deinem Graph, wenn diese noch keins haben. Es werden höchstens 50 pro Tag angefragt. An diese Personen wird nichts gesendet. Wer sein Bild vor dir verbirgt, bleibt ohne Profilbild.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf der Einrichtungsseite neben WhatsApp auf **Entfernen**. Deine Machine hebt die Verknüpfung auf und löscht die gespeicherten WhatsApp-Daten.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, dann WhatsApp und **Details**. Tippe anschließend auf **Trennen**. Hebe die Verknüpfung danach auch auf deinem Handy auf.

## Verknüpfung in WhatsApp aufheben

Öffne auf deinem Handy in WhatsApp die Einstellungen und dann Verknüpfte Geräte. Tippe auf deine Machine und melde sie ab.
