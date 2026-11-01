---
title: Übergaben
area: fleet
summary: Übergib eine Aufgabe an die Machine eines Teammitglieds, mit allem, was es braucht. Frag später nach oder nimm sie zurück.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
---
## Eine Aufgabe übergeben

1. Wähle bei der Aufgabe **An ein Teammitglied übergeben**.
2. Wähle, an wen, prüfe, was mitgeht (lass mit × jeden Teil weg), und füge eine Notiz hinzu. Der Text beginnt mit der Aufgabe und warum sie wichtig ist, aus der Aufgabe, und woher sie kommt (ihr Link). Nichts aus einem privaten Konto oder dem einer anderen Firma geht mit.
3. Schick sie ab. Die Machine des Teammitglieds zeigt sie ihm als Aufgabe.

Ein Intercom-Gespräch geht mit seinem Platz in Intercom mit. Liest ihre Machine denselben Intercom-Workspace, hängt ihre Aufgabe an diesem Gespräch: **Nachricht lesen** öffnet es, der Kunde steht darauf, und ihre Antwort geht in Intercom zurück. Wenn nicht, verlinkt die Aufgabe trotzdem das Gespräch in Intercom.

Während du wartest, steht die Aufgabe unter **Kommt später zurück**, „Bei Pat · wartet“, mit einem Datum zum Nachfragen. **Jetzt nachhaken** fragt, wie es läuft. **Uhrzeit ändern** verschiebt das Nachfragen.

Sie kommt nur dann wieder nach oben, wenn es etwas zu entscheiden gibt: Pat hat geantwortet, abgelehnt oder sie als erledigt markiert, die Übergabe ist fehlgeschlagen oder eine Frist ist erreicht. Bei einer Aufgabe, die heute fällig ist, wird ein paar Stunden später nachgefragt, bei einer bald fälligen am Arbeitstag davor, bei einer dringenden ohne Datum am nächsten Arbeitsmorgen und bei allen anderen nach 3 Arbeitstagen.

Zurück zum Nachhaken steht dort „Noch bei Pat · nachhaken?“: Pat hat sie noch, es kam nichts zurück. **Jetzt nachhaken** öffnet den Chat; **Zurücknehmen** und **An jemand anderen übergeben** stehen daneben, und Als erledigt markieren, Zurückstellen und Nicht nötig sind unter Mehr.

Der Chat der Aufgabe zeigt, wann sie rausging („An die Machine von Pat übergeben · 14:02“) und was zurückkam: angenommen, abgelehnt (mit Notiz) oder erledigt. Ist sie zum Nachfragen zurück und es gibt noch keine Antwort, steht „Noch keine Antwort von Pat“ unter dieser Zeile, mit **Als erledigt markieren**, **Zurückstellen** und **Nicht nötig** (kein Ausführen: Pat hat sie). Um Pat zu erinnern oder sie zurückzunehmen, sag es im Chat.

Wenn die Übergabe nicht rausging, sagen die Aufgabe und ihr Chat das, mit **Erneut versuchen**.

## Stattdessen an jemand anderen übergeben

Solange ein Teammitglied sie hat, sagt die Aufgabe das in einer Zeile („Bei Pat · wartet“), mit **Zurücknehmen** und **An jemand anderen übergeben**. **Zurücknehmen** macht sie wieder zu deiner: Die Machine von Pat erfährt es, und eine Antwort von Pat verschiebt sie nicht mehr.

**An jemand anderen übergeben** öffnet das Übergabeformular, für jemanden, der sie noch nicht hat. Oder sag es im Chat der Aufgabe („das sollte an Kim gehen“). Die neue Übergabe wartet bei der Aufgabe, bis du sie gelesen hast: „Noch bei Pat, bis du sie an Kim schickst“, mit **Übergabe prüfen an** Kim. Das öffnet das Formular mit dem Text, für Kim.

Eine Aufgabe geht an jede Person im Team nur einmal: Solange Pat sie hat, sagt eine erneute Übergabe an Pat „Pat hat diese Aufgabe schon“.

**Zurücknehmen von** Pat ist standardmäßig an. Schalte es aus, wenn beide sie haben sollen. Nichts geht raus, bis du **Übergeben** wählst. Dann sagt der Chat „Von Pat zurückgenommen“ und „An die Machine von Kim übergeben“. Die Machine von Pat erfährt es auch, und die Aufgabe, die sie für Pat angelegt hat, verschwindet.

## Wenn jemand ablehnt

Die Person kann sagen, warum: nicht ihre Sache, schon erledigt oder keine Zeit diese Woche. Wähle dann **Selbst erledigen**, **An jemand anderen übergeben** oder **Als erledigt markieren**.

## Jemand außerhalb des Network

Wähle **Per E-Mail**: Deine Machine entwirft eine E-Mail, die du sendest. Während du die Adresse eingibst, schlägt sie zuerst Teammitglieder vor: Personen in deiner Fleet, dann Personen mit der Domain deiner Firma, dann das Getippte mit dieser Domain. Füge eine Aufgabenseite hinzu, damit die Person mit einem Tippen antworten kann: siehe [Aufgabenseiten](task-pages.md).

Nur für Arbeit-Aufgaben. Hake an, was in die E-Mail kommt: ein paar Zeilen zur Aufgabe, ihr fertiger Entwurf, Links und Dateien. Angeboten wird nur, was dein Team Graph mit dem Team teilt, also bleiben Privat und Nur du draußen. **E-Mail vorbereiten** legt die E-Mail auf die Aufgabe: lies sie und sende sie dann aus deinem eigenen Postfach wie jede E-Mail. Keine Tracking-Pixel.

Die Aufgabe zeigt dann "Per E-Mail an <Name> übergeben" und verfolgt es als Versprechen, bis die Person antwortet, dass es erledigt ist, oder du es als erledigt markierst. Am Ende steht "Übernimm das in deiner eigenen Machine": Wer sich über diesen Link anmeldet, kann deiner Fleet beitreten, und die Aufgabe geht als normale Übergabe in die eigene Machine. Schalte die Zeile in **Einstellungen** unter Fleet aus.
