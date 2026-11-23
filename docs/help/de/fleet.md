---
title: Fleets
area: fleet
summary: Eine Work Fleet für dein Team, eine Family Fleet für Zuhause. Machines, die sich nach deinen Freigaberegeln gegenseitig helfen.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: f75a79e685f3a0cc
---
Mit einer Fleet kann deine Machine über The Machine Network mit den Machines deines Teams, deiner Familie oder deiner Freunde zusammenarbeiten. Was sie einander mitteilen, ist Ende-zu-Ende-verschlüsselt. Deine Machine antwortet nur nach deinen Regeln.

## Arten von Fleets

- **Work Fleet**: für dein Team. Übergib Arbeit, frag, **wer jemanden kennt**, lass Kontakte vermitteln und erhalte ein Team-Briefing.
- **Family Fleet**: für bis zu 6 Personen. Seht, wann alle Zeit haben, teilt Aufgaben und Pläne und stellt den Machines der anderen Fragen. Kostenlos. Gehostete Machines darin gibt es zum Familientarif. Mehr dazu unter [Familie](family.md).
- **Freunde**: einzelne Personen auf The Machine. Kostenlos. Mehr dazu unter [Freunde](friends.md).

## Der Fleet-Tab

Er wird angezeigt, sobald du einer Fleet beigetreten bist. Für jede Fleet gibt es einen Bereich, danach folgen Freunde, Network, Teilen und Aktivität. Inhaber und Admins sehen außerdem **Verwalten**. In einer Work Fleet, die ihren Graph teilt, gibt es zusätzlich **Was geteilt wird**.

## Kosten, Fleet verlassen und eine Fleet starten

Unter dem Namen jeder Fleet zeigt **Was sie kostet** ihre Plätze, wer deine Machine bezahlt und für den Inhaber die Karte und Rechnungen der Fleet. Mit **Diese Fleet verlassen** verlässt du sie. Der Inhaber muss die Fleet zuerst an jemand anderen übergeben. Mit **Weitere Fleet starten** startest du eine neue Fleet.

Jede Option öffnet den entsprechenden Bereich deines Kontos. Bei einer Preisänderung wird dir zuerst der Betrag zur Bestätigung angezeigt. Bei einer selbst gehosteten Machine öffnen sich die Optionen in einem neuen Tab in deinem Konto, wo du dich anmeldest.

## Frag deine Fleet

Frag im Fleet-Tab „Wer kennt jemanden bei Acme?“ oder wähl bei einer Organisation im [Graph](graph.md) **Die Fleet fragen**. Die Machine jedes Teammitglieds antwortet nach den eigenen Freigaberegeln und fragt die Person zuerst, wenn die Regel das vorsieht.

Für alles andere kannst du im Bereich deiner Work Fleet **Frag irgendwas** nutzen. Jedes Teammitglied erhält einen Antwortentwurf aus den eigenen Arbeitskonten. Es wird nichts zurückgeschickt, bevor die Person ihn sendet.

## Automatische Antworten in einer Work Fleet

In einer Standard Work Fleet beantwortet deine Machine drei Arten von Fragen aus dem Team automatisch: **wer jemanden kennt**, **Meeting-Kontext** („Wer ist dieser Gast?“) und **wer geteilte E-Mails bearbeitet**. Sie nutzt nur Informationen, die der [Team Graph](team-graph.md) bereits mit deinem Team teilt, niemals private, persönliche oder sensible Unterhaltungen. Jede Antwort erscheint im Fleet-Tab unter **Aktivität**.

Um eine Antwortart zu stoppen, stell sie unter **Teilen** auf **Nie**. Eine auf **Erst mich fragen** gesetzte Regel gilt wie **Immer**. Solange das Teilen des Team Graph deaktiviert ist, fragt deine Machine dich zuerst, wenn es darum geht, wer jemanden kennt oder um Meeting-Kontext.

In Work Fleets mit vorsichtigen Freigaben, bei Friends und in Family Fleets fragt deine Machine weiterhin zuerst. Für persönliche Kontaktvermittlungen, Übergaben und kostenlose Fragen gelten weiterhin die jeweiligen Regeln.

## Erkenntnisse des Teams

Deine Machine hält fest, wie dein Team arbeitet. Dazu nutzt sie Unterhaltungen mit Kunden, die der Team Graph bereits teilt, höchstens einmal am Tag. Zum Beispiel: „Rückerstattungsanfragen werden über den Support-Posteingang mit der Rückerstattungsvorlage beantwortet.“ Die Erkenntnisse erscheinen im Bereich deiner Work Fleet unter **Erkenntnisse des Teams** und sind für alle in der Fleet sichtbar. Jede wird außerdem unter **Aktivität** protokolliert. Niemand wird vorher gefragt.

