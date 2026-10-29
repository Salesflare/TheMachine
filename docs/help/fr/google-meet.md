---
title: Google Meet
area: connections
summary: Les transcriptions et notes Gemini des réunions Meet que vous organisez. Il ne fait que lire.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## Ce qu’il lit

Les transcriptions et notes Gemini des réunions Google Meet que vous avez organisées, dès que Meet les a créées : les 7 derniers jours quand vous le connectez, puis les nouvelles au fur et à mesure. Meet les conserve 30 jours.

Meet ne les crée que si les transcriptions ou les notes Gemini étaient activées pendant la réunion.

Chacune est associée à la réunion de votre agenda à la même heure. Les notes Gemini apparaissent dans Notes de cette réunion et la transcription dans Transcription, marquées **De Google Meet**, à côté de ce que vous y avez ajouté ; elles ne le remplacent jamais.

## Ce qu’il peut faire

Rien dans Meet, Docs ou Drive. Il ne fait que lire et n’active jamais les transcriptions lui-même.

## Ce qu’il demande

Son propre accord, à part de votre connexion e-mail. Google demande d’autoriser The Machine à :

- Voir vos réunions Google Meet, leurs transcriptions et leurs notes Gemini.
- Voir vos Google Docs, pour lire le document des notes Gemini.

Il ne demande jamais votre Drive. Vos accès à Gmail et à l’agenda restent tels quels.

## Le connecter

Gmail n’a pas besoin d’être connecté. Pour le connecter :

- Machine hébergée : dans le tableau de bord, ouvrez **Connexions**, **+ Ajouter**, choisissez **Google Meet** et appuyez sur **Se connecter avec Google**. Google demande l’accord ci-dessus, puis vous revenez au tableau de bord.
- Votre propre ordinateur, associé à votre compte : les mêmes étapes. La connexion s’ouvre dans un nouvel onglet.

Il vérifie que la connexion peut lire Meet. Sans cet accord, il n’est pas ajouté. La connexion reste valable : rien à coller ni à renouveler.

Si l’accord est retiré plus tard, la carte Google Meet vous demande de vous reconnecter.

## Le retirer

Dans le tableau de bord : **Connexions**, ouvrez Google Meet, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.

## Le révoquer chez Google

Ouvrez myaccount.google.com/permissions et retirez l’accès de The Machine à Google Meet. Gmail et l’agenda continuent de fonctionner.
