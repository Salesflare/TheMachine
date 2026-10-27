---
title: Zoom
area: connections
summary: Les résumés et transcriptions AI Companion des réunions que vous organisez. Il ne fait que lire.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## Ce qu’il lit

Le résumé AI Companion de chaque réunion Zoom que vous organisez, et sa transcription quand Zoom en a une : les 7 derniers jours au moment de la connexion, puis les nouveaux au fur et à mesure. Il lit aussi votre nom et votre e-mail Zoom, pour savoir à qui sont ces réunions.

Les résumés demandent un forfait Zoom payant, AI Companion activé pendant la réunion, et pas de chiffrement de bout en bout.

## Ce qu’il en fait

Chaque résumé est rattaché à la réunion dans votre agenda. Vos revues s’en servent ensuite pour les suivis de cette réunion, et une répartition des suivis dans la Fleet arrive déjà remplie avec qui fait quoi. Vous la vérifiez et la modifiez d’abord ; rien ne part avant que vous l’envoyiez.

## Ce qu’il peut faire

Il ne fait que lire. Il ne crée, ne modifie et ne supprime jamais rien dans Zoom, et il ne voit que vos propres réunions. Votre connexion Zoom est gardée sur votre propre Machine.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez Zoom, choisissez travail ou perso, et appuyez sur **Connecter Zoom**.
3. Connectez-vous à Zoom et autorisez The Machine. Elle est créée par Salesflare.

Sur votre propre ordinateur, une fois [associé à votre compte](fleet.md) : ouvrez **Connexions**, puis **+ Ajouter**, choisissez Zoom et appuyez sur **Se connecter avec Zoom**.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Zoom, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le désinstaller chez Zoom

Connectez-vous sur marketplace.zoom.us, ouvrez Manage, puis Added Apps, et retirez The Machine. Elle ne peut plus rien lire. Ce qu’elle a déjà récupéré reste sur votre Machine jusqu’à ce que vous le supprimiez : voir [Résilier ou supprimer](cancel-and-delete.md).
