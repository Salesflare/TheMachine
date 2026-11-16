---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: a16cc66e51a64fd2
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, d’après vos messages et réunions. Les newsletters, reçus et autres envois ne font apparaître personne tant que vous n’avez pas répondu. Ils se trouvent sous Expéditeurs masqués, en bas de la liste : **Afficher comme une personne** permet d’en ajouter un. Les champs, tags et imports fonctionnent de la même façon dans les trois listes, et chaque liste a ses propres filtres : voir [The Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’une boutique) est rattachée à son organisation, pas à une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et sa ville, puis une phrase sur vos échanges (« Discussions quotidiennes · dernier contact hier · prochaine réunion mar. 27 oct. »). La date du dernier contact est indiquée sous la forme « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, une date s’affiche. Survolez-la pour voir la date exacte. Vous trouverez ensuite :

- **Contact** : ses numéros de téléphone et ses adresses e-mail. Touchez-en une pour appeler ou écrire, ou **Copier** pour la copier. Son **Anniversaire** s’affiche aussi ici, avec sa source (Google Contacts, Google Calendar, Facebook, vos notes ou vous-même) : voir [The Graph](graph.md#birthday).
- **Avec vous** : son lien avec vous, son type de contact, Travail ou Perso, ainsi que votre famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres plateformes où vous échangez avec cette personne. **Slack** ouvre sa page Slack ou votre fil Slack le plus récent avec elle.
- Les **Personnes** et **Projets** auxquels elle participe, les échanges **En cours entre vous** (promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et les chats d’une personne sont automatiquement associés lorsqu’il est évident qu’ils appartiennent à la même personne, par exemple une adresse e-mail professionnelle mise en copie depuis son adresse personnelle.

Si le message **Impossible de charger cette page.** s’affiche, touchez **Réessayer**. S’il s’affiche encore, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne résument les décisions, demandes, projets ou promesses, en nommant les personnes concernées. The Machine le reformule lorsqu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; dans les heures qui suivent un changement, comme une nouvelle échéance ou le retrait d’une demande.

Les informations vagues sont ignorées. S’il n’y a rien de précis à dire, aucun résumé n’apparaît. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une seule date, avec leur nombre. Touchez la date pour les ouvrir.

**Modifier** le résumé pour le reformuler. En cas de nouveauté, The Machine propose une **Mise à jour suggérée**, avec les options **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui confie à nouveau la rédaction.

Les préparatifs de réunion utilisent ce résumé, mais uniquement les lignes liées à la tâche concernée, Travail ou Perso. Il reste sur votre Machine et n’est jamais visible par votre équipe.

## Chronologie

Chaque page de personne ou d’organisation en a une, affichée de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent en haut, sous **À venir**, de la plus proche à la plus éloignée. **Afficher tout ce qui est à venir** affiche les autres réunions. Une réunion indique qui y a participé, chaque personne une seule fois. Celles qui ont des notes ou une transcription portent la mention **Notes** ou **Transcription**. Cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que ce que vos règles de partage autorisent. Sur une page, l’onglet **Équipe**, au-dessus de la chronologie, ajoute les éléments partagés par vos collègues et indique qui les a partagés. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** regroupent les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) prévaut. Sinon, les membres de votre famille et vos amis, ainsi que les personnes qui sont de votre famille ou de vos amis (votre épouse, votre père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais vos contacts personnels.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez son nom, ainsi que son adresse e-mail et son organisation si vous les connaissez. Si une personne similaire figure déjà dans votre Graph, le formulaire l’affiche d’abord pour que vous puissiez ouvrir sa fiche à la place. **Ajouter** ouvre la nouvelle page.

La personne que vous ajoutez reste dans la liste, même si vous n’avez encore aucun message avec elle. Son premier message sera associé à sa fiche.

## Modifier une personne

L’option **Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, sa ville, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, son lien avec vous et son type, Travail ou Perso. Le champ **Notes** vous permet de noter ce que vous souhaitez garder en mémoire. Les notes sont conservées lors d’une fusion. **Enregistrer** conserve les modifications ; **Annuler** les abandonne.

Vos modifications sont conservées même lorsque ses informations sont consultées à nouveau, ainsi qu’après une **Fusionner** ou une **Annuler**. Videz un champ pour réutiliser la valeur consultée. Si vous videz le nom, celui qui apparaît dans ses messages est rétabli.

Pour changer sa photo, cliquez dessus, puis choisissez **Importer une photo**, sélectionnez une photo trouvée pour cette personne ou choisissez **Retirer la photo**. La photo reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux fiches pourraient correspondre à la même personne, une question s’affiche sur leur page et Personnes les regroupe sous **Même personne ?**. **Fusionner** les associe, avec tous leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre choix s’affiche brièvement pour la paire, puis celle-ci disparaît de la liste. La liste disparaît lorsqu’il n’y a plus de question à poser.

Une personne dont l’adresse ressemble seulement à une adresse connue, comme acme-corp.example par rapport à acmecorp.example, ne sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Un nom seul ne suffit jamais pour associer deux personnes de domaines différents, car n’importe qui peut saisir ce nom. Deux adresses de domaines différents ne sont proposées que si un autre élément les relie, comme les mêmes personnes ou un projet. Une personne qui utilise votre nom à une adresse qui n’est pas la vôtre ne vous sera jamais proposée. Ajoutez plutôt vos autres adresses dans **Paramètres**, sous [Vos adresses](settings.md#your-addresses).

Si seul le prénom correspond entre deux domaines, comme « Sam » et « Sam Lee », ces personnes ne sont proposées que si elles ont le même numéro de téléphone ou profil LinkedIn.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel extérieur à votre entreprise et un chat personnel qui n’ont qu’un nom en commun ne sont pas associés automatiquement : ils sont signalés comme une question.

**Tout fusionner** associe toutes les paires de la liste en une fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après permet de toutes les séparer à nouveau.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis **⋯**, **Même personne que…** et sélectionnez l’autre. La page d’une personne associée indique la raison sous **Associée depuis**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯, choisissez **Supprimer définitivement…**, puis **Supprimer**. Cette action supprime la personne et les informations que votre Machine connaît à son sujet : sa fiche, ses adresses, les informations consultées, les messages échangés uniquement entre vous deux et les notes la concernant.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, y compris par un import ou une tâche d’anniversaire Facebook portant son nom ou son adresse. Cette action est irréversible.

## E-mail rejeté

Lorsqu’un e-mail envoyé à une personne est rejeté, la mention **Rejeté** s’affiche à côté de son adresse, avec la date. Une autre de ses adresses apparaît en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse lorsqu’une autre est connue. Si c’est sa seule adresse, un avertissement s’affiche dans la fenêtre d’envoi, mais vous pouvez tout de même envoyer l’e-mail.

Une adresse est considérée comme rejetée lorsque le serveur de messagerie indique qu’elle n’existe pas ou après 3 échecs temporaires sur une semaine. La mention disparaît lorsque la personne vous écrit à partir de cette adresse ou qu’un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse professionnelle obtiennent un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche ne reçoit que leur nom et le domaine de leur entreprise. Pour une photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Lorsque ces informations sont trouvées, leur page affiche aussi leur présentation, la date depuis laquelle elles occupent leur poste actuel et leurs deux postes précédents. Les préparatifs les utilisent aussi, mais n’utilisent la présentation que si la personne n’a pas de bio.

Vos connexions s’enrichissent aussi des informations qu’elles ont déjà partagées : poste, téléphone et fuseau horaire depuis Slack, bio et ville depuis X, titre et photo depuis LinkedIn, postes depuis Google Contacts et Salesflare, et photo depuis Salesflare si le service en conserve une. Survolez la ligne sous son nom pour voir la source des informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées par la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé. Un import des anniversaires Facebook ajoute la photo de profil d’une personne qui n’en a pas lorsque vous l’enregistrez ([Routines](routines.md)). Toutes ces informations restent sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’un Fleet professionnel, une petite copie de la photo professionnelle est jointe à la fiche partagée d’une personne. Les photos de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos adresses et numéros, y compris vos alias, correspondent toujours à vous, jamais à une personne de votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, la page **À propos de vous** s’ouvre et l’import ignore votre propre ligne.

La page À propos de vous liste vos adresses et leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre lien avec cette personne

Les rôles que votre Machine repère dans vos messages s’affichent sur sa page, sous **Pour vous**, avec uniquement les mots qui indiquent le rôle, comme un intitulé de poste. Le fait qu’une personne dise être votre comptable ou votre cliente ne suffit pas : il faut aussi des éléments de votre côté, comme vos propres messages ou réunions avec elle. Rien n’attend votre confirmation. Une erreur ? **Modifier** sur sa page permet de la corriger, ou utilisez **⋯** sur la ligne correspondante dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce qu’elle sait sur une personne

Les informations sur une personne se trouvent sur sa page, sous **Connu à propos de**. La section Apprentissage conserve les informations générales. **Ajouter** permet d’en ajouter une avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la modifier sur place.
- **Pas à propos de** cette personne la transforme à nouveau en information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

La section **Modifications récentes**, repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie les informations que votre Machine a modifiées ou apprises à leur sujet : un rôle, leur lieu de travail, le lien entre deux personnes, un fait ou une évolution de projet. Chaque ligne indique sa date et sa source. Touchez la source pour lire le message.

Si une information est incorrecte, son menu **⋯** permet de la corriger sur place : **Modifier**, **Retirer**, **Pas à propos de** cette personne, ou **Annuler** pour rétablir l’emplacement précédent d’un projet. Trois lignes s’affichent. **Afficher plus** donne accès aux autres.

Une personne dont votre Machine a mis les informations à jour aujourd’hui est signalée par un petit point dans la liste Personnes. Le texte **4 personnes mises à jour aujourd’hui** en haut de la liste indique lesquelles. Voir [The Graph](graph.md).

## Une tâche concernant une personne

**Nouvelle tâche**, dans le menu **⋯** d’une personne, d’une organisation ou d’un projet, permet de créer une tâche à leur sujet.
