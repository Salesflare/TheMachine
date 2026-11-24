---
title: Chat d’une tâche
area: cards
summary: Posez une question sur une tâche ou modifiez son brouillon dans un chat associé à cette tâche.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
translated: 224f6163a84e80ca
---
## Ouvrir le chat

Appuyez sur **Chat** sur la tâche ou sélectionnez-la dans la liste de la barre latérale. Appuyez ou cliquez sur le titre pour le modifier.

## E-mails dans le chat

Chaque e-mail n’affiche que les nouveautés qu’il contient. Les messages précédents qu’il cite sont repliés sous **Messages précédents**. **Lire le fil** ouvre les e-mails dans leur intégralité.

## Ce qu’elle a fait

Pendant qu’elle traite votre message, sa dernière étape s’affiche au-dessus des points de saisie, par exemple « Lecture de l’e-mail », comme sur la tâche pendant sa préparation. Quand elle utilise le navigateur, une petite image de la page s’affiche aussi.

Chaque exécution terminée apparaît sur une seule ligne discrète, par exemple « 12 éléments vérifiés ». Ouvrez-la pour voir chaque type d’étape une seule fois, avec son nombre d’occurrences : « Navigateur utilisé sur example.com · 7 ». Elle indique le nom du site, jamais son adresse, une commande ou un fichier.

Quand elle s’arrête pour vous poser une question, celle-ci apparaît aussi sur une ligne discrète, par exemple « Question posée : l’envoyer aujourd’hui ou lundi ? ». Le message en dessous ne contient que votre réponse.

## Que demander

Avant que vous écriviez, le chat peut proposer jusqu’à trois suggestions à partir de cette tâche, par exemple « Proposer mardi à 10 h à la place ». Appuyez sur une suggestion pour l’ajouter à la zone de message, où vous pouvez l’envoyer ou la modifier. Si aucune suggestion ne convient, il n’y en a pas.

- À propos du fil, des personnes ou du contexte : « Qu’ont-ils demandé la dernière fois ? »
- Pour modifier le brouillon : « Raccourcir » ou « Mentionner la nouvelle date ».

Une question reçoit une réponse sans modifier le brouillon. Pour l’envoi, utilisez les boutons de la tâche : le chat n’envoie jamais un brouillon dans la même réponse que celle où il l’a rédigé. Une modification que vous demandez et qui ne parvient à personne d’autre, comme la mise au propre d’un document, est effectuée tout de suite, sans confirmation supplémentaire. Toute action qui dépasse votre demande attend votre accord. Une tâche qui comporte plusieurs étapes reste ouverte tant qu’elles ne sont pas toutes terminées.

Sur ordinateur, appuyez sur Entrée ou Ctrl+Entrée (Cmd+Entrée sur Mac) pour envoyer, et sur Maj+Entrée pour passer à la ligne. Sur téléphone, utilisez le bouton d’envoi.

## En cas d’erreur

Signalez-le dans le chat, par exemple « Ce n’est pas le PDG » ou « Cette personne a quitté l’entreprise ». The Machine corrige l’information à la source : un rôle, une entreprise, un titre, l’étape d’un projet, le projet associé à la tâche ou une règle qu’elle a apprise. Le chat indique ce qui a changé, par exemple « Corrigé : Sam est responsable des ventes, d’après sa signature e-mail », avec **Annuler**. Cette action rétablit l’ancienne valeur, sauf si elle a changé depuis.

Les autres brouillons fondés sur la valeur erronée sont recréés un par un. Leur chat affiche **Nouveau brouillon après correction**. Les brouillons que vous avez modifiés ou approuvés, ainsi que ceux en cours d’envoi, restent tels quels. La réponse indique leur nombre respectif.

Sur une page GBrain, seule la section de The Machine est modifiée. Ce que vous avez écrit reste inchangé. Quand elle ne peut pas déterminer la source d’une information, elle l’apprend plutôt à partir de votre remarque.

## Modèle et réflexion

Sous la zone de message, le chat affiche son modèle et son niveau de réflexion, par exemple « GPT-6.2 Sol » et « Réflexion faible ». Appuyez sur l’un ou l’autre pour en choisir un autre pour ce chat uniquement. Les nouveaux chats utilisent les paramètres définis dans **Paramètres**, sous **Modèle** (voir [Modèle](model.md)).

**Rapide**, au bas du menu des modèles, accélère les réponses dans les chats de tâches, pour un coût environ deux fois plus élevé (ou une consommation deux fois supérieure de votre forfait). Cette option concerne les messages que vous envoyez et l’action Faire, dans tous vos chats de tâches, jamais le travail en arrière-plan. Elle est désactivée par défaut et grisée pour les modèles qui ne la prennent pas en charge.

## Arrêter une réponse

Pendant la rédaction d’une réponse, le bouton d’envoi devient **Arrêter**. La réponse s’interrompt immédiatement et le texte déjà rédigé est conservé avec la mention **Arrêté**. Envoyez un nouveau message pour continuer ou appuyez sur **Réessayer**.

## Ajouter des fichiers

Appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le chat. Chaque fichier s’affiche au-dessus de la zone de message. Appuyez sur × pour le retirer. Un message peut contenir uniquement des fichiers.

- Les images (PNG, JPEG, GIF, WebP) jusqu’à 5 MB sont envoyées au modèle sous forme d’images.
- Les PDF, fichiers texte, feuilles de calcul (CSV) et fichiers Office jusqu’à 10 MB sont lus par The Machine et peuvent être joints à un brouillon.
- Jusqu’à 5 fichiers par message.

Les fichiers restent sur votre Machine et sont chiffrés comme vos messages. Les fichiers que vous ajoutez sans jamais les envoyer sont supprimés après un jour. Une nouvelle tâche peut aussi contenir des fichiers, depuis **Nouvelle tâche** (voir [Créer une tâche vous-même](cards.md#make-one-yourself)).
