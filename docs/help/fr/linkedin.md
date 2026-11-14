---
title: LinkedIn
area: connections
summary: Vos messages LinkedIn, lus dans le navigateur connecté de votre Machine. Il ne répond qu’après votre accord.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## Ce qu’il lit

Vos messages LinkedIn. Il les lit dans un onglet du navigateur de votre Machine, connecté avec votre compte, de temps en temps pendant la journée. Il n’utilise pas de clé API et ne marque rien comme lu. Les réponses dans les conversations que vous avez archivées et les demandes de message arrivent aussi ; le spam reste dehors.

## Postes et entreprises

Il tient aussi à jour les postes et entreprises de vos relations LinkedIn sur les personnes déjà dans votre Graph, à partir de votre liste de relations. Il n’ouvre pas leurs profils et n’ajoute personne. Quand le poste ou l’entreprise de quelqu’un change, sa chronologie l’indique, par exemple « Maintenant Head of Sales chez Acme, avant Sales Lead chez Acme ».

Le poste vient de leur titre, comme « Head of Sales chez Acme » ou « VP Sales and Strategy », jamais d’un slogan. Il les retrouve par leur lien de profil, ou par nom et entreprise. Sans entreprise à comparer, un nom complet qu’une seule personne de votre Graph porte suffit. Leur page indique aussi depuis quand vous êtes en relation.

Il lit très lentement : une page à la fois, à quelques minutes d’intervalle, quelques dizaines de pages par jour, seulement en journée. Environ 3 000 relations prennent quatre jours. Si LinkedIn freine, il s’arrête jusqu’au lendemain.

## Ce qu’il peut envoyer

Une réponse à un message, ou un nouveau message à un profil que vous indiquez, et seulement après votre accord sur la tâche. D’ici là, il se contente de rédiger.

LinkedIn ne propose pas de moyen officiel pour cela. Lire et envoyer de temps en temps un message que vous avez validé ne pose presque jamais de problème ; un envoi en masse ou automatisé peut faire bloquer un compte.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez LinkedIn, connectez-vous à LinkedIn dans le navigateur de votre Machine quand elle le demande, puis appuyez sur **Se connecter**.

Sur votre propre ordinateur :

1. Connectez-vous une fois à LinkedIn dans le navigateur de votre Machine (Paramètres, **Ouvrir le navigateur de la Machine ↗**).
2. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez LinkedIn. Ou lancez `assistant connect linkedin`.

Un deuxième compte LinkedIn a son propre navigateur. Si LinkedIn déconnecte votre Machine, voir [Déconnecté d’un site](signed-out.md).

## Si LinkedIn demande un code

La première fois que votre Machine se connecte, LinkedIn envoie souvent un code par e-mail. Saisissez-le dans la fenêtre de connexion sous **Code** et appuyez sur **Se connecter**. La page ne bouge pas pendant que vous tapez.

Si LinkedIn revient au début, ou si rien ne se passe pendant deux minutes, LinkedIn a arrêté cette connexion. Attendez une minute et appuyez sur **Réessayer**. Si LinkedIn affiche une vérification anti-robot, terminez-la dans le navigateur de votre Machine.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez LinkedIn, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de lui sur votre page de configuration.

## Le déconnecter sur LinkedIn

Dans LinkedIn, ouvrez Préférences, Connexion et sécurité, Où vous êtes connecté, et déconnectez la session du navigateur de votre Machine.
