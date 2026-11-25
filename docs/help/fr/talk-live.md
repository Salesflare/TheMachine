---
title: Parler en direct
area: cards
summary: Une conversation orale avec The Machine au sujet d’une tâche, grâce à la voix d’OpenAI. Elle se déroule dans le chat de la tâche et n’envoie un brouillon qu’après votre confirmation.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: da63957f0556ff4f
---
## Commencer une conversation

Dans le chat d’une tâche, touchez l’icône d’onde à côté du micro et autorisez l’accès au micro si nécessaire. Quand la barre affiche **En direct**, parlez comme au téléphone. The Machine vous répond à voix haute. Parlez par-dessus elle pour l’interrompre.

Elle connaît cette tâche : ses messages, son brouillon et son chat. Elle peut aussi consulter vos autres tâches. Dites « marquer comme fait », « mettre en attente jusqu’à demain à 9 h » ou « pas nécessaire » pour qu’elle le fasse. Dites « non, pas ça » juste après pour annuler. Les heures suivent le fuseau horaire de vos [Heures de travail](work-hours.md).

Elle vous écoute dans la langue de l’application et dans les langues indiquées par votre navigateur. Les toux, le bruit et les autres langues ne reçoivent aucune réponse et n’apparaissent pas dans la transcription.

La barre comporte **Couper le micro** et **Terminer**. Dites au revoir pour mettre fin à la conversation. Une conversation dure jusqu’à 10 minutes, avec un compte à rebours pendant la dernière minute. Recommencez pour continuer.

## Parler de toutes vos tâches

Touchez **Parler** dans la barre latérale, ou dans le menu sur un téléphone. The Machine vous indique combien de tâches sont en attente, puis traite une par une celles de **Pour vous**, dans l’ordre affiché dans votre liste. Elle vous prévient quand une tâche marquée **En préparation…** est prête.

La fonction Parler a sa propre page : la tâche en cours s’affiche en haut, avec son brouillon et **Ouvrir le chat**.

Demandez-lui de lire un brouillon, de le modifier, de mettre la tâche en attente, de la marquer comme faite ou de passer à la suivante. Ce que vous dites à propos d’une tâche est ajouté à son chat. Elle signale les nouvelles tâches pendant une pause. Dites « ajouter une tâche pour… » pour en ajouter une sans perdre votre place.

Posez une question sur une personne, une organisation, un projet, une réunion ou une promesse : elle effectue une recherche et vous montre le résultat. Elle peut aussi écarter, renommer ou rouvrir des tâches, y compris celles marquées **Fait / écarté**. Pour toute autre demande, elle transmet la question au chat d’une nouvelle tâche et vous donne la réponse.

Elle se souvient de vos conversations précédentes. Demandez « qu’ai-je décidé pour le séminaire ? » et elle vous répond, en précisant quand vous l’avez dit. Seule la fonction Parler dans la barre latérale permet de le faire.

Vous pouvez utiliser d’autres pages entre-temps : la barre reste en bas et **Parler** vous ramène à la conversation. Celle-ci dure jusqu’à 30 minutes. Elle continue en arrière-plan sur ordinateur et Android. Sur iPhone, elle s’arrête quand l’application n’est plus à l’écran.

## Faire une demande et envoyer après confirmation

Demandez quelque chose, par exemple « rédige une réponse pour dire que jeudi me convient », et The Machine transmet votre demande au chat de la tâche comme si vous l’aviez écrite. Le chat suit ses règles habituelles.

Le chat peut aussi rechercher des informations, comme les horaires d’ouverture d’un magasin. Il indique qu’il est en train de chercher, et vous pouvez continuer à parler. Quand la réponse est prête, The Machine vous la donne et vous indique où elle l’a trouvée.

Pour envoyer un brouillon, dites-le. The Machine le lit à voix haute, en indiquant le destinataire, l’objet et le texte, puis vous demande, par exemple : « Envoyer cette réponse par e-mail à Sam ? ». Vous pouvez garder votre téléphone dans votre poche. Répondez clairement oui, par exemple « oui, envoie-la », pour envoyer le brouillon.

- Elle envoie exactement le brouillon qu’elle a lu. Si le brouillon change, elle le lit et vous demande à nouveau confirmation. Une question restée sans réponse pendant 3 minutes expire.
- Sans réponse clairement affirmative, rien n’est envoyé.
- Elle ne relit pas un brouillon que vous avez déjà vu ou entendu. Elle demande simplement, par exemple : « L’envoyer à Pat ? ».
- Dites « envoie tous ceux qui sont prêts » et elle nomme tout le monde dans une seule question. Une seule confirmation suffit pour tout envoyer.
- Après votre confirmation, la fonction Parler affiche **Annuler** avec un compte à rebours. Touchez ce bouton ou dites « annuler » ou « attendez ».
- Une fois le message envoyé, la fonction Parler dit « Envoyé. » et la tâche indique **Envoyé à**, le nom de la personne et l’heure. En cas d’échec, la fonction Parler vous en indique la raison. Demandez « est-ce envoyé ? » à tout moment : elle vérifie et ne devine jamais.

Vous pouvez aussi toucher **Approuver**.

Dites « faire » pour lancer The Machine sur la tâche, comme avec **Faire**. Dites « signaler un bug » pour envoyer un rapport de bug, comme avec **Signaler un bug** dans l’Aide.

## Choisir une voix

Dans **Paramètres**, **Général**, sous **Saisie vocale**, choisissez une **Voix**, puis touchez Lecture pour l’écouter. **Cedar** est la voix par défaut. La voix Cove de ChatGPT n’est pas disponible.

## Un historique dans le chat

Tout ce qui est dit est ajouté au chat de la tâche, sous une ligne **Conversation en direct**, pour que vous puissiez le relire plus tard.

## Ce dont vous avez besoin

La conversation en direct utilise la voix d’OpenAI. Votre Machine doit donc avoir l’un des éléments suivants :

- Une connexion à ChatGPT : incluse dans les forfaits qui la proposent.
- Une clé API OpenAI : OpenAI facture son utilisation à la minute, et la barre vous l’indique. Si vous avez les deux, votre Machine utilise la clé.

**Paramètres**, **Général**, **Saisie vocale** indique si la conversation en direct est prête. Sans OpenAI, l’icône d’onde ne s’affiche pas. Votre audio est envoyé directement de votre navigateur à OpenAI.

## En cas de problème

- **Le micro est bloqué** : autorisez l’accès au micro pour ce site dans les paramètres de votre navigateur.
- **Impossible de lancer la conversation en direct** : vérifiez votre connexion à ChatGPT ou votre clé OpenAI, puis réessayez.
- **La conversation en direct a perdu la connexion** : recommencez. Ce qui a été dit reste dans le chat.
- Elle indique qu’elle ne comprend pas vos paroles : vérifiez votre micro ou écrivez dans le chat.
