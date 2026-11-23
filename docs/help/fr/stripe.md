---
title: Stripe
area: connections
summary: Échecs de paiement, litiges, annulations et nouveaux abonnements importants. Connexion en lecture seule.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## Ce que la connexion lit

Les événements de votre compte Stripe qui peuvent nécessiter votre attention : échecs de paiement, litiges, annulations et nouveaux abonnements importants, avec le client concerné. L’adresse e-mail du client relie l’événement à cette personne et à son organisation dans le [Graph](graph.md).

Un échec de paiement indique à quoi correspond le paiement (un premier paiement, un renouvellement) et quand Stripe réessaiera. Il n’indique pas pourquoi la carte a été refusée : l’événement Stripe ne précise pas cette raison. Ouvrez-le dans Stripe pour la connaître.

## Ce que la connexion peut faire

Rien dans Stripe. Elle ne rembourse rien, ne réessaie aucun paiement et ne modifie rien. Elle demande uniquement un accès en lecture, ce que Stripe vous indique avant l’installation.

## Connecter la connexion

Connectez-vous avec Stripe, c’est plus simple :

1. Dans le tableau de bord : **Connexions**, **Clients**, Stripe. Ou, sur la page de configuration d’une Machine hébergée à l’adresse app.themachine.computer/setup : **Autres sources**, Stripe. Sur votre propre ordinateur, associez d’abord votre Machine à votre compte.
2. Cliquez sur **Se connecter avec Stripe**. Stripe vous demande quel compte utiliser et indique ce que The Machine peut lire.
3. Cliquez sur **Installer**. Vous revenez à la page précédente et Stripe est connecté.

Sur votre propre ordinateur, vous pouvez aussi coller une clé restreinte :

1. Dans Stripe, créez une clé restreinte avec un accès en lecture à Events, Customers et Account, et aucun accès à tout le reste.
2. Trouvez l’identifiant de votre compte (acct_...) dans Paramètres, Informations sur l’entreprise.
3. Ouvrez Stripe comme indiqué ci-dessus (ou exécutez `assistant connect stripe`), puis ouvrez **Ou collez une clé restreinte**. Collez l’identifiant du compte et la clé, puis cliquez sur **Connecter**.

Sur votre propre ordinateur, si l’option de connexion à Stripe n’est pas encore disponible, Connexions vous l’indique et ouvre directement ce formulaire.

## Connecter la connexion une fois pour votre équipe

Dans une Fleet Travail, un propriétaire ou un administrateur connecte Stripe une fois et partage la connexion avec l’équipe :

1. Connectez Stripe sur votre propre Machine (voir ci-dessus). La section **Connexions partagées** de l’onglet Fleet propose aussi **Connecter Stripe**.
2. Dans l’onglet Fleet, ouvrez **Partager Stripe**. Tout le monde est sélectionné. Désélectionnez les personnes qui ne doivent pas y avoir accès, puis cliquez sur **Partager**.

Les Machines de vos collègues peuvent alors aussi accéder aux données. Connexions indique qui a partagé l’accès. Seuls les administrateurs de la Fleet peuvent le modifier ou l’arrêter. Votre Machine renouvelle leur accès toutes les heures. Tant qu’elle est éteinte, leur accès à Stripe est suspendu. Personne n’a accès à vos identifiants de connexion. Pour en savoir plus : [Fleets](fleet.md).

Si un collègue connecte aussi lui-même le même compte Stripe, les données ne sont lues qu’une fois : la connexion partagée reste inactive.

Une connexion Stripe établie par l’intermédiaire d’un service dont la clé donne aussi accès à d’autres applications ne peut pas être partagée. Connectez plutôt Stripe directement pour l’équipe.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Stripe, puis **Détails** et **Déconnecter**. Les données déjà importées sont conservées.
- Sur une Machine hébergée, si vous vous êtes connecté à Stripe, l’option **Déconnecter ↗** ouvre votre page de configuration. Cliquez sur **Retirer** à côté de Stripe.
- Si la connexion est partagée avec une Fleet, cliquez d’abord sur **Arrêter le partage** dans l’onglet Fleet.

## Révoquer l’accès dans Stripe

- Si vous vous êtes connecté avec Stripe : dans Stripe, ouvrez Paramètres, Applications installées, puis supprimez The Machine.
- Pour une clé restreinte : dans Stripe, ouvrez Developers, API keys, puis supprimez ou renouvelez la clé.
