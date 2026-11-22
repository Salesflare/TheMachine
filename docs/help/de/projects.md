---
title: Projekte
area: graph
summary: Was gerade läuft: aus deinen Nachrichten erkannt oder manuell hinzugefügt, auf Boards mit Phasen wie Deals in einem CRM.
code: graph.py, crm.py, dashboard.html
order: 4
translated: 8ab2cc22d536a168
---
Deine Machine benennt Projekte danach, worum es in deinen Nachrichten geht. Nachrichten, die dazugehören könnten, werden als „wahrscheinlich gehört es dazu“ angezeigt. Benennst du ein Projekt nach einem anderen Projekt, werden beide zusammengeführt. Oder verwalte sie manuell, wie Deals in einem CRM.

## Projekt hinzufügen

**Neues Projekt** oben auf einem Board, **+ Hinzufügen** unter einer Phase, **Neues Projekt** oben in der Liste, **+** in der oberen Leiste auf dem Handy oder auf der Seite einer Person oder Organisation.

Gib einen Namen, ein Board und eine Phase, eine Organisation (durchsuche deinen Graph oder füge mit **Hinzufügen** eine neue hinzu), einen Wert, ein voraussichtliches Abschlussdatum, Personen und Notizen an. Projekte in deinem Graph mit einem ähnlichen Namen werden zuerst angezeigt.

## Projekt bearbeiten, gewinnen oder verlieren

- **Bearbeiten** auf der Projektseite oder **Bearbeiten** im **⋯** des Projekts auf dem Board (oder drücke E) ändert alle oben genannten Angaben.
- **Gewonnen** oder **Verloren**, jeweils mit Begründung, für einen Deal: ein Projekt mit einem Wert oder voraussichtlichen Abschlussdatum oder ein Projekt auf einem Board, auf dem es solche Angaben gibt. Gewonnen verschiebt es in die letzte Phase des Boards, Verloren nach „Ins Stocken geraten oder abgelehnt“. Bei anderen Projekten kannst du **Erledigt** auswählen. Mit **Wieder öffnen** machst du das rückgängig.
- **Archivieren** entfernt das Projekt vom Board und aus den Listen. Eine neue Nachricht dazu bringt es zurück.
- **Löschen** entfernt das Projekt endgültig. Die Nachrichten und Personen bleiben erhalten.

## Beschreibung

Ein oder zwei Sätze unter dem Projektnamen: worum es geht und wo es gerade steht. Deine Machine verfasst die Beschreibung anhand der Nachrichten, Aufgaben, Versprechen, Fakten und Phase des Projekts. Ändert sich etwas, etwa durch eine neue Nachricht, einen Phasenwechsel oder einen Gewinn oder Verlust, aktualisiert sie die Beschreibung. Gibt es noch nichts Konkretes zu sagen, wird keine Beschreibung angezeigt.

Du kannst die Beschreibung unter **Beschreibung** in **Bearbeiten** beim Projekt ändern. Danach gehört sie dir: „Von dir bearbeitet“, und deine Machine lässt sie unverändert. Mit **Aktuell halten** darunter oder in **Bearbeiten** übergibst du sie wieder deiner Machine. Wenn du sie leer speicherst, wird keine Beschreibung angezeigt.

Bei einem gemeinsam genutzten Work-Projekt sieht dein Team die Beschreibung nur, wenn auch alle Informationen, auf denen sie basiert, mit dem Team geteilt wurden. Deine eigene Änderung bleibt bei dir.

## Projekt verschieben

Zieh das Projekt in eine andere Phase oder tippe auf dem Handy auf **⋯** und dann auf **Verschieben nach**. Deine Änderung bleibt bestehen, bis eine neuere Nachricht das Projekt verschiebt.

Unter **Phasen** oben auf einem Board kannst du auswählen, welche Phasen angezeigt werden. Die Auswahl gilt nur für dieses Board. Mit **Entfernen** werden wieder alle Phasen angezeigt.

„4 ohne Antwort seit mehr als 10 Tagen“ unter einer Phase: Tippe darauf, um nur diese Projekte auf dem Board und in der Liste anzuzeigen. Tippe noch einmal, um alle anzuzeigen.

## Projekt aufteilen

Wenn ein Projekt mehrere Dinge umfasst, schlägt deine Machine über **Aufteilen…** im **⋯** zwei bis vier neue Projekte vor. Jedes bekommt einen Namen, eine Beschreibung und eine Zuordnung der Threads, Aufgaben und Personen. Zunächst wird nichts geändert: Benenne die Projekte um, verschiebe Einträge in einen anderen Teil, lass sie im Projekt oder entferne sie. Bestätige anschließend.

