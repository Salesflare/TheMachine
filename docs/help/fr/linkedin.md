---
title: LinkedIn
area: connections
summary: Vos messages LinkedIn, lus dans le navigateur connecté de votre Machine. Il ne répond qu’après votre accord.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## Ce qu’il lit

Vos messages LinkedIn. Il les lit dans un onglet du navigateur de votre Machine, connecté avec votre compte, de temps en temps pendant la journée. Il n’utilise pas de clé API et ne marque rien comme lu.

## Ce qu’il peut envoyer

Une réponse à un message, et seulement après votre accord sur la tâche. D’ici là, il se contente de rédiger.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez LinkedIn, connectez-vous à LinkedIn dans le navigateur de votre serveur quand il le demande, puis appuyez sur **Se connecter**.

Sur votre propre ordinateur :

1. Connectez-vous une fois à LinkedIn dans le navigateur de votre Machine (Paramètres, **Ouvrir le navigateur de la Machine ↗**).
2. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez LinkedIn. Ou lancez `assistant connect linkedin`.

Un deuxième compte LinkedIn a son propre navigateur. Si LinkedIn déconnecte votre Machine, voir [Déconnecté d’un site](signed-out.md).

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez LinkedIn, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de lui sur votre page de configuration.

## Le déconnecter sur LinkedIn

Dans LinkedIn, ouvrez Préférences, Connexion et sécurité, Où vous êtes connecté, et déconnectez la session du navigateur de votre Machine.
