---
title: Parler en direct
area: cards
summary: Une conversation vocale avec The Machine au sujet d’une tâche, avec la voix d’OpenAI. Elle se déroule dans le chat de la tâche et n’envoie un brouillon qu’après votre accord.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
translated: 60168384f08de74e
---
## Démarrer une conversation

Dans le chat d’une tâche, touchez l’onde à côté du micro et autorisez l’accès au micro si une demande s’affiche. Quand la barre indique **En direct**, parlez comme au téléphone. The Machine vous répond à voix haute. Parlez par-dessus pour l’interrompre.

Elle connaît cette tâche : ses messages, son brouillon et son chat. Elle peut aussi consulter vos autres tâches. Dites « marque cette tâche comme terminée », « mets-la en attente jusqu’à demain à 9 h » ou « pas nécessaire », et elle s’en charge. Dites « non, pas ça » juste après pour annuler. Les heures suivent le fuseau horaire de vos [Heures de travail](work-hours.md).

Elle comprend la langue de l’application et celles répertoriées par votre navigateur. Les toux, les bruits et les autres langues ne reçoivent pas de réponse et n’apparaissent pas dans la transcription.

La barre comporte **Couper le micro** et **Fin**. Dites au revoir pour mettre fin à la conversation. Elle dure jusqu’à 10 minutes, avec un compte à rebours pendant la dernière minute. Recommencez pour continuer.

## Parler de toutes vos tâches

Touchez **Parler** dans la barre latérale, ou dans le menu sur un téléphone. The Machine vous indique combien de tâches sont en attente, puis traite une par une celles de la section **Pour vous**, en commençant par les plus urgentes. Elle vous prévient quand une tâche **En préparation…** est prête.

La fonction Parler a sa propre page : la tâche en cours apparaît en haut, avec son brouillon et **Ouvrir le chat**.

Demandez-lui de lire un brouillon, de le modifier, de mettre une tâche en attente, de la marquer comme terminée ou de passer à la suivante. Ce que vous dites au sujet d’une tâche est ajouté à son chat. Elle vous signale les nouvelles tâches quand vous faites une pause. Dites « ajoute une tâche pour… » pour en ajouter une sans perdre votre place.

Posez une question sur une personne, une organisation, un projet, une réunion ou une promesse : elle fera une recherche et vous montrera le résultat. Elle peut aussi écarter, renommer ou rouvrir des tâches, y compris celles dans **Fait / écarté**. Pour toute autre demande, elle transmet la question au chat d’une nouvelle tâche et vous donne la réponse.

Elle se souvient de vos conversations précédentes. Demandez « qu’est-ce que j’ai décidé pour le séminaire ? » : elle vous le dira, ainsi que le moment où vous l’avez dit. Seule la fonction Parler dans la barre latérale le permet.

Vous pouvez consulter d’autres pages : la barre reste en bas, et **Parler** vous ramène à la conversation. Celle-ci dure jusqu’à 30 minutes. Sur ordinateur et Android, elle continue en arrière-plan. Sur iPhone, elle s’arrête quand l’application n’est plus à l’écran.

## Faire des demandes et envoyer après confirmation

Demandez quelque chose, par exemple « rédige une réponse pour dire que jeudi me convient », et The Machine transmet votre demande au chat de la tâche comme si vous l’aviez saisie. Le chat suit ses règles habituelles.

Le chat peut aussi faire des recherches, par exemple sur les heures d’ouverture d’un magasin. Il affiche **Je m’en occupe…** et vous pouvez continuer à parler. Quand la réponse est prête, The Machine vous la donne et vous indique où elle l’a trouvée.

Pour envoyer un brouillon, dites-le. The Machine le lit à voix haute (le destinataire, l’objet et le texte), puis vous demande, par exemple : « Envoyer cette réponse à Sam par e-mail ? ». Vous pouvez garder votre téléphone dans votre poche. Dites clairement oui, par exemple « oui, envoie », et le brouillon est envoyé.

- Elle envoie exactement le brouillon qu’elle a lu. Si le brouillon change, elle le relit et vous redemande confirmation. Une question restée sans réponse pendant 3 minutes expire.
- Sans réponse claire par l’affirmative, rien n’est envoyé.
- Si vous avez déjà vu ou entendu un brouillon, elle ne le relit pas. Elle demande seulement, par exemple : « L’envoyer à Pat ? ».
- Dites « envoie tous ceux qui sont prêts » : elle nomme tout le monde dans une seule question. Un oui suffit pour tout envoyer.
- Après votre accord, Parler affiche **Annuler** avec un compte à rebours. Touchez-le, ou dites « annule » ou « attends ».
- Une fois l’envoi effectué, Parler indique « Envoyé. » et la tâche affiche **Envoyé à** cette personne, avec l’heure. En cas d’échec, Parler vous en indique la raison. Demandez « est-ce envoyé ? » à tout moment : elle vérifie au lieu de deviner.

Vous pouvez aussi toucher **Approuver**.

Dites « fais-le » pour lancer The Machine sur la tâche, comme avec **Faire**. Dites « signaler un bug » pour envoyer un rapport de bug, comme avec **Signaler un bug** dans Aide.

## Choisir une voix

Dans **Paramètres**, sous **Général**, puis **Saisie vocale**, choisissez une **Voix** et touchez le bouton de lecture pour l’écouter. Cedar est la voix par défaut. La voix Cove de ChatGPT n’est pas disponible.

## Une trace dans le chat

Tout ce qui est dit est ajouté au chat de la tâche, sous une ligne **Conversation en direct**, pour que vous puissiez le relire plus tard.

## Conditions requises

Parler en direct utilise la voix d’OpenAI. Votre Machine a donc besoin de l’un des éléments suivants :

- Un compte ChatGPT : inclus dans les forfaits qui le proposent.
- Une clé API OpenAI : OpenAI facture chaque minute d’utilisation, et la barre vous l’indique. Si vous avez les deux, votre Machine utilise la clé.

**Paramètres**, **Général**, **Saisie vocale** vous indique si Parler en direct est prêt. Sans OpenAI, l’onde ne s’affiche pas. Votre audio est envoyé directement de votre navigateur à OpenAI.

## En cas de problème

- **Le microphone est bloqué** : autorisez l’accès au micro pour ce site dans les paramètres de votre navigateur.
- **Parler en direct n’a pas pu démarrer** : vérifiez votre compte ChatGPT ou votre clé OpenAI, puis réessayez.
- **La connexion de Parler en direct a été interrompue** : recommencez. Ce qui a été dit reste dans le chat.
- Si elle indique qu’elle ne comprend pas vos paroles, vérifiez votre micro ou écrivez dans le chat.
