---
title: X
area: connections
summary: Vos mentions, réponses et messages privés sur X, consultés dans le navigateur de votre Machine. Rien n’est envoyé sans votre accord.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
translated: e8997ab6eb32523f
---
## Ce que l’app lit

Vos mentions, réponses et messages privés sur X, dans le navigateur de votre Machine, connecté à votre compte. Rien n’est marqué comme lu et l’app ne peut pas lire les messages chiffrés de X Chat.

## Ce que l’app peut envoyer

Une réponse ou un message privé, uniquement après votre approbation dans la tâche.

X migre les comptes vers une nouvelle application web. Si votre compte utilise cette nouvelle application, les réponses ne peuvent pas encore être envoyées par votre Machine. Une réponse que vous approuvez est donc bloquée avant publication, et l’app vous l’indique. Les messages privés continuent d’être envoyés.

Cette intégration ne passe pas par l’API officielle de X. La lecture et l’envoi occasionnel d’une réponse que vous avez approuvée risquent très peu de causer des problèmes. Des envois massifs ou automatisés peuvent entraîner le blocage d’un compte.

## Connecter X

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup, puis accédez à **Plus de sources**.
2. Ouvrez X, saisissez votre identifiant sans le @, puis connectez-vous à X dans le navigateur de votre Machine lorsqu’on vous le demande. Appuyez ensuite sur **Connecter**.

Sur votre propre ordinateur :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez X.
2. Choisissez **Travail** avec le nom de votre entreprise, ou **Perso**, saisissez votre identifiant sans le @, puis appuyez sur **Connecter**.
3. Appuyez sur **Se connecter à X**, puis connectez-vous dans le navigateur de votre Machine. La connexion se fait automatiquement une fois connecté.

Vous pouvez aussi exécuter `assistant connect x` dans un terminal.

Si X déconnecte votre Machine, consultez [Déconnexion d’un site](signed-out.md).

## Supprimer la connexion

- Dans le tableau de bord : ouvrez **Connexions**, choisissez X, puis **Détails** et **Déconnecter**. La lecture s’arrête. Les données déjà importées restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de X, sur votre page de configuration.

## Déconnecter votre Machine de X

Dans X, ouvrez Paramètres, Sécurité et accès au compte, Applications et sessions, puis Sessions. Déconnectez la session du navigateur de votre Machine.
