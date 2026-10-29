---
title: X
area: connections
summary: Vos mentions, réponses et messages privés sur X, lus dans le navigateur de votre Machine. N’envoie qu’après votre accord.
covers: connector:x
code: connectors/x.py, integrations/x_inbox.py
site: Connect, More sources, Remove
---
## Ce qu’il lit

Vos mentions, réponses et messages privés sur X. Il les lit dans le navigateur de votre Machine, connecté avec votre compte. Il n’utilise pas l’API développeur de X, ne marque rien comme vu et ne peut pas lire X Chat, qui est chiffré.

## Ce qu’il peut envoyer

Une réponse ou un message privé, et seulement après votre accord sur la tâche.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez X, tapez votre identifiant sans le @, connectez-vous à X dans le navigateur de votre Machine quand elle le demande, puis appuyez sur **Se connecter**.

Sur votre propre ordinateur :

1. Connectez-vous une fois à X dans le navigateur de votre Machine (Paramètres, **Ouvrir le navigateur de la Machine ↗**).
2. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez X. Ou lancez `assistant connect x`.
3. Tapez votre identifiant, et celui avec lequel le navigateur est connecté d’habitude.

Si X déconnecte votre Machine, voir [Déconnecté d’un site](signed-out.md).

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez X, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le déconnecter sur X

Dans X, ouvrez Paramètres, Sécurité et accès au compte, Applications et sessions, Sessions, et déconnectez la session du navigateur de votre Machine.
