---
title: Telegram
area: connections
summary: Recevez vos tâches sur Telegram, avec les mêmes boutons que dans le tableau de bord, via votre propre bot. Facultatif.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## Ce qu’il fait

Telegram est un moyen de recevoir vos tâches, pas une source que The Machine lit. Votre propre bot envoie chaque tâche pendant vos [heures de travail](work-hours.md), avec les mêmes boutons que dans le tableau de bord : **Faire**, **Mettre en attente**, **Modifier**, **Marquer comme fait**, **Pas nécessaire**, et **Envoyer** pour un message préparé.

Telegram est facultatif. Le tableau de bord en app sur téléphone envoie les mêmes tâches en notifications.

## Ce qu’il peut envoyer

Seulement des messages pour vous, depuis votre propre bot. Un message à quelqu’un d’autre demande toujours votre accord sur la tâche.

## Le connecter

Sur une Machine hébergée :

1. Dans Telegram, écrivez à @BotFather et envoyez /newbot. Copiez le jeton qu’il vous donne.
2. Sur votre page de configuration, sous **Ajoutez-en d’autres à tout moment**, ouvrez Telegram, collez le jeton et appuyez sur **Ajouter mon bot**.

Il ne fait pas partie de la configuration : ajoutez-le quand vous voulez. Votre tableau de bord le suggère dès qu’une tâche mise en attente ne pourrait revenir que là.

Sur votre propre ordinateur, l’installateur le demande, ou lancez `assistant telegram on` avec votre identifiant d’utilisateur Telegram.

## Le retirer

- Sur une Machine hébergée : appuyez sur **Déconnecter Telegram** sur votre page de configuration. Votre bot et son jeton sont retirés de votre serveur.
- Sur votre propre ordinateur : `assistant telegram off`. Ajoutez `--remove-bot` pour oublier aussi le bot.

## Supprimer le bot dans Telegram

Écrivez à @BotFather, envoyez /deletebot et choisissez votre bot.
