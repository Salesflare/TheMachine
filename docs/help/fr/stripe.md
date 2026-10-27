---
title: Stripe
area: connections
summary: Paiements échoués, litiges, résiliations et gros nouveaux abonnements. Il ne fait que lire.
covers: connector:stripe
code: connectors/stripe.py
site: Connect, More sources, Remove
---
## Ce qu’il lit

Les événements de votre compte Stripe qui peuvent avoir besoin de vous : paiements échoués, litiges, résiliations et gros nouveaux abonnements, avec le client concerné.

## Ce qu’il peut faire

Rien dans Stripe. Il n’écrit jamais rien, ne rembourse et ne relance jamais un paiement.

## Le connecter

1. Dans Stripe, créez une clé restreinte avec Lecture sur Events, Customers et Account, et Aucun sur tout le reste.
2. Trouvez l’ID de votre compte (acct_...) sous Paramètres, Informations sur l’entreprise.
3. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources** et ouvrez Stripe. Sur votre propre ordinateur : **Connexions**, **+ Ajouter**, Stripe, ou `assistant connect stripe`.
4. Collez l’ID du compte et la clé, puis appuyez sur **Se connecter**.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Stripe, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le révoquer dans Stripe

Dans Stripe, ouvrez Développeurs, Clés API, et supprimez ou renouvelez la clé restreinte.
