---
title: Benachrichtigungen
area: settings
summary: Was dich wo und wann erreicht: Nur was nicht warten kann, meldet sich, der Rest steht in einer morgendlichen Zusammenfassung.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Wähle in **Einstellungen**, **Benachrichtigungen** für jede Art, wo sie dich erreicht:

- **Neue Aufgaben**: nur was nicht warten kann, etwa etwas, das heute fällig oder dringend ist.
- **Ergebnisse und Fragen**: eine Antwort, bereit zum Senden, eine Anmeldung, die eine Aufgabe braucht, eine Frage aus der Fleet.
- **Erinnerungen**: Zurückgestelltes und Wartendes, das zurückkommt.
- **Morgendliche Zusammenfassung**: eine kurze Übersicht über deinen Tag. Siehe unten.

Jede hat einen Schalter für **Push** (die App auf deinem Handy oder Computer), **Telegram**, wenn es eingerichtet ist, und **E-Mail** auf einer gehosteten Machine oder einer im The Machine Network. Alle sind an, außer der Zusammenfassung auf Telegram.

Die **Arbeitszeiten** stehen im selben Tab: deine Arbeitstage, die Stunden, in denen Benachrichtigungen rausgehen dürfen, wann Zurückgestelltes zurückkommt, die Uhrzeit der Zusammenfassung und deine Zeitzone. Siehe [Arbeitszeiten](work-hours.md).

## Nur was nicht warten kann

Ein Push, eine Telegram-Benachrichtigung oder eine E-Mail geht nur für:

- eine Aufgabe, die heute fällig oder dringend ist;
- eine Antwort, auf die jemand wartet, als Entwurf bereit zum Senden;
- eine Aufgabe, für die du dich anmelden musst;
- Zurückgestelltes, das zur gewählten Zeit zurückkommt.

Alles andere landet still im Dashboard (und ohne Ton in Telegram) und wartet auf die morgendliche Zusammenfassung. An einem freien Tag meldet sich nur Dringendes oder heute Fälliges. Höchstens 8 Pushes am Tag. Nach 3 Tagen ohne Blick ins Dashboard kommt nur noch die morgendliche Zusammenfassung, bis du zurück bist.

## Wann du benachrichtigt wirst

Wie Slack schaut es, ob du das Dashboard benutzt, nicht nur, ob es offen ist:

- In Benutzung: Das Dashboard ist vor dir, im Fokus, und du hast in den letzten 10 Minuten geklickt, getippt, gescrollt oder es berührt. Nichts vibriert. Telegram kommt ohne Ton an.
- Weg: Das Dashboard ist im Hintergrund, minimiert, geschlossen oder seit 10 Minuten unbenutzt. Ein Push geht eine Minute, nachdem du es verlassen hast, raus, außer du kommst zurück und siehst es vorher.
- 15 Minuten später noch ungesehen, und es kann nicht warten: eine E-Mail dazu, höchstens eine pro Stunde. Was du schon erledigt hast, fehlt darin. Meist ist die morgendliche Zusammenfassung die einzige E-Mail.
- Ein Teammitglied übergibt dir eine Aufgabe, und deine Machine hat kein Handy und kein Telegram, um dich zu erreichen: eine E-Mail dazu, 15 Minuten später, falls du sie noch nicht gesehen hast. Nur ihr Titel und ein Link. **E-Mail** bei **Ergebnisse und Fragen** schaltet das aus.
- Außerhalb deiner Arbeitszeiten: nichts. Die morgendliche Zusammenfassung enthält, was reinkam.
- Eine neue Arbeitsaufgabe, die an einem freien Tag reinkommt, wartet bis zur Zusammenfassungszeit deines nächsten Arbeitstags. Die Aufgabe zeigt, wo und wann sie dich erreicht, etwa Benachrichtigung Mo., 2. Nov. · 08:30, nach der Zeile **Neue Aufgaben**. Sind dort Push und Telegram beide aus, steht nichts da.

Nur was dich braucht, benachrichtigt. Fortschritt und Änderungen nicht. Ein neueres Ergebnis zu einer Aufgabe, die du noch nicht gesehen hast, aktualisiert sie ohne neue Benachrichtigung. Viele auf einmal vibrieren nur einmal. Das App-Symbol zeigt, wie viele Aufgaben dich brauchen.

