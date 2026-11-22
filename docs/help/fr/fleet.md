---
title: Fleets
area: fleet
summary: Une Fleet Travail pour votre équipe, une Fleet Famille pour la maison. Des Machines qui s’entraident selon vos règles de partage.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: 974bbbb54608efc3
---
Une Fleet permet à votre Machine de collaborer avec les Machines de votre équipe, de votre famille ou de vos amis, via The Machine Network. Les informations qu’elles échangent sont chiffrées de bout en bout, et votre Machine répond uniquement selon vos règles.

## Types de Fleet

- **Fleet Travail** : votre équipe. Transférez du travail, demandez qui connaît quelqu’un, obtenez des mises en relation et un brief d’équipe.
- **Fleet Famille** : jusqu’à 6 personnes. Quand tout le monde est disponible, partagez des tâches et des projets. C’est gratuit ; les Machines hébergées dans la Fleet bénéficient d’un tarif familial. Voir [Famille](family.md).
- **Amis** : n’importe qui sur The Machine, une personne à la fois. C’est gratuit. Voir [Amis](friends.md).

## L’onglet Fleet

Il s’affiche dès que vous rejoignez une Fleet. Vous y trouverez un panneau pour chaque Fleet, puis Amis, Network, Partage et Activité. Les propriétaires et les administrateurs ont aussi accès à **Gérer**, et une Fleet Travail qui partage son Graph dispose de **Ce qui est partagé**.

## Coût, départ et création d’une Fleet

Sous le nom de chaque Fleet, **Ce qu’elle coûte** indique le nombre de places, qui paie pour votre Machine et, pour le propriétaire, la carte et les factures de la Fleet. **Quitter cette Fleet** vous permet de la quitter ; le propriétaire doit d’abord transférer sa propriété à quelqu’un d’autre. **Créer une autre Fleet** permet d’en créer une nouvelle.

Chaque option ouvre la section correspondante de votre compte. Si le prix change, le montant à confirmer s’affiche d’abord. Sur une Machine hébergée par vos soins, ces options ouvrent votre compte dans un nouvel onglet, où vous pouvez vous connecter.

## Posez une question à votre Fleet

Depuis l’onglet Fleet, demandez « qui connaît quelqu’un chez Acme ? », ou choisissez **Interroger la Fleet** sur une organisation dans le [Graph](graph.md). La Machine de chaque collègue répond selon ses propres règles de partage et lui demande d’abord son accord si la règle le prévoit.

Pour toute autre question, utilisez **Demandez ce que vous voulez** dans le panneau de votre Fleet Travail. Chaque collègue reçoit une réponse en brouillon, préparée à partir de ses propres comptes professionnels. Rien n’est transmis tant qu’il ne l’envoie pas.

## Réponses automatiques dans une Fleet Travail

Dans une Fleet Travail Standard, votre Machine répond automatiquement à trois types de questions des collègues : **qui connaît quelqu’un**, **contexte de réunion** (« qui est cette personne invitée ? ») et **qui gère les e-mails partagés**. Elle utilise uniquement les informations que le [Graph d’équipe](team-graph.md) partage déjà avec votre équipe, jamais les échanges privés, personnels ou sensibles. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**.

Pour désactiver l’une de ces réponses, réglez-la sur **Jamais** dans **Partage**. Une règle réglée sur **Me demander d’abord** fonctionne comme **Toujours**. Tant que le partage du Graph d’équipe est désactivé, les questions sur les personnes que quelqu’un connaît et le contexte des réunions vous sont d’abord adressées.

Les Fleets Travail prudentes, les Amis et les Fleets Famille vous demandent toujours d’abord votre accord. Les mises en relation personnalisées, les transferts et les questions gratuites gardent leurs propres règles.

## Apprentissages de l’équipe

