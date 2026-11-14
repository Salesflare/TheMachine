---
title: Adresses d’expéditeurs similaires
area: security
summary: Les e-mails provenant d’une adresse qui imite celle d’une personne avec qui vous échangez sont signalés dans la tâche correspondante, et les brouillons ne sont jamais envoyés à cette adresse.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## Ce que cette fonctionnalité détecte

Certaines arnaques proviennent d’une adresse qui ressemble à une adresse que vous connaissez : `examp1e.com` au lieu de `example.com`, `example-billing.com`, ou avec une seule lettre de différence. The Machine compare le domaine de chaque expéditeur à ceux des personnes avec qui vous échangez déjà. Si le nouveau domaine ressemble seulement à celui d’une adresse connue, il est considéré comme une imitation.

Le même nom avec une autre extension, comme `example.nl` et `example.com`, correspond à la même organisation, pas à une imitation. Les adresses de messagerie gratuites comme gmail.com ne sont jamais concernées.

## Dans une tâche

La tâche associée à un tel message l’indique clairement, par exemple : « Ce n’est pas Alex. Le message vient de examp1e.com, pas de example.com. » L’expéditeur s’affiche sous forme d’adresse seule, sans photo ni lien vers la personne imitée.

## Ce que The Machine ne fera pas

- Elle ne donne jamais de rôle à un expéditeur qui imite une adresse dans votre Graph.
- Elle ne le fusionne jamais avec la personne qu’il imite et ne le suggère jamais sous **Même personne ?**.
- Une réponse qu’elle prépare est envoyée à l’adresse enregistrée, pas à l’adresse imitatrice.

Vous gardez toujours le dernier mot : vous pouvez quand même attribuer un rôle à cette personne, la fusionner avec une autre ou écrire à n’importe quelle adresse.
