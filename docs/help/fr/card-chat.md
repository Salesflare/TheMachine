---
title: Chat de tâche
area: cards
summary: Posez une question sur une tâche ou modifiez son brouillon dans le chat associé à cette tâche.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 18a428fbe38a70e7
---
## Ouvrir le chat

Appuyez sur **Chat** sur la tâche ou sélectionnez-la dans la liste de la barre latérale. Touchez ou cliquez sur le titre pour le modifier.

## E-mails dans le chat

Chaque e-mail n’affiche que les nouveautés. Les messages précédents qu’il cite sont repliés sous **Messages précédents**. **Lire le fil** affiche les e-mails en entier.

## Ce qu’elle a fait

Pendant que The Machine travaille, **Je m’en occupe…** s’affiche au-dessus de la zone de message, et des points de saisie apparaissent dans le chat. Quand elle utilise le navigateur, une petite image de la page s’affiche aussi.

Chaque exécution apparaît sur une seule ligne discrète qui compte les étapes, par exemple « 12 éléments vérifiés ». Ouvrez-la pour voir chaque type d’étape une seule fois, avec son nombre d’occurrences : « Navigateur utilisé sur example.com · 7 ». Le site est indiqué, jamais son adresse, une commande ou un fichier.

Avec Claude Code, les étapes n’apparaissent pas dans le chat pendant le travail. La dernière étape s’affiche à la place au-dessus des points de saisie, par exemple « Lecture des e-mails », et rien ne s’affiche au-dessus de la zone de message.

Quand The Machine s’arrête pour vous poser une question, celle-ci apparaît aussi sur une ligne discrète, par exemple « Question : l’envoyer aujourd’hui ou lundi ? ». Votre message en dessous n’affiche que votre réponse.

## Que demander

Avant que vous écriviez, le chat peut vous proposer jusqu’à trois suggestions à partir de cette tâche, comme « Proposer mardi à 10 h à la place ». Touchez-en une pour l’ajouter à la zone de message, puis envoyez-la ou modifiez-la. Si aucune suggestion ne convient, rien ne s’affiche.

- Pour parler du fil, des personnes ou du contexte : « Qu’ont-ils demandé la dernière fois ? »
- Pour modifier le brouillon : « Raccourcis-le » ou « Mentionne la nouvelle date ».

Une question reçoit une réponse sans modifier le brouillon. Pour envoyer, utilisez les boutons de la tâche : le chat n’envoie jamais de brouillon dans la même réponse que celle qui l’a rédigé. Si votre demande ne concerne personne d’autre, comme nettoyer un document, le changement est effectué immédiatement, sans autre confirmation. Tout ce qui dépasse votre demande attend votre accord. Une tâche comportant plusieurs étapes reste ouverte tant qu’elles ne sont pas toutes terminées.

Sur ordinateur, appuyez sur Entrée ou Ctrl+Entrée (Cmd+Entrée sur Mac) pour envoyer, et sur Maj+Entrée pour passer à la ligne. Sur téléphone, utilisez le bouton d’envoi.

## En cas d’erreur

Signalez-le dans le chat, par exemple : « Cette personne n’est pas PDG » ou « Elle a quitté l’entreprise ». The Machine corrige l’information à la source : un rôle, une entreprise, un poste, l’étape d’un projet, le projet associé à la tâche ou une règle qu’elle a apprise. Le chat indique ce qui a changé, par exemple : « Correction : Sam est responsable des ventes, d’après sa signature e-mail », avec **Annuler**. Annuler restaure l’ancienne valeur, sauf si elle a changé depuis.

Les autres brouillons fondés sur l’information incorrecte sont rédigés à nouveau, un par un. Leur chat affiche **Nouveau brouillon après correction**. Les brouillons que vous avez modifiés ou approuvés, ainsi que ceux en cours d’envoi, restent inchangés. La réponse indique le nombre de brouillons concernés dans chaque catégorie.

Sur une page GBrain, seule la section de The Machine change. Le contenu que vous avez écrit reste tel quel. Si elle ne peut pas déterminer la source d’une information, elle l’apprend plutôt à partir de votre note.

## Modèle et réflexion

Sous la zone de message, le chat affiche son modèle et son niveau de réflexion, par exemple « GPT-6.2 Sol » et « Réflexion faible ». Touchez l’un ou l’autre pour en choisir un autre, uniquement pour ce chat. Les nouveaux chats utilisent les paramètres définis dans **Paramètres**, **Modèle** (voir [Modèle](model.md)).

L’option **Rapide**, au bas du menu des modèles, accélère les réponses des chats de tâche, pour un coût environ deux fois plus élevé (ou le double de votre forfait). Elle concerne les messages que vous envoyez et l’action **Faire**, dans tous vos chats de tâche, jamais le travail en arrière-plan. Elle est désactivée par défaut et grisée pour les modèles qui ne la prennent pas en charge.

## Arrêter une réponse

Pendant la rédaction d’une réponse, le bouton d’envoi devient **Arrêter**. Appuyez dessus pour mettre fin à la rédaction immédiatement et conserver le texte déjà écrit, qui sera marqué **Arrêté**. Écrivez un nouveau message pour continuer ou touchez **Réessayer**.

## Ajouter des fichiers

Touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le chat. Chaque fichier apparaît au-dessus de la zone de message. Touchez × pour le retirer. Un message peut contenir uniquement des fichiers.

- Les images (PNG, JPEG, GIF, WebP) de 5 Mo maximum sont envoyées au modèle sous forme d’images.
- Pour les PDF, les fichiers texte, les feuilles de calcul (CSV) et les fichiers Office de 10 Mo maximum, The Machine lit le contenu et peut joindre ces fichiers à un brouillon.
- Jusqu’à 5 fichiers par message.

Les fichiers restent sur votre Machine, chiffrés comme vos messages. Les fichiers que vous ajoutez sans jamais les envoyer sont supprimés après un jour. Une nouvelle tâche peut aussi contenir des fichiers, depuis **Nouvelle tâche** (voir [Créer une tâche soi-même](cards.md#make-one-yourself)).