Votre Machine consigne le fonctionnement de votre équipe à partir des échanges clients déjà partagés par le Graph d’équipe, au maximum une fois par jour. Par exemple : « Les demandes de remboursement reçoivent une réponse depuis la boîte de réception du support, avec le modèle de remboursement. » Ils apparaissent dans le panneau de votre Fleet Travail, sous **Apprentissages de l’équipe**, et sont visibles par tout le monde dans la Fleet. Chacun est également enregistré sous **Activité**. Personne n’est sollicité au préalable.

- Seuls les échanges auxquels une personne de votre équipe a participé sont pris en compte. Jamais les échanges privés, personnels ou sensibles.
- Seuls les éléments qui se vérifient auprès de plusieurs clients sont retenus : un processus, un outil, un style rédactionnel ou la répartition des responsabilités. Rien qui concerne un seul client, aucun commentaire sur votre propre produit, et ni noms, adresses, chiffres ou citations.
- Les éléments incertains sont écartés.

Votre Machine utilise les apprentissages pertinents lorsqu’elle prépare une tâche professionnelle pour cette entreprise. Vos propres informations, règles et compétences restent prioritaires, et les tâches personnelles n’en tiennent jamais compte. Une tâche qui en utilise un le précise, par exemple : « Un apprentissage de l’équipe a été utilisé : les remboursements sont traités depuis la boîte de réception du support. » Touchez **Retirer** pour le supprimer pour toute la Fleet.

N’importe qui dans la Fleet peut **Retirer** un apprentissage : il disparaît pour tout le monde et ne sera pas créé à nouveau. Pour désactiver cette fonction, désactivez **Proposer de partager des apprentissages** dans Paramètres, Sécurité. Les Fleets Travail prudentes n’en reçoivent aucun.

## Brief d’équipe

Choisissez **Quotidienne** ou **Hebdomadaire** pour le **Brief d’équipe** dans l’onglet Fleet, sous **Partage**. Votre Machine demande alors aux Machines de vos collègues des nombres et des dates. Les éléments qui nécessitent votre attention apparaissent dans les tâches, sous Travail : un client qui attend la réponse d’un collègue, une entreprise sans nouvelles depuis au moins deux semaines, deux d’entre vous qui écrivent aux mêmes personnes ou une réunion partagée.

- Une tâche indique qui doit agir, depuis quand, ce qui a été demandé et ce qui est en jeu, par exemple un projet en cours. Si rien de précis n’est à signaler, l’élément reste une ligne dans le brief et ne devient pas une tâche.
- Les liens vers l’entreprise et les collègues ouvrent leurs pages. **Détails** affiche ce qu’ils ont écrit (touchez cette option pour le lire), ce qui est en jeu, les personnes de l’équipe en contact et leurs derniers échanges. Seules les informations partagées par le [Graph d’équipe](team-graph.md) sont affichées.
- Si ce qu’ils ont écrit se trouve uniquement dans les e-mails d’un collègue, la tâche indique qui contacter.
- **Demander à l’équipe** leur envoie une question préremplie à ce sujet. Leurs réponses s’affichent dans la tâche.
- **Pas nécessaire** clôt la tâche et le brief en tient compte. Elle ne réapparaît qu’en cas de nouvel élément.
- Quand quelqu’un répond ou s’en charge, la tâche se clôt automatiquement. Si elle concerne une entreprise pour laquelle vous avez déjà une tâche, elle est ajoutée à celle-ci.

## Demandes de brief

Chaque matin, un collègue dont le brief d’équipe est activé demande à votre Machine des nombres et des dates. Dans une Fleet Travail, votre Machine répond automatiquement avec les seules informations déjà partagées par le [Graph d’équipe](team-graph.md), et ne répond pas lorsque le partage du Graph d’équipe est désactivé. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**, jamais sous forme de tâche ou de notification.

Pour arrêter cela, désactivez **Partager mes faits de brief avec l’équipe** dans l’onglet Fleet, sous **Partage**. Votre nom apparaîtra alors dans leur brief comme n’ayant pas répondu.

