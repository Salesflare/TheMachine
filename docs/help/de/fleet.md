---
title: Fleets
area: fleet
summary: Eine Work Fleet für dein Team, eine Family Fleet für zu Hause. Machines, die sich gegenseitig helfen, nach deinen Regeln zum Teilen.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: c9650fc4ffe00e16
---
Mit einer Fleet kann deine Machine über The Machine Network mit den Machines deines Teams, deiner Familie oder deiner Freunde zusammenarbeiten. Was sie einander mitteilen, ist Ende-zu-Ende-verschlüsselt, und deine Machine antwortet nur nach deinen Regeln.

## Arten von Fleets

- **Work Fleet**: dein Team. Gib Arbeit weiter, frag, **wer jemanden kennt**, lass Kontakte herstellen und erhalte ein Team-Briefing.
- **Family Fleet**: bis zu 6 Personen. Wenn alle Zeit haben, könnt ihr Aufgaben und Pläne teilen. Kostenlos. Siehe [Familie](family.md).
- **Freunde**: einzelne Personen auf The Machine. Kostenlos. Siehe [Freunde](friends.md).

## Der Fleet-Tab

Er wird angezeigt, sobald du einer Fleet beigetreten bist. Für jede Fleet gibt es einen Bereich sowie Bereiche für Family, Freunde, Network, Teilen und Aktivität.

## Was sie kostet, Fleet verlassen und eine Fleet starten

Unter dem Namen jeder Fleet zeigt **Was sie kostet** die Plätze, wer für deine Machine bezahlt und für den Inhaber die Karte und Rechnungen der Fleet. Mit **Diese Fleet verlassen** verlässt du sie. Als Inhaber musst du sie zuerst jemand anderem übergeben. Mit **Weitere Fleet starten** startest du eine neue Fleet.

Jede Option öffnet den entsprechenden Bereich deines Kontos. Wenn sich der Preis ändert, wird dir der Betrag zuerst zur Bestätigung angezeigt. Auf einer selbst gehosteten Machine öffnen sich deine Kontoeinstellungen in einem neuen Tab, in dem du dich anmeldest.

## Frag deine Fleet

Frag im Fleet-Tab „wer jemanden bei Acme kennt“ oder wähle bei einer Organisation im [Graph](graph.md) **Fleet fragen**. Die Machine jeder Teamkollegin und jedes Teamkollegen antwortet nach den eigenen Regeln zum Teilen und fragt vorher, wenn die Regel das vorsieht.

## Antworten in einer Work Fleet

In einer Standard-Work-Fleet beantwortet deine Machine drei Arten von Fragen aus dem Team selbst: **wer jemanden kennt**, **Meeting-Kontext** („Wer ist dieser Gast?“) und **wer geteilte E-Mails bearbeitet**. Sie nutzt nur Informationen, die der [Team Graph](team-graph.md) bereits mit deinem Team teilt, niemals private, persönliche oder sensible Unterhaltungen. Jede Antwort erscheint im Fleet-Tab unter **Aktivität**.

Um eine dieser Antworten zu stoppen, stell sie unter **Teilen** auf **Nie**. Eine Regel mit der Einstellung **Erst mich fragen** gilt wie **Immer**. Solange das Teilen im Team Graph ausgeschaltet ist, fragt deine Machine dich vorher, wenn jemand wissen möchte, wer jemanden kennt oder nach Meeting-Kontext fragt.

In sorgfältigen Work Fleets, bei Freunden und in Family Fleets fragt deine Machine weiterhin vorher. Für Kontaktvermittlungen, Übergaben und kostenlose Fragen gelten weiterhin die jeweiligen Regeln.

## Erkenntnisse des Teams

Deine Machine hält fest, wie dein Team arbeitet. Dafür nutzt sie Kundenunterhaltungen, die der Team Graph bereits teilt, und erstellt höchstens einmal am Tag eine Erkenntnis. Zum Beispiel: „Rückerstattungsanfragen werden mit der Vorlage für Rückerstattungen aus dem Support-Postfach beantwortet.“ Die Erkenntnisse erscheinen im Bereich deiner Work Fleet unter **Erkenntnisse des Teams** und sind für alle in der Fleet sichtbar. Jede wird außerdem unter **Aktivität** protokolliert. Niemand wird vorher gefragt.

