---
title: Fleets
area: fleet
summary: Une Fleet Travail pour votre équipe, une Fleet Famille pour la maison. Des Machines qui s’entraident, selon vos règles de partage.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: f75a79e685f3a0cc
---
Une Fleet permet à votre Machine de travailler avec les Machines de votre équipe, de votre famille ou de vos amis, sur The Machine Network. Les informations qu’elles échangent sont chiffrées de bout en bout, et votre Machine répond uniquement selon vos règles.

## Types de Fleet

- **Fleet Travail** : votre équipe. Transférez du travail, demandez qui connaît quelqu’un, obtenez des mises en relation et un brief d’équipe.
- **Fleet Famille** : jusqu’à 6 personnes. Quand tout le monde est libre, partagez des tâches et des projets, et posez des questions aux Machines des autres. C’est gratuit, mais les Machines hébergées dans cette Fleet bénéficient d’un tarif famille. Voir [Famille](family.md).
- **Amis** : toute personne sur The Machine, une par une. C’est gratuit. Voir [Amis](friends.md).

## L’onglet Fleet

Il s’affiche dès que vous rejoignez une Fleet. Il comporte un volet pour chaque Fleet, puis les sections Amis, Network, Partage et Activité. Les propriétaires et les administrateurs ont aussi accès à **Gérer**, et une Fleet Travail qui partage son Graph dispose de la section **Ce qui est partagé**.

## Coût, départ et création d’une Fleet

Sous le nom de chaque Fleet, **Ce qu’elle coûte** indique le nombre de places, qui paie pour votre Machine et, pour le propriétaire, la carte et les factures de la Fleet. **Quitter cette Fleet** vous permet de la quitter. Le propriétaire doit d’abord la transférer à quelqu’un d’autre. **Créer une autre Fleet** permet d’en créer une nouvelle.

Chaque option ouvre la section correspondante de votre compte. Si le prix change, le montant s’affiche pour que vous le confirmiez d’abord. Sur une Machine auto-hébergée, ces options ouvrent votre compte dans un nouvel onglet, où vous vous connectez.

## Interroger votre Fleet

Posez la question « qui connaît quelqu’un chez Acme ? » depuis l’onglet Fleet, ou sélectionnez **Interroger la Fleet** sur une organisation dans le [Graph](graph.md). La Machine de chaque collègue répond selon ses propres règles de partage et lui demande d’abord son accord si la règle le prévoit.

Pour toute autre question, utilisez **Demandez ce que vous voulez** dans le volet de votre Fleet Travail. Chaque collègue reçoit un brouillon de réponse préparé à partir de ses propres comptes professionnels. Rien n’est partagé tant qu’il ne l’envoie pas.

## Réponses automatiques dans une Fleet Travail

Dans une Fleet Travail standard, votre Machine répond automatiquement à trois types de questions de vos collègues : **qui connaît quelqu’un**, **contexte de réunion** (« qui est cette personne invitée ? ») et **qui gère les e-mails partagés**. Elle utilise uniquement les informations déjà partagées avec votre équipe dans le [Graph d’équipe](team-graph.md), jamais des échanges privés, personnels ou sensibles. Chaque réponse s’affiche dans l’onglet Fleet, sous **Activité**.

Pour désactiver une réponse, sélectionnez **Jamais** sous **Partage**. Une règle réglée sur **Me demander d’abord** fonctionne comme **Toujours**. Tant que le partage du Graph de l’équipe est désactivé, les questions sur les personnes que quelqu’un connaît et le contexte de réunion vous sont d’abord soumises.

Les Fleets Travail prudentes, Amis et Famille vous demandent toujours d’abord votre accord. Les mises en relation, les transferts et les questions gratuites conservent leurs propres règles.

## Apprentissages de l’équipe

