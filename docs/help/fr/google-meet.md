---
title: Google Meet
area: connections
summary: Les transcriptions et notes Gemini des réunions Meet que vous organisez. Il ne fait que lire.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## Ce qu’il lit

Les transcriptions et notes Gemini des réunions Google Meet que vous avez organisées, dès que Meet les a créées : les 7 derniers jours quand vous le connectez, puis les nouvelles au fur et à mesure. Meet les conserve 30 jours.

Meet ne les crée que si les transcriptions ou les notes Gemini étaient activées pendant la réunion.

Chacune est associée à la réunion de votre agenda à la même heure. Les notes Gemini apparaissent dans Notes de cette réunion et la transcription dans Transcription, marquées **De Google Meet**, à côté de ce que vous y avez ajouté ; elles ne le remplacent jamais.

## Ce qu’il peut faire

Rien dans Meet ni dans Drive. Il ne fait que lire, et n’active jamais les transcriptions lui-même.

## Le connecter

1. Dans Google Cloud, activez l’API Google Meet et l’API Google Drive.
2. Dans l’OAuth Playground, obtenez un jeton d’accès avec les deux scopes en lecture seule indiqués sur l’écran de connexion.
3. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources** et ouvrez Google Meet. Sur votre propre ordinateur : **Connexions**, **+ Ajouter**, Google Meet, ou `assistant connect google_meet`.
4. Collez le jeton et appuyez sur **Se connecter**.

Le jeton expire après environ une heure. Quand Connexions indique qu’il a été rejeté, collez-en un nouveau.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Google Meet, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le révoquer chez Google

Ouvrez myaccount.google.com/permissions et retirez l’accès de l’OAuth Playground.
