---
title: WhatsApp
area: connections
summary: Deine WhatsApp-Chats, gelesen als verknüpftes Gerät. Antworten erst nach deiner Freigabe.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Was es liest

Deine WhatsApp-Chats, als verknüpftes Gerät des WhatsApp auf deinem Handy, wie WhatsApp auf einem Computer. Beim Verbinden schickt WhatsApp auch deine älteren Chats, oft über Jahre. Deine Machine behält alles, und nur Nachrichten der letzten 7 Tage werden zu Aufgaben.

Ein Foto, eine Sprachnachricht oder eine Datei ohne Beschriftung erscheint als das, was es ist, etwa „Bild gesendet“. Hinweise von WhatsApp selbst, etwa zur Verschlüsselung oder wenn jemand einer Gruppe beitritt, haben keinen Text und bleiben außen vor.

## Fotos lesen

Aus, bis du es einschaltest. Öffne unter **Verbindungen** WhatsApp, dann **Details**, und schalte **Fotos lesen** ein, und The Machine liest die Fotos in deinen Arbeitschats: einen Beleg, einen Screenshot, ein Foto von einem Brief oder einem Formular. **Auch in privaten Chats** liest auch die in deinen privaten Chats. Ob ein Chat Arbeit oder privat ist, sieht sie so wie beim Teilen, ein Chat mit der Familie bleibt also privat.

The Machine lädt jedes Foto einmal herunter und behält es auf deiner Machine wie einen E-Mail-Anhang: verschlüsselt, wenn der Nachrichtenschutz an ist, und gelöscht, wenn seine Nachricht verschwindet. Ihr eigenes Modell liest, was das Foto zeigt und den Text darin. Das gilt als Teil der Nachricht, nie als Anweisung. JPEG, PNG und WebP bis 5 MB. Ein Einmalcode auf einem Foto bleibt außen vor.

Die Aufgabe und die Nachricht zeigen das Foto. Tippe darauf, um es groß zu sehen.

## Was es senden kann

Einen Text in einen Chat, den es schon gibt, erst nachdem du ihn bei der Aufgabe freigegeben hast. Eine Antwort auf die WhatsApp-Nachricht, aus der eine Aufgabe kam, zitiert diese Nachricht, wenn danach noch mehr geschrieben wurde, oder in einer Gruppe; im Entwurf steht **Als Antwort**.

Kam eine Aufgabe per E-Mail rein, aber du schreibst mit der Person über WhatsApp, sag es im Chat der Aufgabe. The Machine findet euren bestehenden Chat und stellt den Entwurf auf WhatsApp um, damit du ihn prüfst und sendest. Sie startet nie einen neuen Chat.

WhatsApp bietet dafür keinen offiziellen Weg. Lesen und ab und zu eine Antwort, die du freigegeben hast, machen so gut wie nie Probleme; massenhaftes oder automatisches Senden kann zur Sperrung eines Kontos führen.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle WhatsApp.
2. Tippe auf **QR-Code zeigen**.
3. Öffne auf deinem Handy in WhatsApp Einstellungen, Verknüpfte Geräte, Gerät hinzufügen, und scanne den QR-Code.
4. Innerhalb einer Minute ist WhatsApp verbunden. Dein Chatverlauf kommt danach weiter an, und die Karte zählt die Nachrichten, solange das läuft.
   Dauert das Verbinden zu lange, sagt sie es nach ein paar Minuten. Tippe auf **Erneut versuchen**, um dort weiterzumachen, wo es stehen blieb.

Du richtest es auf deinem Handy ein und hast keinen zweiten Bildschirm zum Scannen? Öffne **Am Handy? Stattdessen mit einem Code verknüpfen**, gib deine Nummer ein und tippe auf **Code anfordern**. WhatsApp fragt dann nach diesem Code.

Auf deinem eigenen Computer: Öffne **Verbindungen**, dann **+ Hinzufügen**, wähle WhatsApp, gib deine Handynummer mit Ländervorwahl ein und tippe auf **Verbinden**. Es zeigt einen Code. Öffne auf deinem Handy in WhatsApp Einstellungen, Verknüpfte Geräte, Gerät hinzufügen, dann **Stattdessen mit Telefonnummer verknüpfen**, und gib den Code ein.

Oder führe `assistant connect whatsapp` aus und scanne den Code, den es im Terminal zeigt. Beim ersten Mal bietet es an, die WhatsApp-Verbindung zu installieren, einen festgelegten Build, geprüft anhand seiner Prüfsumme ([Quelle](https://github.com/Salesflare/wacli)).

Unter Verknüpfte Geräte steht sie als The Machine. Eine früher verknüpfte Machine behält dort ihren alten Namen, bis du sie neu verknüpfst.

## Bilder

The Machine fragt WhatsApp nach den Profilbildern von Personen in deinem Graph, die keins haben, höchstens 50 am Tag, über die Synchronisierung, die WhatsApp aktuell hält. An die Personen wird nichts gesendet. Wer sein Bild vor dir verbirgt, bleibt ohne.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite daneben auf **Entfernen**. Deine Machine trennt die Verknüpfung selbst und löscht, was sie für WhatsApp gespeichert hat.
- Auf deinem eigenen Computer: **Verbindungen**, WhatsApp öffnen, **Details**, dann **Trennen**. Trenn die Verknüpfung dann auch auf deinem Handy.

## Verknüpfung in WhatsApp trennen

Öffne auf deinem Handy in WhatsApp Einstellungen, Verknüpfte Geräte, tippe auf deine Machine und melde sie ab.
