---
title: Trello
area: connections
summary: Modifications de cartes, commentaires et activité sur un tableau Trello. Il se contente de lire.
covers: connector:trello
code: connectors/trello.py
site: Connect, More sources, Remove
---
## Ce qu’il lit

Les modifications de cartes, les commentaires et l’activité sur un tableau Trello par connexion. Il ne marque jamais un tableau comme vu.

## Ce qu’il peut faire

Rien dans Trello. Il se contente de lire.

## Le connecter

1. Sur trello.com/power-ups/admin, créez un Power-Up avec le nom de votre choix.
2. Ouvrez sa page de clé API et copiez la clé API (pas le secret).
3. Cliquez sur le lien Token à côté, autorisez l’accès en lecture et copiez le jeton.
4. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources** et ouvrez Trello. Sur votre propre ordinateur : **Connexions**, **+ Ajouter**, Trello, ou `assistant connect trello`.
5. Indiquez l’adresse du tableau, la clé API et le jeton, puis appuyez sur **Se connecter**.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez le tableau, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de lui sur votre page de configuration.

## Le révoquer dans Trello

Révoquez le jeton dans les paramètres de votre compte Trello, sous Applications, ou supprimez le Power-Up.