Votre Machine note les méthodes de travail de votre équipe à partir des échanges avec des clients déjà partagés dans le Graph de l’équipe, au maximum une fois par jour. Par exemple : « Les demandes de remboursement reçoivent une réponse depuis la boîte de réception du service client, avec le modèle de remboursement. » Ces apprentissages s’affichent dans le volet de votre Fleet Travail, sous **Apprentissages de l’équipe**, et sont visibles par tous les membres de la Fleet. Chacun est également consigné sous **Activité**. Aucun accord préalable n’est demandé.

- Seuls les échanges auxquels une personne de votre équipe a participé sont pris en compte. Jamais les échanges privés, personnels ou sensibles.
- Seules les informations valables pour plusieurs clients sont retenues : un processus, un outil, un style d’écriture ou la répartition des tâches. Jamais une information sur un seul client, un avis sur votre propre produit, ni des noms, adresses, numéros ou citations.
- Les apprentissages incertains sont écartés.

Votre Machine utilise les apprentissages pertinents lorsqu’elle prépare une tâche professionnelle pour cette entreprise. Vos propres faits, règles et compétences passent en premier, et les tâches personnelles ne les utilisent jamais. Une tâche qui en utilise un le précise, par exemple : « Apprentissage de l’équipe utilisé : les remboursements sont envoyés depuis la boîte de réception du service client. » Sélectionnez **Retirer** pour le supprimer pour toute la Fleet.

Chaque membre de la Fleet peut **Retirer** un apprentissage. Il disparaît pour tout le monde et ne sera pas recréé. Pour empêcher ces apprentissages, désactivez **Proposer de partager des apprentissages** dans les Paramètres, sous Sécurité. Les Fleets Travail prudentes n’en reçoivent pas.

## Brief d’équipe

Choisissez **Quotidienne** ou **Hebdomadaire** pour le **Brief d’équipe** dans l’onglet Fleet, sous **Partage**. Votre Machine demande alors aux Machines de vos collègues des nombres et des dates. Les éléments qui vous concernent apparaissent dans les tâches, sous Travail : un client qui attend une réponse d’un collègue, une entreprise sans nouvelles depuis au moins deux semaines, deux personnes de l’équipe qui écrivent aux mêmes contacts ou une réunion partagée.

- Une tâche indique qui doit répondre, depuis quand, ce qu’on lui a demandé et l’enjeu, par exemple un projet en cours. Si elle ne contient rien de précis, elle reste une ligne du brief et ne devient pas une tâche.
- L’entreprise et les collègues renvoient vers leurs pages. **Détails** affiche ce qu’ils ont écrit, que vous pouvez lire en le sélectionnant, l’enjeu, les personnes de l’équipe en contact et leurs derniers échanges. Seules les informations partagées par le [Graph d’équipe](team-graph.md) sont incluses.
- Si ce qu’ils ont écrit se trouve uniquement dans les e-mails d’un collègue, la tâche indique à qui poser la question.
- **Demander à l’équipe** leur envoie une question préremplie à ce sujet. Leurs réponses s’affichent dans la tâche.
- **Pas nécessaire** clôt la tâche et permet au brief d’en tirer des enseignements. Elle ne réapparaît qu’en cas de nouvel élément.
- Quand quelqu’un répond ou prend la tâche en charge, elle se clôt automatiquement. Une tâche concernant une entreprise pour laquelle vous avez déjà une tâche est ajoutée à celle-ci.

## Demandes de brief

Chaque matin, la Machine d’un collègue qui a activé le brief d’équipe demande à votre Machine des nombres et des dates. Dans une Fleet Travail, votre Machine répond automatiquement, uniquement avec les informations déjà partagées par le [Graph d’équipe](team-graph.md). Elle ne répond pas si le partage du Graph de l’équipe est désactivé. Chaque réponse s’affiche dans l’onglet Fleet, sous **Activité**, jamais sous forme de tâche ou de notification.

Pour désactiver cette option, désactivez **Partager mes faits de brief avec l’équipe** dans l’onglet Fleet, sous **Partage**. Votre nom apparaîtra alors dans leur brief comme n’ayant pas répondu.

