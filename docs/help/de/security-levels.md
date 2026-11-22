---
title: Sicherheitsstufen
area: security
summary: Mit einem Schalter legst du über Standard oder Vorsichtig deine Sicherheits- und Datenschutzeinstellungen fest. Die Admins einer Work Fleet wählen die Einstellung für die Fleet aus.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
translated: cf3ba86c8c1a23f3
---
## Zwei Stufen

Öffne **Einstellungen** und dann **Sicherheit**.

- **Standard**: die aktuellen Standardeinstellungen. Es ändert sich nichts.
- **Vorsichtig**: strengere Einstellungen, wenn weniger auf deinem Handy stehen und weniger gespeichert bleiben soll.

Eine Stufe ist ein Ausgangspunkt. Wenn du danach eine Einstellung änderst, wird **Eigene** angezeigt. Wähle erneut eine Stufe aus, um die Einstellungen zurückzusetzen.

## Was sich für dich mit „Vorsichtig“ ändert

- **Text in Benachrichtigungen** ist aus: In einer Benachrichtigung steht „Neue Aufgabe“ oder „Bereit“, aber nicht, worum es bei der Aufgabe geht.
- **Speichern von Anmeldungen anbieten** ist aus. Deine gespeicherten Anmeldungen für Websites bleiben bestehen, bis du auf **Alle gespeicherten Anmeldungen vergessen** tippst.
- **Arbeitskontakte nachschlagen**, **Anbieten, Erkenntnisse zu teilen** und **Fragen an die Hilfe teilen** sind aus.
- **Prüfen, welche meiner Kontakte eine Machine haben** und **Leute, die meine E-Mail-Adresse haben, dürfen mich finden** sind aus.
- **Ausführen-Details 90 Tage behalten** ist aus: Sie werden 30 Tage lang aufbewahrt.
- **Was andere Machines meine Machine fragen dürfen** ist auf **Aus** gesetzt: Es ist keine Terminplanung mit anderen Machines möglich. Weitere Informationen findest du unter [Freunde und das Network](friends.md#scheduling-with-other-machines).
- In einer Familie musst du der Abfrage deiner Verfügbarkeit erst zustimmen. Bei Freunden wird der Meeting-Kontext abgelehnt.

## Die Stufe einer Work Fleet

Der Inhaber oder ein Admin der Fleet wählt die Stufe in den Fleet-Einstellungen aus: Öffne **Einstellungen** › **Konto** und tippe auf **Fleet**. Alle Mitglieder der Fleet sehen die Auswahl. Wenn „Vorsichtig“ eingestellt ist:

- Antworten an Teammitglieder werden erst nach deiner Zustimmung gesendet, ohne Namen und nur zu Personen aus deinen Arbeitskonten.
- Auch Vorstellungen und Übergaben warten auf deine Zustimmung.
- Der Graph des Teams teilt E-Mails von Kunden ohne Anhänge.
- In Benachrichtigungen zu Arbeitsaufgaben wird kein Text angezeigt.
- Arbeitskontakte werden nicht nachgeschlagen.
- Deine Machine prüft deine Kontakte nicht im Network und macht dich nicht über deine E-Mail-Adresse auffindbar, es sei denn, du hast das selbst aktiviert.
- Alle müssen sich alle 7 Tage erneut anmelden.
- Ein Einladungslink funktioniert nur mit der E-Mail-Adresse, an die er gesendet wurde.

Mitglieder können strengere, aber keine weniger strengen Einstellungen als die Fleet wählen. Ihre eigenen Einstellungen bleiben erhalten und gelten wieder, wenn die Fleet zu Standard zurückkehrt.

## In beiden Stufen gleich

Ohne deine Zustimmung wird nichts gesendet: Du siehst jeden Entwurf und tippst auf „Senden“. Ausführen und Coding-Agenten funktionieren unverändert. Für die Anmeldung ist immer ein Authenticator-Code oder ein Passkey erforderlich.
