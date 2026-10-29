---
title: WhatsApp
area: connections
summary: Deine WhatsApp-Chats, gelesen als verknüpftes Gerät. Antworten erst nach deiner Freigabe.
covers: connector:whatsapp
code: onboarding.py, next_actions.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Was es liest

Deine WhatsApp-Chats, als verknüpftes Gerät des WhatsApp auf deinem Handy, wie WhatsApp auf einem Computer. Beim Verbinden liest es die letzten 7 Tage.

Ein Foto, eine Sprachnachricht oder eine Datei ohne Beschriftung erscheint als das, was es ist, etwa „Bild gesendet“. Hinweise von WhatsApp selbst, etwa zur Verschlüsselung oder wenn jemand einer Gruppe beitritt, haben keinen Text und bleiben außen vor.

## Was es senden kann

Einen Text in einen Chat, den es schon gibt, erst nachdem du ihn bei der Aufgabe freigegeben hast.

Kam eine Aufgabe per E-Mail rein, aber du schreibst mit der Person über WhatsApp, sag es im Chat der Aufgabe. The Machine findet euren bestehenden Chat und stellt den Entwurf auf WhatsApp um, damit du ihn prüfst und sendest. Sie startet nie einen neuen Chat.

## Verbinden

Auf einer gehosteten Machine:

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle WhatsApp.
2. Tippe auf **QR-Code zeigen**.
3. Öffne auf deinem Handy in WhatsApp Einstellungen, Verknüpfte Geräte, Gerät hinzufügen, und scanne den QR-Code.

Du richtest es auf deinem Handy ein und hast keinen zweiten Bildschirm zum Scannen? Öffne **Am Handy? Stattdessen mit einem Code verknüpfen**, gib deine Nummer ein und tippe auf **Code anfordern**. WhatsApp fragt dann nach diesem Code.

Auf deinem eigenen Computer führst du `assistant connect whatsapp` aus und scannst den Code, den es im Terminal zeigt. Ohne wacli bietet es an, den festgelegten Build von [Salesflare/wacli](https://github.com/Salesflare/wacli) zu installieren, geprüft anhand seiner Prüfsumme.

## Bilder

The Machine fragt WhatsApp nach den Profilbildern von Personen in deinem Graph, die keins haben, höchstens 50 am Tag, über die Synchronisierung, die WhatsApp aktuell hält. An die Personen wird nichts gesendet. Wer sein Bild vor dir verbirgt, bleibt ohne.

## Entfernen

- Auf einer gehosteten Machine: Tippe auf deiner Einrichtungsseite daneben auf **Entfernen**. Deine Machine trennt die Verknüpfung selbst und löscht, was sie für WhatsApp gespeichert hat.
- Auf deinem eigenen Computer: **Verbindungen**, WhatsApp öffnen, **Details**, dann **Trennen**. Trenn die Verknüpfung dann auch auf deinem Handy.

## Verknüpfung in WhatsApp trennen

Öffne auf deinem Handy in WhatsApp Einstellungen, Verknüpfte Geräte, tippe auf deine Machine und melde sie ab.
