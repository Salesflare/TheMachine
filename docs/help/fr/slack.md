---
title: Slack
area: connections
summary: Les canaux et messages directs dont vous faites partie. N’envoie un message direct qu’après votre accord.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## Ce qu’elle lit

Les conversations dont vous êtes membre : canaux, canaux privés, messages directs et messages de groupe, les 7 derniers jours au moment de la connexion, puis tout ce qui est nouveau. Elle ne rejoint jamais un canal et n’ouvre jamais une conversation d’elle-même.

## Ce qu’elle peut envoyer

Un message direct à une personne, en votre nom, et seulement après votre accord sur la tâche. Elle ne publie jamais dans un canal.

## La connecter

Connectez-vous avec Slack, le plus simple :

1. Dans le tableau de bord : **Connexions**, **+ Ajouter**, Slack. Ou sur la page de configuration d’une Machine hébergée sur app.themachine.computer/setup : **Plus de sources**, Slack. Sur votre propre ordinateur, associez-le d’abord à votre compte.
2. Appuyez sur **Se connecter avec Slack**. Slack demande quel espace de travail et montre ce que The Machine peut lire et envoyer.
3. Appuyez sur **Allow**. Vous revenez là où vous étiez, et Slack est connecté.

Dans certains espaces de travail, seuls les admins approuvent les nouvelles apps. Slack demande alors d’abord à un admin ; une fois approuvé, reconnectez-vous.

Ou utilisez Maton :

1. Connectez-vous sur maton.ai, connectez-y Slack et copiez votre clé API Maton depuis Home.
2. Ouvrez Slack comme ci-dessus (ou lancez `assistant connect slack`), ouvrez **Ou utilisez une clé API Maton**, collez la clé et appuyez sur **Se connecter**.

Slack déjà connecté via Maton ? Il continue de fonctionner. Connexions affiche **Reconnecter Slack** : appuyez dessus et connectez-vous avec Slack pour ne plus passer par Maton. Ce que Slack a déjà apporté reste.

## La retirer

- Dans le tableau de bord : **Connexions**, ouvrez Slack, **Détails**, puis **Déconnecter**. Ce qu’elle a déjà importé reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté d’elle sur votre page de configuration.

## La désinstaller côté Slack

- Connecté avec Slack : dans Slack, ouvrez la page Manage apps de votre espace de travail (ou Paramètres, Apps), trouvez The Machine et retirez-la. Un admin Slack peut aussi la retirer pour tout l’espace de travail.
- Via Maton : retirez la connexion Slack dans Maton et supprimez la clé API Maton que vous avez donnée.
