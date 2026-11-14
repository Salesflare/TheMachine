---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, ainsi que les façons d’ajouter, de modifier, de fusionner ou de supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 2fe1c104a74711c4
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, à partir de vos messages et de vos réunions. Les newsletters, reçus et autres envois ne créent pas de fiche tant que vous n’y répondez pas. Ils apparaissent sous Expéditeurs masqués, sous la liste : **Afficher comme personne** en ajoute un. Les champs, tags et importations fonctionnent de la même manière dans les trois listes, chacune ayant ses propres filtres : voir [The Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’un magasin) est associée à son organisation, pas à une personne, même si vous lui écrivez.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et sa ville, puis une ligne résume votre relation (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, une date s’affiche. Survolez-la pour voir la date exacte. En dessous :

- **Contact** : ses numéros de téléphone et adresses e-mail. Touchez-en un pour appeler ou écrire, ou pour le **Copier**. Son **Anniversaire** s’affiche aussi ici, avec sa source (Google Contacts, Google Calendar, Facebook ou vous) : voir [The Graph](graph.md#birthday).
- **Avec vous** : ce que cette personne représente pour vous, son type de contact (professionnel ou personnel) et votre famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres plateformes où vous échangez avec cette personne. **Slack** ouvre sa fiche dans Slack, ou votre dernier fil Slack avec elle.
- Les **Personnes** et **Projets** auxquels elle participe, les éléments **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**), et sa **Chronologie**.

Les adresses et les chats d’une personne sont associés automatiquement quand il est évident qu’il s’agit d’une seule personne, par exemple une adresse e-mail professionnelle avec sa propre adresse en copie.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message s’affiche toujours, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes courtes en haut de la page d’une personne : ce qui a été décidé, demandé, prévu ou promis, avec le nom de chaque personne concernée. The Machine le réécrit quand il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; en quelques heures si un sujet avec cette personne évolue, par exemple une nouvelle échéance ou une demande retirée.

Les lignes trop vagues sont omises. S’il n’y a rien de précis à dire, le résumé n’apparaît pas. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une seule date, avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine affiche une **Mise à jour suggérée**, avec **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui redonne la main.

Les préparations de réunion l’utilisent, mais uniquement les lignes du volet de cette tâche (Travail ou Perso). Le résumé reste sur votre Machine : votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent en haut, sous **À venir**, de la plus proche à la plus éloignée. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les personnes présentes, chacune une seule fois. Celles qui ont des notes ou une transcription sont marquées **Notes** ou **Transcription**. Cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que les informations autorisées par vos règles de partage. Sur une page, **Équipe** au-dessus de la chronologie ajoute les informations partagées par vos collègues, avec le nom de la personne qui les a partagées. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** répertorient les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les membres de la famille ou les amis pour qui vous êtes un proche (une épouse, un père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais vos contacts personnels.

## Ajouter une personne

Utilisez **Nouvelle personne** en haut de Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire figure déjà dans votre Graph, le formulaire l’affiche d’abord pour que vous puissiez ouvrir sa fiche. **Ajouter** ouvre la nouvelle fiche.

La personne que vous ajoutez reste dans votre liste, même sans aucun message. Son premier message l’associe à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, sa ville, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, ce qu’elle représente pour vous, ainsi que son type (professionnel ou personnel). Le champ **Notes** permet d’ajouter ce que vous voulez garder en mémoire ; les notes sont conservées lors des fusions. **Enregistrer** sauvegarde les modifications. **Annuler** les abandonne.

Vos modifications sont conservées, y compris quand ses informations sont recherchées à nouveau, et lors d’une **Fusionner** ou d’une **Annuler**. Videz un champ pour utiliser de nouveau la valeur trouvée lors de la recherche. Si vous effacez le nom, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus : utilisez **Importer une photo**, choisissez une photo trouvée pour cette personne ou sélectionnez **Retirer la photo**. La photo reste sur votre Machine.

## Fusionner deux personnes

Quand deux personnes pourraient être la même, leur page vous demande si c’est le cas, et Personnes les affiche sous **Même personne ?**. **Fusionner** les associe, avec tous leurs messages, notes, rôles et projets. **Pas la même** les garde définitivement séparées. Votre réponse reste affichée quelque temps sur la paire, puis celle-ci disparaît de la liste. La liste disparaît quand il n’y a plus de question à poser.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel externe à votre entreprise et une personne avec qui vous échangez à titre personnel, dont le seul point commun est un nom, ne sont pas associés automatiquement : ils sont affichés sous forme de question.

**Tout fusionner** fusionne toutes les paires de la liste en une seule fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après permet de toutes les séparer à nouveau.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis **⋯**, **Même personne que…** et choisissez l’autre personne. La page de la personne fusionnée indique la raison sous **Fusionnée à partir de**, avec **Annuler** pour séparer les fiches à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. La personne et les informations que votre Machine connaît à son sujet sont supprimées : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous, ainsi que les notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, pas même par une importation ou une tâche d’anniversaire Facebook contenant son nom ou son adresse. Cette action est irréversible.

## E-mails non distribués

Quand un e-mail envoyé à une personne n’est pas distribué, son adresse est marquée **Non distribué**, avec la date. Une autre de ses adresses s’affiche en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si une autre est connue. Si c’est sa seule adresse, une alerte apparaît dans la fenêtre d’envoi, mais vous pouvez quand même envoyer le message.

Une adresse est considérée comme non distribuée quand le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires sur une semaine. L’indication disparaît si la personne vous écrit à nouveau depuis cette adresse, ou si un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse professionnelle reçoivent un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche utilise uniquement leur nom et le domaine de leur entreprise. Pour trouver une photo, Gravatar reçoit le hachage de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Quand les informations sont trouvées, leur page affiche aussi leur présentation, la date à laquelle elles ont commencé leur poste actuel et les deux postes précédents. Les préparations les utilisent aussi, mais n’incluent la présentation que si elles n’ont pas de biographie.

Vos connexions s’enrichissent aussi à partir des informations qu’elles ont déjà consultées : poste, téléphone et fuseau horaire depuis Slack ; biographie et ville depuis X ; titre de profil et photo depuis LinkedIn ; postes depuis Google Contacts et Salesflare ; et photo d’un contact depuis Salesflare si Salesflare en conserve une. Survolez la ligne sous son nom pour voir la source des informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées via la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour sur chaque service, uniquement pour les personnes déjà dans votre Graph. Aucune notification ne leur est envoyée. Une importation des anniversaires Facebook ajoute la photo de profil des personnes sans photo lorsque vous l’enregistrez ([Routines](routines.md)). Toutes ces informations restent sur votre Machine.

Dans le [Team Graph](team-graph.md) d’un Fleet professionnel, une petite copie d’une photo professionnelle accompagne la fiche partagée d’une personne. Les photos de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours associés à vous, jamais à une personne de votre Graph. Si vous vous recherchez ou si vous ajoutez une personne avec l’une de vos adresses, la page **À propos de vous** s’ouvre. Une importation ignore votre propre ligne.

La page À propos de vous répertorie vos adresses et indique leur source. Pour les modifier, allez dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Ce que vous représentez pour eux

Les rôles que votre Machine déduit de vos messages s’affichent sur leur page, sous **Pour vous**, avec la phrase d’où ils ont été déduits. Vous n’avez pas besoin de confirmer. Une erreur ? **Modifier** sur leur page permet de la corriger, ou utilisez **⋯** sur sa ligne dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce qu’elle sait sur une personne

Les informations sur une personne figurent sur sa page, sous **Informations connues**. L’onglet Apprentissage conserve les informations générales. **Ajouter** permet d’en ajouter une autre, avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la changer directement.
- **Pas à propos de cette personne** la redevient générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

**Modifications récentes**, dans la section repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a modifié ou appris à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, une information ou un changement de projet. Chaque ligne indique la date et la source. Touchez la source pour lire le message.

Si une information est incorrecte, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Pas à propos de cette personne** ou **Annuler** pour rétablir l’emplacement précédent d’un projet. Trois lignes s’affichent. **Afficher plus** permet de voir les autres.

Une personne dont votre Machine a modifié les informations aujourd’hui est signalée par un petit point dans la liste Personnes. La mention **4 personnes mises à jour aujourd’hui** en haut de la liste indique leur nombre. Voir [The Graph](graph.md).

## Une tâche concernant une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à son sujet.
