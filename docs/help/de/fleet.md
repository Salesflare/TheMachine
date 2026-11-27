---
title: Fleets
area: fleet
summary: Eine Work Fleet für dein Team, eine Family Fleet für zu Hause. Machines, die sich gegenseitig helfen, nach deinen Regeln fürs Teilen.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 17927ccd0e4aa40d
---
Mit einer Fleet kann deine Machine über The Machine Network mit den Machines deines Teams, deiner Familie oder deiner Freunde zusammenarbeiten. Alles, was sie einander mitteilen, ist Ende-zu-Ende-verschlüsselt. Deine Machine antwortet nur nach deinen Regeln.

## Arten von Fleets

- **Work Fleet**: dein Team. Übergib Arbeit, frag, **wer jemanden kennt**, lass dich vorstellen und erhalte ein Team-Briefing.
- **Family Fleet**: bis zu 6 Personen. Wenn alle Zeit haben, könnt ihr Aufgaben und Pläne teilen und die Machine der anderen fragen. Kostenlos. Für gehostete Machines in der Fleet gilt ein Familientarif. Siehe [Familie](family.md).
- **Freunde**: beliebige Personen auf The Machine, einzeln. Kostenlos. Siehe [Freunde](friends.md).

## Der Fleet-Tab

Er wird angezeigt, sobald du einer Fleet beigetreten bist. Für jede Fleet gibt es einen eigenen Bereich, danach kommen Freunde, Network, Teilen und Aktivität. Inhaber und Admins sehen auch **Verwalten**. Wenn eine Work Fleet ihren Graph teilt, gibt es zusätzlich **Was geteilt wird**.

## Kosten, Fleet verlassen und eine Fleet starten

Unter dem Namen jeder Fleet zeigt **„Was sie kostet“** die Plätze, wer für deine Machine zahlt und, für den Inhaber, die Karte und Rechnungen der Fleet. Mit **„Diese Fleet verlassen“** verlässt du sie. Ein Inhaber muss die Fleet vorher an jemand anderen übergeben. Mit **„Weitere Fleet starten“** startest du eine neue Fleet.

Jede Option öffnet den entsprechenden Bereich deines Kontos. Bei einer Preisänderung wird dir der Betrag zuerst zur Bestätigung angezeigt. Auf einer selbst gehosteten Machine öffnet sich dein Konto in einem neuen Tab, in dem du dich anmeldest.

## Frag deine Fleet

Frag im Fleet-Tab „wer jemanden bei Acme kennt“ oder wähl bei einer Organisation im [Graph](graph.md) **„Fleet fragen“**. Die Machine jedes Teammitglieds antwortet nach den eigenen Regeln fürs Teilen und fragt die Person zuerst, wenn die Regel das vorsieht.

Für alles andere kannst du im Bereich deiner Work Fleet **Frag irgendwas** nutzen. Jedes Teammitglied erhält einen Entwurf, der auf den eigenen Arbeitskonten basiert. Nichts wird zurückgesendet, bevor die Person es abschickt. Der Entwurf berücksichtigt nur, was die Person geschrieben oder besprochen hat. Eingegangene Nachrichten, die sie nicht selbst geschrieben hat, etwa ein Newsletter oder eine CC, werden zwar als gefunden angezeigt, aber fließen in keinen Entwurf ein.

## Automatische Antworten in einer Work Fleet

In einer Standard-Work-Fleet beantwortet deine Machine drei Arten von Fragen aus dem Team automatisch: **wer jemanden kennt**, **Meeting-Kontext** („Wer ist dieser Gast?“) und **wer geteilte E-Mails bearbeitet**. Sie verwendet nur Informationen, die der [Team Graph](team-graph.md) bereits mit deinem Team teilt, niemals private, persönliche oder vertrauliche Unterhaltungen. Jede Antwort wird im Fleet-Tab unter **Aktivität** angezeigt.

Um automatische Antworten für eine dieser Fragen zu stoppen, stell sie unter **Teilen** auf **Nie**. Eine Regel mit **Erst mich fragen** funktioniert wie **Immer**. Solange das Teilen über Team Graph deaktiviert ist, fragt die Machine bei Fragen dazu, wer jemanden kennt, und zum Meeting-Kontext zuerst dich.

In sorgfältig konfigurierten Work Fleets, bei Freunde und in Family Fleets fragt die Machine weiterhin zuerst dich. Für persönliche Vorstellungen, Übergaben und kostenlose Fragen gelten eigene Regeln.

## Erkenntnisse des Teams

