---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: b23d3ebdc4f162f2
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, à partir de vos messages et réunions. Les newsletters, reçus et autres envois ne créent pas de contact tant que vous n’y répondez pas. Ils se trouvent sous Expéditeurs masqués, au-dessous de la liste : **Afficher comme une personne** en ajoute un. Les champs, tags et options d’import sont les mêmes dans les trois listes, et chacune a ses propres filtres : voir [Le Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’une boutique) est associée à son organisation, pas à une personne, même après que vous lui avez écrit.

## Page d’une personne

En haut de la page : sa photo, son nom, son poste, son organisation et son lieu, puis une ligne sur vos échanges (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, la date s’affiche. Survolez-la pour voir la date exacte. Plus bas :

- **Contact** : ses numéros de téléphone et adresses e-mail. Touchez-en un pour appeler ou écrire, ou **Copier**. Son **Anniversaire** s’affiche aussi ici, avec sa source (Google Contacts, Google Agenda, Facebook, vos notes ou vous-même) : voir [Le Graph](graph.md#birthday).
- **Avec vous** : ce que cette personne représente pour vous, son type de contact, Travail ou Perso, et votre Famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres services où vous échangez avec elle. **Slack** ouvre son profil Slack ou votre dernier fil Slack avec elle.
- Les **Personnes** et **Projets** auxquels elle participe, les éléments **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et chats d’une personne sont automatiquement associés quand il est clair qu’il s’agit de la même personne, par exemple une adresse e-mail professionnelle accompagnée de sa propre adresse en copie. C’est aussi le cas si une personne avec qui vous échangez réserve un appel à partir du lien que vous lui avez envoyé et que son entreprise ou son nom de famille correspond.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message reste affiché, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne résument les décisions, demandes, projets ou promesses, en nommant les personnes concernées. The Machine le réécrit quand il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; dans les quelques heures qui suivent un changement important, comme une nouvelle échéance ou une demande retirée.

Les lignes trop vagues sont omises. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une date avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine propose une **Mise à jour suggérée**, avec les options **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui redonne la main.

Les préparations de réunion l’utilisent, mais uniquement les lignes correspondant au type de tâche (Travail ou Perso). Le résumé reste sur votre Machine ; votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les pastilles en haut affichent une seule source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent en haut, sous **À venir**, de la plus proche à la plus lointaine. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les personnes présentes, chacune une seule fois. Les réunions avec des notes ou une transcription portent la mention **Notes** ou **Transcription** ; cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que les informations autorisées par vos règles de partage. Sur une page, **Équipe**, au-dessus de la chronologie, ajoute les éléments partagés par vos collègues, avec le nom de la personne qui les a partagés. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** classent les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les personnes qui sont de la famille ou des amis pour vous (une épouse, un père), sont classés comme Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais les contacts Perso.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de la section Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire existe déjà dans votre Graph, le formulaire l’affiche en premier, pour que vous puissiez ouvrir sa page. **Ajouter** ouvre la nouvelle page.

Une personne que vous ajoutez reste dans la liste, même si vous n’avez encore aucun message avec elle. Son premier message sera associé à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et adresses e-mail, ce qu’elle représente pour vous, ainsi que son type Travail ou Perso. Le champ **Notes** permet d’ajouter ce que vous voulez garder en mémoire. Les notes sont conservées lors des fusions. **Enregistrer** garde les modifications ; **Annuler** les abandonne.

Vos modifications sont conservées, même quand ses informations sont de nouveau recherchées, et après une **Fusionner** ou une **Annuler**. Videz un champ pour réutiliser la valeur trouvée. Si vous videz le nom, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus : choisissez **Importer une photo**, une photo trouvée pour cette personne ou **Retirer la photo**. La photo reste sur votre Machine.

## Fusionner deux personnes

Quand deux personnes pourraient n’en être qu’une, leur page vous demande si elles sont la même personne, et la liste Personnes les affiche sous **Même personne ?**. **Fusionner** les rassemble avec tous leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre réponse s’affiche quelque temps sur la paire, puis celle-ci disparaît de la liste. La liste disparaît quand il n’y a plus rien à vérifier.

Une personne dont l’adresse ressemble seulement à celle d’un contact connu, comme acme-corp.example par rapport à acmecorp.example, n’est jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais à associer deux personnes de domaines différents, car n’importe qui peut saisir ce nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, comme les mêmes personnes ou un projet. Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne vous est jamais proposée. Ajoutez plutôt vos autres adresses dans **Paramètres**, sous [Vos adresses](settings.md#your-addresses).

Si seul le prénom correspond entre deux domaines, comme « Sam » et « Sam Lee », les personnes ne sont proposées que si elles ont le même numéro de téléphone ou profil LinkedIn.

Si seul le prénom correspond entre une personne et une réunion créée à partir d’un chat, ou si l’adresse appartient à une personne que vous connaissiez déjà et que seule la personne dans le chat dit qu’elle est la sienne, vous devez confirmer. The Machine n’ouvre jamais de lien pour vérifier.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel extérieur à votre entreprise et un contact personnel qui n’ont qu’un nom en commun ne sont pas associés automatiquement : ils sont proposés pour vérification.

**Tout fusionner** fusionne d’un coup toutes les paires de la liste, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après permet de toutes les séparer à nouveau.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis choisissez **⋯**, **Même personne que…** et sélectionnez l’autre personne. La page d’une personne fusionnée indique la raison sous **Fusionnée à partir de**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯, choisissez **Supprimer définitivement…**, puis **Supprimer**. La personne et les informations que votre Machine connaît à son sujet sont supprimées : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et les notes la concernant.

Les tâches auxquelles elle participe sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée de nouveau, y compris lors d’un import ou d’une tâche d’anniversaire Facebook contenant son nom ou son adresse. Cette action est irréversible.

## E-mail rejeté

Quand un e-mail envoyé à une personne est rejeté, son adresse est marquée **Rejetée**, avec la date, et une autre de ses adresses s’affiche en premier. Si une autre adresse est connue, les nouveaux brouillons ne lui seront jamais envoyés. Si c’est sa seule adresse, un avertissement s’affiche dans l’écran d’envoi, mais vous pouvez quand même envoyer le message.

Une adresse est considérée comme rejetée si le serveur de messagerie indique qu’elle n’existe pas, ou après trois échecs temporaires en une semaine. Le statut est effacé si la personne vous écrit de nouveau depuis cette adresse ou si un e-mail lui est envoyé avec succès.

## Poste et photo

Pour les personnes ayant une adresse professionnelle, le poste, la photo, le profil LinkedIn et la ville sont recherchés comme les [informations sur l’organisation](organization-data.md). Sur une Machine hébergée, la recherche ne reçoit que leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Ce réglage désactive aussi la consultation de sites web avant une première réunion, ainsi que la recherche sur le Web si un moteur de recherche est configuré (voir [Prête pour vos réunions](calendar.md#ready-for-your-meetings)).

Quand les informations sont trouvées, la page affiche aussi leur présentation, la date de début de leur poste actuel et leurs deux postes précédents. Les préparations les consultent également, mais n’utilisent la présentation que si la personne n’a pas de biographie.

Vos connexions se complètent avec les informations qu’elles consultent déjà : un poste, un numéro de téléphone et un fuseau horaire depuis Slack, une biographie et un lieu depuis X, un titre de profil et une photo depuis LinkedIn, des postes depuis Google Contacts et Salesflare, ainsi que la photo d’un contact depuis Salesflare si ce service en conserve une. Survolez la ligne sous son nom pour voir la source.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées par la synchronisation WhatsApp et la connexion aux chats Telegram : jusqu’à 50 par jour et par service, uniquement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé. Un import d’anniversaires Facebook ajoute la photo de profil d’une personne qui n’en a pas quand vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans un [Graph d’équipe](team-graph.md) de Fleet Travail, une petite copie d’une photo professionnelle accompagne la fiche partagée d’une personne. Les photos issues de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours associés à vous, jamais à une personne de votre Graph. Si vous faites une recherche sur vous-même ou ajoutez une personne avec l’une de vos adresses, la page **À propos de vous** s’ouvre, et vos propres lignes sont ignorées lors d’un import.

La page À propos de vous répertorie vos adresses et leur provenance. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Ce que cette personne représente pour vous

Les rôles que votre Machine repère dans vos messages s’affichent sur sa page, sous **Pour vous**, avec uniquement les mots qui indiquent le rôle, comme un titre. Le fait qu’une personne dise être votre comptable ou votre client ne suffit pas : il faut aussi un élément de votre côté, comme vos propres messages ou réunions avec elle. Vous n’avez pas à confirmer. Une erreur ? **Modifier** sur sa page permet de corriger le rôle, ou utilisez **⋯** sur la ligne correspondante dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce qu’elle sait sur une personne

Les informations sur cette personne se trouvent sur sa page, sous **Informations connues**. La section Apprentissage contient les informations générales. **Ajouter** permet d’ajouter une information avec vos propres mots. Chaque information a son propre menu :

- **Modifier** permet de la modifier directement.
- **Ne concerne pas** cette personne la redevient une information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

La section **Modifications récentes**, repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie les informations que votre Machine a modifiées ou apprises à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, un fait ou l’évolution d’un projet. Chaque ligne indique la date et la source. Touchez la source pour lire le message.

Si une information est incorrecte, le menu **⋯** de sa ligne permet de la corriger directement avec **Modifier**, **Retirer**, **Ne concerne pas** cette personne ou **Annuler** pour remettre un projet à sa place précédente. Trois lignes s’affichent ; **Afficher plus** révèle les autres.

Une personne dont votre Machine a mis la fiche à jour aujourd’hui est marquée d’un petit point dans la liste Personnes. Le nombre de personnes concernées s’affiche en haut de la liste, par exemple **4 personnes mises à jour aujourd’hui**. Voir [Le Graph](graph.md).

## Une tâche concernant une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à son sujet.
