---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 84312952f04b8597
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, d’après vos messages et vos réunions. Les newsletters, reçus et autres envois ne sont pas ajoutés tant que vous n’y répondez pas. Ils se trouvent sous Expéditeurs masqués, en dessous de la liste. **Afficher comme une personne** permet d’en ajouter un. Les champs, tags et imports fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [Le Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’un magasin) est associée à son organisation, pas à une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et son lieu, puis une ligne résume votre relation (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, une date s’affiche. Passez la souris dessus pour voir la date exacte. Plus bas :

- **Contact** : ses numéros de téléphone et ses adresses e-mail. Touchez-en une pour appeler ou écrire, ou **Copier** pour la copier. Son **Anniversaire** apparaît aussi ici, avec sa source (Google Contacts, Google Agenda, Facebook, vos notes ou vous) : voir [Le Graph](graph.md#birthday).
- **Avec vous** : le rôle de cette personne pour vous, son type de contact, professionnel ou personnel, et votre Fleet Famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres plateformes où vous échangez avec cette personne. **Slack** ouvre son profil dans Slack, ou votre dernière conversation Slack avec elle.
- Les **Personnes** et **Projets** auxquels elle participe, **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**), et sa **Chronologie**.

Les coordonnées et les chats d’une personne sont associés automatiquement lorsqu’il est évident qu’il s’agit de la même personne, par exemple une adresse e-mail professionnelle mise en copie de son adresse personnelle. C’est aussi le cas lorsqu’une personne avec qui vous échangez réserve un appel à partir du lien que vous lui avez envoyé, et que son entreprise ou son nom de famille correspond.

Si le message **Impossible de charger cette page.** s’affiche, touchez **Réessayer**. S’il s’affiche encore, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne résument ce qui a été décidé, demandé, prévu ou promis, en nommant toutes les personnes concernées. The Machine le réécrit lorsqu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour. Dans les heures qui suivent si quelque chose change, comme une nouvelle échéance ou une demande retirée.

Les lignes vagues sont ignorées. Si rien de précis n’est à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source. Les messages d’une même journée sont regroupés sous une seule date, avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine affiche une **Mise à jour suggérée**, avec **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui permet de reprendre la main.

Les préparations de réunion l’utilisent, mais uniquement les lignes correspondant au contexte de la tâche, Travail ou Perso. Le résumé reste sur votre Machine. Votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne ou d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent en haut, sous **À venir**, de la plus proche à la plus lointaine. **Afficher tout ce qui est à venir** affiche les autres réunions. Une réunion indique qui y a participé, chaque personne une seule fois. Les réunions avec des notes ou une transcription sont marquées **Notes** ou **Transcription**. Cliquez dessus pour les lire.

Vos chronologies vous appartiennent. Le Graph de l’équipe n’affiche que ce que vos règles de partage autorisent. Sur une page, **Équipe**, au-dessus de la chronologie, ajoute ce que vos collègues ont partagé, avec le nom de la personne à l’origine de chaque élément. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** répertorient les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les personnes dont vous êtes un proche (une épouse, un père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais vos contacts personnels.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de la page Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire existe déjà dans votre Graph, le formulaire l’affiche en premier pour vous permettre d’ouvrir sa page. **Ajouter** ouvre la nouvelle page.

La personne que vous ajoutez reste dans la liste, même si vous n’avez pas encore échangé de messages avec elle. Son premier message sera associé à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, son rôle pour vous, ainsi que son type, professionnel ou personnel. Le champ **Notes** sert à noter ce dont vous voulez vous souvenir. Les notes sont conservées lors des fusions. **Enregistrer** garde vos modifications. **Annuler** rétablit la version précédente.

Vos modifications sont conservées, même lorsque ses informations sont recherchées à nouveau, et après une **Fusionner** ou une **Annuler**. Effacez un champ pour réutiliser la valeur trouvée. Si vous effacez le nom, celui qui figure dans ses messages réapparaît.

Pour changer sa photo, cliquez dessus. Vous pouvez **Importer une photo**, choisir une photo trouvée pour cette personne ou **Retirer la photo**. Elle reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux personnes pourraient n’en former qu’une, leur page vous demande s’il s’agit de la même personne, et la liste Personnes les affiche sous **Même personne ?**. **Fusionner** associe leurs messages, notes, rôles et projets. **Pas la même** les garde séparées définitivement. Votre réponse s’affiche quelque temps pour la paire, puis celle-ci disparaît de la liste. La liste disparaît lorsqu’il n’y a plus de question à poser.

Une personne dont l’adresse ressemble seulement à une adresse que vous connaissez, comme acme-corp.example et acmecorp.example, ne sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais pour associer deux personnes de domaines différents, car n’importe qui peut saisir ce nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, comme les mêmes personnes ou un petit projet. Pour un prénom seul (« Sam » et « Sam Lee »), il faut davantage d’éléments : la même entreprise, le même numéro de téléphone ou le même profil LinkedIn.

Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne sera jamais proposée. Ajoutez plutôt vos autres adresses dans **Paramètres**, sous [Vos adresses](settings.md#your-addresses).

Lorsque seul le prénom correspond pour des domaines différents, comme « Sam » et « Sam Lee », les personnes ne sont proposées que si elles ont le même numéro de téléphone ou le même profil LinkedIn.

Lorsque seul le prénom correspond à une réunion créée depuis un chat, ou que l’adresse appartient à une personne que vous connaissiez déjà et que seule la personne dans le chat dit qu’elle est à elle, The Machine vous pose la question. The Machine n’ouvre jamais de lien pour le vérifier.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui écrivent par son intermédiaire. Un contact professionnel extérieur à votre entreprise et un chat personnel qui n’ont qu’un nom en commun ne sont pas associés automatiquement : ils sont affichés comme une question.

**Tout fusionner** associe toutes les paires de la liste en une seule fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après permet de toutes les séparer à nouveau.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis **⋯**, **Même personne que…** et choisissez l’autre personne. La page d’une personne associée indique la raison sous **Associé à partir de**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯, choisissez **Supprimer définitivement…**, puis **Supprimer**. La personne et tout ce que votre Machine sait à son sujet sont supprimés : sa fiche, ses coordonnées, les informations trouvées, les messages échangés uniquement entre vous deux et les notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, y compris lors d’un import ou d’une tâche d’anniversaire Facebook contenant son nom ou son adresse. Cette action est irréversible.

## E-mail non distribué

Lorsqu’un e-mail envoyé à une personne n’est pas distribué, son adresse est marquée **Non distribué** avec la date, et une autre de ses adresses s’affiche en premier. Si une autre adresse est connue, les nouveaux brouillons ne seront jamais envoyés à l’adresse concernée. Si c’est sa seule adresse, la fenêtre d’envoi vous avertit, mais vous pouvez tout de même envoyer le message.

Une adresse est considérée comme non distribuée lorsque le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires sur une semaine. Le statut est effacé lorsque la personne vous écrit à partir de cette adresse, ou lorsqu’un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse d’entreprise peuvent avoir un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche ne transmet que leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit le hachage de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Cette option désactive aussi la consultation du site web avant une première réunion et la recherche sur le Web (voir [Prêt pour vos réunions](calendar.md#ready-for-your-meetings)).

Lorsque ces informations sont trouvées, la page affiche aussi leur présentation, la date depuis laquelle la personne occupe son poste actuel et ses deux postes précédents. Les préparations les utilisent aussi. La présentation n’est utilisée que si la personne n’a pas sa propre bio.

Vos connexions complètent les informations avec celles qu’elles ont déjà lues : un poste, un numéro de téléphone et un fuseau horaire depuis Slack, une bio et un lieu depuis X, un titre et une photo depuis LinkedIn, des postes depuis Google Contacts et Salesflare, et la photo d’un contact depuis Salesflare lorsque Salesflare en conserve une. Passez la souris sur la ligne sous son nom pour voir d’où viennent les informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées via votre synchronisation WhatsApp et votre connexion aux chats Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé. Un import d’anniversaires Facebook ajoute la photo de profil des personnes sans photo lorsque vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’une Fleet Travail, une petite copie de la photo professionnelle est associée à la fiche partagée d’une personne. Les photos de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos adresses et numéros, y compris vos alias, correspondent toujours à vous et jamais à une autre personne de votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre. Votre propre ligne est ignorée lors d’un import.

La page À propos de vous répertorie vos adresses et leur provenance. Pour les modifier, allez dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre rôle pour cette personne

Les rôles que votre Machine trouve dans vos messages s’affichent sur sa page, sous **Pour vous**, avec uniquement les mots qui indiquent le rôle, comme un titre. Le fait qu’une personne dise être votre comptable ou votre client ne suffit pas : il faut aussi des éléments de votre côté, comme vos propres messages ou réunions avec elle. Vous n’avez pas à confirmer le rôle. S’il est incorrect, **Modifier** sur sa page permet de le corriger, tout comme **⋯** sur la ligne correspondante dans **Modifications récentes**. The Machine tient compte de vos modifications.

## Ce que The Machine sait sur une personne

Les informations sur cette personne se trouvent sur sa page, sous **Informations connues**. La section **Apprentissage** conserve les informations générales. **Ajouter** permet d’en ajouter une avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la modifier directement.
- **Pas à propos de** cette personne en fait à nouveau une information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

La section **Modifications récentes**, repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie les changements et les nouvelles informations sur celle-ci : un rôle, son lieu de travail, le lien entre deux personnes, une information ou le déplacement d’un projet. Chaque ligne indique la date et la source. Touchez la source pour lire le message.

Si une ligne est incorrecte, utilisez son menu **⋯** pour la corriger directement : **Modifier**, **Retirer**, **Pas à propos de** cette personne ou **Annuler** pour replacer un projet là où il était. Trois lignes s’affichent. **Afficher plus** permet de voir les autres.

Une personne dont votre Machine a mis à jour la fiche aujourd’hui est signalée par un petit point dans la liste Personnes. Le message **4 personnes mises à jour aujourd’hui**, en haut de la liste, indique lesquelles. Voir [Le Graph](graph.md).

## Une tâche à propos d’une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à son sujet.
