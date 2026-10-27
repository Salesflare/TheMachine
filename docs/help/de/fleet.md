---
title: Fleets
area: fleet
summary: Eine Work Fleet für dein Team, eine Family Fleet für zu Hause. Machines, die sich gegenseitig helfen, nach deinen Freigaberegeln.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV
order: 1
---
The Machine Network verbindet Machines. Was sie sich gegenseitig sagen, ist Ende-zu-Ende-verschlüsselt, und jede Machine antwortet nur nach deinen Regeln.

## Arten von Fleet

- **Work Fleet**: dein Team. Übergib Arbeit, frag, wer jemanden kennt, bekomm Vorstellungen und ein Team-Briefing.
- **Family Fleet**: bis zu 6 Personen. Wann alle frei sind, gemeinsame Aufgaben und Pläne. Kostenlos. Siehe [Familie](family.md).
- **Freunde**: alle auf The Machine, einzeln. Kostenlos. Siehe [Freunde](friends.md).

## Der Fleet-Tab

Er erscheint, sobald du in einer Fleet bist, mit einem Bereich für jede Fleet, Familie, Freunde, Network, Teilen und Aktivität.

## Deine Fleet fragen

Frag „Wer kennt jemanden bei Acme?“ im Fleet-Tab, oder nutze **Die Fleet fragen** bei einer Organisation im [Graph](graph.md). Die Machine jeder Person im Team antwortet nach deren eigenen Freigaberegeln und fragt sie zuerst, wenn die Regel das verlangt.

## Von selbst beantwortet in einer Work Fleet

In einer Work Fleet mit Standard beantwortet deine Machine **wer jemanden kennt**, **Meeting-Kontext** („Wer ist dieser Gast?“) und **wer geteilte E-Mails bearbeitet** von Teammitgliedern von selbst. Sie nutzt nur, was der [Team-Graph](team-graph.md) schon mit deinem Team teilt. Private, persönliche und sensible Threads zählen nie, und Namen kommen nur von Personen, die der Team-Graph schon teilt. Jede Antwort erscheint im Fleet-Tab unter **Aktivität**.

Um eine zu stoppen, stell sie unter **Teilen** auf **Nie**. Eine Regel, die als **Erst mich fragen** gespeichert ist, wirkt jetzt wie **Immer**. Solange das Teilen im Team-Graph deiner Fleet aus ist, fragen wer jemanden kennt und Meeting-Kontext weiter zuerst dich.

Work Fleets mit Vorsichtig, Freunde und Familie fragen weiter zuerst dich. Warme Vorstellungen, Übergaben, geteilte Follow-ups und freie Fragen behalten ihre eigenen Regeln.

## Erkenntnisse des Teams

Höchstens einmal am Tag liest deine Machine ein paar Kunden-Threads, die der Team-Graph schon mit deinem Team teilt, und schreibt auf, wie das Team arbeitet. Zum Beispiel: „Rückerstattungen werden aus dem Support-Postfach mit der Vorlage für Rückerstattungen beantwortet.“ Sie erscheinen im Bereich deiner Work Fleet unter **Erkenntnisse des Teams**, für alle in der Fleet, und jede wird unter **Aktivität** protokolliert. Niemand wird vorher gefragt.

- Nur Threads, in denen jemand aus deinem Team geschrieben hat. Nie private, persönliche oder sensible.
- Nur, was über mehrere Kunden hinweg gilt: ein Ablauf, ein Tool, ein Schreibstil oder wer was bearbeitet. Nie etwas über einen einzelnen Kunden, nie Feedback zu deinem eigenen Produkt und nie Namen, Adressen, Zahlen oder Zitate.
- Jede hat ein Label: welche Art es ist, dass sie aus Gesprächen im Team stammt und dass sie für diese Fleet ist. Solche, bei denen sie unsicher ist, fallen weg.

Alle in der Fleet können eine Erkenntnis **Entfernen**. Dann ist sie für alle weg und wird nicht neu erstellt. Zum Stoppen schalte **Anbieten, Erkenntnisse zu teilen** in Einstellungen, Sicherheit aus. Work Fleets mit Vorsichtig bekommen keine.