Deine Machine hält fest, wie dein Team arbeitet. Dafür nutzt sie Kundenunterhaltungen, die der Team Graph bereits teilt, und erstellt höchstens einmal täglich eine Erkenntnis. Zum Beispiel: „Rückerstattungen werden über den Support-Posteingang mit der Rückerstattungsvorlage bearbeitet.“ Die Erkenntnisse werden im Bereich deiner Work Fleet unter **Erkenntnisse des Teams** angezeigt und sind für alle in der Fleet sichtbar. Jede wird auch unter **Aktivität** protokolliert. Niemand wird vorher gefragt.

- Nur Unterhaltungen, an denen jemand aus deinem Team beteiligt war. Niemals private, persönliche oder vertrauliche Unterhaltungen.
- Nur Erkenntnisse, die auf mehrere Kunden zutreffen: ein Ablauf, ein Tool, ein Schreibstil oder wer was bearbeitet. Niemals etwas über einen einzelnen Kunden, Feedback zu deinem eigenen Produkt oder Namen, Adressen, Zahlen oder Zitate.
- Erkenntnisse, bei denen sich die Machine nicht sicher ist, werden verworfen.

Deine Machine verwendet passende Erkenntnisse, wenn sie eine Arbeitsaufgabe für dieses Unternehmen vorbereitet. Deine eigenen Fakten, Regeln und Skills haben Vorrang. Für persönliche Aufgaben werden diese Erkenntnisse nie verwendet. Bei einer Aufgabe, die eine Erkenntnis nutzt, steht das dabei, zum Beispiel: „Teamerkenntnis verwendet: Rückerstattungen werden über den Support-Posteingang bearbeitet.“ Tippe dort auf **Entfernen**, um die Erkenntnis aus der gesamten Fleet zu löschen.

Jede Person in der Fleet kann eine Erkenntnis **„Entfernen“**: Sie ist dann für alle gelöscht und wird nicht erneut erstellt. Um das zu verhindern, deaktiviere unter Einstellungen und Sicherheit **„Anbieten, Erkenntnisse zu teilen“**. In sorgfältig konfigurierten Work Fleets werden keine Erkenntnisse erstellt.

## Team-Briefing

Wähl im Fleet-Tab unter **Teilen** für **Team-Briefing** die Option **Täglich** oder **Wöchentlich**. Deine Machine fragt dann die Machines deiner Teammitglieder nach Zahlen und Datumsangaben. Was deine Aufmerksamkeit erfordert, erscheint unter Arbeit bei den Aufgaben: ein Kunde wartet auf ein Teammitglied, ein Unternehmen hat seit mindestens zwei Wochen nichts von euch gehört, zwei von euch schreiben denselben Personen oder es gibt ein gemeinsames Meeting.

- Eine Aufgabe nennt, auf wen sie wartet, seit wann, worum die Person gebeten hat und was auf dem Spiel steht, zum Beispiel ein laufendes Projekt. Wenn es nichts Konkretes zu sagen gibt, bleibt der Punkt im Briefing und wird nicht zur Aufgabe.
- Das Unternehmen und die Teammitglieder sind mit ihren Seiten verknüpft. **Details** zeigt, was sie geschrieben haben (tippe darauf, um es zu lesen), worum es geht, wer aus dem Team Kontakt hat und die neuesten Unterhaltungen. Angezeigt werden nur Inhalte, die der [Team Graph](team-graph.md) teilt.
- Wenn das Geschriebene nur in den E-Mails eines Teammitglieds steht, nennt die Aufgabe, wen du fragen kannst.
- Über **Das Team fragen** wird eine vorausgefüllte Frage dazu gesendet. Die Antworten erscheinen in der Aufgabe.
- **Nicht nötig** schließt die Aufgabe ab und das Briefing lernt daraus. Sie erscheint nur wieder, wenn es etwas Neues gibt.
- Wenn jemand antwortet oder die Aufgabe übernimmt, wird sie automatisch geschlossen. Eine Aufgabe zu einem Unternehmen, für das du bereits eine Aufgabe hast, wird dieser Aufgabe hinzugefügt.

## Briefing-Anfragen

Jeden Morgen fragt die Machine eines Teammitglieds mit aktiviertem Team-Briefing deine Machine nach Zahlen und Datumsangaben. In einer Work Fleet antwortet deine Machine automatisch, aber nur mit Informationen, die der [Team Graph](team-graph.md) bereits teilt. Solange das Teilen über Team Graph deaktiviert ist, antwortet sie nicht. Jede Antwort wird im Fleet-Tab unter **Aktivität** angezeigt, niemals als Aufgabe oder Benachrichtigung.

Um das zu stoppen, deaktiviere im Fleet-Tab unter **Teilen** die Option **„Meine Kurzfakten mit dem Team teilen“**. Im Briefing der anderen wirst du dann als unbeantwortet aufgeführt.

