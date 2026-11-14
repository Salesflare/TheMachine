---
title: Fleets
area: fleet
summary: Une Work Fleet pour votre équipe, une Family Fleet pour la maison. Les Machines s’entraident selon vos règles de partage.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
translated: c9650fc4ffe00e16
---
Une Fleet permet à votre Machine de travailler avec celles de votre équipe, de votre famille ou de vos amis, sur The Machine Network. Les informations qu’elles échangent sont chiffrées de bout en bout, et votre Machine ne répond qu’en suivant vos règles.

## Types de Fleet

- **Work Fleet** : votre équipe. Transférez du travail, demandez **qui connaît quelqu’un**, obtenez des mises en relation et un brief d’équipe.
- **Family Fleet** : jusqu’à 6 personnes. Des tâches et des projets partagés, quand tout le monde est disponible. Gratuit. Voir [Famille](family.md).
- **Amis** : avec n’importe quelle personne sur The Machine, une par une. Gratuit. Voir [Amis](friends.md).

## L’onglet Fleet

Il s’affiche dès que vous rejoignez une Fleet, avec un panneau pour chaque Fleet, ainsi que les panneaux Famille, **Amis**, Network, **Partage** et **Activité**.

## Ce qu’elle coûte, quitter et créer une Fleet

Sous le nom de chaque Fleet, **Ce qu’elle coûte** indique le nombre de places, qui paie pour votre Machine et, pour le propriétaire, la carte et les factures de la Fleet. **Quitter cette Fleet** vous permet de la quitter. Le propriétaire doit d’abord transférer la Fleet à quelqu’un d’autre. **Créer une autre Fleet** en crée une nouvelle.

Chaque option ouvre la page correspondante de votre compte. Si le prix change, le montant s’affiche pour que vous le confirmiez d’abord. Sur une Machine auto-hébergée, votre compte s’ouvre dans un nouvel onglet, où vous devez vous connecter.

## Poser une question à votre Fleet

Demandez « qui connaît quelqu’un chez Acme ? » depuis l’onglet Fleet, ou sélectionnez **Demander à la Fleet** sur une organisation dans le [Graph](graph.md). La Machine de chaque coéquipier répond selon ses propres règles de partage et lui demande d’abord son accord si sa règle le prévoit.

## Réponses automatiques dans une Work Fleet

Dans une Work Fleet Standard, votre Machine répond automatiquement à trois types de questions de vos coéquipiers : **qui connaît quelqu’un**, le **contexte de réunion** (« qui est cet invité ? ») et **qui gère les e-mails partagés**. Elle utilise uniquement les informations que le [Team Graph](team-graph.md) partage déjà avec votre équipe, jamais les échanges privés, personnels ou sensibles. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**.

Pour désactiver une réponse, choisissez **Jamais** sous **Partage**. Une règle réglée sur **Me demander d’abord** fonctionne comme **Toujours**. Tant que le partage du Team Graph est désactivé, les questions sur les personnes que l’on connaît et le contexte de réunion vous sont d’abord soumises.

Les Work Fleets en mode prudent, les amis et la famille vous demandent toujours votre accord. Les mises en relation, les transferts et les questions gratuites suivent leurs propres règles.

## Apprentissages de l’équipe

Votre Machine note la façon dont votre équipe travaille à partir des échanges clients que le Team Graph partage déjà, au maximum une fois par jour. Par exemple : « Les demandes de remboursement reçoivent une réponse depuis la boîte de réception du support, avec le modèle de remboursement. » Ces apprentissages s’affichent dans le panneau de votre Work Fleet, sous **Apprentissages de l’équipe**, où tout le monde dans la Fleet peut les consulter. Chacun est également consigné sous **Activité**. Personne n’est sollicité au préalable.

- Uniquement les échanges auxquels une personne de votre équipe a participé. Jamais les échanges privés, personnels ou sensibles.
- Uniquement les éléments qui s’appliquent à plusieurs clients : un processus, un outil, un style rédactionnel ou la répartition des tâches. Jamais un élément concernant un seul client, un commentaire sur votre propre produit, ni des noms, des adresses, des numéros ou des citations.
- Les éléments dont elle n’est pas sûre sont écartés.

Votre Machine utilise les apprentissages pertinents lorsqu’elle prépare une tâche professionnelle pour cette entreprise. Vos propres faits, règles et compétences restent prioritaires, et les tâches personnelles ne les utilisent jamais. Une tâche qui s’appuie sur un apprentissage le précise, par exemple : « Apprentissage de l’équipe utilisé : les remboursements sont envoyés depuis la boîte de réception du support. » Sélectionnez **Retirer** pour le supprimer pour toute la Fleet.

Toute personne dans la Fleet peut **Retirer** un apprentissage. Il disparaît pour tout le monde et ne sera pas créé à nouveau. Pour les désactiver, désactivez **Proposer de partager des apprentissages** dans Paramètres, Sécurité. Les Work Fleets en mode prudent n’en reçoivent pas.

## Brief d’équipe

Choisissez **Quotidienne** ou **Hebdomadaire** pour le **brief d’équipe** dans l’onglet Fleet, sous **Partage**. Votre Machine demande alors aux Machines de vos coéquipiers des nombres et des dates. Les éléments qui nécessitent votre attention apparaissent dans les tâches, sous Travail : un client qui attend la réponse d’un coéquipier, une entreprise sans activité depuis au moins deux semaines, deux d’entre vous qui écrivent aux mêmes personnes ou une réunion partagée.

