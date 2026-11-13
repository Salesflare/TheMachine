---
title: Slack
area: connections
summary: Les canaux et messages directs dont vous faites partie. N’envoie un message direct qu’après votre accord.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## Ce qu’elle lit

Les conversations dont vous êtes membre : canaux, canaux privés, messages directs et messages de groupe, les 7 derniers jours au moment de la connexion, puis tout ce qui est nouveau. Elle ne rejoint jamais un canal et n’ouvre jamais une conversation d’elle-même. Un canal calme est lu environ une fois par jour ; quand une tâche a besoin de ses derniers messages, The Machine le lit tout de suite.

Environ un an d’anciens messages arrive ensuite, petit à petit, comme [historique](history.md).

Les personnes apparaissent sous leur nom et les apps sous le leur, jamais sous un ID Slack. Une personne dont le compte Slack n’existe plus apparaît comme ancien utilisateur de Slack.

## Ce qu’elle peut envoyer

Un message direct à une personne, en votre nom, et seulement après votre accord sur la tâche. Une réponse au message Slack d’où vient une tâche va dans le fil de ce message, dans le message direct ou le canal ; le brouillon indique **Dans le fil**. Elle ne lance jamais une nouvelle publication dans un canal.

## La connecter

1. **Connexions**, **Chat**, **Slack**, puis **Se connecter avec Slack**, et autorisez-la dans Slack. Sur votre propre ordinateur, associez-le d’abord à votre compte sur themachine.computer.
2. Les nouveaux messages et les messages directs arrivent d’abord. Slack laisse les apps lire environ une conversation par minute, les messages plus anciens arrivent donc en quelques heures.

Ou utilisez une clé API Maton : connectez-vous sur maton.ai, connectez-y Slack et copiez votre clé API Maton depuis Home. Ouvrez ensuite **Ou utilisez une clé API Maton** sous Slack et collez-la, ou lancez `assistant connect slack` sur votre propre ordinateur. Un Slack connecté via Maton continue de fonctionner tel quel.

## La retirer

- Dans le tableau de bord : **Connexions**, ouvrez Slack, **Détails**, puis **Déconnecter**. Ce qu’elle a déjà importé reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté d’elle sur votre page de configuration.

## La désinstaller côté Slack

Connectée avec Slack : ouvrez la page Manage apps de votre espace de travail dans Slack et retirez The Machine. Via Maton : retirez la connexion Slack dans Maton, et supprimez la clé API Maton que vous avez fournie. Un admin Slack peut aussi retirer l’une ou l’autre app de l’espace de travail, sous Manage apps.