- Nur Unterhaltungen, an denen jemand aus deinem Team beteiligt war. Niemals private, persönliche oder sensible Unterhaltungen.
- Nur Erkenntnisse, die für mehrere Kunden gelten: ein Ablauf, ein Tool, ein Schreibstil oder wer für was zuständig ist. Niemals etwas über einen einzelnen Kunden, Feedback zu deinem eigenen Produkt oder Namen, Adressen, Zahlen oder Zitate.
- Erkenntnisse, bei denen sich deine Machine nicht sicher ist, werden verworfen.

Deine Machine berücksichtigt passende Erkenntnisse, wenn sie eine Work-Aufgabe für dieses Unternehmen erstellt. Deine eigenen Fakten, Regeln und Skills haben Vorrang. Persönliche Aufgaben verwenden diese Erkenntnisse nie. Bei einer Aufgabe, für die eine Erkenntnis verwendet wurde, steht das dabei, zum Beispiel: „Eine Erkenntnis des Teams wurde verwendet: Rückerstattungen werden über den Support-Posteingang verschickt.“ Wähl dort **Entfernen**, um sie aus der gesamten Fleet zu löschen.

Jede Person in der Fleet kann eine Erkenntnis **Entfernen**. Sie wird dann für alle gelöscht und nicht erneut erstellt. Um das zu verhindern, deaktiviere in den Einstellungen unter Sicherheit **Anbieten, Erkenntnisse zu teilen**. In Work Fleets mit vorsichtigen Freigaben werden keine Erkenntnisse geteilt.

## Team-Briefing

Wähl im Fleet-Tab unter **Teilen** für das Team-Briefing **Täglich** oder **Wöchentlich**. Deine Machine fragt dann die Machines deiner Teammitglieder nach Zahlen und Datumsangaben. Was deine Aufmerksamkeit braucht, erscheint unter Work in deinen Aufgaben: zum Beispiel ein Kunde, der auf ein Teammitglied wartet, ein Unternehmen, von dem es seit mindestens zwei Wochen nichts Neues gibt, zwei Personen aus dem Team, die dieselben Kontakte anschreiben, oder ein gemeinsames Meeting.

- Eine Aufgabe zeigt, auf wen sie wartet, seit wann, worum die Person gebeten hat und was auf dem Spiel steht, zum Beispiel ein laufendes Projekt. Gibt es nichts Konkretes zu berichten, bleibt der Punkt im Briefing und wird nicht zur Aufgabe.
- Das Unternehmen und die Teammitglieder sind mit ihren Seiten verknüpft. **Details** zeigt, was sie geschrieben haben (wähl den Eintrag, um ihn zu lesen), was auf dem Spiel steht, wer aus dem Team Kontakt hat und die letzten Unterhaltungen. Angezeigt werden nur Informationen, die der [Team Graph](team-graph.md) teilt.
- Steht das, was sie geschrieben haben, nur in den Mails eines Teammitglieds, steht in der Aufgabe, wen du fragen kannst.
- Mit **Das Team fragen** schickst du eine vorausgefüllte Frage dazu. Die Antworten erscheinen in der Aufgabe.
- **Nicht nötig** schließt die Aufgabe. Das Briefing merkt sich deine Auswahl und zeigt sie nur wieder an, wenn es etwas Neues gibt.
- Wenn jemand antwortet oder die Aufgabe übernimmt, wird sie automatisch geschlossen. Eine Aufgabe zu einem Unternehmen, für das du bereits eine Aufgabe hast, wird dieser Aufgabe hinzugefügt.

## Briefing-Anfragen

Jeden Morgen fragt ein Teammitglied mit aktiviertem Team-Briefing deine Machine nach Zahlen und Datumsangaben. In einer Work Fleet antwortet deine Machine automatisch, aber nur mit Informationen, die der [Team Graph](team-graph.md) bereits teilt. Solange das Teilen des Team Graph deaktiviert ist, antwortet sie nicht. Jede Antwort erscheint im Fleet-Tab unter **Aktivität**, niemals als Aufgabe oder Benachrichtigung.

Um das zu stoppen, deaktiviere im Fleet-Tab unter **Teilen** die Option **Meine Kurzfakten mit dem Team teilen**. In den Briefings der anderen wirst du dann als Person aufgeführt, die nicht geantwortet hat.

