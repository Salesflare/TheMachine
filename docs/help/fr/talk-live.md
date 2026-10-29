---
title: Parler en direct
area: cards
summary: Une conversation à voix haute avec The Machine à propos d’une tâche, avec la voix d’OpenAI. Elle travaille dans le chat de la tâche, mais n’envoie jamais rien.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Lancer une conversation

Dans le chat d’une tâche, touchez l’onde à côté du micro. Autorisez le micro si votre navigateur le demande. Quand la barre affiche **En direct**, parlez comme lors d’un appel. The Machine répond à voix haute, et vous pouvez parler par-dessus pour l’interrompre.

Elle connaît la tâche où vous êtes : ses messages, son brouillon et son chat. Elle peut aussi consulter vos autres tâches.

La barre a **Couper le micro** et **Fin**. Une conversation dure jusqu’à 10 minutes. Une minute avant la fin, le minuteur montre le temps restant. Relancez-la pour continuer.

## Rien n’est envoyé depuis une conversation

Quand vous demandez quelque chose, comme « écris une réponse pour dire que jeudi me va » ou « mets ça en attente jusqu’à lundi », The Machine le transmet au chat de la tâche, comme si vous l’aviez tapé. Le chat suit ses règles habituelles : il peut modifier le brouillon ou mettre la tâche en attente, mais un brouillon attend votre **Approuver**.

Dire « oui » ou « envoie-le » ne fait rien. Seul votre appui sur **Approuver** envoie.

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