- Nur Unterhaltungen, an denen jemand aus deinem Team beteiligt war. Niemals private, persönliche oder sensible Unterhaltungen.
- Nur Informationen, die für mehrere Kunden gelten: ein Ablauf, ein Tool, ein Schreibstil oder wer für was zuständig ist. Niemals Informationen über einen einzelnen Kunden, Feedback zu deinem eigenen Produkt oder Namen, Adressen, Zahlen oder Zitate.
- Erkenntnisse, bei denen deine Machine unsicher ist, werden verworfen.

Deine Machine nutzt passende Erkenntnisse, wenn sie eine Aufgabe für diese Firma vorbereitet. Deine eigenen Fakten, Regeln und Skills haben Vorrang. Für persönliche Aufgaben werden die Erkenntnisse nie verwendet. Bei einer Aufgabe, für die eine Erkenntnis genutzt wurde, steht das dabei, zum Beispiel: „Team-Erkenntnis verwendet: Rückerstattungen werden über das Support-Postfach verschickt.“ Tippe dort auf **Entfernen**, um die Erkenntnis für die gesamte Fleet zu löschen.

Alle in der Fleet können eine Erkenntnis über **Entfernen** löschen. Sie verschwindet dann für alle und wird nicht erneut erstellt. Um das zu verhindern, deaktiviere unter Einstellungen, Sicherheit die Option **Anbieten, Erkenntnisse zu teilen**. Sorgfältige Work Fleets erhalten keine Erkenntnisse.

## Team-Briefing

Wähle im Fleet-Tab unter **Teilen** für das **Team-Briefing** die Option **Täglich** oder **Wöchentlich**. Deine Machine fragt dann die Machines deiner Teamkolleginnen und Teamkollegen nach Zahlen und Daten. Was deine Aufmerksamkeit braucht, erscheint unter Arbeit in Aufgaben: ein Kunde wartet auf eine Antwort von einem Teammitglied, bei einer Firma gab es seit mindestens zwei Wochen keine Aktivität, zwei von euch schreiben denselben Personen oder es gibt ein gemeinsames Meeting.

- Eine Aufgabe nennt die Person, auf deren Antwort gewartet wird, seit wann, worum sie gebeten wurde und was auf dem Spiel steht, zum Beispiel ein laufendes Projekt. Wenn es nichts Konkretes zu sagen gibt, bleibt der Punkt im Briefing und wird nicht zu einer Aufgabe.
- Die Firma und die Teamkolleginnen und Teamkollegen sind mit ihren Seiten verknüpft. **Details** zeigt, was sie geschrieben haben. Tippe darauf, um es zu lesen. Dort steht auch, was auf dem Spiel steht, wer aus dem Team Kontakt hat und welche Unterhaltungen zuletzt geführt wurden. Es werden nur Informationen geteilt, die der [Team Graph](team-graph.md) freigibt.
- Wenn das Geschriebene nur in den E-Mails eines Teammitglieds steht, nennt die Aufgabe die Person, die du fragen kannst.
- Mit **Das Team fragen** schickst du eine vorausgefüllte Frage dazu. Die Antworten erscheinen in der Aufgabe.
- Mit **Nicht nötig** schließt du die Aufgabe und das Briefing lernt daraus. Sie erscheint erst wieder, wenn es etwas Neues gibt.
- Wenn jemand antwortet oder die Aufgabe übernimmt, wird sie automatisch geschlossen. Eine Aufgabe zu einer Firma, für die du bereits eine Aufgabe hast, wird dieser Aufgabe hinzugefügt.

## Brief-Anfragen

Jeden Morgen fragt die Machine eines Teammitglieds mit aktiviertem Team-Briefing deine Machine nach Zahlen und Daten. In einer Work Fleet antwortet deine Machine selbstständig, aber nur mit Informationen, die der [Team Graph](team-graph.md) bereits teilt. Solange das Teilen im Team Graph ausgeschaltet ist, antwortet sie nicht. Jede Antwort erscheint im Fleet-Tab unter **Aktivität**, niemals als Aufgabe oder Benachrichtigung.

Um das zu stoppen, deaktiviere im Fleet-Tab unter **Teilen** die Option **Meine Kurzfakten mit dem Team teilen**. Im Briefing der anderen Person wird dann angezeigt, dass du nicht geantwortet hast.

In einer sorgfältigen Fleet warten Anfragen im Fleet-Tab unter **Brief-Anfragen** auf dich. Wähle **Einmal teilen**, **Immer teilen**, **Ablehnen** oder **Nie**. Es wird nichts geteilt, bevor du dich entscheidest. Nicht beantwortete Anfragen laufen ab.

