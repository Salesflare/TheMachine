---
title: Intercom
area: connections
summary: Les conversations clients de votre espace de travail Intercom. Elle ne répond qu’après votre envoi, en votre nom.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, Or paste an access token, Connect, More sources, Remove
---
## Ce qu’il lit

Les conversations clients de votre espace de travail Intercom : les 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. Il lit aussi à quel espace de travail et à quel admin appartient la connexion.

## Ce qu’il peut faire

Elle lit les conversations. Avec votre propre **Se connecter avec Intercom**, elle peut aussi répondre dans une conversation en votre nom, uniquement après que vous avez appuyé sur **Envoyer** pour ce texte précis. Elle n’assigne, ne ferme, n’étiquette et n’écrit jamais de notes. Un Intercom partagé avec vous via votre Fleet ne fait que lire.

## Tâches venues d’Intercom

Une tâche venue d’une conversation Intercom montre son origine : **Lire le message** ouvre la conversation, avec un lien vers elle dans Intercom, et le client figure sur la tâche. Sa réponse est une réponse Intercom dans cette conversation, sauf si vous demandez un e-mail.

Quand Intercom ne peut pas répondre depuis votre Machine (partagé avec vous en lecture seule, réponses non activées, ou non connecté), le brouillon part par e-mail. La tâche dit pourquoi, et sa revue demande **Envoyer plutôt par e-mail ?** Pour répondre vous-même dans Intercom, appuyez sur **Connectez votre propre Intercom** sur la tâche et connectez-vous. Rien ne part avant que vous l’envoyiez.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez Intercom et appuyez sur **Se connecter avec Intercom**.
3. Approuvez The Machine dans Intercom. Elle est créée par Salesflare.

Ou dans le tableau de bord : **Connexions**, **+ Ajouter**, choisissez Intercom et appuyez sur **Se connecter avec Intercom**. Une fois terminé, vous revenez au tableau de bord.

Si la connexion ne convient pas à votre espace de travail, ouvrez plutôt **Ou collez un jeton d’accès**, collez un jeton du Developer Hub d’Intercom et appuyez sur **Se connecter**.

Sur votre propre ordinateur :

1. Dans le Developer Hub d’Intercom, ouvrez votre app, puis Authentication, et copiez son jeton d’accès.
2. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez Intercom. Ou lancez `assistant connect intercom`.
3. Collez le jeton. Un jeton d’un autre espace de travail devient un second compte Intercom.

Intercom compte toujours comme travail, pour l’entreprise que nomme son espace de travail.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Intercom, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de lui sur votre page de configuration.

## Le désinstaller dans Intercom

- Connecté avec Intercom : dans Intercom, ouvrez Settings, Apps, Installed apps, et retirez The Machine.
- Un jeton collé : supprimez-le ou renouvelez-le dans le Developer Hub, ou supprimez l’app dans laquelle vous l’avez créé.
