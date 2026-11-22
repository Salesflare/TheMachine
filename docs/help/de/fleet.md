---
title: Fleets
area: fleet
summary: Eine Work Fleet für dein Team, eine Family Fleet für zu Hause. Machines, die sich nach deinen Freigaberegeln gegenseitig helfen.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 974bbbb54608efc3
---
Mit einer Fleet kann deine Machine über The Machine Network mit den Machines deines Teams, deiner Familie oder deiner Freunde zusammenarbeiten. Alles, was sie einander mitteilen, ist Ende-zu-Ende-verschlüsselt. Deine Machine antwortet nur nach deinen Regeln.

## Fleet-Arten

- **Work Fleet**: dein Team. Übergib Aufgaben, frag, wer jemanden kennt, lass dir Kontakte vermitteln und bekomm ein Team-Briefing.
- **Family Fleet**: bis zu 6 Personen. Gemeinsame Aufgaben und Pläne, wenn alle Zeit haben. Kostenlos. Für gehostete Machines in der Fleet gilt ein Familienpreis. Siehe [Familie](family.md).
- **Freunde**: einzelne Personen auf The Machine. Kostenlos. Siehe [Friends](friends.md).

## Der Fleet-Tab

Er wird angezeigt, sobald du einer Fleet beigetreten bist. Für jede Fleet gibt es einen eigenen Bereich, danach folgen Freunde, Network, Teilen und Aktivität. Inhaber und Admins sehen auch **Verwalten**. Bei einer Work Fleet, die ihren Graph teilt, wird außerdem **Was geteilt wird** angezeigt.

## Kosten, Fleet verlassen und eine Fleet starten

Unter dem Namen jeder Fleet zeigt **Was sie kostet** die Plätze, wer für deine Machine bezahlt und für den Inhaber die Karte und Rechnungen der Fleet. Mit **Diese Fleet verlassen** verlässt du die Fleet. Als Inhaber musst du sie zuerst an jemand anderen übergeben. Mit **Weitere Fleet starten** startest du eine neue Fleet.

Jede Option öffnet den entsprechenden Bereich deines Kontos. Ändert sich der Preis, wird dir zuerst der Betrag zur Bestätigung angezeigt. Bei einer selbst gehosteten Machine wird dein Konto in einem neuen Tab geöffnet, in dem du dich anmeldest.

## Deine Fleet fragen

Frag im Fleet-Tab „wer jemanden bei Acme kennt“ oder wähl **Die Fleet fragen** bei einer Organisation im [Graph](graph.md). Die Machine jedes Teammitglieds antwortet nach den eigenen Freigaberegeln und fragt die Person zuerst, wenn die Regel das vorsieht.

Für alles andere kannst du **Frag irgendwas** im Bereich deiner Work Fleet verwenden. Jedes Teammitglied erhält einen Antwortentwurf aus den eigenen Arbeitskonten. Die Antwort wird erst weitergegeben, wenn das Teammitglied sie sendet.

## Automatische Antworten in einer Work Fleet

In einer Work Fleet mit der Stufe „Standard“ beantwortet deine Machine drei Arten von Fragen von Teammitgliedern automatisch: **wer jemanden kennt**, **Meeting-Kontext** („Wer ist dieser Gast?“) und **wer geteilte E-Mails bearbeitet**. Sie verwendet nur Informationen, die der [Team Graph](team-graph.md) bereits mit deinem Team teilt, niemals private, persönliche oder sensible Unterhaltungen. Jede Antwort wird im Fleet-Tab unter **Aktivität** angezeigt.

Um eine davon zu stoppen, stell sie unter **Teilen** auf **Nie**. Eine Regel mit der Einstellung **Erst mich fragen** funktioniert wie **Immer**. Wenn das Teilen über den Team Graph deaktiviert ist, fragt deine Machine dich zuerst, wenn jemand wissen möchte, wer jemanden kennt oder nach dem Meeting-Kontext.

In vorsichtigen Work Fleets, bei Freunden und in Family Fleets fragt deine Machine weiterhin zuerst. Für Kontaktvermittlungen, Übergaben und kostenlose Fragen gelten weiterhin die jeweiligen eigenen Regeln.

## Erkenntnisse des Teams

Deine Machine hält fest, wie dein Team arbeitet. Dafür nutzt sie Kundenunterhaltungen, die der Team Graph bereits teilt, höchstens einmal am Tag. Zum Beispiel: „Rückerstattungsanfragen werden vom Support-Posteingang aus mit der Rückerstattungsvorlage beantwortet.“ Die Erkenntnisse werden im Bereich deiner Work Fleet unter **Erkenntnisse des Teams** angezeigt, wo sie für alle in der Fleet sichtbar sind. Jede Erkenntnis wird außerdem unter **Aktivität** protokolliert. Niemand wird vorher gefragt.

