---
title: Ähnliche Absender
area: security
summary: E-Mails von einer Adresse, die jemanden aus deinem Umfeld nachahmt, werden in der Aufgabe gekennzeichnet. Entwürfe gehen nie an diese Adresse.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## Was erkannt wird

Manche Betrugsversuche kommen von einer Adresse, die einer bekannten ähnelt: `examp1e.com` statt `example.com`, `example-billing.com` oder mit einem Buchstaben Unterschied. The Machine vergleicht die Domain jedes Absenders mit denen, mit denen du bereits zu tun hast. Wenn die neuere Domain nur einer bekannten ähnelt, wird sie als Lookalike eingestuft.

Derselbe Name mit einer anderen Endung, wie `example.nl` neben `example.com`, gehört zur selben Organisation und ist kein Lookalike. Kostenlose Mailanbieter wie gmail.com zählen nie dazu.

## In einer Aufgabe

In einer Aufgabe zu einer solchen Nachricht steht ein klarer Hinweis, zum Beispiel: „Das ist nicht Alex. Die Nachricht kam von examp1e.com, nicht von example.com.“ Der Absender wird als reine Adresse angezeigt, ohne Bild und ohne Link zu der Person, die er nachahmt.

## Was The Machine nicht tut

- Sie gibt einem Lookalike-Absender nie eine Rolle in deinem Graph.
- Sie führt ihn nie mit der Person zusammen, die er nachahmt, und schlägt ihn auch nie unter **Gleiche Person?** vor.
- Ein Antwortentwurf geht an die hinterlegte Adresse, nicht an die des Lookalikes.

Deine Entscheidung gilt immer: Du kannst dem Absender trotzdem eine Rolle geben, ihn mit jemandem zusammenführen oder an jede beliebige Adresse schreiben.
