---
title: Chat d’une tâche
area: cards
summary: Posez des questions sur une tâche ou modifiez son brouillon dans le chat associé.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 64a15c6ce46c6679
---
## Ouvrir le chat

Sur un téléphone, touchez le titre de la tâche. Sur un ordinateur, cliquez sur **Voir dans le chat ›** ou sur le lien vers son chat. Cliquer sur le titre sur un ordinateur renomme la tâche.

## E-mails dans le chat

Chaque e-mail affiche uniquement ce qu’il contient de nouveau. Les messages précédents qu’il cite sont repliés sous **Messages précédents**. **Lire le fil** ouvre les e-mails dans leur intégralité.

## Ce qu’elle a fait

Pendant qu’elle travaille sur votre message, sa dernière étape s’affiche au-dessus des points de saisie, par exemple « Lecture de l’e-mail », comme dans la tâche pendant qu’elle se prépare. Quand elle utilise le navigateur, une petite image de la page s’affiche aussi.

Chaque exécution terminée s’affiche sur une seule ligne discrète, par exemple « 12 éléments vérifiés ». Ouvrez-la pour voir chaque type d’étape une seule fois, avec le nombre d’occurrences : « A utilisé le navigateur sur example.com · 7 ». Elle indique le nom du site, jamais l’adresse, une commande ou un fichier.

Quand elle s’arrête pour vous poser une question, celle-ci s’affiche aussi sur une ligne discrète, par exemple « A demandé : Envoyer aujourd’hui ou lundi ? ». Votre message en dessous ne montre que votre réponse.

## Que demander

Avant que vous écriviez, le chat peut proposer jusqu’à trois suggestions basées sur cette tâche, par exemple « Proposer mardi à 10 h à la place ». Touchez l’une d’elles pour l’ajouter au champ de message, puis envoyez-la ou modifiez-la. Si aucune suggestion pertinente ne s’applique, le chat n’en propose pas.

- À propos du fil, des personnes ou du contexte : « Qu’ont-ils demandé la dernière fois ? »
- Pour modifier le brouillon : « Raccourcis-le » ou « Mentionne la nouvelle date ».

Une question reçoit une réponse sans modifier le brouillon. Pour envoyer un message, utilisez les boutons de la tâche : le chat n’envoie jamais un brouillon dans la même réponse que celle où il l’a rédigé. Une modification que vous demandez et qui ne touche personne d’autre, comme corriger un document, est effectuée immédiatement, sans confirmation supplémentaire. Tout ce qui dépasse votre demande attend votre accord. Une tâche comportant plusieurs étapes reste ouverte tant qu’elles ne sont pas toutes terminées.

Sur un ordinateur, appuyez sur Entrée ou Ctrl+Entrée (Cmd+Entrée sur Mac) pour envoyer un message, et sur Maj+Entrée pour passer à la ligne. Sur un téléphone, utilisez le bouton d’envoi.

## En cas d’erreur

Signalez-le dans le chat, par exemple : « Ce n’est pas le PDG » ou « Cette personne a quitté l’entreprise ». The Machine corrige l’information à la source : un rôle, une entreprise, un intitulé, l’étape d’un projet, le projet de la tâche ou une règle qu’elle a apprise. Le chat indique ce qui a changé, par exemple : « Correction : Sam est responsable des ventes, d’après sa signature e-mail », avec **Annuler**. Cette action rétablit l’ancienne valeur, sauf si elle a changé depuis.

Vos autres brouillons qui reposent sur la mauvaise valeur sont rédigés à nouveau, un par un. Leur chat affiche **Nouveau brouillon après une correction**. Les brouillons que vous avez modifiés ou approuvés, ainsi que ceux en cours d’envoi, restent inchangés. La réponse indique combien il y en a de chaque type.

Sur une page GBrain, seule la section de The Machine est modifiée. Votre contenu reste intact. Quand elle ne peut pas savoir d’où vient une information, elle l’apprend plutôt à partir de votre note.

## Modèle et réflexion

Sous le champ de message, le chat affiche son modèle et son niveau de réflexion, par exemple « GPT-6.2 Sol » et « Réflexion faible ». Touchez l’un ou l’autre pour en choisir un autre pour ce chat uniquement. Les nouveaux chats utilisent les paramètres définis dans **Paramètres**, **Modèle** (voir [Modèle](model.md)).

**Rapide**, à la fin du menu des modèles, permet aux chats de tâche de répondre plus vite, pour un coût environ deux fois plus élevé (ou deux fois plus de votre forfait). Cette option couvre les messages que vous envoyez et l’action **Faire**, dans tous vos chats de tâche, mais pas le travail en arrière-plan. Elle est désactivée par défaut et grisée pour les modèles qui ne la prennent pas en charge.

## Arrêter une réponse

Pendant la rédaction d’une réponse, le bouton d’envoi devient **Arrêter**. Cette action met fin à la rédaction immédiatement et conserve le texte déjà écrit, marqué **Arrêté**. Écrivez un nouveau message pour continuer ou touchez **Réessayer**.

## Ajouter des fichiers

Touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le chat. Chaque fichier s’affiche au-dessus du champ de message. Touchez × pour le retirer. Un message peut contenir uniquement des fichiers.

- Les images (PNG, JPEG, GIF, WebP) de 5 Mo maximum sont envoyées au modèle comme images.
- Les PDF, fichiers texte, feuilles de calcul (CSV) et fichiers Office de 10 Mo maximum sont lus par The Machine, qui peut les joindre à un brouillon.
- Jusqu’à 5 fichiers par message.

Les fichiers restent sur votre Machine et sont chiffrés comme vos messages. Les fichiers que vous ajoutez sans jamais les envoyer sont supprimés au bout d’un jour. Vous pouvez aussi joindre des fichiers à une nouvelle tâche depuis **Nouvelle tâche** (voir [Créer une tâche soi-même](cards.md#make-one-yourself)).