## Buttons in Benachrichtigungen

Jede Benachrichtigung hat Buttons für den nächsten Schritt. In der App auf dem Handy:

- Neues To-do: Ausführen, Zurückstellen, Als erledigt markieren.
- Entwurf fertig: Entwurf öffnen, Zurückstellen, Als erledigt markieren.
- Ergebnis fertig: Öffnen, Als erledigt markieren, Zurückstellen.
- Frage, hängt fest oder Anmeldung nötig: Antworten, Öffnen oder Anmelden, dann Zurückstellen und Als erledigt markieren.
- Erinnerung: Als erledigt markieren, Zurückstellen, Öffnen.
- Morgendliche Zusammenfassung: zum Öffnen antippen.

Ein Browser und Telegram zeigen zwei davon. Fleet-Fragen behalten Einmal antworten und Ablehnen.

Aus einer Benachrichtigung wird nie etwas gesendet, bezahlt oder eingereicht. Ein Entwurf öffnet sich immer zuerst, damit du ihn siehst, bevor er rausgeht. Entwurf öffnen zeigt die Aufgabe in deiner Liste mit dem ganzen Entwurf. Ausführen startet nur die Arbeit an einer neuen Aufgabe.

In der App fragen Zurückstellen und Als erledigt markieren zuerst nach dem Entsperren. Im Browser öffnen sie das Dashboard, das es erledigt und Rückgängig anbietet. Zurückstellen bringt das To-do in zwei Stunden zurück, bei einer Erinnerung morgen früh.

E-Mails mit dem, was auf dich wartet, haben die Links Öffnen und Zurückstellen. Sie öffnen nur das Dashboard.

## Die morgendliche Zusammenfassung

Sie kommt an Arbeitstagen zu deiner Uhrzeit für die **Morgendliche Zusammenfassung**, außer es gibt nichts zu sagen. **Vorschau** in ihrer Zeile zeigt sie, ohne sie zu senden. Standardmäßig kommt sie als Push und als E-Mail, kurz genug für einen Blick:

- ein Gruß mit dem, was heute zählt, etwa "Guten Morgen Sam, 2 Antworten sind bereit zum Senden" oder, bei einer Aufgabe, "Guten Morgen Sam, wartet auf dein OK: Schick das Bestellformular";
- höchstens drei Dinge zu tun, jedes mit einem Link Öffnen: zuerst fertige Entwürfe und heute fällige Versprechen;
- wie viele weitere warten können und wie lange sie in deinem Tempo dauern, etwa "12 weitere können warten, etwa 5 Min. zum Erledigen." Aufgaben, die auf deine Antwort warten, zählen bei der Zeit nicht mit.
- deine Termine in einer Zeile.

Öffnen zeigt die Aufgabe hervorgehoben in deiner Liste. Ist sie erledigt, zurückgestellt oder in einer anderen Ansicht, öffnet sich ihr Chat. Ein Versprechen öffnet seine Aufgabe oder, solange es keine hat, seine eigene Seite.

Der Push sagt dasselbe ohne Links. Tippst du darauf, öffnet sich heute im **Kalender**.

## Datenschutz

Push geht von deiner Machine direkt an dein Gerät, verschlüsselt für dieses Gerät. Die Steuerungsebene sieht ihn nie. E-Mails verschickt der Mailserver von The Machine an die Adresse deines Kontos, der Text geht also über ihn und deinen Mailanbieter. Wenn [Vorsichtig](security-levels.md) den Text von Aufgaben in Benachrichtigungen ausblendet, enthalten E-Mails nur Anzahlen. Schalte **E-Mail** für eine Art aus, damit sie gar nicht per E-Mail kommt.

Schalte Push für ein Gerät unter **Dieses Gerät** ein, oder siehe [App installieren](phone-app.md). Die [mobile App](mobile-app.md) bekommt über Apple oder Google eine feste Zeile, ohne Text einer Aufgabe. Dann fragt sie deine Machine nach dem Titel und dem nächsten Schritt.
