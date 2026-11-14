---
title: X
area: connections
summary: Vos mentions, réponses et messages privés sur X, lus dans le navigateur de votre Machine. Les messages ne sont envoyés qu’après votre approbation.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Ce que The Machine lit

Vos mentions, réponses et messages privés sur X, dans le navigateur de votre Machine, connecté à votre compte. Elle ne marque rien comme lu et ne peut pas lire les messages chiffrés de X Chat.

## Ce qu’elle peut envoyer

Une réponse ou un message privé, uniquement après votre approbation dans la tâche.

Cela ne passe pas par l’API officielle de X. La lecture et l’envoi occasionnel d’une réponse que vous avez approuvée ont très peu de chances de poser problème. L’envoi massif ou automatisé peut entraîner le blocage d’un compte.

## Connecter X

Sur une Machine hébergée :

1. Ouvrez votre page de configuration à l’adresse app.themachine.computer/setup, puis accédez à **Plus de sources**.
2. Ouvrez X, saisissez votre identifiant sans le @, connectez-vous à X dans le navigateur de votre Machine lorsque l’invite s’affiche, puis cliquez sur **Se connecter**.

Sur votre propre ordinateur :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez X.
2. Choisissez **Travail** et l’entreprise associée, ou **Perso**, saisissez votre identifiant sans le @, puis cliquez sur **Se connecter**.
3. Cliquez sur **Se connecter à X** et connectez-vous dans le navigateur de votre Machine. La connexion se fait automatiquement une fois la session ouverte.

Vous pouvez aussi exécuter `assistant connect x` dans un terminal.

Si X déconnecte votre Machine, consultez l’article [Déconnexion d’un site](signed-out.md).

## Supprimer X

- Dans le tableau de bord : ouvrez **Connexions**, sélectionnez X, puis **Détails** et **Déconnecter**. La lecture s’arrête. Les données déjà importées restent.
- Sur une Machine hébergée, vous pouvez aussi cliquer sur **Retirer** à côté de X sur votre page de configuration.

## Déconnecter votre session sur X

Dans X, ouvrez Paramètres, Sécurité et accès au compte, Applications et sessions, puis Sessions. Déconnectez la session du navigateur de votre Machine.
