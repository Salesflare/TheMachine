---
title: Parler en direct
area: cards
summary: Une conversation orale avec The Machine au sujet d’une tâche, avec la voix d’OpenAI. Elle se déroule dans le chat de la tâche et n’envoie un brouillon qu’après votre accord.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: f5555cb693a23682
---
## Lancer une conversation

Dans le chat d’une tâche, touchez l’onde à côté du micro et autorisez l’accès au micro si votre navigateur le demande. Quand la barre affiche **En direct**, parlez comme au téléphone. The Machine vous répond à voix haute. Parlez par-dessus elle pour l’interrompre.

Elle connaît cette tâche : ses messages, son brouillon et son chat, et peut consulter vos autres tâches. Dites « marque ça comme fait », « mets-la en attente jusqu’à demain à 9 h » ou « pas nécessaire » pour qu’elle le fasse. Dites « non, pas ça » juste après pour annuler. Les heures suivent le fuseau horaire de vos [Heures de travail](work-hours.md).

Elle comprend la langue de l’app et celles répertoriées par votre navigateur. Les toux, le bruit et les autres langues ne reçoivent pas de réponse et n’apparaissent pas dans la transcription.

La barre contient **Couper le micro** et **Terminer**. Dites au revoir pour mettre fin à la conversation. Une conversation dure jusqu’à 10 minutes, avec un compte à rebours pendant la dernière minute. Recommencez pour continuer.

## Parler de toutes vos tâches

Touchez **Parler** dans la barre latérale, ou dans le menu sur un téléphone. The Machine vous indique combien de tâches sont en attente et passe en revue celles de **Pour vous**, une par une, dans l’ordre affiché dans votre liste. Elle vous prévient quand une tâche marquée **En préparation…** est prête.

Parler a sa propre page : la tâche en cours s’affiche en haut, avec son brouillon et **Ouvrir le chat**.

Demandez-lui de lire un brouillon, de le modifier, de mettre la tâche en attente, de la marquer comme faite ou de passer à la suivante. Ce que vous dites au sujet d’une tâche est ajouté à son chat. Elle vous signale les nouvelles tâches pendant une pause. Dites « ajoute une tâche pour… » pour en ajouter une sans perdre votre place.

Posez une question sur une personne, une organisation, un projet, une réunion ou une promesse : elle recherche l’information et vous l’affiche. Elle peut aussi écarter, renommer ou rouvrir des tâches, y compris celles marquées **Fait / écarté**. Pour toute autre demande, elle transmet la question au chat d’une nouvelle tâche et vous donne la réponse.

Elle se souvient de vos conversations précédentes. Demandez « qu’est-ce que j’ai décidé pour le séminaire ? » : elle vous répond et vous indique quand vous l’avez dit. Seule la fonction Parler de la barre latérale le permet.

Vous pouvez consulter d’autres pages pendant ce temps : la barre reste en bas, et **Parler** vous ramène à la conversation. Celle-ci dure jusqu’à 30 minutes. Elle continue en arrière-plan sur les ordinateurs et les appareils Android. Sur iPhone, elle s’arrête quand l’app quitte l’écran.

## Demander des choses et envoyer après confirmation

Demandez quelque chose, par exemple « rédige une réponse pour dire que jeudi me convient », et The Machine transmet votre demande au chat de la tâche comme si vous l’aviez saisie. Le chat suit ses règles habituelles.

Le chat peut aussi rechercher des informations, comme les horaires d’ouverture d’un magasin. Il affiche **Je m’en occupe…** et vous pouvez continuer à parler. Quand la réponse est prête, The Machine vous la donne et vous indique où elle l’a trouvée.

Pour envoyer un brouillon, dites-le. The Machine le lit à voix haute (destinataire, objet et texte), puis vous demande, par exemple : « Envoyer cette réponse à Sam par e-mail ? ». Vous pouvez garder votre téléphone dans votre poche. Répondez clairement oui, par exemple « oui, envoie-le », et le brouillon est envoyé.

- Elle envoie exactement le brouillon qu’elle a lu. Si le brouillon change, elle le lit et vous redemande confirmation. Une question reste sans réponse pendant 3 minutes avant d’expirer.
- Toute réponse autre qu’un oui clair n’envoie rien.
- Si vous avez déjà vu ou entendu le brouillon, elle ne le lit pas à nouveau. Elle demande seulement, par exemple : « L’envoyer à Pat ? ».
- Dites « envoie tous ceux qui sont prêts » : elle nomme tout le monde dans une seule question. Un seul oui suffit pour tout envoyer.
- Après votre accord, Parler affiche **Annuler** avec un compte à rebours. Touchez-le ou dites « annule » ou « attends ».
- Une fois le message envoyé, Parler indique « Envoyé. » et la tâche affiche **Envoyé à** la personne concernée, avec l’heure. En cas d’échec, Parler vous en explique la raison. Demandez « est-ce que c’est envoyé ? » à tout moment : elle vérifie et ne devine jamais.

Vous pouvez aussi toucher **Approuver**.

Dites « faites-le » pour lancer The Machine sur la tâche, comme avec **Faire**. Dites « signaler un bug » pour envoyer un rapport de bug, comme avec **Signaler un bug** dans **Aide**.

## Choisir une voix

Dans **Paramètres**, **Général**, sous **Saisie vocale**, choisissez une **Voix** et touchez le bouton de lecture pour l’écouter. **Cedar** est la voix par défaut. La voix Cove de ChatGPT n’est pas disponible.

## Une trace dans le chat

Tout ce qui est dit apparaît dans le chat de la tâche, sous la mention **Conversation en direct**, pour que vous puissiez le relire plus tard.

## Ce dont vous avez besoin

Parler en direct utilise la voix d’OpenAI. Votre Machine doit donc disposer de l’un des éléments suivants :

- Un compte ChatGPT : inclus dans les forfaits qui le proposent.
- Une clé API OpenAI : OpenAI vous facture à la minute, et la barre l’indique. Si vous disposez des deux, votre Machine utilise la clé.

**Paramètres**, **Général**, **Saisie vocale** vous indiquent si Parler en direct est prêt. Sans OpenAI, l’onde ne s’affiche pas. Votre audio passe directement de votre navigateur à OpenAI.

## En cas de problème

- **Le micro est bloqué** : autorisez l’accès au micro pour ce site dans les paramètres de votre navigateur.
- **Impossible de démarrer Parler en direct** : vérifiez votre connexion à ChatGPT ou votre clé OpenAI, puis réessayez.
- **Parler en direct a perdu la connexion** : recommencez. Ce qui a été dit reste dans le chat.
- Si elle indique qu’elle ne comprend pas vos paroles, vérifiez votre micro ou saisissez votre message dans le chat.
