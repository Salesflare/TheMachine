---
title: Zoom
area: connections
summary: Les résumés et transcriptions de l’AI Companion pour les réunions que vous organisez. La connexion est en lecture seule.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
translated: 9533caa1429fb3fc
---
## Ce que la connexion lit

Le résumé de l’AI Companion pour chaque réunion Zoom que vous organisez, ainsi que sa transcription quand Zoom en fournit une : celles des 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. La connexion lit aussi votre nom et votre adresse e-mail Zoom pour savoir à qui appartiennent les réunions.

Les résumés nécessitent un forfait Zoom payant, l’AI Companion activé pendant la réunion et l’absence de chiffrement de bout en bout.

## Ce que la connexion en fait

Chaque résumé est associé à la réunion correspondante dans votre calendrier. Il apparaît dans les **Notes** de cette réunion, et la transcription dans sa **Transcription**, avec la mention **De Zoom**, à côté des éléments que vous avez ajoutés. Votre Machine crée des tâches à partir des prochaines étapes qui vous reviennent. Rien n’est envoyé tant que vous ne l’envoyez pas.

## Ce que la connexion peut faire

La connexion ne fait que lire, et uniquement vos réunions. Elle ne crée, ne modifie et ne supprime jamais rien dans Zoom. Vos identifiants Zoom restent sur votre Machine.

## Connecter la connexion

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup, puis accédez à **Plus de sources**.
2. Ouvrez Zoom, choisissez « professionnel » ou « personnel », puis appuyez sur **Connecter Zoom**.
3. Connectez-vous à Zoom et autorisez The Machine (créée par Salesflare).

Ou depuis le tableau de bord : **Connexions**, **Réunions**, choisissez Zoom, puis appuyez sur **Se connecter avec Zoom**. Une fois la connexion terminée, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois celui-ci [associé à votre compte](friends.md#a-machine-on-your-own-computer) : ouvrez **Connexions**, puis **Réunions**, choisissez Zoom et appuyez sur **Se connecter avec Zoom**.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Zoom, **Détails**, puis **Déconnecter**. La connexion cesse de lire vos données. Les données déjà importées restent sur votre Machine.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Zoom sur votre page de configuration.

## Désinstaller l’application dans Zoom

Connectez-vous sur marketplace.zoom.us, ouvrez Manage, puis Added Apps, et supprimez The Machine. La connexion ne peut alors plus rien lire. Les données déjà importées restent sur votre Machine jusqu’à ce que vous les supprimiez : consultez [Annuler et supprimer](cancel-and-delete.md).
