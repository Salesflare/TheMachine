---
title: Shortcut
area: connections
summary: Les stories qui changent d’état, avec leurs responsables et leurs échéances. Il ne fait que lire.
covers: connector:shortcut
code: connectors/shortcut.py
site: Connect, More sources, Remove
---
## Ce qu’il lit

Les stories de votre espace de travail Shortcut qui changent d’état, avec leurs responsables et leurs échéances.

## Ce qu’il peut faire

Rien dans Shortcut. Il ne fait que lire, même si les jetons Shortcut permettent plus.

## Le connecter

1. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources** et ouvrez Shortcut. Sur votre propre ordinateur : **Connexions**, **+ Ajouter**, Shortcut, ou `assistant connect shortcut`.
2. Appuyez sur **Obtenir votre jeton**. Shortcut ouvre sa page API Tokens dans un nouvel onglet : créez un jeton et copiez-le.
3. Collez-le et appuyez sur **Se connecter**. Le jeton est vérifié tout de suite, avec le nom et l’espace de travail connectés.

Dans plusieurs espaces Shortcut ? Un jeton appartient à un seul espace : passez d’abord à celui-ci dans Shortcut.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Shortcut, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le révoquer dans Shortcut

Supprimez le jeton sur la même page API Tokens.