## Brief-Anfragen

Ein Teammitglied mit eingeschaltetem Team-Brief fragt deine Machine jeden Morgen nach Zahlen und Terminen. In einer Work Fleet antwortet deine Machine von selbst, nur mit dem, was der [Team-Graph](team-graph.md) schon mit deinem Team teilt. Private und persönliche Threads zählen nie, und nichts geht raus, solange das Teilen im Team-Graph deiner Fleet aus ist. Jede Antwort erscheint im Fleet-Tab unter **Aktivität**. Daraus wird nie eine Aufgabe oder Benachrichtigung.

Zum Stoppen schalte **Meine Kurzfakten mit dem Team teilen** im Fleet-Tab unter **Teilen** aus. Ihr Brief führt dich dann als nicht beantwortet.

In einer Fleet mit Vorsichtig warten Anfragen im Fleet-Tab unter **Brief-Anfragen** auf dich: **Einmal teilen**, **Immer teilen**, **Ablehnen** oder **Nie**. Nur die neueste Anfrage pro Teammitglied wartet, unbeantwortete laufen ab. Nichts wird geteilt, bevor du wählst.

## Team-Graph

In einer Work Fleet wird Kundenarbeit mit deinem Team geteilt, nachdem du sie durchgesehen hast. Siehe [Team-Graph](team-graph.md).

## Geteilte Connectors

Ein Owner oder Admin kann Stripe oder Intercom einmal verbinden und mit dem Team teilen, im Kasten **Geteilte Connectors** im Fleet-Tab. Die Machines der Teammitglieder lesen es, nur lesend, und sehen, wer es geteilt hat. Nur Admins ändern oder stoppen es. Siehe [Stripe](stripe.md) und [Intercom](intercom.md).

## Was deine Machine antwortet

Das stellst du pro Fleet im Bereich Teilen ein. Siehe [Freigaberegeln](sharing-rules.md). **Einstellungen** hat eine Abkürzung: **Fleet-Regeln**.

## Firmenanmeldung

Für eine gehostete Work Fleet. Ein Owner oder Admin, der mit einem Firmenkonto bei Google Workspace oder Microsoft 365 angemeldet ist, kann auf der Kontoseite **Firmenanmeldung** einschalten. Sie nutzt die Domain dieses Kontos.

Teammitglieder, die sich mit einem Konto auf dieser Domain anmelden, sehen dann **Beitritt anfragen**. Ein Owner oder Admin muss jede Anfrage **Freigeben**. Private Konten bei Gmail und Outlook.com zählen nie.

Wer aus der Fleet entfernt wird, wird überall abgemeldet.

Wie du einer Fleet beitrittst, eine gründest oder eine Machine auf deinem eigenen Computer koppelst, steht in [Tarife und Abrechnung](plans-and-billing.md) und [Freunde und das Network](friends.md).

## Für Owner und Admins

Der Fleet-Teil deiner Kontoseite zeigt zwei weitere Dinge:

- **Kürzlich entfernt**: jede Person, die entfernt wurde oder gegangen ist. Dort steht **Entfernt, bestätigt**, sobald ihre Machine die Arbeitsdaten entfernt hat, Google die Abmeldung bestätigt hat und jedes geteilte Token, das sie hatte, ersetzt wurde. Bis dahin steht dort **Ausstehend** und warum.
- **Aktivität**: wer was wann gemacht hat. Einladungen, Beitritte, Entfernungen, Rollen, Server und Abrechnung, geteilte Connectoren und Freigaben. Es listet auch jedes Mal, wenn unser Team den Server eines Mitglieds oder seine Logs geöffnet hat. Nie Nachrichteninhalte. **CSV herunterladen** exportiert es. Wird 12 Monate aufbewahrt.

Nach **Nicht mehr teilen** zeigt ein geteilter Connector **Entfernt, bestätigt**, sobald jede Machine das Token gelöscht hat.
