---
title: Parler en direct
area: cards
summary: Une conversation à voix haute avec The Machine à propos d’une tâche, avec la voix d’OpenAI. Elle travaille dans le chat de la tâche et n’envoie un brouillon qu’après votre oui.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Lancer une conversation

Dans le chat d’une tâche, touchez l’onde à côté du micro. Autorisez le micro si votre navigateur le demande. Quand la barre affiche **En direct**, parlez comme lors d’un appel. The Machine répond à voix haute, et vous pouvez parler par-dessus pour l’interrompre.

Elle connaît la tâche où vous êtes : ses messages, son brouillon et son chat. Elle peut aussi consulter vos autres tâches.

La barre a **Couper le micro** et **Fin**. Dites au revoir, ou que vous avez fini, et elle s’arrête d’elle-même. Une conversation dure jusqu’à 10 minutes. Une minute avant la fin, le minuteur montre le temps restant. Relancez-la pour continuer.

## Passer en revue toutes vos tâches à voix haute

Touchez **Parler** dans la barre latérale (dans le menu sur un téléphone) pour passer en revue à la voix tout ce qui vous attend. The Machine dit combien il y en a et les prend une par une : d’abord **Prête**, puis **À décider**. Parler a sa propre page : une conversation du début à la fin, avec en haut la tâche dont elle parle, son brouillon et **Ouvrir le chat**. Elle ne vous fait pas passer de chat en chat.

Demandez-lui de lire un brouillon, de le modifier, de le reporter, de le marquer comme fait ou de passer à la suivante. L’envoi fonctionne comme dans le chat d’une tâche : un brouillon par question, après un oui clair. Ce que vous dites sur une tâche va dans le chat de cette tâche. Quand une nouvelle tâche arrive, elle la mentionne lors d’une pause.

Vous pouvez aller sur une autre page entre-temps : la barre reste en bas, et **Parler** dans la barre latérale vous y ramène. Cette conversation dure 30 minutes au plus.

## Demandez, et envoyez d’un oui

Quand vous demandez quelque chose, comme « écris une réponse pour dire que jeudi me va » ou « mets ça en attente jusqu’à lundi », The Machine le transmet au chat de la tâche, comme si vous l’aviez tapé. Le chat suit ses règles habituelles : il peut modifier le brouillon ou mettre la tâche en attente.

Le chat peut aussi chercher des choses, comme les horaires d’un magasin sur le web. Pendant ce temps, il affiche **Je m’en occupe…**, et vous pouvez continuer à parler. Quand la réponse est prête, The Machine vous la dit, avec l’endroit où elle l’a trouvée. Si vous demandez autre chose entre-temps, cela attend son tour.

Pour envoyer un brouillon, dites-le. The Machine demande d’abord, en précisant à qui et comment, par exemple « Envoyer cette réponse à Lotte par e-mail ? ». Sur un téléphone, elle lit d’abord tout le brouillon à voix haute. Répondez par un oui clair, dans n’importe quelle langue, et ce brouillon part.

- Elle ne demande que pour le brouillon affiché dans le chat. S’il change après la question, elle redemande.
- Si votre réponse n’est pas un oui clair, rien ne part et elle redemande. « Non » n’envoie rien.
- Un oui envoie toujours un seul brouillon. Pour en envoyer plusieurs, utilisez la revue des relances.
- Le chat affiche **Approuvé à la voix** avec **Annuler** pendant quelques secondes avant l’envoi.

Vous pouvez toujours appuyer sur **Approuver** à la place.

## Choisir une voix

Dans **Paramètres**, **Général**, sous **Saisie vocale**, choisissez à **Voix** comment The Machine sonne. Touchez lecture pour entendre un extrait. **Cedar** est la voix par défaut. La voix Cove de ChatGPT n’est pas disponible pour parler en direct.

## Une trace dans le chat

Ce que vous dites tous les deux est écrit dans le chat de la tâche, sous une ligne **Conversation en direct**. Vous pouvez le relire plus tard.

## Ce qu’il vous faut

Parler en direct utilise la voix en temps réel d’OpenAI, donc OpenAI doit être configuré dans OpenClaw :

- Une connexion ChatGPT : incluse dans votre forfait, si votre forfait y donne accès.
- Une clé API OpenAI : OpenAI facture votre clé à la minute de conversation, et la barre l’indique. Quand les deux sont configurés, OpenClaw utilise la clé.

**Paramètres**, **Général**, **Saisie vocale** indique si Parler en direct est prêt. Sans OpenAI, l’onde n’apparaît pas. Votre audio va directement de votre navigateur à OpenAI. Votre clé n’atteint jamais le navigateur.

## Quand ça ne marche pas

- **Le micro est bloqué** : autorisez le micro pour ce site dans les paramètres de votre navigateur.
- **Parler en direct n’a pas pu démarrer** : vérifiez OpenAI dans OpenClaw, puis réessayez.
- **Parler en direct a perdu la connexion** : relancez-le. Ce qui a été dit jusque-là reste dans le chat.