Dans une Fleet prudente, les demandes apparaissent dans l’onglet Fleet, sous **Demandes de brief** : **Partager une fois**, **Toujours partager**, **Refuser** ou **Jamais**. Rien n’est partagé avant que vous choisissiez une option, et les demandes sans réponse expirent.

## Graph de l’équipe

Dans une Fleet Travail, le travail client est partagé avec votre équipe après que vous l’avez vérifié. Voir [Graph d’équipe](team-graph.md).

## Connexions partagées

Un propriétaire ou un administrateur peut connecter Stripe ou Intercom une seule fois et partager la connexion avec l’équipe depuis **Connexions partagées** dans l’onglet Fleet. Les collègues peuvent consulter la connexion, mais pas la modifier, et voient qui l’a partagée. Seuls les administrateurs peuvent la modifier ou arrêter le partage. Voir [Stripe](stripe.md) et [Intercom](intercom.md).

## Réponses de votre Machine

Configurez cette option pour chaque Fleet, dans le volet Partage. Voir [Règles de partage](sharing-rules.md). Un raccourci vers **Règles Fleet** se trouve dans les **Paramètres**.

## Connexion avec un compte d’entreprise

Permettez à vos collègues de rejoindre la Fleet avec leur compte d’entreprise. Dans une Fleet Travail hébergée, un propriétaire ou un administrateur connecté avec Google Workspace ou Microsoft 365 peut activer **Connexion avec un compte d’entreprise** sur la page Compte.

Les collègues qui se connectent avec le domaine de leur entreprise voient **Demander à rejoindre**. Un propriétaire ou un administrateur doit **Approuver** chaque demande. Les comptes Gmail personnels et Outlook.com ne sont jamais acceptés.

Retirer une personne de la Fleet la déconnecte partout.

Pour rejoindre une Fleet, en créer une ou associer une Machine sur votre propre ordinateur, consultez [Forfaits et facturation](plans-and-billing.md) et [Les amis et le Network](friends.md).

## Pour les propriétaires et les administrateurs

**Gérer** dans l’onglet Fleet répertorie chaque Fleet que vous gérez, ses membres, leurs rôles et les invitations. Sur une Machine hébergée, vous pouvez inviter des personnes, modifier leurs rôles, les retirer et répondre aux demandes pour rejoindre la Fleet, directement depuis cette page. Si une modification a une incidence sur le prix, votre compte s’ouvre pour que vous la confirmiez d’abord. Sur une Machine auto-hébergée, cette page indique les membres de la Fleet et propose un lien vers ses paramètres dans votre compte, où vous pouvez gérer les membres et les invitations.

**Paramètres de la Fleet**, sous le nom de chaque Fleet dans son volet et dans la section Gérer, ouvre les paramètres de cette Fleet dans votre compte : connexions partagées, sécurité, connexion avec un compte d’entreprise, Machine qui répond, ainsi que les deux options suivantes :

- **Personnes retirées récemment** : chaque personne retirée ou ayant quitté la Fleet. « Retrait confirmé » signifie que sa Machine a supprimé les données professionnelles et que la personne est déconnectée partout. Jusque-là, le statut indique **En attente** et en précise la raison.
- **Activité** : qui a fait quoi et quand : invitations, arrivées, retraits, rôles, Machines hébergées, facturation, connexions partagées et approbations. Cela inclut aussi chaque fois que notre équipe d’assistance consulte le rapport de Machine d’un membre ou ses journaux. Le contenu des messages n’est jamais inclus. **Télécharger le CSV** permet de l’exporter. Les données sont conservées pendant 12 mois.

Pour le propriétaire, l’option **Me demander avant de démarrer la Machine d’un membre** fonctionne ainsi : activée, la Machine d’un nouveau membre attend votre accord, même dans une Fleet gratuite. Désactivée, la Machine démarre immédiatement dans une Fleet gratuite, et vous en êtes informé. Une Machine payante attend toujours que vous confirmiez le montant.

Après avoir sélectionné **Arrêter le partage**, une connexion partagée affiche « Retrait confirmé » dès que toutes les Machines n’y ont plus accès.
