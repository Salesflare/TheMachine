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
- **Morgendliche Zusammenfassung**: die Meetings von heute, was fällig ist, was über Nacht reinkam und die ersten wartenden Aufgaben, in der Reihenfolge deiner Aufgabenliste.

Jede hat einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, wenn es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network. Alle sind an, außer der Zusammenfassung auf Telegram.

Die **Arbeitszeiten** stehen im selben Tab: deine Arbeitstage, die Stunden, in denen Benachrichtigungen rausgehen dürfen, wann Zurückgestelltes zurückkommt, die Uhrzeit der Zusammenfassung und deine Zeitzone. Siehe [Arbeitszeiten](work-hours.md).

## Wann du benachrichtigt wirst

Wie Slack schaut es, ob du das Dashboard benutzt, nicht nur, ob es offen ist:

- In Benutzung: Das Dashboard ist vor dir, im Fokus, und du hast in den letzten 10 Minuten geklickt, getippt, gescrollt oder es berührt. Nichts vibriert. Telegram kommt ohne Ton an.
- Weg: Das Dashboard ist im Hintergrund, minimiert, geschlossen oder seit 10 Minuten unbenutzt. Ein Push geht eine Minute, nachdem du es verlassen hast, raus, außer du kommst zurück und siehst es vorher.
- 15 Minuten später noch ungesehen: eine E-Mail mit allem, was noch auf dich wartet. Höchstens eine pro Stunde. Was du inzwischen erledigt hast, auf Telegram oder anderswo, fehlt darin. Wer das Dashboard nutzt, nachdem etwas hereinkam, hat es gesehen. An einem Tag am Dashboard kommt also womöglich gar keine E-Mail.
- Ein Teammitglied übergibt dir eine Aufgabe, und deine Machine hat kein Handy und kein Telegram, um dich zu erreichen: eine E-Mail dazu, 15 Minuten später, falls du sie noch nicht gesehen hast. Nur ihr Titel und ein Link. **E-Mail** bei **Ergebnisse und Fragen** schaltet das aus.
- Außerhalb deiner Arbeitszeiten: nichts. Die morgendliche Zusammenfassung enthält, was reinkam.
- Eine neue Arbeitsaufgabe, die an einem freien Tag reinkommt, wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Die Aufgabe zeigt, wo und wann sie dich erreicht, etwa Benachrichtigung Mo., 2. Nov. · 08:30, nach der Zeile **Neue Aufgaben**. Sind dort Push und Telegram beide aus, steht nichts da.

Nur was dich braucht, benachrichtigt. Fortschritt und Änderungen nicht. Viele auf einmal vibrieren nur einmal. Das App-Symbol zeigt, wie viele Aufgaben dich brauchen.

## Buttons in Benachrichtigungen

Jede Benachrichtigung hat Buttons für den nächsten Schritt. In der App auf dem Handy:

- Neues To-do: Ausführen, 2 Std. zurückstellen, Als erledigt markieren.
- Entwurf fertig: Entwurf öffnen, 2 Std. zurückstellen, Als erledigt markieren.
- Ergebnis fertig: Öffnen, Als erledigt markieren, 2 Std. zurückstellen.
- Frage, hängt fest oder Anmeldung nötig: Antworten, Öffnen oder Anmelden, dann 2 Std. zurückstellen und Als erledigt markieren.
- Erinnerung: Als erledigt markieren, Zurückstellen, Öffnen.
- Morgendliche Zusammenfassung: zum Öffnen antippen.

Ein Browser und Telegram zeigen zwei davon. Fleet-Fragen behalten Einmal antworten und Ablehnen.

Aus einer Benachrichtigung wird nie etwas gesendet, bezahlt oder eingereicht. Ein Entwurf öffnet sich immer zuerst, damit du ihn siehst, bevor er rausgeht. Entwurf öffnen zeigt die Aufgabe in deiner Liste mit dem ganzen Entwurf. Ausführen startet nur die Arbeit an einer neuen Aufgabe.

In der App fragen Zurückstellen und Als erledigt markieren zuerst nach dem Entsperren. Im Browser öffnen sie das Dashboard, das es erledigt und Rückgängig anbietet. 2 Std. zurückstellen bringt das To-do in zwei Stunden zurück, Zurückstellen morgen früh.

E-Mails mit dem, was auf dich wartet, haben die Links Öffnen und Zurückstellen. Sie öffnen nur das Dashboard.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zu deiner Uhrzeit für die **Morgendliche Zusammenfassung** und fällt nur aus, wenn es nichts zu sagen gibt: keine Meetings, nichts fällig oder neu und keine wartenden Aufgaben. **Vorschau** in ihrer Zeile zeigt sie auf der Seite, ohne sie zu senden. Standardmäßig kommt sie als Push und als E-Mail. Der Push nennt, wie viele Aufgaben warten, die ersten zwei und die Uhrzeit deines ersten Termins. Tippst du auf den Push, öffnet sich heute im **Kalender**.

## Datenschutz

Push geht von deiner Machine direkt an dein Gerät, verschlüsselt für dieses Gerät. Die Steuerungsebene sieht ihn nie. E-Mails verschickt der Mailserver von The Machine an die Adresse deines Kontos, der Text geht also über ihn und deinen Mailanbieter. Wenn [Vorsichtig](security-levels.md) den Text von Aufgaben in Benachrichtigungen ausblendet, enthalten E-Mails nur Anzahlen. Schalte **E-Mail** für eine Art aus, damit sie gar nicht per E-Mail kommt. Sie sagt auch, wie lange dich die wartenden Aufgaben kosten, etwa "4 bereit · etwa 2 Min.".

Schalte Push für ein Gerät unter **Dieses Gerät** ein, oder siehe [App installieren](phone-app.md). Die [mobile App](mobile-app.md) bekommt über Apple oder Google eine feste Zeile, ohne Text einer Aufgabe. Dann fragt sie deine Machine nach dem Titel und dem nächsten Schritt.
