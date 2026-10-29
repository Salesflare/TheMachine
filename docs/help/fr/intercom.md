---
title: Intercom
area: connections
summary: Les conversations clients de votre espace de travail Intercom. Elle ne répond qu’après votre envoi, en votre nom.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
---
## Ce qu’il lit

Les conversations clients de votre espace de travail Intercom : les 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. Il lit aussi à quel espace de travail et à quel admin appartient la connexion.

## Ce qu’il peut faire

Elle lit les conversations. Avec votre propre **Se connecter avec Intercom**, elle peut aussi répondre dans une conversation en votre nom, uniquement après que vous avez appuyé sur **Envoyer** pour ce texte précis. Elle n’assigne, ne ferme, n’étiquette et n’écrit jamais de notes. Un Intercom partagé avec vous via votre Fleet ne fait que lire.

## Tâches venues d’Intercom

Une tâche venue d’une conversation Intercom montre son origine : **Lire le message** ouvre la conversation, avec un lien vers elle dans Intercom, et le client figure sur la tâche. Sa réponse est une réponse Intercom dans cette conversation, sauf si vous demandez un e-mail.

Quand Intercom ne peut pas répondre depuis votre Machine (partagé avec vous en lecture seule, réponses non activées, ou non connecté), le brouillon part par e-mail. La tâche dit pourquoi, et sa revue demande **Envoyer plutôt par e-mail ?** Pour répondre vous-même dans Intercom, appuyez sur **Connectez votre propre Intercom** sur la tâche et connectez-vous. Rien ne part avant que vous l’envoyiez.

## Le connecter

1. Dans le tableau de bord : **Connexions**, **+ Ajouter**, Intercom. Ou sur la page de configuration d’une Machine hébergée, sur app.themachine.computer/setup : **Plus de sources**, Intercom. Sur votre propre ordinateur, associez-le d’abord à votre compte.
2. Appuyez sur **Se connecter avec Intercom**.
3. Approuvez The Machine dans Intercom. Elle est créée par Salesflare. Une fois terminé, vous revenez là où vous avez commencé.

Se connecter à un autre espace de travail ajoute un second compte Intercom.

Intercom compte toujours comme travail, pour l’entreprise que nomme son espace de travail.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Intercom, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de lui sur votre page de configuration.

## Le désinstaller dans Intercom

Dans Intercom, ouvrez Settings, Apps, Installed apps, et retirez The Machine.
