---
title: Shortcut
area: connections
summary: Stories dont l’état change, avec leurs responsables et leurs échéances. Lecture seule.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## Ce qu’elle lit

Les stories de votre espace de travail Shortcut dont l’état change, avec leurs responsables et leurs échéances.

## Ce qu’elle peut faire

Elle ne modifie rien dans Shortcut. Elle se contente de lire.

## Connecter Shortcut

1. Dans le tableau de bord : **Connexions**, **Projets et code**, Shortcut. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Shortcut. Sur votre propre ordinateur, associez-la d’abord à votre compte.
2. Appuyez sur **Se connecter avec Shortcut** et autorisez l’accès en lecture. Elle ne demande à Shortcut qu’un accès en lecture.
3. De retour dans The Machine, elle vérifie immédiatement la connexion et indique sous quelle identité elle s’est connectée et dans quel espace de travail.

Vous avez plusieurs espaces de travail Shortcut ? Sélectionnez d’abord celui que vous voulez dans Shortcut. Pour en connecter un autre, ajoutez Shortcut de nouveau.

## Coller un jeton à la place

Sous **Ou collez un jeton d’API**, appuyez sur **Obtenir votre jeton**. Shortcut ouvre la page des jetons d’API dans un nouvel onglet : créez un jeton, copiez-le, collez-le, puis appuyez sur **Connecter**. Sur votre propre ordinateur, `assistant connect shortcut` vous le demande aussi. Un jeton donne un accès complet à votre compte, mais The Machine ne fait que lire avec ce jeton.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Shortcut, puis **Détails** et **Déconnecter**. Les données déjà importées restent disponibles.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Shortcut sur la page de configuration.

## Révoquer l’accès dans Shortcut

Pour un jeton collé : supprimez-le sur la page des jetons d’API. Si vous vous êtes connecté, déconnecter Shortcut ici met fin à toute lecture.
