---
title: Täuschend ähnliche Absender
area: security
summary: E-Mails von einer Adresse, die jemanden nachahmt, mit dem du zu tun hast, werden bei der Aufgabe gekennzeichnet. Entwürfe gehen nie an diese Adresse.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## Was erkannt wird

Manche Betrugsversuche kommen von einer Adresse, die einer bekannten Adresse ähnelt: zum Beispiel `examp1e.com` statt `example.com`, `example-billing.com` oder mit nur einem Buchstaben Unterschied. The Machine vergleicht die Domain jedes Absenders mit den Domains, mit denen du bereits zu tun hast. Wenn eine neuere Adresse nur einer bekannten ähnelt, gilt sie als täuschend ähnlich.

Derselbe Name mit einer anderen Endung, zum Beispiel `example.nl` neben `example.com`, gehört zur selben Organisation und gilt nicht als täuschend ähnlich. Kostenlose Mailanbieter wie gmail.com zählen nie dazu.

## Bei einer Aufgabe

Bei einer Aufgabe zu einer solchen Nachricht steht es klar dabei, zum Beispiel: „Das ist nicht Alex. Die Nachricht kam von examp1e.com, nicht von example.com.“ Der Absender wird als reine Adresse ohne Bild und ohne Link zu der Person angezeigt, die nachgeahmt wird.

## Was The Machine nicht tut

- Sie gibt einem täuschend ähnlichen Absender nie eine Rolle in deinem Graph.
- Sie führt ihn nie mit der nachgeahmten Person zusammen und schlägt ihn nie unter **Gleiche Person?** vor.
- Eine Antwort, die sie vorbereitet, geht an die gespeicherte Adresse, nicht an die täuschend ähnliche.

Deine Entscheidung gilt immer: Du kannst dem Absender trotzdem eine Rolle geben, ihn mit jemandem zusammenführen oder an eine beliebige Adresse schreiben.
