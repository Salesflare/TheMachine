---
title: Fleets
area: fleet
summary: Eine Work Fleet für dein Team, eine Family Fleet für zu Hause. Machines, die sich gegenseitig helfen, mit deinem Ja zu jeder Antwort.
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

## Brief-Anfragen

Ein Teammitglied mit eingeschaltetem Team-Brief fragt deine Machine jeden Morgen nach Zahlen und Terminen. Daraus wird nie eine Aufgabe. Die Anfrage wartet im Fleet-Tab, im Bereich deiner Arbeits-Fleet, unter **Brief-Anfragen**: **Einmal teilen**, **Immer teilen**, **Ablehnen** oder **Nie**. Nur die neueste Anfrage pro Teammitglied wartet, unbeantwortete laufen ab. Nichts wird geteilt, bevor du wählst.

## Team-Graph

In einer Work Fleet wird Kundenarbeit mit deinem Team geteilt, nachdem du sie durchgesehen hast. Siehe [Team-Graph](team-graph.md).

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
