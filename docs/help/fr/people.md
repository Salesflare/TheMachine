---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, ainsi que la façon d’ajouter, de modifier, de fusionner ou de supprimer quelqu’un.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 0eb2dcc70fba84c2
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, à partir de vos messages et réunions. Les newsletters, reçus et autres envois ne font apparaître personne tant que vous n’y répondez pas. Ils se trouvent sous Expéditeurs masqués, au bas de la liste : **Afficher comme une personne** permet d’ajouter quelqu’un. Les champs, les tags et l’import fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [The Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’une boutique) est associée à son organisation, pas à une personne, même si vous lui écrivez.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et sa ville, puis une ligne indique comment vous êtes en contact ("Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct."). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours », et les contacts plus anciens par une date. Passez le curseur dessus pour voir la date exacte. En dessous :

- **Contact** : ses numéros et adresses e-mail. Touchez-en un pour appeler ou écrire, ou **Copier**. Son **Anniversaire** apparaît aussi ici, avec sa source (Google contacts, Google Calendar, Facebook, vos notes ou vous) : voir [The Graph](graph.md#birthday).
- **Avec vous** : son lien avec vous, son type de contact (pro ou perso) et son appartenance à votre famille ou à votre Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous échangez avec elle. **Slack** ouvre son profil dans Slack ou votre fil Slack le plus récent avec elle.
- Les **Personnes** et **Projets** auxquels elle est associée, **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**), et sa **Chronologie**.

Les adresses et les chats d’une personne sont automatiquement regroupés quand il est clair qu’il s’agit de la même personne, par exemple une adresse e-mail professionnelle avec sa propre adresse en copie.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message revient, touchez **Un problème ?** au bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne indiquent ce qui a été décidé, demandé, prévu ou promis, et par qui. The Machine le réécrit lorsqu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, après avoir vérifié chaque ligne. En général, une fois par jour, ou dans les heures qui suivent un changement important, comme une nouvelle échéance ou une demande retirée.

Les lignes vagues sont ignorées. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une date avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine propose une **Mise à jour suggérée**, avec **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui redonne la main.

Les préparatifs de réunion l’utilisent, mais uniquement les lignes liées au type de tâche correspondant (Travail ou Perso). Le résumé reste sur votre Machine et n’est jamais visible par votre équipe.

## Chronologie

Chaque page de personne et d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent en haut, sous **À venir**, de la plus proche à la plus lointaine. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les participants, chaque personne une seule fois. Les réunions avec des notes ou une transcription affichent **Notes** ou **Transcription**. Cliquez dessus pour les lire.

