---
title: Täuschend ähnliche Absender
area: security
summary: Mails von einer Adresse, die jemanden nachahmt, mit dem du zu tun hast, werden bei der zugehörigen Aufgabe markiert. Entwürfe gehen nie an diese Adresse.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## Was erkannt wird

Manche Betrugsversuche kommen von einer Adresse, die einer bekannten ähnelt: `examp1e.com` statt `example.com`, `example-billing.com`, mit einem Buchstaben Unterschied oder mit zwei vertauschten Buchstaben. The Machine vergleicht die Domain jedes Absenders mit den Domains, mit denen du bereits zu tun hast.

Von zwei ähnlich aussehenden Absendern ist derjenige der echte, an den du geschrieben hast, den du getroffen oder selbst eingerichtet hast, auch wenn der andere zuerst geschrieben hat. Wenn keiner von beiden dadurch hervorsticht, gilt der neuere als täuschend ähnlicher Absender.

Derselbe Name mit einer anderen Endung, etwa `example.nl` neben `example.com`, steht für dieselbe Organisation und ist kein täuschend ähnlicher Absender. Kostenlose Maildienste wie gmail.com zählen nie dazu.

## Bei einer Aufgabe

Eine Aufgabe zu einer solchen Nachricht sagt es klar, zum Beispiel: „Das ist nicht Alex. Die Nachricht kam von examp1e.com, nicht von example.com.“ Der Absender wird als reine Adresse angezeigt, ohne Bild und ohne Link zur imitierten Person.

## Was The Machine nicht tut

- The Machine weist einem täuschend ähnlichen Absender nie eine Rolle in deinem Graph zu und macht seine Domain nie zur Organisation eines Projekts.
- The Machine führt ihn nie mit der imitierten Person zusammen, auch dann nicht, wenn er in derselben Unterhaltung unter demselben Namen schreibt, und schlägt ihn nie unter **Gleiche Person?** vor.
- Eine von The Machine vorbereitete Antwort geht an die gespeicherte Adresse, nicht an die täuschend ähnliche.

Deine Entscheidung hat immer Vorrang: Du kannst dem Absender trotzdem eine Rolle zuweisen, ihn mit jemandem zusammenführen oder an jede beliebige Adresse schreiben.
