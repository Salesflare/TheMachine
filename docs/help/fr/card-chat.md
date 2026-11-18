---
title: Chat d’une tâche
area: cards
summary: Posez des questions sur une tâche ou modifiez son brouillon dans un chat associé à cette tâche.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 340b9cfc0e3a424d
---
## Ouvrir le chat

Sur téléphone, touchez le titre de la tâche. Sur ordinateur, cliquez sur **Voir dans le chat ›** ou sur le lien du chat de la tâche. Cliquer sur le titre sur ordinateur renomme la tâche.

## E-mails dans le chat

Chaque e-mail n’affiche que les nouveautés qu’il contient. Les messages précédents qu’il cite sont repliés sous **Messages précédents**. **Lire le fil** ouvre les e-mails en entier.

## Ce qu’elle a fait

Chaque exécution apparaît sous la forme d’une ligne discrète, comme « 12 éléments vérifiés ». Ouvrez-la pour voir une seule fois chaque type d’étape, avec son nombre d’occurrences : « Navigateur utilisé sur example.com · 7 ». La ligne indique le nom du site, jamais l’adresse, une commande ou un fichier.

Quand elle s’arrête pour vous poser une question, celle-ci apparaît aussi sous la forme d’une ligne discrète, comme « Question posée : l’envoyer aujourd’hui ou lundi ? ». Votre message en dessous ne montre que votre réponse.

## Que demander

Avant que vous écriviez, le chat peut proposer jusqu’à trois suggestions à toucher, générées à partir de cette tâche, comme « Proposer mardi à 10 h à la place ». Touchez-en une pour l’ajouter au champ de message, où vous pouvez l’envoyer ou la modifier. Si aucune suggestion ne convient, le chat n’en propose pas.

- À propos du fil, des personnes ou du contexte : « Qu’ont-ils demandé la dernière fois ? »
- Pour modifier le brouillon : « Raccourcis-le » ou « Mentionne la nouvelle date ».

Une question reçoit une réponse sans modifier le brouillon. Pour envoyer, utilisez les boutons de la tâche : le chat n’envoie jamais de brouillon dans la même réponse que celle qui l’a rédigé. Une modification demandée qui n’atteint personne d’autre, comme le nettoyage d’un document, est faite immédiatement, sans confirmation supplémentaire. Tout ce qui dépasse votre demande attend votre accord. Une tâche comportant plusieurs étapes reste ouverte jusqu’à ce qu’elles soient toutes terminées.

Sur ordinateur, Enter ou Ctrl+Enter (Cmd+Enter sur Mac) envoie le message. Shift+Enter crée une nouvelle ligne. Sur téléphone, utilisez le bouton d’envoi.

## En cas d’erreur

Signalez-le dans le chat, par exemple : « Ce n’est pas le PDG » ou « Cette personne a quitté l’entreprise ». The Machine corrige l’information à la source : un poste, une entreprise, un titre, l’étape d’un projet, le projet de la tâche ou une règle qu’elle a apprise. Le chat indique ce qui a changé, par exemple : « Corrigé : Sam est directeur des ventes, d’après sa signature d’e-mail », avec **Annuler**. Annuler rétablit l’ancienne valeur, sauf si elle a changé depuis.

Les autres brouillons créés à partir de la valeur erronée sont rédigés à nouveau, un par un. Leur chat indique **Brouillon repris après correction**. Les brouillons que vous avez modifiés ou approuvés, ainsi que ceux en cours d’envoi, restent inchangés. La réponse indique combien il y en a dans chaque catégorie.

Sur une page GBrain, seule la section de The Machine change. Votre texte reste tel quel. Si The Machine ne peut pas déterminer l’origine d’une information, elle l’apprend plutôt à partir de votre note.

## Modèle et réflexion

Sous le champ de message, le chat affiche son modèle et son niveau de réflexion, par exemple « GPT-6.2 Sol » et « Réflexion faible ». Touchez l’un ou l’autre pour en choisir un autre, uniquement pour ce chat. Les nouveaux chats utilisent vos réglages dans **Paramètres**, sous **Modèle** (voir [Modèle](model.md)).

**Rapide**, au bas du menu des modèles, permet aux chats de tâche de répondre plus vite, pour un coût environ deux fois plus élevé (ou deux fois plus de votre forfait). Cette option concerne les messages que vous envoyez et l’action **Faire**, dans tous vos chats de tâche, jamais les tâches exécutées en arrière-plan. Elle est désactivée par défaut et grisée pour les modèles qui ne la prennent pas en charge.

## Arrêter une réponse

Pendant la rédaction d’une réponse, le bouton d’envoi devient **Arrêter**. Touchez-le pour interrompre immédiatement la réponse et conserver ce qui a déjà été écrit, marqué **Arrêté**. Écrivez un nouveau message pour continuer ou touchez **Réessayer**.

## Ajouter des fichiers

Touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le chat. Chaque fichier apparaît au-dessus du champ de message. Touchez × pour le retirer. Un message peut contenir uniquement des fichiers.

- Les images (PNG, JPEG, GIF, WebP) de 5 MB maximum sont envoyées au modèle sous forme d’images.
- Pour les PDF, les fichiers texte, les feuilles de calcul (CSV) et les fichiers Office de 10 MB maximum, The Machine les lit et peut les joindre à un brouillon.
- Jusqu’à 5 fichiers par message.

Les fichiers restent sur votre Machine, chiffrés comme vos messages. Les fichiers ajoutés mais jamais envoyés sont supprimés après un jour. Une nouvelle tâche peut aussi contenir des fichiers, depuis **Nouvelle tâche** (voir [Créer une tâche](cards.md#make-one-yourself)).