- Nur Unterhaltungen, an denen jemand aus deinem Team mitgeschrieben hat. Niemals private, persönliche oder sensible Unterhaltungen.
- Nur Dinge, die für mehrere Kunden gelten: ein Ablauf, ein Tool, ein Schreibstil oder wer wofür zuständig ist. Niemals etwas über einen einzelnen Kunden, Feedback zu deinem eigenen Produkt oder Namen, Adressen, Zahlen oder Zitate.
- Erkenntnisse, bei denen sich deine Machine nicht sicher ist, werden verworfen.

Deine Machine nutzt passende Erkenntnisse, wenn sie eine Arbeitsaufgabe für dieses Unternehmen erstellt. Deine eigenen Fakten, Regeln und Skills haben Vorrang. Für persönliche Aufgaben werden Erkenntnisse des Teams nie verwendet. Bei einer Aufgabe, für die eine Erkenntnis genutzt wurde, steht das dabei, zum Beispiel: „Teamerkenntnis verwendet: Rückerstattungen werden vom Support-Posteingang aus verschickt.“ Tippe dort auf **Entfernen**, um die Erkenntnis aus der gesamten Fleet zu löschen.

Alle in der Fleet können eine Erkenntnis **Entfernen**. Sie ist dann für alle gelöscht und wird nicht erneut erstellt. Um das zu verhindern, deaktiviere unter Einstellungen und Sicherheit **Anbieten, Erkenntnisse zu teilen**. In vorsichtigen Work Fleets werden keine Erkenntnisse geteilt.

## Team-Briefing

Wähl im Fleet-Tab unter **Teilen** für das **Team-Briefing** **Täglich** oder **Wöchentlich** aus. Deine Machine fragt dann die Machines deiner Teammitglieder nach Zahlen und Daten. Was deine Aufmerksamkeit braucht, erscheint unter Arbeit bei den Aufgaben: ein Kunde wartet auf ein Teammitglied, ein Unternehmen hat seit mindestens zwei Wochen nichts von sich hören lassen, zwei von euch schreiben denselben Personen oder es gibt ein gemeinsames Meeting.

- Eine Aufgabe nennt, auf wen sie wartet, seit wann, worum die Person gebeten hat und was auf dem Spiel steht, zum Beispiel ein offenes Projekt. Wenn es nichts Konkretes zu sagen gibt, bleibt der Punkt im Brief und wird nicht zu einer Aufgabe.
- Unternehmen und Teammitglieder sind mit ihren Seiten verknüpft. Unter **Details** siehst du, was sie geschrieben haben (tippe darauf, um es zu lesen), was auf dem Spiel steht, wer aus dem Team Kontakt hat und welche Unterhaltungen zuletzt geführt wurden. Angezeigt werden nur Informationen, die der [Team Graph](team-graph.md) teilt.
- Wenn das Geschriebene nur in den E-Mails eines Teammitglieds steht, nennt die Aufgabe die Person, die du fragen kannst.
- Über **Das Team fragen** wird eine vorausgefüllte Frage dazu gesendet. Die Antworten erscheinen bei der Aufgabe.
- **Nicht nötig** schließt die Aufgabe und der Brief lernt daraus. Sie erscheint nur wieder, wenn es etwas Neues gibt.
- Wenn jemand antwortet oder die Aufgabe übernimmt, wird sie automatisch geschlossen. Eine Aufgabe zu einem Unternehmen, für das du bereits eine Aufgabe hast, wird dieser Aufgabe hinzugefügt.

## Brief-Anfragen

Ein Teammitglied, das das Team-Briefing aktiviert hat, fragt deine Machine jeden Morgen nach Zahlen und Daten. In einer Work Fleet antwortet deine Machine automatisch. Sie verwendet nur Informationen, die der [Team Graph](team-graph.md) bereits teilt, und antwortet nicht, solange das Teilen über den Team Graph deaktiviert ist. Jede Antwort wird im Fleet-Tab unter **Aktivität** angezeigt, niemals als Aufgabe oder Benachrichtigung.

Um das zu stoppen, deaktiviere im Fleet-Tab unter **Teilen** die Option **Meine Kurzfakten mit dem Team teilen**. Im Team-Briefing wird dann angezeigt, dass du nicht geantwortet hast.

