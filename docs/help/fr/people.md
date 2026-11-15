---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, ainsi que la façon d’ajouter, de modifier, de fusionner ou de supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 907cec019dc70184
---
Toutes les personnes avec qui vous êtes en contact, en commençant par les plus proches, d’après vos messages et vos réunions. Les newsletters, reçus et autres envois ne sont pas ajoutés tant que vous n’y répondez pas. Ils se trouvent sous Expéditeurs masqués, sous la liste : **Afficher comme personne** permet d’ajouter l’expéditeur. Les champs, étiquettes et importations fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [The Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom de boutique) est rattachée à son organisation, pas à une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et son lieu, puis une ligne indique la nature de votre relation (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le contact récent est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours », et les contacts plus anciens par une date. Survolez-la pour voir la date exacte. Plus bas :

- **Contact** : ses numéros de téléphone et adresses e-mail. Touchez l’un d’eux pour appeler ou écrire, ou **Copier** pour le copier. Son **Anniversaire** apparaît aussi ici, avec la source de l’information (contacts Google, Google Calendar, Facebook, vos notes ou vous-même) : voir [The Graph](graph.md#birthday).
- **Avec vous** : la nature de votre relation, contact Travail ou Perso, ainsi que votre famille ou votre Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous échangez avec cette personne. **Slack** ouvre son profil dans Slack, ou votre dernier fil Slack avec elle.
- Les **Personnes** et **Projets** dont elle fait partie, les éléments **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et les chats d’une personne sont automatiquement associés lorsqu’il est évident qu’il s’agit de la même personne, par exemple une adresse e-mail professionnelle mise en copie avec son adresse personnelle.

Si une page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message persiste, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes courtes en haut de la page d’une personne : ce qui a été décidé, demandé, prévu ou promis, avec le nom de chaque personne. The Machine le réécrit lorsqu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; dans les quelques heures qui suivent un changement important, comme une nouvelle échéance ou le retrait d’une demande.

Les lignes vagues sont omises. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée partagent une date et un nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouvelle information, The Machine affiche une **Mise à jour suggérée**, avec **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui rend la main.

Les préparations de réunion l’utilisent, mais uniquement les lignes correspondant au type de la tâche, Travail ou Perso. Le résumé reste sur votre Machine ; votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation en a une, classée de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les prochaines réunions apparaissent en haut, sous **À venir**, de la plus proche à la plus lointaine. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique qui y a participé, chaque personne une seule fois. Celles avec des notes ou une transcription affichent **Notes** ou **Transcription**. Cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que ce que vos règles de partage autorisent. Sur une page, **Équipe**, au-dessus de la Chronologie, ajoute ce que vos collègues ont partagé. Chaque élément indique sa source. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** répertorient les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, votre famille et vos amis, ainsi que les personnes qui sont de votre famille ou de vos amis (votre épouse, votre père), sont classés dans Perso, quelle que soit l’adresse utilisée. Votre équipe ne voit jamais les contacts Perso.

## Ajouter une personne

**Nouvelle personne** en haut de Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne semblable figure déjà dans votre Graph, le formulaire l’affiche d’abord pour que vous puissiez ouvrir sa page à la place. **Ajouter** ouvre la nouvelle page.

Une personne que vous ajoutez reste dans la liste, même sans message. Son premier message est associé à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, la nature de votre relation et son type, Travail ou Perso. Le champ **Notes** permet de noter ce dont vous voulez vous souvenir. Les notes sont conservées lors des fusions. **Enregistrer** conserve les modifications ; **Annuler** les abandonne.

Vos modifications sont conservées, même lorsque ses informations sont recherchées à nouveau, ainsi qu’après **Fusionner** et **Annuler**. Videz un champ pour réutiliser la valeur trouvée. Si vous videz le nom, celui qui figure dans ses messages réapparaît.

Pour changer sa photo, cliquez dessus : **Importer une photo**, choisissez-en une trouvée pour cette personne ou **Retirer la photo**. Elle reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux personnes sont peut-être la même, leur page vous demande si c’est le cas, et Personnes les affiche sous **Même personne ?**. **Fusionner** les réunit, avec tous leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre réponse s’affiche quelque temps pour la paire, puis celle-ci disparaît de la liste. La liste disparaît lorsqu’il n’y a plus de question à poser.

Une personne dont l’adresse ressemble seulement à celle d’un contact connu, comme acme-corp.example par rapport à acmecorp.example, ne sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais pour associer deux personnes de domaines différents, car n’importe qui peut saisir ce nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, comme les mêmes personnes ou un projet. Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne vous sera jamais proposée. Ajoutez plutôt vos autres adresses sous Paramètres, [Vos adresses](settings.md#your-addresses).

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui écrivent par son intermédiaire. Un contact professionnel extérieur à votre entreprise et un chat personnel dont le seul point commun est un nom ne sont pas associés automatiquement : ils sont présentés sous forme de question.

**Tout fusionner** fusionne toutes les paires de la liste en une fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après les sépare à nouveau.

Pour associer vous-même deux personnes, ouvrez la page de l’une d’elles, puis **⋯**, **Même personne que…** et choisissez l’autre. La page de la personne associée indique la raison sous **Associée depuis**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. Cette action supprime la personne et tout ce que votre Machine sait à son sujet : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et les notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, pas même par une importation ou une tâche d’anniversaire Facebook contenant son nom ou son adresse. Cette action est irréversible.

## E-mails non distribués

Lorsqu’un e-mail envoyé à une personne n’est pas distribué, son adresse affiche **Non distribué**, avec la date, et une autre de ses adresses apparaît en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse lorsqu’une autre est connue. S’il s’agit de sa seule adresse, la fenêtre d’envoi vous en avertit, mais vous pouvez quand même envoyer le message.

Une adresse est considérée comme non distribuée lorsque le serveur de messagerie indique qu’elle n’existe pas, ou après trois échecs temporaires sur une semaine. Le statut est effacé lorsque la personne vous écrit depuis cette adresse ou lorsqu’un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse professionnelle reçoivent un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche n’utilise que leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option sous **Paramètres**, dans Sécurité : **Rechercher les contacts pro**.

Lorsque ces informations sont trouvées, leur page affiche aussi leur présentation, depuis quand elles occupent leur poste actuel et leurs deux postes précédents. Les préparations les utilisent également, mais ne reprennent la présentation que si elles n’ont pas leur propre biographie.

Vos Connexions se complètent avec les informations déjà lues : un poste, un numéro de téléphone et un fuseau horaire depuis Slack, une biographie et un lieu depuis X, un titre et une photo depuis LinkedIn, des postes depuis les contacts Google et Salesflare, et la photo d’un contact depuis Salesflare lorsque le service en conserve une. Survolez la ligne sous son nom pour voir d’où vient l’information.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont ajoutées via la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, et uniquement pour les personnes déjà présentes dans votre Graph. Rien ne leur est envoyé. Une importation d’anniversaires Facebook ajoute, lorsque vous l’enregistrez, la photo de profil des personnes qui n’ont pas encore de photo ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’un Fleet Travail, une petite copie d’une photo professionnelle accompagne la fiche partagée d’une personne. Les photos provenant des contacts Google, de WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours les vôtres et ne sont jamais ceux d’une autre personne dans votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre, et votre propre ligne est ignorée lors d’une importation.

La page À propos de vous répertorie vos adresses et leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## La nature de votre relation

Les rôles que votre Machine repère dans vos messages apparaissent sur sa page, sous **Pour vous**, avec la phrase dans laquelle ils ont été repérés. Rien n’attend votre confirmation. Une erreur ? **Modifier** sur sa page permet de la corriger, ou utilisez **⋯** sur sa ligne dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce qu’elle sait sur une personne

Les informations sur cette personne se trouvent sur sa page, sous Informations connues. L’Apprentissage conserve les informations générales. **Ajouter** permet d’en ajouter une autre, avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la modifier directement.
- **Pas à son sujet** la requalifie en information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

La section **Modifications récentes**, repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a modifié ou appris à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, une information ou l’évolution d’un projet. Chaque ligne indique sa date et sa source. Touchez la source pour lire le message.

Pour corriger une ligne erronée, utilisez son menu **⋯** : **Modifier**, **Retirer**, **Pas à son sujet**, ou **Annuler** pour remettre un projet à sa place. Trois lignes s’affichent ; **Afficher plus** affiche les autres.

Une personne dont votre Machine a mis les informations à jour aujourd’hui est signalée par un petit point dans la liste Personnes, et **4 personnes mises à jour aujourd’hui** les indique en haut de la liste. Voir [The Graph](graph.md).

## Tâche concernant une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à leur sujet.