In einer sorgfältig konfigurierten Fleet warten Anfragen im Fleet-Tab unter **Briefing-Anfragen** auf dich: **Einmal teilen**, **Immer teilen**, **Ablehnen** oder **Nie**. Es wird nichts geteilt, bevor du dich entscheidest. Nicht beantwortete Anfragen laufen ab.

## Team Graph

In einer Work Fleet werden Kundenprojekte mit deinem Team geteilt, nachdem du sie überprüft hast. Siehe [Team Graph](team-graph.md).

## Geteilte Verbindungen

Ein Inhaber oder Admin kann Stripe oder Intercom einmal verbinden und die Verbindung über **Geteilte Verbindungen** im Fleet-Tab mit dem Team teilen. Teammitglieder können die Verbindung ansehen, aber nicht ändern. Sie sehen auch, wer sie geteilt hat. Nur Admins können sie ändern oder beenden. Siehe [Stripe](stripe.md) und [Intercom](intercom.md).

## Was deine Machine beantwortet

Leg die Regeln für jede Fleet im Bereich „Teilen“ fest. Siehe [Freigaberegeln](sharing-rules.md). Unter **Einstellungen** findest du die Verknüpfung **Fleet-Regeln**.

## Anmeldung mit dem Unternehmenskonto

Erlaube Teammitgliedern, mit ihrem Unternehmenskonto beizutreten. In einer gehosteten Work Fleet kann ein Inhaber oder Admin, der mit Google Workspace oder Microsoft 365 angemeldet ist, auf der Kontoseite **Unternehmensanmeldung** aktivieren.

Teammitglieder, die sich mit der Unternehmensdomain anmelden, sehen **Beitritt anfragen**. Ein Inhaber oder Admin muss jede Anfrage **Freigeben**. Persönliche Gmail- und Outlook.com-Konten zählen nie.

Wenn du jemanden aus der Fleet entfernst, wird die Person überall abgemeldet.

Wie du einer Fleet beitrittst, eine startest oder eine Machine auf deinem eigenen Computer koppelst, erfährst du unter [Tarife und Abrechnung](plans-and-billing.md) und [Freunde und das Network](friends.md).

## Für Inhaber und Admins

Unter **Verwalten** im Fleet-Tab findest du jede Fleet, die du verwaltest, mit den Personen, ihren Rollen und den Einladungen. Auf einer gehosteten Machine kannst du Personen einladen, ihre Rollen ändern, sie entfernen und Beitrittsanfragen direkt dort beantworten. Wenn sich eine Änderung auf den Preis auswirkt, öffnet sich zuerst dein Konto zur Bestätigung. Auf einer selbst gehosteten Machine siehst du, wer zur Fleet gehört. Ein Link führt zu den Einstellungen dieser Fleet in deinem Konto, wo du Personen und Einladungen verwaltest.

**Fleet-Einstellungen** unter dem Namen jeder Fleet im jeweiligen Bereich und unter „Verwalten“ öffnet die Einstellungen der Fleet in deinem Konto. Dort findest du geteilte Verbindungen, Sicherheit, Unternehmensanmeldung, die Einstellungen dazu, welche Machine antwortet, und diese beiden Punkte:

- **Kürzlich entfernt**: alle Personen, die entfernt wurden oder die Fleet verlassen haben. „Entfernt, bestätigt“ bedeutet, dass ihre Machine die Arbeitsdaten gelöscht hat und sie überall abgemeldet sind. Bis dahin wird **Ausstehend** mit dem Grund angezeigt.
- **Aktivität**: wer was wann getan hat, darunter Einladungen, Beitritte, Entfernungen, Rollen, gehostete Machines, Abrechnung, geteilte Verbindungen und Freigaben. Außerdem jedes Mal, wenn unser Supportteam den Machine-Bericht oder die Protokolle eines Mitglieds gelesen hat. Nachrichteninhalte werden nie erfasst. Mit **CSV herunterladen** exportierst du die Daten. Sie werden 12 Monate lang aufbewahrt.

Für den Inhaber: Bei aktivierter Option **Vor dem Starten der Machine eines Mitglieds fragen** wartet die Machine eines neuen Mitglieds auf deine Freigabe, auch in einer kostenlosen Fleet. Ist die Option deaktiviert, startet die Machine in einer kostenlosen Fleet sofort, und du wirst benachrichtigt. Bei einer kostenpflichtigen Machine musst du den Betrag immer erst bestätigen.

Nach **Nicht mehr teilen** wird bei einer geteilten Verbindung „Entfernt, bestätigt“ angezeigt, sobald alle Machines den Zugriff darauf verloren haben.
