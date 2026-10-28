---
title: Chat d’une tâche
area: cards
summary: Posez une question sur une tâche ou changez son brouillon, dans un chat propre à cette tâche.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py
order: 4
---
## L’ouvrir

Sur un téléphone, appuyez sur le titre de la tâche. Sur ordinateur, utilisez le lien du chat de la tâche ou **Voir dans le chat ›**. Sur ordinateur, cliquer sur le titre renomme la tâche.

## Quoi demander

- Sur le fil, les personnes ou le contexte : « Qu’ont-ils demandé la dernière fois ? »
- Pour changer le brouillon : « Fais plus court » ou « Mentionne la nouvelle date ».

Une question reçoit une réponse et laisse le brouillon tel quel. Les approbations restent sur les boutons de la tâche : le chat n’envoie jamais un brouillon dans la réponse qui l’a rédigé.

Sur ordinateur, Entrée ou Ctrl+Entrée (Cmd+Entrée sur Mac) envoie, et Maj+Entrée passe à la ligne. Sur un téléphone, utilisez le bouton d’envoi.

## Modèle et réflexion

Sous la zone de message, le chat affiche son modèle et son niveau de réflexion, comme « GPT-6.1 Sol » et « Réflexion faible ». Appuyez sur l’un ou l’autre pour en choisir un autre pour ce chat seulement. Les nouveaux chats utilisent ce que vous avez réglé dans **Paramètres**, **Modèle** (voir [Modèle](model.md)).

## Arrêter une réponse

Pendant qu’une réponse s’écrit, le bouton d’envoi devient **Arrêter**. Arrêter la termine tout de suite et garde ce qui est déjà écrit, marqué **Arrêté**. Écrivez un nouveau message pour continuer, ou appuyez sur **Réessayer**.

## Ajouter des fichiers

Appuyez sur le trombone, collez une capture d’écran, ou déposez des fichiers sur le chat. Chaque fichier s’affiche au-dessus de la zone de message, et × le retire. Un message peut ne contenir que des fichiers.

- Les images (PNG, JPEG, GIF, WebP) jusqu’à 5 Mo vont au modèle sous forme d’images.
- Les PDF, textes, CSV, JSON et fichiers Office jusqu’à 10 Mo sont des fichiers que The Machine lit, et peut joindre à un brouillon.
- Jusqu’à 5 fichiers par message.

Les fichiers restent sur votre Machine, dans son dossier de données, chiffrés comme vos messages. Les fichiers ajoutés mais jamais envoyés sont supprimés au bout d’un jour. Une nouvelle tâche peut aussi avoir des fichiers, depuis **Nouvelle tâche** (voir [En créer une vous-même](cards.md#make-one-yourself)).
