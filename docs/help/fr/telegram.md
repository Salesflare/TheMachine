---
title: Telegram
area: connections
summary: Recevez vos tâches dans Telegram avec les mêmes boutons que sur le tableau de bord, grâce à votre propre bot. Facultatif.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
translated: a2b74e4831832977
---
## Fonctionnement

Recevez vos tâches dans Telegram, depuis votre propre bot et pendant vos [Heures de travail](work-hours.md). Chaque tâche comporte les mêmes boutons que sur le tableau de bord : **Faire**, **Mettre en attente**, **Demander des modifications**, **Marquer comme fait**, **Pas nécessaire** et **Envoyer** pour un message préparé. Pour que The Machine lise plutôt vos chats Telegram, consultez [Chats Telegram](telegram-chats.md).

C’est facultatif : l’application mobile envoie les mêmes tâches sous forme de notifications.

## Ce qui peut être envoyé

Uniquement des messages qui vous sont destinés, depuis votre propre bot. Tout message destiné à quelqu’un d’autre doit encore être approuvé dans la tâche.

## Connecter Telegram

Sur une Machine hébergée :

1. Dans Telegram, envoyez un message à @BotFather, puis envoyez /newbot. Copiez le jeton qu’il vous donne.
2. Sur votre page de configuration, sous **Ajouter d’autres intégrations à tout moment**, ouvrez Telegram, collez le jeton et appuyez sur **Ajouter mon bot**.

Vous pouvez l’ajouter quand vous le souhaitez.

Sur votre propre ordinateur, l’installateur vous le demande. Vous pouvez aussi exécuter `assistant telegram on` avec votre identifiant utilisateur Telegram.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Déconnecter Telegram** sur votre page de configuration. Votre bot et son jeton sont supprimés de votre Machine.
- Sur votre propre ordinateur : `assistant telegram off`. Ajoutez `--remove-bot` pour supprimer aussi le bot.

## Supprimer le bot dans Telegram

Envoyez un message à @BotFather, puis envoyez /deletebot et sélectionnez votre bot.
