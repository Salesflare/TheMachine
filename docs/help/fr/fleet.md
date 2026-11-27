---
title: Fleets
area: fleet
summary: Une Fleet Travail pour votre équipe, une Fleet Famille pour la maison. Des Machines qui s’entraident, selon vos règles de partage.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 17927ccd0e4aa40d
---
Une Fleet permet à votre Machine de travailler avec les Machines de votre équipe, de votre famille ou de vos amis, via The Machine Network. Les informations qu’elles échangent sont chiffrées de bout en bout, et votre Machine ne répond qu’en suivant vos règles.

## Types de Fleet

- **Fleet Travail** : votre équipe. Transférez du travail, demandez **qui connaît quelqu’un**, obtenez des mises en relation et un brief d’équipe.
- **Fleet Famille** : jusqu’à 6 personnes. Quand tout le monde est disponible, partagez des tâches et des projets, et posez des questions à la Machine des autres. C’est gratuit. Les Machines hébergées dans la Fleet bénéficient d’un tarif famille. Voir [Famille](family.md).
- **Amis** : ajoutez les personnes de The Machine une par une. C’est gratuit. Voir [Amis](friends.md).

## L’onglet Fleet

Il s’affiche dès que vous rejoignez une Fleet. Vous y trouverez un volet pour chaque Fleet, puis Amis, Network, Partage et Activité. Les propriétaires et les admins y trouvent aussi **Gérer**. Une Fleet Travail qui partage son Graph dispose également de l’onglet **Ce qui est partagé**.

## Coût, départ et création d’une Fleet

Sous le nom de chaque Fleet, **Ce qu’elle coûte** indique le nombre de places, qui paie pour votre Machine et, pour le propriétaire, la carte et les factures de la Fleet. **Quitter cette Fleet** vous permet de la quitter. Le propriétaire doit d’abord transférer son rôle à quelqu’un d’autre. **Créer une autre Fleet** en démarre une nouvelle.

Chaque option ouvre la page correspondante de votre compte. Si le prix change, le montant à confirmer s’affiche d’abord. Sur une Machine auto-hébergée, ces options ouvrent votre compte dans un nouvel onglet, où vous pouvez vous connecter.

## Posez une question à votre Fleet

Posez la question « qui connaît quelqu’un chez Acme ? » depuis l’onglet Fleet, ou choisissez **Demander à la Fleet** sur une organisation dans le [Graph](graph.md). La Machine de chaque collègue répond selon ses propres règles de partage et lui demande son accord d’abord si la règle le prévoit.

Pour toute autre question, utilisez **Demandez ce que vous voulez** dans le volet de votre Fleet Travail. Chaque collègue reçoit un brouillon de réponse préparé à partir de ses comptes professionnels, et rien ne vous est transmis avant qu’il l’envoie. Le brouillon ne tient compte que de ce qu’il a écrit ou des réunions auxquelles il a participé. Les messages seulement reçus, comme une newsletter ou un e-mail en copie, sont signalés comme trouvés, mais ne génèrent pas de brouillon.

## Réponses automatiques dans une Fleet Travail

Dans une Fleet Travail standard, votre Machine répond automatiquement à trois types de questions de collègues : **qui connaît quelqu’un**, **contexte de réunion** (« qui est cette personne invitée ? ») et **qui gère les e-mails partagés**. Elle utilise uniquement les informations du [Graph d’équipe](team-graph.md) déjà partagées avec votre équipe, jamais les échanges privés, personnels ou sensibles. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**.

Pour désactiver une réponse, réglez-la sur **Jamais** dans **Partage**. Une règle définie sur **Me demander d’abord** fonctionne comme **Toujours**. Tant que le partage du Graph d’équipe est désactivé, votre Machine vous demande d’abord votre accord pour les questions sur les personnes connues et le contexte des réunions.

Les Fleets Travail avec validation, les Fleets Amis et les Fleets Famille vous demandent toujours votre accord d’abord. Les mises en relation, les transferts et les questions gratuites suivent leurs propres règles.

## Apprentissages de l’équipe