Dans une Fleet prudente, les demandes apparaissent dans l’onglet Fleet, sous **Demandes de brief**. Choisissez **Partager une fois**, **Toujours partager**, **Refuser** ou **Jamais**. Rien n’est partagé avant que vous choisissiez une option, et les demandes sans réponse expirent.

## Graph d’équipe

Dans une Fleet Travail, le travail client est partagé avec votre équipe après que vous l’avez vérifié. Voir [Graph d’équipe](team-graph.md).

## Connexions partagées

Un propriétaire ou un administrateur peut connecter Stripe ou Intercom une seule fois et partager le service avec l’équipe depuis **Connexions partagées** dans l’onglet Fleet. Les collègues peuvent consulter la connexion, mais pas la modifier, et voient qui l’a partagée. Seuls les administrateurs peuvent la modifier ou arrêter le partage. Voir [Stripe](stripe.md) et [Intercom](intercom.md).

## Réponses de votre Machine

Configurez cette option pour chaque Fleet, dans le panneau Partage. Voir [Règles de partage](sharing-rules.md). **Paramètres** propose un raccourci : **Règles Fleet**.

## Connexion avec le compte de l’entreprise

Permettez aux collègues de rejoindre la Fleet avec leur compte professionnel. Dans une Fleet Travail hébergée, un propriétaire ou un administrateur connecté avec Google Workspace ou Microsoft 365 peut activer **Connexion avec le compte de l’entreprise** sur la page Compte.

Les collègues qui se connectent avec le domaine de l’entreprise voient **Demander à rejoindre**. Un propriétaire ou un administrateur doit **Approuver** chaque demande. Les comptes personnels Gmail et Outlook.com ne sont jamais acceptés.

Retirer une personne de la Fleet la déconnecte partout.

Pour rejoindre une Fleet, en créer une ou jumeler une Machine sur votre propre ordinateur, consultez [Forfaits et facturation](plans-and-billing.md) et [Les amis et le Network](friends.md).

## Pour les propriétaires et les administrateurs

**Gérer** dans l’onglet Fleet répertorie chaque Fleet dont vous vous occupez : ses membres, leurs rôles et les invitations. Sur une Machine hébergée, vous pouvez inviter des personnes, modifier leurs rôles, les retirer et répondre aux demandes d’adhésion directement depuis cette page. Si une modification a une incidence sur le prix, votre compte s’ouvre pour que vous la confirmiez d’abord. Sur une Machine hébergée par vos soins, la page indique les membres et fournit un lien vers les paramètres de la Fleet dans votre compte, où vous pouvez gérer ses membres et ses invitations.

**Paramètres de la Fleet**, sous le nom de chaque Fleet dans son panneau et dans Gérer, ouvre les paramètres de cette Fleet dans votre compte : connexions partagées, sécurité, connexion avec le compte de l’entreprise, Machines autorisées à répondre, ainsi que les deux options suivantes :

- **Personnes récemment retirées** : chaque personne qui a été retirée ou qui est partie. « Retiré, confirmé » signifie que sa Machine a supprimé les données professionnelles et qu’elle est déconnectée partout. Jusque-là, l’état **En attente** s’affiche, avec la raison.
- **Activité** : qui a fait quoi et quand : invitations, arrivées, retraits, rôles, Machines hébergées, facturation, connexions partagées et approbations. La liste indique aussi chaque fois que notre équipe d’assistance a consulté le rapport ou les journaux de la Machine d’un membre. Le contenu des messages n’est jamais inclus. **Télécharger le CSV** permet d’exporter la liste. Elle est conservée pendant 12 mois.

**Me demander avant de démarrer la Machine d’un membre**, pour le propriétaire : lorsque cette option est activée, la Machine d’un nouveau membre attend votre accord, même dans une Fleet gratuite. Si elle est désactivée, dans une Fleet gratuite, la Machine démarre tout de suite et vous en êtes informé. Une Machine payante attend toujours que vous confirmiez le montant.

Après avoir choisi **Arrêter le partage**, une connexion partagée affiche « Retiré, confirmé » dès que toutes les Machines en ont perdu l’accès.