Die neuen Projekte werden auf demselben Board und in derselben Phase angelegt und mit denselben Personen wie das ursprüngliche Projekt geteilt, aber niemals mit mehr Personen. Auf der Seite steht anschließend, in welche Projekte es aufgeteilt wurde. Mit **Rückgängig** wird alles wiederhergestellt.

## Aufgaben eines Projekts

Eine Aufgabe kann zu einem Projekt gehören. Deine Machine ordnet sie einem Projekt zu, wenn ihr Thread oder die Personen, um die es geht, nur in einem offenen Projekt vorkommen. Der Projektname steht dann unter dem Titel der Aufgabe. Mit **Projekt** unter **Details** der Aufgabe oder **Einem Projekt zuordnen** im Befehlsmenü (Ctrl K) kannst du die Zuordnung ändern oder entfernen. Deine Auswahl bleibt bestehen.

Auf der Projektseite werden die Aufgaben unter **Aufgaben** aufgeführt, offene zuerst. Auf dem Board steht, wie viele Aufgaben offen sind. Wenn du eine Aufgabe mit einem gemeinsam genutzten Projekt verknüpfst, wird dadurch nichts weiter geteilt: Dein Team sieht weiterhin nur Inhalte aus gemeinsam genutzten Nachrichten.

Einmal pro Woche sucht deine Machine nach Projekten, bei denen es ruhig geworden ist: Seit mindestens 10 Tagen gibt es nichts Neues, keine offene Aufgabe und kein offenes Versprechen. Bei höchstens drei Projekten fügt sie eine Aufgabe mit einem konkreten nächsten Schritt hinzu, zum Beispiel „Schick Sam das unterschriebene Bestellformular“, und verknüpft sie mit der Nachricht, aus der sie den Schritt abgeleitet hat. Findet sie keinen klaren nächsten Schritt, fügt sie keine Aufgabe hinzu. Verwirfst du einen Vorschlag, wird das Projekt vier Wochen lang nicht erneut vorgeschlagen.

## Organisation eines Projekts

Jedes Projekt kann mit einer Organisation verknüpft werden. Die Organisation wird auf der Projektseite, in der Liste und auf dem Board mit einem Link angezeigt.

Wenn niemand eine Organisation ausgewählt hat, ordnet deine Machine dem Projekt anhand der Personen und Nachrichten eine zu. Deine Kolleginnen und Kollegen lässt sie dabei außen vor. Das macht sie nur, wenn klar ist, wer die andere Seite ist: Persönliche E-Mail-Adressen wie Gmail zählen nie, und bei Projekten mit mehreren Unternehmen bleibt die Organisation leer. Im Projektformular steht dann „Aus seinen Personen“.

Sie wartet außerdem, bis du jemandem bei dieser Organisation geschrieben oder die Person getroffen hast. So wird einem Projekt nicht die Organisation einer fremden Person zugeordnet, nur weil sie dir eine E-Mail geschickt hat.

Bei einer weiteren Prüfung wird die Organisation mit dem Projektthema abgeglichen. Eine Organisation, bei der lediglich jemand aus dem Projekt arbeitet, etwa der Arbeitgeber eines Freundes bei einem Konzert, wird entfernt.

Deine Auswahl unter **Bearbeiten** bleibt immer bestehen, auch wenn du die Organisation entfernst. Mit **Gleiche Organisation wie…** ziehen die Projekte einer Organisation mit um, und mit **Abtrennen** kehren sie zurück.

## Boards

Auf einem Board werden Projekte einer Art in Phasen organisiert, etwa eine Evaluierungs-Pipeline. Über **⋯** auf einem Board kannst du **Board bearbeiten** (Name, Phasen und zugehörige Projekte), **Auf diesem Board öffnen** und **Neues Board** auswählen.

Prüfungen fügen passende Projekte hinzu und ordnen sie einer Phase zu. Wenn sie unsicher sind, zeigt das Board „2 Projekte könnten hierher gehören“ an: **Hinzufügen** oder **Auslassen**. Wähle einzelne Projekte oder **Alle auswählen**, um mehrere auf einmal zu bearbeiten. Falls du es dir anders überlegst, kannst du direkt danach **Rückgängig** wählen. Wird ein Projekt mit mehreren Gegenparteien hinzugefügt, entsteht für jede Gegenpartei ein eigenes Projekt.

Ein neues Board oder ein gespeichertes Board aus den Vorschlägen durchsucht einmal deinen gesamten Verlauf. Es erstellt für jede passende Organisation ein Projekt und ordnet es einer Phase zu. Währenddessen steht in der Kopfzeile „Dein Verlauf wird durchsucht…“. Anschließend wird angezeigt, wie viele Projekte hinzugefügt wurden und wie viele noch auf dich warten. Bei einem Board mit „Nur du“ bleibt alles Gefundene bei dir.