Votre Machine note la façon dont votre équipe travaille à partir des échanges clients déjà partagés dans le Graph d’équipe, au maximum une fois par jour. Par exemple : « Les demandes de remboursement reçoivent une réponse depuis la boîte de réception du support, avec le modèle de remboursement. » Ces apprentissages apparaissent dans le volet de votre Fleet Travail, sous **Apprentissages de l’équipe**, et sont visibles par toutes les personnes de la Fleet. Chacun est aussi consigné sous **Activité**. Personne n’est consulté au préalable.

- Seuls les échanges auxquels une personne de votre équipe a participé sont utilisés. Jamais les échanges privés, personnels ou sensibles.
- Seuls les éléments qui se retrouvent chez plusieurs clients sont retenus : un processus, un outil, un style d’écriture ou la répartition des responsabilités. Jamais les informations sur un seul client, les commentaires sur votre propre produit, ni les noms, adresses, numéros ou citations.
- Les éléments dont votre Machine n’est pas sûre sont écartés.

Votre Machine utilise les apprentissages pertinents lorsqu’elle prépare une tâche professionnelle pour cette entreprise. Vos propres faits, règles et compétences passent en premier, et les tâches personnelles ne les utilisent jamais. Une tâche qui s’appuie sur un apprentissage le précise, par exemple : « Apprentissage de l’équipe utilisé : les remboursements sont envoyés depuis la boîte de réception du support. » Appuyez sur **Retirer** pour le supprimer de toute la Fleet.

N’importe qui dans la Fleet peut **Retirer** un apprentissage. Il disparaît pour tout le monde et ne sera pas créé à nouveau. Pour empêcher leur création, désactivez **Proposer de partager des apprentissages** dans Paramètres, Sécurité. Les Fleets Travail avec validation n’en reçoivent pas.

## Brief d’équipe

Dans l’onglet Fleet, sous **Partage**, choisissez **Quotidienne** ou **Hebdomadaire** pour le **Brief d’équipe**. Votre Machine demande alors aux Machines de vos collègues des nombres et des dates. Les éléments qui nécessitent votre attention apparaissent dans les tâches, sous Travail : un client qui attend la réponse d’un collègue, une entreprise sans activité depuis au moins deux semaines, deux personnes de votre équipe qui écrivent aux mêmes contacts, ou une réunion partagée.

- Une tâche indique qui doit agir, depuis quand, ce qui a été demandé et ce qui est en jeu, par exemple un projet en cours. S’il n’y a rien de précis à signaler, l’élément reste dans le brief et ne devient pas une tâche.
- L’entreprise et les collègues renvoient vers leurs pages. **Détails** indique ce qu’ils ont écrit (appuyez pour le lire), ce qui est en jeu, qui dans l’équipe est en contact et les derniers échanges, uniquement ceux que le [Graph d’équipe](team-graph.md) partage.
- Si ce qu’un collègue a écrit se trouve uniquement dans ses e-mails, la tâche indique qui contacter.
- **Demander à l’équipe** leur envoie une question préremplie à ce sujet. Leurs réponses s’affichent dans la tâche.
- **Pas nécessaire** clôt la tâche et permet au brief d’en tenir compte. Elle ne réapparaît qu’en cas de nouveauté.
- Quand quelqu’un répond ou prend la tâche en charge, elle se clôt automatiquement. Si une tâche concerne une entreprise pour laquelle vous avez déjà une tâche, elle s’y ajoute.

## Demandes de brief

Chaque matin, la Machine d’un collègue qui a activé le brief d’équipe demande à votre Machine des nombres et des dates. Dans une Fleet Travail, votre Machine répond automatiquement avec les seules informations déjà partagées dans le [Graph d’équipe](team-graph.md). Elle ne répond pas si le partage du Graph d’équipe est désactivé. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**, jamais sous forme de tâche ou de notification.

Pour arrêter le partage, désactivez **Partager mes faits de brief avec l’équipe** dans l’onglet Fleet, sous **Partage**. Votre nom apparaîtra alors dans leur brief comme n’ayant pas répondu.

