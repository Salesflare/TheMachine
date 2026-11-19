---
title: WhatsApp
area: connections
summary: Deine WhatsApp-Chats werden wie auf einem verknüpften Gerät gelesen. Antworten werden erst nach deiner Freigabe gesendet.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 9446d22f96229653
---
## Was gelesen wird

Deine WhatsApp-Chats werden wie auf einem mit dem WhatsApp-Konto deines Handys verknüpften Gerät gelesen, ähnlich wie bei WhatsApp auf einem Computer. Wenn du die Verbindung herstellst, sendet WhatsApp auch ältere Chats, oft mehrere Jahre zurück. Deine Machine speichert alles, aber nur Nachrichten der letzten 7 Tage werden zu Aufgaben.

Ein Foto, eine Sprachnachricht oder eine Datei ohne Bildunterschrift wird als das angezeigt, was sie ist, zum Beispiel als „Foto“ mit dem entsprechenden Symbol. WhatsApps eigene Hinweise, etwa zur Verschlüsselung oder wenn jemand einer Gruppe beitritt, enthalten keinen Text und werden ausgelassen.

## Fotos lesen

Die Funktion ist deaktiviert, bis du sie einschaltest. Öffne in **Verbindungen** WhatsApp und dann **Details**. Aktiviere **Fotos lesen**, damit The Machine Fotos in deinen beruflichen Chats liest, zum Beispiel einen Kassenbon, einen Screenshot, ein Foto von einem Brief oder ein Formular. Mit **Auch in privaten Chats** werden auch Fotos aus deinen privaten Chats gelesen. Ob ein Chat beruflich oder privat ist, richtet sich danach, wie er beim Teilen eingestuft wird. Ein Chat mit deiner Familie bleibt also privat.

The Machine lädt jedes Foto einmal herunter und speichert es auf deiner Machine wie einen E-Mail-Anhang: verschlüsselt, wenn der Nachrichtenschutz aktiviert ist, und gelöscht, sobald die zugehörige Nachricht gelöscht wird. Das eigene Modell von The Machine liest, was auf dem Foto zu sehen ist und welchen Text es enthält. Das gilt als Teil der Nachricht, niemals als Anweisung. Unterstützt werden JPEG, PNG und WebP bis zu 5 MB. Ein Einmalcode auf einem Foto wird ausgelassen.

Die Aufgabe und die Nachricht zeigen das Foto. Tippe darauf, um es groß anzusehen.

## Was gesendet werden kann

Einen Text oder eine Datei mit optionaler Bildunterschrift in einen bereits bestehenden Chat, aber erst, nachdem du die Aufgabe freigegeben hast. Vor dem Senden zeigt die Aufgabe die Datei an, die du öffnen kannst. Dateien dürfen bis zu 18 MB groß sein. Wenn nach der Nachricht, aus der eine Aufgabe entstanden ist, noch weitere Nachrichten gesendet wurden oder die Nachricht in einer Gruppe war, wird sie beim Antworten zitiert. Im Entwurf steht dann **Als Antwort**.

Wenn eine Aufgabe per E-Mail eingegangen ist, du aber mit der Person über WhatsApp kommunizierst, erwähne das im Chat der Aufgabe. The Machine findet deinen bestehenden Chat mit der Person und stellt den Entwurf auf WhatsApp um, damit du ihn prüfen und senden kannst. The Machine beginnt nie einen neuen Chat.

WhatsApp bietet dafür keine offizielle Möglichkeit. Lesen und gelegentliches Antworten nach deiner Freigabe führen sehr wahrscheinlich zu keinen Problemen. Massenversand oder automatisiertes Senden kann dazu führen, dass ein Konto gesperrt wird.

## Verbindung herstellen

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle WhatsApp aus.
2. Tippe auf **QR-Code zeigen**.
3. Öffne WhatsApp auf deinem Handy, gehe zu Einstellungen, Verknüpfte Geräte, Gerät verknüpfen und scanne den QR-Code.
4. Innerhalb einer Minute wird WhatsApp als verbunden angezeigt. Danach wird dein Chatverlauf weiter geladen. Die Karte zeigt dabei an, wie viele Nachrichten geladen wurden.
   Wenn die Verbindung zu lange dauert, wird das nach ein paar Minuten angezeigt. Tippe auf **Erneut versuchen**, um dort weiterzumachen, wo der Vorgang angehalten wurde.

Richtest du WhatsApp auf deinem Handy ein und hast keinen zweiten Bildschirm zum Scannen? Öffne **Am Handy? Stattdessen mit einem Code verknüpfen**, gib deine Telefonnummer ein und tippe auf **Code holen**. WhatsApp fragt dich anschließend nach diesem Code.

Auf deinem eigenen Computer: Öffne **Verbindungen**, dann **Chat**, wähle WhatsApp aus, gib deine Telefonnummer mit Ländervorwahl ein und tippe auf **Verbinden**. Ein Code wird angezeigt. Öffne WhatsApp auf deinem Handy, gehe zu Einstellungen, Verknüpfte Geräte, Gerät verknüpfen und dann **Stattdessen mit Telefonnummer verknüpfen**. Gib den Code ein.

Oder führe `assistant connect whatsapp` aus und scanne den im Terminal angezeigten Code. Beim ersten Mal wird angeboten, den WhatsApp-Connector zu installieren. Dabei handelt es sich um einen festgelegten Build, dessen Prüfsumme überprüft wurde ([Quellcode](https://github.com/Salesflare/wacli)).

Unter „Verknüpfte Geräte“ wird The Machine angezeigt. Eine Machine, die bereits verknüpft war, behält dort ihren alten Namen, bis du sie erneut verknüpfst.

Wenn WhatsApp deine Machine abmeldet, steht auf der Karte **WhatsApp hat die Verknüpfung mit dieser Machine aufgehoben**. Tippe auf **Neu verbinden** und verknüpfe sie erneut.

## Bilder

The Machine fragt WhatsApp über die Synchronisierung, die WhatsApp auf dem neuesten Stand hält, nach Profilbildern von Personen in deinem Graph, denen noch eines fehlt. Das passiert höchstens 50-mal am Tag. Niemand erhält dabei eine Nachricht. Wer sein Bild vor dir verbirgt, bleibt ohne Profilbild.

## Verbindung entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite daneben auf **Entfernen**. Deine Machine hebt die Verknüpfung selbst auf und löscht die gespeicherten WhatsApp-Daten.
- Auf deinem eigenen Computer: Öffne **Verbindungen**, dann WhatsApp und **Details**, und tippe auf **Trennen**. Hebe anschließend auch auf deinem Handy die Verknüpfung auf.

## WhatsApp-Verknüpfung aufheben

Öffne WhatsApp auf deinem Handy, gehe zu Einstellungen, Verknüpfte Geräte, tippe auf deine Machine und melde sie ab.
