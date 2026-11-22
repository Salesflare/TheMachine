---
title: Slack
area: connections
summary: Les canaux et messages privés auxquels vous participez. N’envoie un message privé qu’après votre approbation.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
translated: 23f9e98f4680d23c
---
## Ce qu’elle lit

Les conversations auxquelles vous participez : canaux, canaux privés, messages privés et messages de groupe. Elle lit les 7 derniers jours au moment de la connexion, puis tous les nouveaux messages. Elle ne rejoint jamais un canal et n’ouvre jamais une conversation d’elle-même. Elle consulte un canal peu actif environ une fois par jour. Si une tâche a besoin des messages les plus récents, The Machine les lit immédiatement.

Environ un an d’anciens messages est ensuite importé progressivement dans [l’historique](history.md).

Les personnes apparaissent sous leur nom, tout comme les applications, jamais sous un identifiant Slack. Si le compte Slack d’une personne a été supprimé, elle apparaît comme un ancien utilisateur Slack.

## Ce qu’elle peut envoyer

Un message privé à une personne, en votre nom, et seulement après votre approbation sur la tâche. Une réponse au message Slack à l’origine d’une tâche est publiée dans le fil de ce message, dans le message privé ou le canal correspondant. Le brouillon indique **Dans le fil**. Elle ne publie jamais de nouveau message dans un canal.

## Ce qu’elle conserve

Les données qu’elle lit restent sur votre Machine jusqu’à ce que vous les supprimiez ou supprimiez la Machine. Le service d’hébergement ne conserve aucune copie de vos messages ni aucune connexion Slack, et aucun modèle d’IA n’est entraîné avec vos données Slack. The Machine utilise l’IA, qui peut se tromper. Vous voyez donc chaque message avant son envoi.

## La connecter

1. Sélectionnez **Connexions**, **Chat**, **Slack**, puis **Se connecter avec Slack**, et autorisez l’accès dans Slack. Sur votre propre ordinateur, associez d’abord The Machine à votre compte sur themachine.computer.
2. Les nouveaux messages et les messages privés sont importés en premier. Slack limite la lecture des applications à environ une conversation par minute. Les anciens messages sont donc importés progressivement sur quelques heures.

Vous pouvez aussi utiliser une clé API Maton : connectez-vous sur maton.ai, connectez Slack depuis ce site et copiez votre clé API Maton depuis Home. Ouvrez ensuite **Ou utilisez une clé API Maton** sous Slack et collez-la, ou exécutez `assistant connect slack` sur votre propre ordinateur. Une connexion Slack via Maton continue de fonctionner comme avant.

## La supprimer

- Dans le tableau de bord : sélectionnez **Connexions**, ouvrez Slack, puis sélectionnez **Détails** et **Déconnecter**. Les données déjà importées restent.
- Sur une Machine hébergée, vous pouvez aussi sélectionner **Retirer** à côté de Slack sur votre page de configuration.

## La désinstaller de Slack

Si vous vous êtes connecté avec Slack, ouvrez la page Manage apps de votre espace de travail dans Slack et supprimez The Machine. Elle cesse immédiatement de lire les messages et vous demande de vous connecter à nouveau. Les données déjà importées restent. Si vous avez utilisé Maton, supprimez la connexion Slack dans Maton et supprimez la clé API Maton que vous avez fournie. Un administrateur Slack peut aussi supprimer l’une ou l’autre application de l’espace de travail depuis Manage apps.