Dans une Fleet avec validation, les demandes apparaissent dans l’onglet Fleet, sous **Demandes de brief**. Choisissez **Partager une fois**, **Toujours partager**, **Refuser** ou **Jamais**. Rien n’est partagé avant votre choix, et les demandes sans réponse expirent.

## Graph d’équipe

Dans une Fleet Travail, le travail client est partagé avec votre équipe après que vous l’avez vérifié. Voir [Graph d’équipe](team-graph.md).

## Connexions partagées

Un propriétaire ou un admin peut connecter Stripe ou Intercom une seule fois et partager la connexion avec l’équipe depuis **Connexions partagées** dans l’onglet Fleet. Les collègues peuvent consulter la connexion, mais pas la modifier, et voient qui l’a partagée. Seuls les admins peuvent la modifier ou arrêter le partage. Voir [Stripe](stripe.md) et [Intercom](intercom.md).

## Réponses de votre Machine

Définissez les règles pour chaque Fleet dans le volet Partage. Voir [Règles de partage](sharing-rules.md). Vous pouvez aussi y accéder depuis **Paramètres** : **Règles Fleet**.

## Connexion avec le compte de l’entreprise

Permettez à vos collègues de rejoindre la Fleet avec leur compte professionnel. Dans une Fleet Travail hébergée, un propriétaire ou un admin connecté avec Google Workspace ou Microsoft 365 peut activer **Connexion avec le compte de l’entreprise** sur la page Compte.

Les collègues qui se connectent avec le domaine de l’entreprise voient **Demander à rejoindre**. Un propriétaire ou un admin doit **Approuver** chaque demande. Les comptes Gmail personnels et Outlook.com ne sont jamais acceptés.

Le retrait d’une personne de la Fleet la déconnecte partout.

Pour rejoindre une Fleet, en créer une ou associer une Machine sur votre propre ordinateur, consultez [Forfaits et facturation](plans-and-billing.md) et [Les amis et le Network](friends.md).

## Pour les propriétaires et les admins

Dans l’onglet Fleet, **Gérer** répertorie chaque Fleet dont vous êtes responsable, ses membres, leurs rôles et les invitations. Sur une Machine hébergée, vous pouvez inviter des personnes, modifier les rôles, retirer des membres et répondre aux demandes d’adhésion depuis cet écran. Si une modification change le prix, votre compte s’ouvre d’abord pour vous permettre de la confirmer. Sur une Machine auto-hébergée, cette page indique les membres de la Fleet et renvoie vers ses paramètres dans votre compte, où vous pouvez gérer les membres et les invitations.

**Paramètres de la Fleet**, sous le nom de chaque Fleet dans son volet et dans Gérer, ouvre les paramètres de cette Fleet dans votre compte : connexions partagées, sécurité, connexion avec le compte de l’entreprise, Machine qui répond, ainsi que ces deux options :

- **Retirés récemment** : chaque personne retirée ou qui a quitté la Fleet. « Retiré, confirmé » signifie que sa Machine a supprimé les données professionnelles et qu’elle est déconnectée partout. Sinon, le statut **En attente** indique pourquoi.
- **Activité** : qui a fait quoi et quand : invitations, arrivées, retraits, rôles, Machines hébergées, facturation, connexions partagées et approbations. L’activité indique aussi chaque fois que notre équipe d’assistance a consulté le rapport d’une Machine membre ou ses journaux. Jamais le contenu des messages. **Télécharger le CSV** permet d’exporter les données. Elles sont conservées pendant 12 mois.

**Me demander avant de démarrer la Machine d’un membre**, pour le propriétaire : si l’option est activée, la Machine d’un nouveau membre attend votre accord, même dans une Fleet gratuite. Si elle est désactivée, la Machine démarre immédiatement dans une Fleet gratuite et vous en êtes informé. Une Machine payante attend toujours votre confirmation du montant.

Après **Arrêter le partage**, une connexion partagée affiche « Retirée, confirmée » dès que toutes les Machines en ont perdu l’accès.