Mit **Nachfassen…** im **⋯** eines Boards wird automatisch nachgefasst, wenn jemand nicht antwortet. Mehr dazu unter [Nachfassen](follow-ups.md).

## Fertig, wenn

Unter **Bearbeiten** eines beliebigen Projekts, auf einem Board oder nicht, kannst du mit **Fertig, wenn** in einfachen Worten festlegen, woran man erkennt, dass es abgeschlossen ist: **Eine Live-Seite** (The Machine öffnet den Link aus der Nachricht und prüft, ob dort auf dich verwiesen wird) oder **Ihre Nachricht**. Für Partner-Listings schlagen Prüfungen eine Option vor.

Eine Prüfung verschiebt ein Projekt nur dann mit dem entsprechenden Nachweis, der auf der Projektseite verlinkt ist, in die letzte Phase. Ist das Projekt keinem Board zugeordnet, wird es stattdessen als erledigt markiert. Im **⋯** unter „Kürzliche Änderungen“ kannst du das mit **Rückgängig** rückgängig machen.

Änderst du später **Fertig, wenn** und ein erledigtes Projekt erfüllt den neuen Nachweis nicht mehr, wird es wieder geöffnet. Die zugehörige Aufgabe wird ebenfalls angepasst. **Erledigt** oder **Gewonnen** kannst du weiterhin manuell auswählen. Auf der Projektseite wird außerdem angezeigt, was es aufhält, zum Beispiel eine Antwort, die seit mehr als 10 Tagen aussteht, oder ein überfälliges Versprechen. Wenn es noch keine Aufgabe dafür gibt, wird eine hinzugefügt. Die Prüfung findet an jedem Arbeitstag statt, auch wenn keine neuen Nachrichten eingegangen sind. Ohne dich wird nichts verschickt.

## Pipeline

**Pipeline** oben auf einem Board zeigt für jede Phase den Gesamtwert der offenen Projekte sowie den voraussichtlichen Abschlusswert pro Monat anhand der jeweiligen Abschlussdaten. Gewonnene, verlorene und ins Stocken geratene Projekte gelten nicht als offen. Was du diesen Monat gewonnen hast, wird separat angezeigt.

Die Werte werden in Euro angezeigt, sofern für deine Machine nicht eine andere Währung festgelegt ist. Ist im Filter **Inhaber** ausgewählt, werden nur deine Projekte gezählt.

## Board eines Teammitglieds

Unter **Team** werden die Boards angezeigt, die deine Teammitglieder mit dir teilen. Die Boards mit den meisten deiner Projekte stehen zuerst. In der Kopfzeile siehst du, wem das Board gehört und mit wem es geteilt wird: mit dem ganzen Team („Adas Board, mit dem Team geteilt“) oder nur mit ausgewählten Teammitgliedern („Ada hat dieses Board mit dir geteilt“).

Bei jedem Projekt steht mit Datum, was zuletzt passiert ist: die neueste mit dem Team geteilte Zeile oder, falls später, die letzte Verschiebung. Auf einem Board mit Projekten von mehreren Teammitgliedern steht am Ende der Zeile, wem das Projekt gehört („von Ada“).

Auf dem Board eines Teammitglieds können weniger Projekte stehen, als die Person selbst sieht: Ein Projekt, das sie privat hält oder das eine persönliche Unterhaltung enthält, verlässt ihre Machine nicht. Personen, die für sie als privat markiert sind, erscheinen nicht in den geteilten Projekten. Auf deinem eigenen Board steht in der Kopfzeile „Mit dem Team geteilt“ und wie viele Projekte nur für dich sichtbar bleiben. Diese Projekte sind mit einem Schloss gekennzeichnet.

Mit **Meine**, **Wartet auf mich** und **Alle** legst du fest, welche Projekte ein geteiltes Board und die zugehörige Projektliste unter Team anzeigen. **Meine** zeigt Projekte, an denen du beteiligt bist: über einen Thread, als Projektinhaberin oder mit einer eigenen Aufgabe dazu. **Wartet auf mich** zeigt Projekte, bei denen etwas von dir erwartet wird: eine offene Aufgabe dazu oder ein Thread, in dem die neueste Nachricht an dich gerichtet war.

Jedes Projekt sieht genauso aus wie auf dem Board der Person, der es gehört, und steht an derselben Stelle: mit Organisation, Tagen in der Phase, nächstem Schritt und „Keine Antwort seit N Tagen“. Ein nächster Schritt oder Grund aus einer Nachricht, die nur diese Person sehen kann, wird nicht angezeigt. Der Rest einer Phase wird unter **N weitere anzeigen** eingeklappt. Nichts davon ändert, was geteilt wird.

Auf jedem Board wird bei einem Projekt, das nach dem Board benannt ist, der Boardname nicht angezeigt („Listings: Acme“ wird auf Listings als „Acme“ angezeigt).
