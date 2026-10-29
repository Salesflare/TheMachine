---
title: Fleets
area: fleet
summary: Une Fleet Travail pour votre équipe, une Fleet Famille pour la maison. Des Machines qui s’entraident, selon vos règles de partage.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV
order: 1
---
The Machine Network relie les Machines. Ce qu’elles se disent est chiffré de bout en bout, et chaque Machine ne répond que selon vos règles.

## Types de Fleet

- **Fleet Travail** : votre équipe. Transférez du travail, demandez qui connaît quelqu’un, obtenez des mises en relation et un brief d’équipe.
- **Fleet Famille** : jusqu’à 6 personnes. Quand tout le monde est libre, des tâches et des projets partagés. Gratuite. Voir [Famille](family.md).
- **Amis** : n’importe qui sur The Machine, un par un. Gratuit. Voir [Amis](friends.md).

## L’onglet Fleet

Il apparaît dès que vous faites partie d’une Fleet, avec un volet pour chaque Fleet, Famille, Amis, Network, Partage et Activité.

## Demander à votre Fleet

Demandez « qui connaît quelqu’un chez Acme ? » depuis l’onglet Fleet, ou avec **Demander à la Fleet** sur une organisation dans le [Graph](graph.md). La Machine de chaque collègue répond selon ses propres règles de partage, et lui demande d’abord quand la règle le prévoit.

## Réponses automatiques dans une Fleet Travail

Dans une Fleet Travail Standard, votre Machine répond d’elle-même aux demandes d’un collègue de type **qui connaît quelqu’un**, **contexte de réunion** (« qui est cet invité ? ») et **qui gère les e-mails partagés**. Elle n’utilise que ce que le [Graph d’équipe](team-graph.md) partage déjà avec votre équipe. Les fils privés, perso et sensibles ne comptent jamais, et elle ne cite que des personnes que le Graph d’équipe partage déjà. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**.

Pour en arrêter une, réglez-la sur **Jamais** sous **Partage**. Une règle enregistrée sur **Me demander d’abord** fonctionne désormais comme **Toujours**. Tant que le partage du Graph d’équipe de votre Fleet est désactivé, qui connaît quelqu’un et contexte de réunion continuent de vous demander d’abord.

Les Fleets Travail Prudentes, Amis et Famille vous demandent toujours d’abord. Les mises en relation, transferts, suivis partagés et questions libres gardent leurs propres règles.

## Apprentissages de l’équipe

Au plus une fois par jour, votre Machine lit quelques fils clients que le Graph d’équipe partage déjà avec votre équipe, et note comment l’équipe travaille. Par exemple : « Les demandes de remboursement reçoivent une réponse depuis la boîte support avec le modèle de remboursement. » Ils apparaissent dans le volet de votre Fleet Travail sous **Apprentissages de l’équipe**, pour tout le monde dans la Fleet, et chacun est consigné sous **Activité**. Personne n’est consulté avant.

- Seulement des fils où quelqu’un de votre équipe a écrit. Jamais des fils privés, perso ou sensibles.
- Seulement ce qui vaut pour plusieurs clients : un processus, un outil, un style d’écriture, ou qui gère quoi. Jamais quelque chose sur un seul client, jamais des retours sur votre propre produit, et jamais de noms, adresses, numéros ou citations.
- Chacun porte une étiquette : son type, le fait qu’il vient de conversations d’équipe, et qu’il est pour cette Fleet. Ceux dont elle n’est pas sûre sont écartés.

Tout membre de la Fleet peut **Retirer** un apprentissage. Il disparaît pour tout le monde et n’est pas recréé. Pour arrêter, désactivez **Proposer de partager des apprentissages** dans Paramètres, Sécurité. Les Fleets Travail Prudentes n’en ont aucun.

## Demandes de brief

Un collègue qui a activé le brief d’équipe demande chaque matin à votre Machine des chiffres et des dates. Dans une Fleet Travail, votre Machine répond d’elle-même, avec seulement ce que le [Graph d’équipe](team-graph.md) partage déjà avec votre équipe. Les fils privés et perso ne comptent jamais, et rien ne part tant que le partage du Graph d’équipe de votre Fleet est désactivé. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**. Cela ne devient jamais une tâche ni une notification.

Pour arrêter, désactivez **Partager mes faits de brief avec l’équipe** dans l’onglet Fleet, sous **Partage**. Leur brief vous indique alors comme sans réponse.

Dans une Fleet Prudente, les demandes vous attendent dans l’onglet Fleet sous **Demandes de brief** : **Partager une fois**, **Toujours partager**, **Refuser** ou **Jamais**. Seule la dernière demande de chaque collègue attend, et celles sans réponse expirent. Rien n’est partagé tant que vous n’avez pas choisi.

## Graph d’équipe

Dans une Fleet Travail, le travail client est partagé avec votre équipe, après votre relecture. Voir [Graph d’équipe](team-graph.md).

## Connexions partagées

Un propriétaire ou un admin peut connecter Stripe ou Intercom une fois et le partager avec l’équipe, depuis l’encadré **Connexions partagées** de l’onglet Fleet. Les Machines des collègues le lisent, en lecture seule, et voient qui l’a partagé. Seuls les admins le modifient ou l’arrêtent. Voir [Stripe](stripe.md) et [Intercom](intercom.md).

## Ce que votre Machine répond

Réglez-le pour chaque Fleet, dans le volet Partage. Voir [Règles de partage](sharing-rules.md). Les **Paramètres** ont un raccourci : **Règles Fleet**.

## Connexion d’entreprise

Pour une Fleet Travail hébergée. Un propriétaire ou un admin connecté avec un compte Google Workspace ou Microsoft 365 d’entreprise peut activer la **Connexion d’entreprise** sur la page du compte. Elle utilise le domaine de ce compte.

Les collègues qui se connectent avec un compte sur ce domaine voient alors **Demander à rejoindre**. Un propriétaire ou un admin doit **Approuver** chaque demande. Les comptes Gmail personnels et Outlook.com ne comptent jamais.

Retirer quelqu’un de la Fleet le déconnecte partout.

Pour rejoindre une Fleet, en créer une ou associer une Machine sur votre propre ordinateur, voir [Forfaits et facturation](plans-and-billing.md) et [Amis et le Network](friends.md).

## Pour les propriétaires et les admins

La partie Fleet de la page de votre compte affiche deux éléments de plus :

- **Retirés récemment** : chaque personne retirée, ou partie. La ligne indique **Supprimé, confirmé** une fois que sa Machine a supprimé les données de travail, que Google a confirmé la déconnexion et que tout jeton partagé qu’elle avait a été remplacé. D’ici là, elle indique **En attente** et pourquoi.
- **Activité** : qui a fait quoi et quand. Invitations, arrivées, retraits, rôles, Machines hébergées et facturation, connecteurs partagés et accords. La liste indique aussi chaque fois que notre équipe a ouvert la Machine d’un membre ou ses journaux. Jamais le contenu des messages. **Télécharger le CSV** l’exporte. Conservé 12 mois.

Après **Arrêter le partage**, un connecteur partagé affiche **Supprimé, confirmé** une fois que chaque Machine a supprimé le jeton.
