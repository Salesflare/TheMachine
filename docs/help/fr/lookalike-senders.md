---
title: Expéditeurs qui imitent vos contacts
area: security
summary: Les e-mails provenant d’une adresse qui imite quelqu’un avec qui vous échangez sont signalés dans la tâche correspondante, et les brouillons ne sont jamais envoyés à cette adresse.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## Ce que cette fonction détecte

Certaines arnaques proviennent d’une adresse qui ressemble à une adresse que vous connaissez : `examp1e.com` au lieu de `example.com`, `example-billing.com`, une lettre différente ou deux lettres inversées. The Machine compare le domaine de chaque expéditeur à ceux avec lesquels vous échangez déjà.

Parmi deux adresses qui se ressemblent, la vraie est celle à laquelle vous avez écrit, que vous avez rencontrée ou que vous avez configurée vous-même, même si l’autre vous a écrit en premier. Si aucune ne se distingue de cette façon, la plus récente est considérée comme l’adresse imitatrice.

Un même nom avec une autre extension, comme `example.nl` à côté de `example.com`, désigne la même organisation, pas un imitateur. Les services de messagerie gratuits, comme gmail.com, ne sont jamais concernés.

## Dans une tâche

Une tâche concernant un tel message le signale clairement, par exemple : « Ce n’est pas Alex. Le message vient de examp1e.com, et non de example.com. » L’expéditeur apparaît sous forme d’adresse seule, sans photo ni lien vers la personne qu’il imite.

## Ce que The Machine ne fera pas

- Elle n’attribue jamais de rôle à un expéditeur imitateur dans votre Graph et ne fait jamais de son domaine l’organisation d’un projet.
- Elle ne fusionne jamais cet expéditeur avec la personne qu’il imite, même s’ils écrivent dans la même conversation sous le même nom, et ne le suggère jamais sous **Même personne ?**.
- Une réponse qu’elle prépare est envoyée à l’adresse enregistrée, pas à celle de l’imitateur.

Votre choix reste toujours prioritaire : vous pouvez quand même lui attribuer un rôle, le fusionner avec une autre personne ou écrire à n’importe quelle adresse.