- Une tâche indique qui doit agir, depuis quand, ce qui a été demandé et ce qui est en jeu, par exemple un projet en cours. Si elle n’a rien de précis à signaler, elle reste une ligne du brief et ne devient pas une tâche.
- Les liens de l’entreprise et des coéquipiers mènent à leurs pages. **Détails** affiche ce qu’ils ont écrit (sélectionnez cette option pour le lire), ce qui est en jeu, les personnes de l’équipe en contact et leurs échanges les plus récents, uniquement ceux que le [Team Graph](team-graph.md) partage.
- Lorsque les informations écrites se trouvent uniquement dans les e-mails d’un coéquipier, la tâche indique à qui poser la question.
- **Demander à l’équipe** leur envoie une question préremplie à ce sujet. Leurs réponses apparaissent dans la tâche.
- **Pas nécessaire** clôt la tâche et permet au brief d’en tirer des enseignements. Elle ne réapparaît qu’en cas de nouveauté.
- Lorsqu’une personne répond ou prend la tâche en charge, celle-ci se clôt automatiquement. Une tâche concernant une entreprise pour laquelle vous avez déjà une tâche est ajoutée à celle-ci.

## Demandes de brief

Chaque matin, un coéquipier qui a activé le brief d’équipe demande à votre Machine des nombres et des dates. Dans une Work Fleet, votre Machine répond automatiquement, uniquement à partir des informations déjà partagées par le [Team Graph](team-graph.md), et ne répond pas tant que le partage du Team Graph est désactivé. Chaque réponse apparaît dans l’onglet Fleet, sous **Activité**, jamais sous forme de tâche ou de notification.

Pour arrêter le partage, désactivez **Partager mes faits de brief avec l’équipe** dans l’onglet Fleet, sous **Partage**. Votre nom apparaîtra alors dans le brief de vos coéquipiers avec la mention « sans réponse ».

Dans une Fleet en mode prudent, les demandes apparaissent dans l’onglet Fleet, sous **Demandes de brief** : **Partager une fois**, **Toujours partager**, **Refuser** ou **Jamais**. Rien n’est partagé avant votre choix, et les demandes sans réponse expirent.

## Team Graph

Dans une Work Fleet, le travail client est partagé avec votre équipe après que vous l’avez vérifié. Voir [Team Graph](team-graph.md).

## Connexions partagées

Un propriétaire ou un administrateur peut connecter Stripe ou Intercom une seule fois et partager la connexion avec l’équipe depuis **Connexions partagées** dans l’onglet Fleet. Les coéquipiers peuvent la consulter, mais pas la modifier, et voient qui l’a partagée. Seuls les administrateurs peuvent la modifier ou arrêter le partage. Voir [Stripe](stripe.md) et [Intercom](intercom.md).

## Ce à quoi votre Machine répond

Définissez les règles pour chaque Fleet dans le panneau Partage. Voir [Règles de partage](sharing-rules.md). Un raccourci vers **Règles Fleet** se trouve dans **Paramètres**.

## Connexion avec un compte d’entreprise

Permettez à vos coéquipiers de rejoindre la Fleet avec leur compte d’entreprise. Dans une Work Fleet hébergée, un propriétaire ou un administrateur connecté avec Google Workspace ou Microsoft 365 peut activer **Connexion avec un compte d’entreprise** sur la page Compte.

Les coéquipiers qui se connectent avec le domaine de leur entreprise voient **Demander à rejoindre**. Un propriétaire ou un administrateur doit **Approuver** chaque demande. Les comptes Gmail personnels et Outlook.com ne sont jamais pris en compte.

Supprimer une personne de la Fleet la déconnecte de tous ses appareils.

Pour rejoindre une Fleet, en créer une ou associer une Machine sur votre propre ordinateur, consultez [Offres et facturation](plans-and-billing.md) et [Amis et Network](friends.md).

## Pour les propriétaires et les administrateurs

**Gérer** dans l’onglet Fleet répertorie chaque Fleet que vous gérez : ses membres, leurs rôles et les invitations. Sur une Machine hébergée, vous pouvez inviter des personnes, modifier les rôles, supprimer des membres et répondre aux demandes d’adhésion directement depuis cette page. Toute modification qui a une incidence sur le prix ouvre votre compte pour que vous puissiez d’abord la confirmer. Sur une Machine auto-hébergée, la page indique qui en fait partie et contient un lien vers les paramètres de cette Fleet dans votre compte, où vous gérez les membres et les invitations.

**Réglages de la Fleet**, sous le nom de chaque Fleet dans son panneau et dans Gérer, ouvre les paramètres de cette Fleet dans votre compte : les connexions partagées, la sécurité, la connexion avec un compte d’entreprise, les réponses de la Machine et ces deux éléments :

- **Retirés récemment** : chaque personne supprimée ou qui a quitté la Fleet. « Supprimée, confirmé » signifie que sa Machine a effacé les données de travail et qu’elle est déconnectée de tous ses appareils. D’ici là, le statut indique **En attente** et en précise la raison.
- **Activité** : qui a fait quoi et quand : invitations, adhésions, suppressions, rôles, Machines hébergées, facturation, connexions partagées et approbations. La liste indique aussi chaque fois que notre équipe d’assistance a consulté le rapport de Machine d’un membre ou ses journaux. Jamais le contenu des messages. **Télécharger le CSV** permet de l’exporter. Les données sont conservées 12 mois.

**Me demander avant de démarrer la Machine d’un membre**, pour le propriétaire : si l’option est activée, la Machine d’un nouveau membre attend votre accord, même dans une Fleet gratuite. Si elle est désactivée, la Machine démarre immédiatement dans une Fleet gratuite et vous en êtes informé. Une Machine payante attend toujours que vous confirmiez le montant.

Après avoir sélectionné **Arrêter le partage**, une connexion partagée affiche « Supprimée, confirmé » dès que toutes les Machines en ont perdu l’accès.
