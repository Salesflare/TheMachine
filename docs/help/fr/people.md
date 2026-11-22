---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e808343918f7f47
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, à partir de vos messages et réunions. Les newsletters, reçus et autres envois ne créent pas de personne tant que vous n’avez pas répondu. Ils apparaissent sous Expéditeurs masqués, en bas de la liste : **Afficher comme personne** en ajoute une. Les champs, tags et imports fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [Le Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom propre d’un magasin) est associée à son organisation, et non à une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son titre, son organisation et son lieu, puis une ligne sur vos échanges (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le contact récent est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, une date s’affiche ; passez la souris dessus pour voir la date exacte. En dessous :

- **Contact** : ses numéros de téléphone et adresses e-mail. Touchez l’un d’eux pour appeler ou écrire, ou **Copier** pour le copier. Son **Anniversaire** s’affiche aussi ici, avec sa source (Google Contacts, Google Agenda, Facebook, vos notes ou vous-même) : voir [Le Graph](graph.md#birthday).
- **Avec vous** : son lien avec vous, contact Travail ou Perso, et votre Famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres plateformes où vous échangez avec cette personne. **Slack** ouvre son profil dans Slack ou votre fil Slack le plus récent avec elle.
- Les **Personnes** et **Projets** auxquels elle est liée, les éléments **En cours entre vous** (promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et chats d’une personne sont associés automatiquement lorsqu’il est clair qu’ils correspondent à la même personne, par exemple une adresse e-mail professionnelle mise en copie de ses propres échanges.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message s’affiche encore, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne résument ce qui a été décidé, demandé, prévu ou promis, en nommant toutes les personnes concernées. The Machine le réécrit en cas de nouveauté, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; en quelques heures si un sujet évolue avec cette personne, par exemple une nouvelle échéance ou une demande retirée.

Les lignes trop vagues sont ignorées. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une date, avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine affiche une **Mise à jour suggérée**, avec les options **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui redonne la main.

Les préparations de réunion l’utilisent, uniquement avec les lignes qui concernent le type de la tâche (Travail ou Perso). Le résumé reste sur votre Machine ; votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation en a une, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent tout en haut, sous **À venir**, de la plus proche à la plus lointaine ; **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les personnes qui y ont participé, chacune une seule fois. Si elle comporte des notes ou une transcription, elle affiche **Notes** ou **Transcription** ; cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph d’équipe n’affiche que les informations autorisées par vos règles de partage. Sur une page, **Équipe**, au-dessus de la Chronologie, ajoute les éléments partagés par vos collègues, en indiquant leur source ; **Les miens** affiche uniquement les vôtres.

## Travail et perso

Les onglets **Travail** et **Perso** répertorient les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les membres de leur famille ou leurs amis à vos yeux (une épouse, un père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais les contacts Perso.

## Ajouter une personne

Utilisez **Nouvelle personne** en haut de la section Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire figure déjà dans votre Graph, le formulaire l’affiche d’abord pour que vous puissiez ouvrir sa fiche. **Ajouter** ouvre la nouvelle page.

La personne que vous ajoutez reste dans la liste, même sans message. Son premier message est ensuite associé à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son titre, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, son lien avec vous et son type Travail ou Perso. Le champ **Notes** vous permet de noter ce que vous voulez garder en mémoire ; les notes sont conservées lors des fusions. **Enregistrer** conserve les modifications, et **Annuler** les abandonne.

Vos modifications sont conservées, même lorsque ses informations sont recherchées à nouveau, ainsi qu’après **Fusionner** ou **Annuler**. Videz un champ pour réutiliser la valeur trouvée automatiquement. Si vous videz le nom, celui qui figure dans ses messages réapparaît.

Pour changer sa photo, cliquez dessus, puis choisissez **Importer une photo**, sélectionnez une photo trouvée pour cette personne ou choisissez **Retirer la photo**. Elle reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux fiches pourraient correspondre à la même personne, une question s’affiche sur leur page et elles apparaissent dans la liste Personnes sous **Même personne ?**. **Fusionner** les associe, avec tous leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre réponse s’affiche brièvement pour la paire, puis celle-ci disparaît de la liste. La liste disparaît lorsqu’il n’y a plus de question.

Une personne dont l’adresse ressemble seulement à une adresse que vous connaissez, comme acme-corp.example et acmecorp.example, n’est jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais à associer deux personnes de domaines différents, car n’importe qui peut en saisir un. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, par exemple les mêmes contacts ou un projet. Une personne qui utilise votre nom à une adresse qui ne vous appartient pas ne vous est jamais proposée. Ajoutez plutôt vos autres adresses dans **Paramètres**, sous [Vos adresses](settings.md#your-addresses).

Lorsque seul le prénom correspond entre deux domaines, comme « Sam » et « Sam Lee », les personnes ne sont proposées que si elles ont le même numéro de téléphone ou le même profil LinkedIn.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel extérieur à votre entreprise et une conversation personnelle dont le seul point commun est un nom ne sont pas associés automatiquement : ils apparaissent comme une question.

**Tout fusionner** associe toutes les paires de la liste en une seule fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** permet de toutes les séparer à nouveau juste après.

Pour associer vous-même deux personnes, ouvrez l’une de leurs fiches, puis choisissez **⋯**, **Même personne que…** et sélectionnez l’autre. La page d’une personne associée indique les raisons de l’association sous **Associée depuis**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. La personne et tout ce que votre Machine sait à son sujet sont supprimés : sa fiche, ses adresses, les informations recherchées, les messages échangés uniquement entre vous deux et les notes la concernant.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, même par un import ou une tâche d’anniversaire Facebook contenant son nom ou son adresse. Cette action est irréversible.

## Adresse rejetée

Lorsqu’un e-mail envoyé à une personne est rejeté, son adresse affiche **Rejetée**, avec la date, et une autre de ses adresses apparaît en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si une autre est connue. Si c’est sa seule adresse, la fenêtre d’envoi vous avertit, mais vous pouvez tout de même envoyer le message.

Une adresse est considérée comme rejetée lorsque le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires sur une semaine. Le statut est effacé si la personne vous écrit à nouveau depuis cette adresse ou si un e-mail lui est envoyé avec succès.

## Titre professionnel et photo

Les personnes ayant une adresse professionnelle reçoivent un titre professionnel, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur l’organisation](organization-data.md). Sur une Machine hébergée, la recherche n’utilise que leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit le hachage de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Ce réglage désactive aussi la brève recherche sur le Web effectuée avant une première réunion (voir [Préparez vos réunions](calendar.md#ready-for-your-meetings)).

Lorsque ces informations sont trouvées, la page affiche aussi sa présentation, la date depuis laquelle la personne occupe son poste actuel et ses deux postes précédents. Les préparations les consultent aussi, mais n’utilisent la présentation que si la personne n’a pas de biographie.

Vos connexions s’enrichissent également des informations qu’elles ont déjà consultées : un titre, un numéro de téléphone et un fuseau horaire depuis Slack, une biographie et un lieu depuis X, un titre et une photo depuis LinkedIn, des titres professionnels depuis Google Contacts et Salesflare, ainsi que la photo d’un contact depuis Salesflare si cette plateforme en conserve une. Passez la souris sur la ligne sous son nom pour voir d’où proviennent ces informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les titres professionnels et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont importées par la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà dans votre Graph. Aucun message ne leur est envoyé. Un import d’anniversaires Facebook ajoute la photo de profil d’une personne qui n’en a pas lorsque vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’une Fleet Travail, une petite copie de la photo professionnelle est ajoutée à la fiche partagée de la personne. Les photos provenant de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que celles que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, correspondent toujours à vous, jamais à une personne de votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre. Un import ignore votre propre ligne.

La page À propos de vous répertorie vos adresses et leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre lien avec cette personne

Les rôles que votre Machine repère dans vos messages s’affichent sur sa page, sous **Pour vous**, avec uniquement les mots qui indiquent le rôle, comme un titre. Le fait qu’une personne dise être votre comptable ou votre client ne suffit pas : il faut aussi des éléments de votre côté, comme vos propres messages ou réunions avec elle. Vous n’avez rien à confirmer. Une erreur ? **Modifier** sur sa page permet de la corriger, tout comme **⋯** sur la ligne correspondante dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce que votre Machine sait sur une personne

Les informations sur cette personne figurent sur sa page, sous **Informations connues** ; les informations générales restent dans **Apprentissage**. **Ajouter** permet d’en ajouter une avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la changer directement.
- **Pas à propos de cette personne** en refait une information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

**Modifications récentes**, replié juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a modifié ou appris à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, une information ou l’avancement d’un projet. Chaque ligne indique sa date et sa source. Touchez la source pour lire le message.

Si une ligne est erronée, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Pas à propos de cette personne** ou **Annuler** pour remettre un projet à sa place. Trois lignes s’affichent ; **Afficher plus** montre les autres.

Une personne dont votre Machine a mis les informations à jour aujourd’hui est signalée par un petit point dans la liste Personnes. Le message **4 personnes mises à jour aujourd’hui** en haut de la liste les indique. Voir [Le Graph](graph.md).

## Une tâche à propos d’une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à son sujet.
