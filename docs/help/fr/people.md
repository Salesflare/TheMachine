---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, ainsi que les façons d’ajouter, de modifier, de fusionner ou de supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e671ff84b143e74
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, à partir de vos messages et de vos réunions. Les newsletters, reçus et autres envois ne deviennent des personnes que si vous répondez. Ils se trouvent sous Expéditeurs masqués, sous la liste : **Afficher comme personne** en ajoute un. Les champs, tags et imports fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [Le Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom propre d’une boutique) est associée à son organisation, et non à une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et sa ville, puis une ligne indique vos échanges (« Vous parlez chaque jour · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact s’affiche sous la forme « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours », ou sous forme de date pour les contacts plus anciens. Survolez-le pour voir la date exacte. En dessous :

- **Contact** : ses numéros de téléphone et ses adresses e-mail. Touchez-en un pour appeler ou écrire, ou **Copier**. Son **Anniversaire** s’affiche aussi ici, avec sa source (Google Contacts, Google Agenda, Facebook, vos notes ou vous) : voir [Le Graph](graph.md#birthday).
- **Avec vous** : la nature de votre lien avec cette personne, si c’est un contact professionnel ou personnel, et votre Fleet Famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous échangez avec elle. **Slack** ouvre son profil dans Slack, ou votre fil Slack le plus récent avec elle.
- Les **Personnes** et **Projets** auxquels elle participe, **En cours entre vous** (les promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**), ainsi que sa **Chronologie**.

Les adresses et les chats d’une personne sont automatiquement associés quand il est évident qu’il s’agit de la même personne, par exemple une adresse professionnelle avec sa propre adresse en copie. C’est aussi le cas lorsqu’une personne avec qui vous discutez réserve un appel à partir du lien que vous lui avez envoyé, et que son entreprise ou son nom de famille correspond.

Si une page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message s’affiche encore, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes courtes en haut de la page d’une personne : ce qui a été décidé, demandé, prévu ou promis, avec le nom de toutes les personnes concernées. The Machine le réécrit quand il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour, ou en quelques heures si quelque chose change avec cette personne, comme une nouvelle échéance ou une demande annulée.

Les lignes vagues sont écartées. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée partagent une date indiquant leur nombre et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine affiche une **Mise à jour suggérée**, avec les options **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui rend la main.

Les préparatifs de réunion s’en servent, mais uniquement pour les lignes liées au côté de cette tâche concerné (Travail ou Perso). Le résumé reste sur votre Machine : votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation en a une, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les pastilles en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les prochaines réunions s’affichent en haut, sous **À venir**, de la plus proche à la plus éloignée. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les personnes présentes, chacune une seule fois. Si elle comporte des notes ou une transcription, **Notes** ou **Transcription** s’affiche. Cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que les informations autorisées par vos règles de partage. Sur une page, **Équipe**, au-dessus de la chronologie, ajoute les informations partagées par vos collègues, avec le nom de la personne qui a partagé chaque élément. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** répertorient les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, votre famille et vos amis, ainsi que les personnes qui sont de la famille ou des amis pour vous (une épouse, un père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais les contacts personnels.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de Personnes, ou **+** dans la barre du haut sur un téléphone. Indiquez un nom, puis une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire figure déjà dans votre Graph, le formulaire l’affiche en premier pour que vous puissiez ouvrir sa page. **Ajouter** ouvre la nouvelle page.

La personne que vous ajoutez reste dans la liste, même si vous n’avez encore aucun message avec elle. Son premier message sera associé à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, sa ville, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, la nature de votre lien avec elle, ainsi que son classement Travail ou Perso. Le champ **Notes** sert à noter ce dont vous voulez vous souvenir. Les notes sont conservées lors des fusions. **Enregistrer** garde les modifications, et **Annuler** rétablit la version précédente.

Vos modifications sont conservées, même si ses informations sont recherchées de nouveau, et après une **Fusionner** ou une **Annuler**. Videz un champ pour réutiliser la valeur trouvée. Si vous videz le nom, celui de ses messages est rétabli.

Pour changer sa photo, cliquez dessus : **Importer une photo**, choisissez une photo trouvée pour cette personne ou **Retirer la photo**. Elle reste sur votre Machine.

## Fusionner deux personnes

Quand deux fiches pourraient correspondre à la même personne, leur page vous le demande, et Personnes les regroupe sous **Même personne ?**. **Fusionner** les réunit avec tous leurs messages, notes, rôles et projets. **Pas la même** les garde séparées définitivement. Votre réponse s’affiche un moment sur les deux fiches, puis elles disparaissent de la liste. La liste disparaît quand il n’y a plus rien à vérifier.

Une personne dont l’adresse ressemble simplement à celle d’un contact connu, par exemple acme-corp.example au lieu de acmecorp.example, n’est jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais pour associer deux personnes de domaines différents, car n’importe qui peut saisir un nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, comme des personnes en commun ou un projet. Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne vous est jamais proposée. Ajoutez plutôt vos autres adresses dans Paramètres, [Vos adresses](settings.md#your-addresses).

Si seul le prénom correspond dans des domaines différents, comme « Sam » et « Sam Lee », les personnes ne sont proposées que si elles ont le même numéro de téléphone ou le même profil LinkedIn.

Si seul le prénom correspond à une réunion créée à partir d’un chat, ou si l’adresse appartient à une personne que vous connaissez déjà et que seule la personne dans le chat dit qu’elle est à elle, une confirmation vous est demandée. The Machine n’ouvre jamais de lien pour vérifier.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui écrivent par son intermédiaire. Un contact professionnel extérieur à votre entreprise et un contact personnel avec seulement un nom en commun ne sont pas associés automatiquement : ils apparaissent comme une question à vérifier.

**Tout fusionner** fusionne toutes les paires de la liste en même temps, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après les sépare toutes de nouveau.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis **⋯**, **Même personne que…** et choisissez l’autre. La page d’une personne fusionnée indique la raison sous **Fusionnée à partir de**, avec **Annuler** pour les séparer de nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. La personne et tout ce que votre Machine sait à son sujet sont supprimés : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et les notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée de nouveau, y compris par un import ou une tâche d’anniversaire Facebook portant son nom ou son adresse. Cette action est irréversible.

## E-mail non distribué

Quand un e-mail envoyé à une personne n’est pas distribué, son adresse affiche **Non distribué**, avec la date, et une autre de ses adresses s’affiche en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si vous en connaissez une autre. Si c’est sa seule adresse, la fenêtre d’envoi vous en avertit, mais vous pouvez quand même envoyer le message.

Une adresse est considérée comme non distribuable quand le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires sur une semaine. Le statut est effacé quand la personne vous écrit de nouveau depuis cette adresse, ou quand un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse professionnelle reçoivent un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche n’utilise que leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit le hachage de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Cette option désactive aussi la consultation du site Web avant une première réunion et la recherche sur le Web, si elle est configurée (voir [Prête pour vos réunions](calendar.md#ready-for-your-meetings)).

Quand la recherche trouve des informations, la page affiche aussi leur texte de présentation, la date de début de leur poste actuel et leurs deux postes précédents. Les préparatifs de réunion les consultent également, mais n’utilisent le texte de présentation que si la personne n’a pas de biographie.

Vos connexions s’enrichissent aussi des informations déjà consultées : poste, téléphone et fuseau horaire depuis Slack, biographie et ville depuis X, titre et photo depuis LinkedIn, postes depuis Google Contacts et Salesflare, et photo d’un contact depuis Salesflare si le service en conserve une. Survolez la ligne sous son nom pour voir la source de ces informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées via la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, et uniquement pour les personnes déjà dans votre Graph. Aucun message ne leur est envoyé. Un import des anniversaires Facebook ajoute la photo de profil d’une personne qui n’a pas de photo lorsque vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’un Fleet Travail, une petite copie d’une photo professionnelle accompagne la fiche partagée d’une personne. Les photos provenant de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que celles que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, correspondent toujours à vous, jamais à une personne de votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, la page **À propos de vous** s’ouvre. Un import ignore votre propre ligne.

La page À propos de vous répertorie vos adresses et leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre lien avec cette personne

Les rôles que votre Machine repère dans vos messages s’affichent sur sa page sous **Pour vous**, avec uniquement les mots qui indiquent le rôle, comme un titre. Il ne suffit pas qu’une personne dise qu’elle est votre comptable ou votre cliente : vos propres échanges avec elle, par exemple vos messages ou vos réunions, doivent aussi le confirmer. Vous n’avez rien à approuver. Si le rôle est incorrect, **Modifier** sur sa page permet de le corriger, tout comme **⋯** sur sa ligne dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce que votre Machine sait sur une personne

Les faits à son sujet se trouvent sur sa page, sous **Informations connues**. La section Apprentissage conserve les informations générales. **Ajouter** permet d’en ajouter une autre avec vos propres mots. Chaque fait a un menu :

- **Modifier** le modifie directement.
- **Ne concerne pas** cette personne le retransforme en fait général, sous **Apprentissage**, **Faits**.
- **Retirer** le supprime partout.

## Modifications récentes

**Modifications récentes**, dans la section repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a modifié ou appris à leur sujet : un rôle, leur lieu de travail, le lien entre deux personnes, un fait ou un changement de projet. Chaque ligne indique la date et la source. Touchez la source pour lire le message.

Si une ligne est incorrecte, **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Ne concerne pas** cette personne ou **Annuler** pour remettre un projet à son emplacement précédent. Trois lignes s’affichent. **Afficher plus** affiche les autres.

Une personne dont votre Machine a mis les informations à jour aujourd’hui est signalée par un petit point dans la liste Personnes. Le haut de la liste indique aussi **4 personnes mises à jour aujourd’hui** et les nomme. Voir [Le Graph](graph.md).

## Une tâche au sujet d’une personne

**Nouvelle tâche**, dans le menu **⋯** d’une personne, d’une organisation ou d’un projet, crée une tâche à son sujet.
