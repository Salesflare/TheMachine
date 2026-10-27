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

1. Dans Shortcut, ouvrez Settings, Account, API Tokens, et créez un jeton.
2. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources** et ouvrez Shortcut. Sur votre propre ordinateur : **Connexions**, **+ Ajouter**, Shortcut, ou `assistant connect shortcut`.
3. Indiquez l’adresse ou le slug de votre espace de travail et collez le jeton, puis appuyez sur **Se connecter**.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Shortcut, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le révoquer dans Shortcut

Supprimez le jeton sur la même page API Tokens.
