---
title: Parler en direct
area: cards
summary: Une conversation à voix haute avec The Machine à propos d’une tâche, avec la voix d’OpenAI. Elle peut chercher des choses et faire des suggestions, mais n’envoie jamais rien.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Lancer une conversation

Dans le chat d’une tâche, touchez l’onde à côté du micro. Autorisez le micro si votre navigateur le demande. Quand la barre affiche **En direct**, parlez comme lors d’un appel. The Machine répond à voix haute.

Elle connaît la tâche où vous êtes : ses messages et son brouillon. Elle peut aussi consulter vos autres tâches.

La barre a **Couper le micro** et **Fin**. Une conversation dure jusqu’à 10 minutes. Une minute avant la fin, le minuteur montre le temps restant. Relancez-la pour continuer.

## Rien n’est envoyé depuis une conversation

The Machine ne peut rien envoyer, modifier ni approuver pendant que vous parlez. Quand vous demandez quelque chose, comme « écris une réponse pour dire que jeudi me va », elle affiche la demande au-dessus de la barre. Touchez **Envoyer au chat** pour la confier au chat. Ce que le chat rédige attend ensuite votre **Approuver**, comme toujours.

Dire « oui » ou « envoie-le » ne fait rien. Seuls vos touchers comptent.

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
