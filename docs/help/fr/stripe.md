---
title: Stripe
area: connections
summary: Échecs de paiement, litiges, résiliations et nouveaux abonnements importants. La connexion est en lecture seule.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## Ce que la connexion lit

Les événements de votre compte Stripe qui peuvent nécessiter votre intervention : échecs de paiement, litiges, résiliations et nouveaux abonnements importants, ainsi que le client concerné. L’adresse e-mail du client relie l’événement à cette personne et à son organisation dans le [Graph](graph.md).

## Ce que la connexion peut faire

Rien dans Stripe. Elle ne rembourse jamais, ne relance jamais de paiement et ne modifie rien. Elle demande uniquement un accès en lecture, comme Stripe vous l’indique avant l’installation.

## Connecter Stripe

Connectez-vous avec Stripe, en toute simplicité :

1. Dans le tableau de bord : **Connexions**, **Clients**, Stripe. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Stripe. Sur votre ordinateur, associez d’abord votre Machine à votre compte.
2. Cliquez sur **Se connecter avec Stripe**. Stripe vous demande de choisir un compte et vous indique ce que The Machine peut lire.
3. Cliquez sur **Installer**. Vous revenez à la page de départ et Stripe est connecté.

Sur votre ordinateur, vous pouvez aussi coller une clé à accès restreint :

1. Dans Stripe, créez une clé à accès restreint avec un accès en lecture aux événements, aux clients et au compte, et aucun accès au reste.
2. Trouvez l’identifiant de votre compte (acct_...) sous Paramètres, Informations sur l’entreprise.
3. Ouvrez Stripe comme indiqué ci-dessus (ou exécutez `assistant connect stripe`), ouvrez **Ou collez une clé restreinte**, collez l’identifiant du compte et la clé, puis cliquez sur **Connecter**.

Sur votre ordinateur, si la connexion avec Stripe n’est pas encore disponible, Connexions vous l’indique et ouvre directement ce formulaire.

## Connecter Stripe une fois pour toute l’équipe

Dans une Fleet Travail, un propriétaire ou un administrateur connecte Stripe une seule fois et partage la connexion avec l’équipe :

1. Connectez Stripe sur votre Machine (voir ci-dessus). La section **Connexions partagées** de l’onglet Fleet contient aussi le bouton **Connecter Stripe**.
2. Dans l’onglet Fleet, ouvrez **Partager Stripe**. Tout le monde est sélectionné. Désélectionnez les personnes qui ne doivent pas y avoir accès, puis cliquez sur **Partager**.

Les Machines des membres de l’équipe peuvent alors aussi lire les données. Connexions indique qui a partagé la connexion. Seuls les administrateurs de la Fleet peuvent la modifier ou y mettre fin. Votre Machine renouvelle leur accès toutes les heures. Si elle est éteinte, leur accès à Stripe est suspendu. Personne n’a accès à vos identifiants de connexion. En savoir plus : [Fleets](fleet.md).

Si un membre de l’équipe connecte aussi lui-même le même compte Stripe, les données ne sont lues qu’une fois : la connexion partagée reste inactive.

Une connexion Stripe établie via un service dont la clé donne aussi accès à d’autres applications ne peut pas être partagée. Connectez directement Stripe pour l’équipe.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Stripe, cliquez sur **Détails**, puis sur **Déconnecter**. Les données déjà importées sont conservées.
- Sur une Machine hébergée, la connexion Stripe affiche **Déconnecter ↗**, qui ouvre votre page de configuration. Cliquez sur **Retirer** à côté.
- Si la connexion est partagée avec une Fleet : cliquez d’abord sur **Arrêter le partage** dans l’onglet Fleet.

## Révoquer l’accès dans Stripe

- Si vous vous êtes connecté avec Stripe : dans Stripe, ouvrez Paramètres, Applications installées, puis supprimez The Machine.
- Avec une clé à accès restreint : dans Stripe, ouvrez Développeurs, Clés API, puis supprimez ou renouvelez la clé.