Vos chronologies restent privées : le Graph de l’équipe n’affiche que ce que vos règles de partage autorisent. Sur une page, **Équipe** au-dessus de la chronologie affiche les éléments partagés par vos collègues, avec le nom de la personne qui les a partagés. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** classent les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les personnes qui sont de la famille ou des amis pour vous (votre épouse, votre père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais vos contacts persos.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de la liste Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, et une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire figure déjà dans votre Graph, le formulaire l’affiche d’abord pour que vous puissiez ouvrir sa fiche. **Ajouter** ouvre la nouvelle page.

Une personne que vous ajoutez reste dans votre liste, même sans aucun message. Son premier message est ensuite associé à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, sa ville, son profil LinkedIn, ses numéros et adresses e-mail, son lien avec vous et son type, pro ou perso. Le champ **Notes** permet d’ajouter ce dont vous voulez vous souvenir. Les notes sont conservées lors des fusions. **Enregistrer** conserve les modifications, **Annuler** les abandonne.

Vos modifications sont conservées, même si ses informations sont recherchées à nouveau, et après **Fusionner** ou **Annuler**. Effacez un champ pour réutiliser la valeur trouvée. Si vous effacez son nom, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus, puis choisissez **Importer une photo**, sélectionnez une photo trouvée pour elle ou choisissez **Retirer la photo**. La photo reste sur votre Machine.

## Fusionner deux personnes

Si deux personnes sont peut-être la même, leur page vous demande si c’est le cas, et la liste Personnes les affiche sous **Même personne ?**. **Fusionner** les regroupe avec tous leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre réponse s’affiche brièvement sur la paire, puis celle-ci disparaît de la liste. La liste disparaît quand il n’y a plus de question à poser.

Une personne dont l’adresse ressemble seulement à une adresse connue, comme acme-corp.example par rapport à acmecorp.example, ne sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais pour associer des personnes de domaines différents, car n’importe qui peut saisir un nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, comme des contacts en commun ou un projet. Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne sera jamais proposée. Ajoutez plutôt vos autres adresses dans **Paramètres**, sous [Vos adresses](settings.md#your-addresses).

Si seul le prénom correspond entre deux domaines, comme « Sam » et « Sam Lee », les personnes ne sont proposées que si elles ont le même numéro de téléphone ou le même profil LinkedIn.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui écrivent à cette adresse. Un contact professionnel extérieur à votre entreprise et un contact perso qui n’ont qu’un nom en commun ne sont pas automatiquement associés : ils sont signalés comme une question.

**Tout fusionner** associe toutes les paires de la liste en une fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** permet de toutes les séparer à nouveau juste après.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis touchez **⋯**, **Même personne que…** et sélectionnez l’autre personne. La page d’une personne associée indique pourquoi sous **Associé à partir de**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. Cela supprime la personne et tout ce que votre Machine sait à son sujet : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et vos notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, y compris par un import ou une tâche d’anniversaire Facebook qui porte son nom ou son adresse. Cette action est irréversible.

## Adresse e-mail rejetée

Quand un e-mail envoyé à une personne est rejeté, son adresse est marquée **Rejetée**, avec la date, et une autre de ses adresses est affichée en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si une autre est connue. Si c’est sa seule adresse, un avertissement s’affiche avant l’envoi, mais vous pouvez quand même envoyer l’e-mail.

Une adresse est considérée comme rejetée quand le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires sur une semaine. Le statut est effacé si la personne vous écrit à nouveau depuis cette adresse ou si un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse d’entreprise peuvent avoir un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur l’organisation](organization-data.md). Sur une Machine hébergée, la recherche ne récupère que leur nom et le domaine de leur entreprise. Pour trouver une photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Quand ces informations sont trouvées, leur page affiche aussi leur présentation, la date depuis laquelle elles occupent leur poste actuel et leurs deux postes précédents. Les préparatifs les utilisent aussi, mais ne reprennent la présentation que si la personne n’a pas de bio.

Vos connexions complètent les informations à partir de ce qu’elles ont déjà consulté : un poste, un numéro de téléphone et un fuseau horaire depuis Slack, une bio et une ville depuis X, un titre et une photo depuis LinkedIn, des postes depuis Google contacts et Salesflare, et la photo d’un contact depuis Salesflare si le service en conserve une. Passez le curseur sur la ligne sous son nom pour voir d’où viennent les informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées via la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé. Un import des anniversaires Facebook ajoute la photo de profil d’une personne qui n’en a pas quand vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’un Work Fleet, une petite copie de la photo professionnelle d’une personne accompagne la fiche partagée. Les photos de Google contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours les vôtres et ne représentent jamais quelqu’un dans votre Graph. Si vous vous recherchez vous-même ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre. Un import ignore votre propre ligne.

La page À propos de vous répertorie vos adresses et leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre lien avec cette personne

Les rôles que votre Machine repère dans vos messages s’affichent sur sa page sous **Pour vous**, avec la phrase où ils ont été repérés. Aucune confirmation de votre part n’est nécessaire. Une erreur ? **Modifier** sur sa page permet de la corriger, ou touchez **⋯** sur la ligne correspondante dans **Modifications récentes**. L’apprentissage tient compte de vos modifications.

## Ce qu’elle sait sur quelqu’un

Les informations à son sujet figurent sur sa page, sous **Informations connues**. L’**Apprentissage** conserve les informations générales. **Ajouter** permet d’en ajouter une avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la changer directement.
- **Pas à son sujet** la transforme à nouveau en information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

**Modifications récentes**, dans la section repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a modifié ou appris à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, une information ou l’évolution d’un projet. Chaque ligne indique sa date et sa source. Touchez la source pour lire le message.

Si une ligne est erronée, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Pas à son sujet** ou **Annuler** pour remettre un projet à son état précédent. Trois lignes s’affichent. **Afficher plus** permet de voir les autres.

Une personne dont votre Machine a mis à jour les informations aujourd’hui est signalée par un petit point dans la liste Personnes. Le nombre de personnes mises à jour aujourd’hui est indiqué en haut de la liste, par exemple **4 personnes mises à jour aujourd’hui**. Voir [The Graph](graph.md).

## Une tâche à propos de quelqu’un

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à son sujet.
