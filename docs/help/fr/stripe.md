---
title: Stripe
area: connections
summary: Paiements échoués, litiges, résiliations et gros nouveaux abonnements. Il ne fait que lire.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## Ce qu’il lit

Les événements de votre compte Stripe qui peuvent avoir besoin de vous : paiements échoués, litiges, résiliations et gros nouveaux abonnements, avec le client concerné. L’e-mail d’un client relie l’événement à cette personne et à son organisation dans le [Graph](graph.md).

## Ce qu’il peut faire

Rien dans Stripe. Il n’écrit jamais rien, ne rembourse et ne relance jamais un paiement. L’app Stripe de The Machine ne demande à Stripe que des autorisations de lecture, et Stripe les affiche avant que vous l’installiez.

## Le connecter

Connectez-vous avec Stripe, le plus simple :

1. Dans le tableau de bord : **Connexions**, **+ Ajouter**, Stripe. Ou sur la page de configuration d’une Machine hébergée, sur app.themachine.computer/setup : **Plus de sources**, Stripe. Sur votre propre ordinateur, associez-le d’abord à votre compte.
2. Appuyez sur **Se connecter avec Stripe**. Stripe demande quel compte, et montre ce que The Machine peut lire.
3. Appuyez sur **Installer**. Vous revenez là où vous avez commencé, et Stripe est connecté.

Ou collez plutôt une clé restreinte :

1. Dans Stripe, créez une clé restreinte avec Lecture sur Events, Customers et Account, et Aucun sur tout le reste.
2. Trouvez l’ID de votre compte (acct_...) sous Paramètres, Informations sur l’entreprise.
3. Ouvrez Stripe comme ci-dessus (ou lancez `assistant connect stripe`), ouvrez **Ou collez une clé restreinte**, collez l’ID du compte et la clé, puis appuyez sur **Se connecter**.

## Le connecter une fois pour votre équipe

Dans une Fleet Travail, un propriétaire ou un admin connecte Stripe une fois et le partage avec l’équipe :

1. Connectez Stripe sur votre propre Machine (ci-dessus). L’encadré **Connecteurs partagés** de l’onglet Fleet propose aussi **Connecter Stripe**.
2. Dans l’onglet Fleet, ouvrez **Partager Stripe**. Tout le monde est coché ; décochez qui ne doit pas l’avoir. Appuyez sur **Partager**.

Les Machines des collègues le lisent aussi, en lecture seule. Sous Connexions, il indique qui l’a partagé, et seuls les admins de la Fleet peuvent le modifier ou l’arrêter. Votre Machine renouvelle leur accès toutes les heures, donc si elle reste éteinte plus longtemps, leur Stripe se met en pause jusqu’à son retour. Personne ne reçoit jamais votre connexion elle-même. Détails : [Fleets](fleet.md).

Une connexion Stripe qui passe par un autre service, avec une seule clé pour de nombreuses connexions, ne peut pas être partagée : cette clé ouvre plus que Stripe. Connectez plutôt Stripe seul pour l’équipe.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Stripe, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.
- Partagé avec une Fleet : d’abord **Arrêter le partage** dans l’onglet Fleet.

## Le révoquer dans Stripe

- Connecté avec Stripe : dans Stripe, ouvrez Paramètres, Applications installées, et retirez The Machine.
- Clé restreinte : dans Stripe, ouvrez Développeurs, Clés API, et supprimez ou renouvelez la clé.
