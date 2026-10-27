---
title: Benachrichtigungen
area: settings
summary: Was dich wo und wann erreicht: Push, Telegram oder E-Mail je nach Art, deine Arbeitszeiten und die morgendliche Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Wähle in **Einstellungen**, **Benachrichtigungen** für jede Art, wo sie dich erreicht:

- **Neue Aufgaben**: eine Antwort, auf die jemand wartet, eine Anfrage, alles Dringende.
- **Ergebnisse und Fragen**: ein Entwurf, der bereit zum Freigeben oder Senden ist, eine Aufgabe, die festhängt oder eine Anmeldung braucht, eine Frage aus der Fleet.
- **Erinnerungen**: Zurückgestelltes und Wartendes, das zurückkommt.
- **Morgendliche Zusammenfassung**: die Meetings von heute, was fällig ist und was über Nacht reinkam.

Jede hat einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, wenn es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network. Alle sind an, außer der Zusammenfassung auf Telegram.

Die **Arbeitszeiten** stehen im selben Tab: deine Arbeitstage, die Stunden, in denen Benachrichtigungen rausgehen dürfen, wann Zurückgestelltes zurückkommt, die Uhrzeit der Zusammenfassung und deine Zeitzone. Siehe [Arbeitszeiten](work-hours.md).

## Wann du benachrichtigt wirst

Wie Slack schaut es, ob du das Dashboard benutzt, nicht nur, ob es offen ist:

- In Benutzung: Das Dashboard ist vor dir, im Fokus, und du hast in den letzten 10 Minuten geklickt, getippt, gescrollt oder es berührt. Nichts vibriert. Telegram kommt ohne Ton an.
- Weg: Das Dashboard ist im Hintergrund, minimiert, geschlossen oder seit 10 Minuten unbenutzt. Ein Push geht eine Minute, nachdem du es verlassen hast, raus, außer du kommst zurück und siehst es vorher.
- 15 Minuten später noch ungesehen: eine E-Mail mit allem, was noch auf dich wartet. Höchstens eine pro Stunde. Was du inzwischen erledigt hast, auf Telegram oder anderswo, fehlt darin.
- Außerhalb deiner Arbeitszeiten: nichts. Die morgendliche Zusammenfassung enthält, was reinkam.

Nur was dich braucht, benachrichtigt. Fortschritt und Änderungen nicht. Viele auf einmal vibrieren nur einmal. Das App-Symbol zeigt, wie viele Aufgaben dich brauchen.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zu deiner Uhrzeit für die **Morgendliche Zusammenfassung** und fällt aus, wenn es nichts zu sagen gibt. **Vorschau** in ihrer Zeile zeigt sie auf der Seite, ohne sie zu senden. Standardmäßig kommt sie als Push und als E-Mail.

## Datenschutz

Push geht von deiner Machine direkt an dein Gerät, verschlüsselt für dieses Gerät. Die Steuerungsebene sieht ihn nie. E-Mails verschickt der Mailserver von The Machine an die Adresse deines Kontos, der Text geht also über ihn und deinen Mailanbieter. Wenn [Vorsichtig](security-levels.md) den Text von Aufgaben in Benachrichtigungen ausblendet, enthalten E-Mails nur Anzahlen. Schalte **E-Mail** für eine Art aus, damit sie gar nicht per E-Mail kommt.

Schalte Push für ein Gerät unter **Dieses Gerät** ein, oder siehe [App installieren](phone-app.md).
