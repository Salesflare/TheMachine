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

Elle connaît la tâche où vous êtes : ses messages, son brouillon et son chat. Elle peut aussi consulter vos autres tâches. Dites « marque-la comme faite », « reporte-la » ou « pas nécessaire » et elle le fait elle-même. Dites « non, pas ça » juste après pour revenir en arrière.

L’écoute se fait dans vos langues : celle de l’app et celles que votre navigateur indique. Un bruit, une toux ou un son dans une autre langue ne reçoit pas de réponse et reste hors de la transcription.

La barre a **Couper le micro** et **Fin**. Dites au revoir, ou que vous avez fini, et elle s’arrête d’elle-même. Une conversation dure jusqu’à 10 minutes. Une minute avant la fin, le minuteur montre le temps restant. Relancez-la pour continuer.

## Passer en revue toutes vos tâches à voix haute

Touchez **Parler** dans la barre latérale (dans le menu sur un téléphone) pour passer en revue à la voix tout ce qui vous attend. The Machine dit combien il y en a et les prend une par une : d’abord **Prête**, puis **À décider**. Elle voit aussi vos autres tâches, comme celles encore **En préparation**, et vous prévient quand l’une est prête.

Parler a sa propre page : une conversation du début à la fin, avec en haut la tâche dont elle parle, son brouillon et **Ouvrir le chat**. Elle ne vous fait pas passer de chat en chat.

Demandez-lui de lire un brouillon, de le modifier, de le reporter, de le marquer comme fait ou de passer à la suivante. L’envoi fonctionne comme dans le chat d’une tâche : un brouillon par question, après un oui clair. Ce que vous dites sur une tâche va dans le chat de cette tâche. Quand une nouvelle tâche arrive, elle la mentionne lors d’une pause. Dites « ajoute une tâche pour… » et elle en crée une nouvelle, sans quitter celle en cours.

Elle accède aussi au reste de The Machine. Demandez une personne, une organisation, un projet, une réunion ou une promesse, et elle la cherche et l’affiche. Elle peut reporter une tâche, la marquer comme faite, l’écarter, la renommer ou la rouvrir, même une tâche dans **Fait / écarté**. Pour tout le reste, elle crée une tâche, laisse son chat s’en charger et vous donne la réponse.

Elle se souvient aussi de vos conversations précédentes. Demandez « Qu’avais-je décidé pour le séminaire ? » ou « Qu’ai-je dit sur Acme la semaine dernière ? », et elle vous le dit, avec le moment où vous l’avez dit. Seul Parler dans la barre latérale le fait, pas Parler dans le chat d’une tâche.

Vous pouvez aller sur une autre page entre-temps : la barre reste en bas, et **Parler** dans la barre latérale vous y ramène. Cette conversation dure 30 minutes au plus. Elle continue en arrière-plan sur ordinateur et sur Android. Sur iPhone, elle s’arrête quand l’app quitte l’écran.

## Demandez, et envoyez d’un oui

Quand vous demandez quelque chose, comme « écris une réponse pour dire que jeudi me va » ou « mets ça en attente jusqu’à lundi », The Machine le transmet au chat de la tâche, comme si vous l’aviez tapé. Le chat suit ses règles habituelles : il peut modifier le brouillon ou mettre la tâche en attente.

Le chat peut aussi chercher des choses, comme les horaires d’un magasin sur le web. Pendant ce temps, il affiche **Je m’en occupe…**, et vous pouvez continuer à parler. Quand la réponse est prête, The Machine vous la dit, avec l’endroit où elle l’a trouvée. Si vous demandez autre chose entre-temps, cela attend son tour.

Pour envoyer un brouillon, dites-le. The Machine demande d’abord, en précisant à qui et comment, par exemple « Envoyer cette réponse à Sam par e-mail ? ». Elle lit d’abord tout le brouillon à voix haute : à qui il va, l’objet et le texte. Ça marche donc aussi avec le téléphone dans la poche. Répondez par un oui clair, comme « oui, envoie-le », et ce brouillon part.

- Elle envoie exactement le brouillon qu’elle a lu. S’il change après la question, elle le relit et redemande. Une question sans réponse au bout de 3 minutes expire.
- Si votre réponse n’est pas un oui clair, rien ne part et elle redemande. « Non » n’envoie rien.
- Un brouillon déjà vu à l’écran, ou entendu dans cette conversation, n’est pas relu : elle demande seulement, par exemple « L’envoyer à Pat ? ».
- Dites « envoie les deux » ou « envoie tous ceux qui sont prêts », et elle nomme tout le monde en une question. Un oui les envoie chacun.
- Parler dit combien de secondes il vous reste et affiche **Annuler** avec le même compte à rebours. Touchez-le, ou dites « annule » ou « attends ».
- Une fois envoyé par la Machine, Parler dit « Envoyé. » et la barre et la tâche affichent **Envoyé à** cette personne avec l’heure. Si l’envoi a échoué, Parler dit pourquoi. Demandez « c’est parti ? » à tout moment : elle vérifie, elle ne devine jamais.

Vous pouvez toujours appuyer sur **Approuver** à la place.

« Fais-le » lance The Machine sur la tâche, comme **Faire**, y compris dans le navigateur. « Marque-la comme faite » la ferme. Dites « signale un bug » et elle envoie un signalement, comme **Signaler un bug** dans l’aide, en demandant d’abord si elle peut ajouter plus.

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
- Si elle dit qu’elle ne comprend pas vos mots, ce que vous avez dit n’est pas passé deux fois de suite. Vérifiez votre micro, ou écrivez dans le chat. Elle le dit une fois, puis attend de vous entendre.
