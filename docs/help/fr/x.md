---
title: X
area: connections
summary: Vos mentions, réponses et messages privés sur X, lus dans le navigateur de votre Machine. Rien n’est envoyé sans votre approbation.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: 5cbe43055458daf4
---
## Ce que la connexion lit

Vos mentions, réponses et messages privés sur X, dans le navigateur de votre Machine, connecté à votre compte. Elle ne marque rien comme lu et ne peut pas lire les messages chiffrés de X Chat.

## Ce qu’elle peut envoyer

Une réponse ou un message privé, uniquement après votre approbation dans la tâche.

Cette connexion ne passe pas par l’API officielle de X. La lecture et l’envoi occasionnel d’une réponse approuvée ne devraient pas poser de problème. En revanche, des envois massifs ou automatisés peuvent entraîner le blocage d’un compte.

## Connecter X

Avec une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup, puis accédez à **Plus de sources**.
2. Ouvrez X, saisissez votre nom d’utilisateur sans le @, puis connectez-vous à X dans le navigateur de votre Machine quand vous y êtes invité. Appuyez ensuite sur **Se connecter**.

Sur votre propre ordinateur :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez X.
2. Choisissez **Travail** et son entreprise, ou **Perso**, saisissez votre nom d’utilisateur sans le @, puis appuyez sur **Se connecter**.
3. Appuyez sur **Se connecter à X** et connectez-vous dans le navigateur de votre Machine. La connexion se fait automatiquement une fois la session ouverte.

Vous pouvez aussi exécuter `assistant connect x` dans un terminal.

Si X déconnecte votre Machine, consultez l’article [Déconnexion d’un site](signed-out.md).

## Supprimer la connexion

- Dans le tableau de bord : ouvrez **Connexions**, choisissez X, puis **Détails** et **Déconnecter**. La lecture s’arrête. Les données déjà importées restent disponibles.
- Avec une Machine hébergée, vous pouvez aussi appuyer sur **Retirer**, à côté de X, sur votre page de configuration.

## Déconnecter votre session sur X

Dans X, ouvrez Paramètres, Sécurité et accès au compte, Applications et sessions, puis Sessions. Déconnectez la session du navigateur de votre Machine.