In einer vorsichtigen Fleet warten die Anfragen im Fleet-Tab unter **Briefing-Anfragen** auf dich. Wähl **Einmal teilen**, **Immer teilen**, **Ablehnen** oder **Nie**. Es wird nichts geteilt, bevor du dich entscheidest. Unbeantwortete Anfragen laufen ab.

## Team Graph

In einer Work Fleet werden Kundenprojekte mit deinem Team geteilt, nachdem du sie geprüft hast. Siehe [Team Graph](team-graph.md).

## Geteilte Verbindungen

Ein Inhaber oder Admin kann Stripe oder Intercom einmal verbinden und die Verbindung über **Geteilte Verbindungen** im Fleet-Tab mit dem Team teilen. Teammitglieder können die Verbindung lesen, aber nicht ändern. Sie sehen, wer sie geteilt hat. Nur Admins können sie ändern oder beenden. Siehe [Stripe](stripe.md) und [Intercom](intercom.md).

## Was deine Machine beantwortet

Leg das für jede Fleet einzeln im Bereich Teilen fest. Siehe [Freigaberegeln](sharing-rules.md). Unter **Einstellungen** gibt es eine Verknüpfung zu **Fleet-Regeln**.

## Anmeldung mit dem Firmenkonto

Erlaube Teammitgliedern, mit ihrem Firmenkonto beizutreten. In einer gehosteten Work Fleet kann ein Inhaber oder Admin, der mit Google Workspace oder Microsoft 365 angemeldet ist, auf der Kontoseite **Firmenanmeldung** aktivieren.

Teammitglieder, die sich mit der Domain der Firma anmelden, sehen **Um Beitritt bitten**. Ein Inhaber oder Admin muss jede Anfrage **Freigeben**. Private Gmail- und Outlook.com-Konten zählen nicht.

Wenn du jemanden aus der Fleet entfernst, wird die Person überall abgemeldet.

Informationen zum Beitreten oder Starten einer Fleet oder zum Koppeln einer Machine auf deinem eigenen Computer findest du unter [Tarife und Abrechnung](plans-and-billing.md) und [Freunde und das Network](friends.md).

## Für Inhaber und Admins

Unter **Verwalten** im Fleet-Tab werden alle Fleets angezeigt, die du verwaltest, mit den Personen, ihren Rollen und den Einladungen. Bei einer gehosteten Machine kannst du dort Personen einladen, Rollen ändern, Personen entfernen und Beitrittsanfragen beantworten. Wenn sich dadurch der Preis ändert, wird zuerst dein Konto zur Bestätigung geöffnet. Bei einer selbst gehosteten Machine siehst du, wer dabei ist, sowie einen Link zu den Einstellungen dieser Fleet in deinem Konto, wo du Personen und Einladungen verwaltest.

**Fleet-Einstellungen** findest du unter dem Namen jeder Fleet in ihrem Bereich und unter Verwalten. Damit öffnest du die Einstellungen der Fleet in deinem Konto: geteilte Verbindungen, Sicherheit, Firmenanmeldung, welche Machine antwortet und diese beiden Optionen:

- **Kürzlich entfernt**: alle Personen, die entfernt wurden oder gegangen sind. „Entfernt, bestätigt“ bedeutet, dass ihre Machine die Arbeitsdaten gelöscht hat und die Person überall abgemeldet ist. Bis dahin steht dort **Ausstehend** mit einer Begründung.
- **Aktivität**: wer was wann getan hat: Einladungen, Beitritte, Entfernungen, Rollen, gehostete Machines, Abrechnung, geteilte Verbindungen und Freigaben. Außerdem jedes Mal, wenn unser Supportteam den Machine-Bericht oder die Protokolle eines Mitglieds gelesen hat. Keine Nachrichteninhalte. Über **CSV herunterladen** kannst du die Daten exportieren. Sie werden 12 Monate lang gespeichert.

**Mich fragen, bevor die Machine eines Mitglieds gestartet wird** ist eine Option für den Inhaber. Wenn sie aktiviert ist, wartet die Machine eines neuen Mitglieds auf deine Zustimmung, auch in einer kostenlosen Fleet. Ist sie deaktiviert, startet die Machine in einer kostenlosen Fleet sofort und du wirst benachrichtigt. Eine kostenpflichtige Machine wartet immer auf deine Bestätigung des Betrags.

Nachdem du **Nicht mehr teilen** gewählt hast, wird bei einer geteilten Verbindung „Entfernt, bestätigt“ angezeigt, sobald keine Machine mehr darauf zugreifen kann.
