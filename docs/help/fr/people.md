---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 315403ed8889dbac
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux moins proches, à partir de vos messages et réunions. Les newsletters, reçus et autres e-mails groupés n’ajoutent personne tant que vous n’y répondez pas. Ils apparaissent sous Expéditeurs masqués, sous la liste : **Afficher comme une personne** permet d’ajouter une personne. Les champs, tags et importations fonctionnent de la même façon dans les trois listes, mais chaque liste a ses propres filtres : voir [Le Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’un magasin) est associée à son organisation, pas à une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et son lieu, puis une ligne sur vos échanges (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, une date s’affiche. Survolez-la pour voir la date exacte. En dessous :

- **Contact** : ses numéros de téléphone et ses adresses e-mail. Touchez-en une pour appeler ou écrire, ou **Copier** pour la copier. Son **Anniversaire** apparaît aussi ici, avec sa source (Google Contacts, Google Agenda, Facebook, vos notes ou vous-même) : voir [Le Graph](graph.md#birthday).
- **Avec vous** : son rôle auprès de vous, son type de contact, Travail ou Perso, et votre Fleet Famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous échangez avec cette personne. **Slack** ouvre son profil dans Slack ou votre discussion Slack la plus récente avec elle.
- Les **Personnes** et **Projets** auxquels elle participe, les **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et les chats d’une personne sont automatiquement regroupés lorsqu’il est clair qu’ils lui appartiennent, par exemple une adresse professionnelle avec sa propre adresse en copie. C’est aussi le cas lorsqu’une personne avec qui vous échangez réserve un appel à partir du lien que vous lui avez envoyé, et que son entreprise ou son nom de famille correspond.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message réapparaît, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne indiquent ce qui a été décidé, demandé, prévu ou promis, et par qui. The Machine les reformule lorsqu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour. Le résumé est mis à jour en quelques heures si un point change, par exemple si une nouvelle échéance est fixée ou si une demande est retirée.

Les lignes trop vagues sont ignorées. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une seule date, avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. Quand il y a du nouveau, The Machine affiche une **Mise à jour suggérée**, avec les options **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui rend la main.

Les préparations de réunion reprennent le résumé, mais uniquement les lignes liées au contexte de cette tâche, Travail ou Perso. Il reste sur votre Machine. Votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les prochaines réunions apparaissent en haut, sous **À venir**, de la plus proche à la plus éloignée. **Afficher tout ce qui est à venir** affiche le reste. Une réunion indique qui y a participé, chaque personne n’apparaissant qu’une fois. Les réunions avec des notes ou une transcription portent la mention **Notes** ou **Transcription**. Cliquez dessus pour les consulter.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que les éléments autorisés par vos règles de partage. Sur une page, **Équipe**, au-dessus de la chronologie, ajoute les éléments partagés par vos collègues et indique qui les a partagés. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** répertorient les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les personnes de votre famille ou vos amis (votre épouse, votre père, par exemple), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais vos contacts personnels.

## Ajouter une personne

Utilisez **Nouvelle personne** en haut de la page Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, puis une adresse e-mail et une organisation si vous les connaissez. Si une personne correspond déjà dans votre Graph, elle s’affiche en premier dans le formulaire : vous pouvez alors ouvrir sa fiche. **Ajouter** ouvre la nouvelle page.

Une personne que vous ajoutez reste dans votre liste, même si vous n’avez pas encore échangé de messages avec elle. Votre premier message avec elle l’associe à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, son rôle auprès de vous, ainsi que son type, Travail ou Perso. Le champ **Notes** permet d’ajouter ce que vous souhaitez retenir. Les notes sont conservées lors des fusions. **Enregistrer** conserve les modifications. **Annuler** rétablit les informations précédentes.

Vos modifications sont conservées, même lorsque ses informations sont recherchées à nouveau, ainsi qu’après **Fusionner** et **Annuler**. Videz un champ pour utiliser à nouveau la valeur trouvée. Si vous effacez le nom, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus : **Importer une photo**, choisissez une photo trouvée pour cette personne ou **Retirer la photo**. La photo reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux fiches pourraient correspondre à la même personne, sa page vous demande s’il s’agit de la même personne. La liste Personnes les affiche sous **Même personne ?**. **Fusionner** regroupe leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre réponse s’affiche un instant sur la paire, puis celle-ci disparaît de la liste. La liste disparaît lorsqu’il n’y a plus rien à vérifier.

Une personne dont l’adresse ressemble seulement à une adresse connue, par exemple acme-corp.example et acmecorp.example, ne sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom identique ne suffit jamais pour fusionner des personnes de deux domaines différents, car n’importe qui peut saisir ce nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, par exemple les mêmes personnes ou un petit projet. Pour un prénom seul (« Sam » et « Sam Lee »), il faut un élément supplémentaire : la même entreprise, le même numéro de téléphone ou le même profil LinkedIn.

Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne sera jamais proposée. Ajoutez plutôt vos autres adresses dans **Paramètres**, sous [Vos adresses](settings.md#your-addresses).

Si seul le prénom correspond entre deux domaines différents, comme « Sam » et « Sam Lee », la fusion n’est proposée que si le numéro de téléphone ou le profil LinkedIn est le même.

Si seul le prénom correspond à une réunion créée à partir d’un chat, ou si l’adresse est celle d’une personne que vous connaissiez déjà et que seule la personne dans le chat dit qu’elle lui appartient, The Machine vous demande confirmation. The Machine n’ouvre jamais de lien pour vérifier.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel extérieur à votre entreprise et un chat personnel qui n’ont qu’un nom en commun ne sont pas automatiquement associés : ils sont affichés sous forme de question.

**Tout fusionner** fusionne toutes les paires de la liste, sauf celles que vous avez marquées **Pas la même**. **Annuler** les sépare toutes à nouveau si vous le faites tout de suite.

Pour fusionner vous-même deux personnes, ouvrez l’une de leurs fiches, puis sélectionnez **⋯**, **Même personne que…** et choisissez l’autre. La fiche de la personne fusionnée indique la raison sous **Fusionnée depuis**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯, choisissez **Supprimer définitivement…**, puis **Supprimer**. Cette action supprime la personne et les informations que votre Machine connaît à son sujet : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous, ainsi que vos notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, y compris lors d’une importation ou par une tâche d’anniversaires Facebook portant son nom ou son adresse. Cette action est irréversible.

## E-mails non distribués

Lorsqu’un e-mail envoyé à une personne n’est pas distribué, son adresse affiche la mention **Non distribué** et la date. Une autre de ses adresses s’affiche en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si une autre est connue. Si c’est sa seule adresse, la fenêtre d’envoi vous avertit, mais vous pouvez quand même envoyer le message.

Une adresse est considérée comme non distribuée lorsque le serveur de messagerie indique qu’elle n’existe pas, ou après trois échecs temporaires en une semaine. La mention disparaît lorsque la personne vous écrit à nouveau depuis cette adresse ou qu’un e-mail lui est bien envoyé.

## Poste et photo

Les personnes qui ont une adresse d’entreprise peuvent avoir un poste, une photo, un profil LinkedIn et une ville recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche utilise uniquement leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Pour désactiver cette option, allez dans **Paramètres**, sous Sécurité, puis **Rechercher les contacts pro**.

Ce réglage désactive aussi la consultation du site Web avant une première réunion et la recherche sur le Web si elle est configurée (voir [Prête pour vos réunions](calendar.md#ready-for-your-meetings)).

Lorsque la recherche trouve des informations, la page affiche aussi sa biographie, la date depuis laquelle elle occupe son poste actuel et ses deux postes précédents. Les préparations les utilisent aussi, mais ne reprennent sa biographie que si elle n’en a pas rédigé elle-même.

Vos connexions s’enrichissent aussi des informations déjà consultées : poste, téléphone et fuseau horaire depuis Slack, biographie et lieu depuis X, titre de profil et photo depuis LinkedIn, postes depuis Google Contacts et Salesflare, et photo d’un contact depuis Salesflare si le service en a une. Survolez la ligne sous son nom pour voir la source de ces informations.

Outlook ajoute les photos de vos collègues et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées par la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà présentes dans votre Graph. Aucun message ne leur est envoyé. Une importation des anniversaires Facebook ajoute la photo de profil d’une personne qui n’en a pas lorsque vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’un Fleet Travail, une petite copie d’une photo professionnelle accompagne la fiche partagée d’une personne. Les photos venant de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que celles que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours associés à vous et jamais à une personne de votre Graph. Une recherche sur vous-même ou l’ajout d’une personne avec l’une de vos adresses ouvre **À propos de vous**. Une importation ignore votre propre ligne.

La section À propos de vous répertorie vos adresses et indique leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre rôle auprès de cette personne

Les rôles que votre Machine repère dans vos messages s’affichent sur la page de la personne, sous **Pour vous**, avec uniquement les mots qui indiquent le rôle, comme un titre. Le fait qu’une personne dise être votre comptable ou votre client ne suffit pas : il faut aussi un élément de votre côté, comme vos propres messages ou réunions avec elle. Vous n’avez pas besoin de confirmer. Une erreur ? **Modifier** sur sa page permet de la corriger, tout comme **⋯** sur la ligne correspondante dans **Modifications récentes**. The Machine tient compte de vos modifications.

## Ce que The Machine sait sur une personne

Les informations sur une personne se trouvent sur sa page, sous **Informations connues**. La section **Apprentissage** contient les informations générales. **Ajouter** permet d’en ajouter une autre avec vos propres mots. Chaque information a son propre menu :

- **Modifier** permet de la modifier directement.
- **Ne concerne pas** cette personne la transforme à nouveau en information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

La section **Modifications récentes**, repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a modifié ou appris à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, une information ou une étape d’un projet. Chaque ligne indique la date et la source. Touchez la source pour lire le message.

Si une ligne est incorrecte, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Ne concerne pas** cette personne ou **Annuler** pour remettre un projet à son état précédent. Trois lignes s’affichent. **Afficher plus** révèle les autres.

Une personne dont votre Machine a mis à jour les informations aujourd’hui est signalée par un petit point dans la liste Personnes. Le message **4 personnes mises à jour aujourd’hui**, en haut de la liste, indique lesquelles. Voir [Le Graph](graph.md).

## Une tâche à propos d’une personne

**Nouvelle tâche**, dans le menu **⋯** d’une personne, d’une organisation ou d’un projet, permet de créer une tâche à son sujet.