In einer Fleet mit vorsichtigen Freigaben warten Anfragen im Fleet-Tab unter **Briefing-Anfragen** auf dich. Du kannst **Einmal teilen**, **Immer teilen**, **Ablehnen** oder **Nie** wählen. Es wird nichts geteilt, bevor du dich entscheidest. Nicht beantwortete Anfragen laufen ab.

## Team Graph

In einer Work Fleet wird Kundenarbeit mit deinem Team geteilt, nachdem du sie geprüft hast. Mehr dazu unter [Team Graph](team-graph.md).

## Geteilte Verbindungen

Ein Inhaber oder Admin kann Stripe oder Intercom einmal verbinden und im Fleet-Tab unter **Geteilte Verbindungen** mit dem Team teilen. Teammitglieder können die Verbindung ansehen, aber nicht ändern. Sie sehen auch, wer sie geteilt hat. Nur Admins können sie ändern oder die Freigabe beenden. Mehr dazu unter [Stripe](stripe.md) und [Intercom](intercom.md).

## Was deine Machine beantwortet

Lege das für jede Fleet im Bereich Teilen fest. Mehr dazu unter [Freigaberegeln](sharing-rules.md). Unter **Einstellungen** gibt es eine Verknüpfung zu **Fleet-Regeln**.

## Anmeldung mit dem Unternehmenskonto

Erlaube Teammitgliedern, mit ihrem Unternehmenskonto beizutreten. In einer gehosteten Work Fleet kann ein Inhaber oder Admin, der mit Google Workspace oder Microsoft 365 angemeldet ist, auf der Kontoseite **Unternehmensanmeldung** aktivieren.

Teammitglieder, die sich mit der Unternehmensdomain anmelden, sehen **Beitritt anfragen**. Ein Inhaber oder Admin muss jede Anfrage **Freigeben**. Private Gmail- und Outlook.com-Konten zählen nicht.

Wenn du jemanden aus der Fleet entfernst, wird die Person überall abgemeldet.

Wie du einer Fleet beitrittst, eine startest oder eine Machine auf deinem eigenen Computer koppelst, erfährst du unter [Tarife und Abrechnung](plans-and-billing.md) und [Freunde und das Network](friends.md).

## Für Inhaber und Admins

Unter **Verwalten** im Fleet-Tab findest du alle Fleets, die du verwaltest, mit ihren Mitgliedern, Rollen und Einladungen. Bei einer gehosteten Machine kannst du dort Personen einladen, Rollen ändern, Personen entfernen und Beitrittsanfragen beantworten. Änderungen, die sich auf den Preis auswirken, öffnen zuerst dein Konto zur Bestätigung. Bei einer selbst gehosteten Machine siehst du, wer dazugehört, und findest einen Link zu den Einstellungen der Fleet in deinem Konto. Dort verwaltest du Mitglieder und Einladungen.

**Fleet-Einstellungen** findest du unter dem Namen jeder Fleet in ihrem Bereich und unter Verwalten. Sie öffnen die Einstellungen dieser Fleet in deinem Konto. Dort findest du geteilte Verbindungen, Sicherheit, die Unternehmensanmeldung, die Einstellungen dazu, welche Machine antwortet, und diese beiden Optionen:

- **Kürzlich entfernt**: zeigt alle Personen, die entfernt wurden oder die Fleet verlassen haben. „Entfernt, bestätigt“ bedeutet, dass ihre Machine die Arbeitsdaten gelöscht hat und die Person überall abgemeldet ist. Bis dahin steht dort **Ausstehend** mit einer Begründung.
- **Aktivität**: zeigt, wer was und wann getan hat, darunter Einladungen, Beitritte, Entfernungen, Rollen, gehostete Machines, Abrechnung, geteilte Verbindungen und Freigaben. Auch jeder Zugriff unseres Supportteams auf den Bericht oder die Protokolle einer Machine wird erfasst. Nachrichteninhalte werden nie erfasst. Mit **CSV herunterladen** kannst du die Daten exportieren. Sie werden 12 Monate lang gespeichert.

Für den Inhaber: **Vor dem Start der Machine eines Mitglieds fragen**. Ist die Option aktiviert, wartet die Machine eines neuen Mitglieds auf deine Zustimmung, auch in einer kostenlosen Fleet. Ist sie deaktiviert, startet die Machine in einer kostenlosen Fleet sofort und du wirst benachrichtigt. Bei einer kostenpflichtigen Machine musst du den Betrag immer erst bestätigen.

Nach **Nicht mehr teilen** steht bei einer geteilten Verbindung „Entfernt, bestätigt“, sobald alle Machines den Zugriff darauf verloren haben.
