---
title: Keine neuen Aufgaben
area: troubleshooting
summary: Prüfungen sind aus, warten oder stehen beim Nutzungslimit deines Modells. Woran du das erkennst und was du tun kannst.
covers: 
code: dashboard.html, assistant.py
order: 3
---
Aufgaben entstehen aus Prüfungen: Deine Machine liest, was reingekommen ist, in kleinen Paketen, innerhalb von etwa 15 Minuten.

## Gerade angemeldet

Auf einer neuen gehosteten Machine starten die Prüfungen von selbst, sobald deine KI und deine E-Mails verbunden sind. Während deine Machine deine E-Mails liest, steht unter Aufgaben "Deine E-Mails werden gelesen, die ersten Aufgaben kommen in ein paar Minuten". Sobald sie weiß, wie viel es ist, sagt sie ungefähr, wie lange es dauert: "Erste Aufgaben in etwa 10 Min." Fehlt ein Schritt, nennt ihn **Braucht dich**, etwa **Mail verbinden**, mit einem Link zu diesem Schritt.

Während sie liest, zeigt Aufgaben, wie weit sie ist, ein paar der Personen und Organisationen, auf die sie gestoßen ist, und deine erste Aufgabe, sobald sie da ist. Die Namen stammen aus deinen eigenen E-Mails, und nur du siehst sie.

## Prüfungen sind aus

Oben in Aufgaben steht „Die Prüfung ist aus, daher kommen noch keine Aufgaben.“ Auf einer gehosteten Machine tippst du auf **Prüfung einschalten**. Auf deinem eigenen Computer führst du `./install.sh --activate` aus.

## Das Limit deines Modells

Prüfungen dessen, was reingekommen ist, pausieren bei etwa 65 % des 5-Stunden-Limits deines Tarifs und bei 90 % des Wochenlimits, damit Platz für deine eigenen Chats bleibt. Ein Board, das deinen Verlauf durchgeht, ist langsamer, mit etwa einem Siebtel der Woche pro Tag. Mit einem funktionierenden Ersatzmodell mit anderem Tarif oder Anbieter warten Prüfungen nicht. Siehe [Modell](model.md).

Während Prüfungen warten, steht oben im Dashboard, bis wann, etwa „Die Prüfung wartet bis 07:15, um deine ChatGPT-Woche zu schonen.“ **Jetzt prüfen** startet sofort eine. Ist ein Limit erreicht, steht oben im Dashboard, welches und wann es zurückgesetzt wird. **Verbindungen**, dann **Prüfungen** zeigt es neben dem Durchlauf. **Einstellungen**, **Modell** zeigt deine Limits. Siehe [Modell](model.md).

Während es wartet, geht nichts verloren: Was reingekommen ist, wird geprüft, sobald es geht.

## Ein Durchlauf ist fehlgeschlagen

**Letzte Durchläufe** unter **Prüfungen** zeigt jeden Durchlauf. Ein fehlgeschlagenes Paket wird von selbst erneut versucht.
