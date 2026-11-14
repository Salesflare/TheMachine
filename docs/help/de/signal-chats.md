---
title: Signal-Chats
area: connections
summary: Deine Signal-Chats und Gruppen, gelesen als verknüpftes Gerät deines Handys. Antworten erst nach deiner Freigabe.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
translated: b85609009f246615
---
## Was es liest

Deine Chats und Gruppen, als verknüpftes Gerät deines Handys, wie Signal Desktop. Signal gibt einem neu verknüpften Gerät keine älteren Nachrichten, daher liest es ab dem Moment, in dem du es verknüpfst.

Fotos, Sprachnachrichten und Dateien erscheinen als das, was sie sind („Hat ein Foto gesendet“), nie mit ihrem Inhalt. Einmal ansehbare Medien behalten gar keinen Inhalt. Bearbeitungen und Löschungen folgen dem, was auf deinem Handy passiert ist, und verschwindende Nachrichten gehen von deiner Machine, sobald ihre Zeit abgelaufen ist.

Storys, Reaktionen, Anrufe und Notiz an mich werden übersprungen. Nichts wird als gelesen markiert.

## Was es senden kann

Einen Text in einen Chat, den es schon gibt, erst nachdem du ihn in der Aufgabe freigegeben hast. Eine Antwort zitiert die Nachricht, auf die sie antwortet, wenn das hilft. Nachrichten gehen einzeln raus, mit einer Pause dazwischen.

Kam eine Aufgabe per E-Mail, aber du schreibst mit dieser Person auf Signal, sag das im Chat der Aufgabe. The Machine findet deinen bestehenden Chat mit ihr und stellt den Entwurf auf Signal um, damit du ihn prüfst und sendest. Sie beginnt nie einen neuen Chat.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **Chat**, und wähle Signal-Chats.
2. Öffne auf deinem Handy in Signal Einstellungen, **Verknüpfte Geräte**, **Neues Gerät verknüpfen**, und scanne den Code.

Du brauchst einen zweiten Bildschirm zum Scannen: Signal verknüpft ein Gerät nur per QR-Code. Oder führe `assistant connect signal` in einem Terminal aus und scanne den Code, der dort erscheint.

Deine Machine behält die Schlüssel des verknüpften Geräts bei sich. Sie verlassen sie nie.

## Wenn es aufhört

Es nutzt signal-cli, einen inoffiziellen Signal-Client. Deine Machine lädt eine festgelegte Version herunter und prüft ihre Prüfsumme, bevor sie läuft. Signal kann ihn jederzeit nicht mehr akzeptieren.

- **Signal hat diese Machine entkoppelt**: Du hast sie auf deinem Handy entfernt, oder Signal hat die Verknüpfung beendet. Tippe in **Verbindungen** auf **Neu verbinden** und scanne einen neuen Code.
- **Aktualisiere The Machine für Signal**: Signal akzeptiert den Signal-Client dieser Machine nicht mehr. Aktualisiere The Machine.

## Entfernen

**Verbindungen**, Signal-Chats öffnen, **Details**, dann **Trennen**. Deine Machine löscht die Schlüssel und was sie für Signal gespeichert hat. Entferne sie danach auch auf deinem Handy: Signal, Einstellungen, **Verknüpfte Geräte**, tippe auf The Machine und entkopple sie.