## Team Graph

In einer Work Fleet wird die Arbeit mit Kunden nach deiner Prüfung mit dem Team geteilt. Siehe [Team Graph](team-graph.md).

## Geteilte Verbindungen

Ein Inhaber oder Admin kann Stripe oder Intercom einmal verbinden und im Fleet-Tab unter **Geteilte Verbindungen** mit dem Team teilen. Teammitglieder können die Verbindung nutzen, aber nicht ändern, und sehen, wer sie geteilt hat. Nur Admins können sie ändern oder beenden. Siehe [Stripe](stripe.md) und [Intercom](intercom.md).

## Was deine Machine beantwortet

Leg die Regeln für jede Fleet einzeln im Bereich Teilen fest. Siehe [Regeln zum Teilen](sharing-rules.md). Unter **Einstellungen** findest du die Verknüpfung **Fleet-Regeln**.

## Anmeldung mit Firmenkonto

Erlaube Teammitgliedern, mit ihrem Firmenkonto beizutreten. In einer gehosteten Work Fleet kann ein Inhaber oder Admin, der mit Google Workspace oder Microsoft 365 angemeldet ist, auf der Kontoseite **Anmeldung mit Firmenkonto** aktivieren.

Teammitglieder, die sich mit einer E-Mail-Adresse dieser Firmendomäne anmelden, sehen **Beitritt anfragen**. Ein Inhaber oder Admin muss jede Anfrage **Freigeben**. Persönliche Gmail- und Outlook.com-Konten zählen nie.

Wenn du jemanden aus der Fleet entfernst, wird die Person überall abgemeldet.

Wie du einer Fleet beitrittst, eine startest oder eine Machine auf deinem eigenen Computer koppelst, erfährst du unter [Tarife und Abrechnung](plans-and-billing.md) und [Freunde und das Network](friends.md).

## Für Inhaber und Admins

Unter **Verwalten** im Fleet-Tab findest du jede Fleet, die du verwaltest, mit den Mitgliedern, ihren Rollen und den Einladungen. Auf einer gehosteten Machine kannst du dort Personen einladen, ihre Rollen ändern, sie entfernen und Beitrittsanfragen beantworten. Wenn sich dadurch der Preis ändert, wird dein Konto geöffnet, damit du die Änderung zuerst bestätigen kannst. Auf einer selbst gehosteten Machine siehst du, wer zur Fleet gehört, und findest einen Link zu den Einstellungen dieser Fleet in deinem Konto. Dort verwaltest du Mitglieder und Einladungen.

**Fleet-Einstellungen** findest du unter dem Namen jeder Fleet in ihrem Bereich und unter Verwalten. Damit öffnest du die Einstellungen dieser Fleet in deinem Konto: geteilte Verbindungen, Sicherheit, Anmeldung mit Firmenkonto, welche Machine antwortet und diese beiden Bereiche:

- **Kürzlich entfernt**: alle Personen, die entfernt wurden oder die Fleet verlassen haben. „Entfernt, bestätigt“ bedeutet, dass ihre Machine die Arbeitsdaten gelöscht hat und sie überall abgemeldet wurden. Bis dahin steht dort **Ausstehend** und der Grund dafür.
- **Aktivität**: wer was wann getan hat, einschließlich Einladungen, Beitritten, Entfernungen, Rollen, gehosteten Machines, Abrechnung, geteilten Verbindungen und Freigaben. Hier wird auch jedes Mal protokolliert, wenn unser Supportteam den Bericht einer Mitglieds-Machine oder deren Logs gelesen hat. Nachrichteninhalte werden nie protokolliert. Mit **CSV herunterladen** kannst du die Daten exportieren. Sie werden 12 Monate lang gespeichert.

**Vor dem Start der Machine eines Mitglieds fragen**: Für den Inhaber. Ist die Option aktiviert, wartet die Machine eines neuen Mitglieds auf deine Freigabe, auch in einer kostenlosen Fleet. Ist sie deaktiviert, startet sie in einer kostenlosen Fleet sofort und du wirst benachrichtigt. Bei einer kostenpflichtigen Machine musst du den Betrag immer zuerst bestätigen.

Nach **Nicht mehr teilen** wird bei einer geteilten Verbindung „Entfernt, bestätigt“ angezeigt, sobald keine Machine mehr darauf zugreifen kann.
