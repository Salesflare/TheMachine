---
title: Expéditeurs qui se font passer pour quelqu’un
area: security
summary: Les e-mails provenant d’une adresse qui imite celle d’une personne avec qui vous échangez sont signalés dans la tâche correspondante, et les brouillons ne sont jamais adressés à cette adresse.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## Ce que cette détection repère

Certaines arnaques utilisent une adresse qui ressemble à une adresse connue : `examp1e.com` pour `example.com`, `example-billing.com`, ou avec une seule lettre de différence. The Machine compare le domaine de chaque expéditeur à ceux des personnes avec qui vous échangez déjà. Si le nouveau domaine ressemble seulement à un domaine connu, l’expéditeur est considéré comme un sosie.

Un même nom avec une autre extension, comme `example.nl` à côté de `example.com`, désigne la même organisation, pas un sosie. Les services de messagerie gratuits comme gmail.com ne sont jamais pris en compte.

## Dans une tâche

Une tâche concernant un tel message le dit clairement, par exemple : « Ce n’est pas Alex. Le message vient de examp1e.com, et non de example.com. » L’expéditeur apparaît sous la forme de son adresse seule, sans photo ni lien vers la personne qu’il imite.

## Ce que The Machine ne fera pas

- Elle ne donne jamais de rôle à un expéditeur sosie dans votre Graph.
- Elle ne le fusionne jamais avec la personne qu’il imite et ne le propose jamais sous **Même personne ?**.
- Une réponse qu’elle prépare est envoyée à l’adresse enregistrée, pas à celle du sosie.

Votre choix prévaut toujours : vous pouvez quand même lui attribuer un rôle, le fusionner avec une autre personne ou écrire à n’importe quelle adresse.
