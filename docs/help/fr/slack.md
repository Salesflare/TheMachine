---
title: Slack
area: connections
summary: Les canaux et messages directs dont vous faites partie. N’envoie un message direct qu’après votre accord.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py
site: Connect, More sources, Remove
---
## Ce qu’elle lit

Les conversations dont vous êtes membre : canaux, canaux privés, messages directs et messages de groupe, les 7 derniers jours au moment de la connexion, puis tout ce qui est nouveau. Elle ne rejoint jamais un canal et n’ouvre jamais une conversation d’elle-même.

Les personnes apparaissent sous leur nom et les apps sous le leur, jamais sous un ID Slack. Une personne dont le compte Slack n’existe plus apparaît comme ancien utilisateur de Slack.

## Ce qu’elle peut envoyer

Un message direct à une personne, en votre nom, et seulement après votre accord sur la tâche. Elle ne publie jamais dans un canal.

## La connecter

Slack est lu via Maton, qui détient la connexion Slack.

1. Connectez-vous sur maton.ai, connectez-y Slack et copiez votre clé API Maton depuis Home.
2. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources**, ouvrez Slack, collez la clé et appuyez sur **Se connecter**.
3. Sur votre propre ordinateur : lancez `assistant connect slack`, ou **Connexions**, **+ Ajouter**, Slack.

## La retirer

- Dans le tableau de bord : **Connexions**, ouvrez Slack, **Détails**, puis **Déconnecter**. Ce qu’elle a déjà importé reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté d’elle sur votre page de configuration.

## La désinstaller côté Slack

Retirez la connexion Slack dans Maton, et supprimez la clé API Maton que vous avez fournie. Un admin Slack peut aussi retirer l’app de l’espace de travail, sous Manage apps.
