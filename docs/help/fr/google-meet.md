---
title: Google Meet
area: connections
summary: Transcriptions et notes Gemini des réunions Google Meet que vous organisez. The Machine ne fait que lire.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
translated: cea7230915b5a536
---
## Ce que The Machine lit

Les transcriptions et les notes Gemini des réunions Google Meet que vous avez organisées, dès que Meet les a créées : celles des 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. Meet les conserve pendant 30 jours.

Meet ne les crée que si les transcriptions ou les notes Gemini étaient activées pendant la réunion.

Chaque élément est ajouté à la réunion correspondante dans votre agenda : les notes Gemini sous Notes, la transcription sous Transcription, avec la mention **De Google Meet**. Ce que vous avez ajouté vous-même reste en place.

## Ce que The Machine peut faire

Rien dans Meet, Docs ou Drive. The Machine ne fait que lire et n’active jamais les transcriptions elle-même.

## Ce qu’elle vous demande

Une autorisation propre à cette connexion, distincte de celle pour vos e-mails. Google vous demande d’autoriser The Machine à :

- Voir vos réunions Google Meet, leurs transcriptions et leurs notes Gemini.
- Voir vos Google Docs pour lire le document contenant les notes Gemini.

The Machine ne demande jamais l’accès à votre Drive. Vos accès à Gmail et Google Agenda restent inchangés.

## Connecter Google Meet

Gmail n’a pas besoin d’être connecté. Pour connecter Google Meet :

- Machine hébergée : dans le tableau de bord, ouvrez **Connexions**, puis **Réunions**, sélectionnez **Google Meet** et cliquez sur **Se connecter avec Google**. Autorisez l’accès ci-dessus pour revenir au tableau de bord.
- Votre propre ordinateur, associé à votre compte : suivez les mêmes étapes. La page de connexion s’ouvre dans un nouvel onglet.

Sans cette autorisation pour Meet, la connexion n’est pas ajoutée. Rien n’est à coller ni à renouveler.

Si vous retirez l’autorisation plus tard, Google Meet dans **Connexions** vous demande de vous connecter à nouveau.

## Supprimer Google Meet

Dans le tableau de bord, ouvrez **Connexions**, puis Google Meet, **Détails**, et enfin **Déconnecter**. Les éléments déjà importés restent en place.

## Révoquer l’accès dans Google

Ouvrez myaccount.google.com/permissions et retirez à The Machine l’accès à Google Meet. Gmail et Google Agenda continueront de fonctionner.
