---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Toutes les personnes avec qui vous êtes en contact, des plus proches aux autres, à partir de vos messages et réunions. Les newsletters, reçus et autres envois groupés n’ajoutent personne tant que vous ne répondez pas. Ils se trouvent sous Expéditeurs masqués, sous la liste : **Afficher comme personne** en ajoute un. Les champs, tags et importations fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [Le Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’une boutique) compte pour son organisation, pas comme une personne, même après que vous lui avez écrit.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et son lieu de résidence, puis une ligne sur vos échanges (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Les contacts récents sont indiqués par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours », et les plus anciens par une date. Passez la souris dessus pour voir la date exacte. En dessous :

- **Contact** : ses numéros de téléphone et ses adresses e-mail. Touchez-en un pour appeler ou écrire, ou **Copier** pour le copier. Son **Anniversaire** apparaît aussi ici, avec sa source (Google contacts, Google Calendar, Facebook ou vous) : voir [Le Graph](graph.md#birthday).
- **Avec vous** : ce qu’elle représente pour vous, contact pro ou perso, et votre famille ou votre Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous échangez avec elle. **Slack** l’ouvre dans Slack, ou ouvre votre fil Slack le plus récent avec elle.
- Les **Personnes** et **Projets** dont elle fait partie, les **En cours entre vous** (promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et les chats d’une personne sont automatiquement associés quand il est clair qu’il s’agit de la même personne, par exemple une adresse e-mail professionnelle mise en copie avec son adresse personnelle.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message revient, utilisez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes courtes en haut de la page d’une personne : ce qui a été décidé, demandé, prévu ou promis, avec le nom de chaque personne. The Machine le réécrit quand il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne d’abord. En général, une fois par jour ; sous quelques heures quand un sujet la concernant évolue, comme une nouvelle échéance ou une demande retirée.

Les lignes vagues sont omises ; s’il n’y a rien de précis à dire, il n’y a pas de résumé. Chaque ligne renvoie à sa source : les messages d’une même journée partagent une date et sont regroupés, avec leur nombre.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine propose une **Mise à jour suggérée**, avec **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui rend la main.

Les préparations de réunion l’utilisent, mais uniquement les lignes correspondant au contexte de cette tâche (Travail ou Perso). Le résumé reste sur votre Machine ; votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne et d’organisation en a une, des éléments les plus récents aux plus anciens : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les prochaines réunions apparaissent tout en haut, sous **À venir**, de la plus proche à la plus lointaine ; **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les personnes présentes, chacune une seule fois. Celles qui ont des notes ou une transcription affichent **Notes** ou **Transcription** ; cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que ce que vos règles de partage autorisent. Sur une page, **Équipe** au-dessus de la Chronologie ajoute ce que vos collègues ont partagé, avec la personne à l’origine de chaque élément ; **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** listent les personnes selon leur type, celui indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les personnes de votre famille et vos amis, ainsi que les membres de votre famille ou vos amis (une épouse, un père), sont classés comme personnels, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais vos contacts personnels.

## Ajouter une personne

**Nouvelle personne** en haut de Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne semblable existe déjà dans votre Graph, le formulaire l’affiche en premier pour que vous puissiez ouvrir sa page. **Ajouter** ouvre la nouvelle page.

La personne que vous ajoutez reste dans la liste, même sans messages. Son premier message l’associe à son profil.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, ce qu’elle représente pour vous, ainsi que son statut Travail ou Perso. Le champ **Notes** sert à noter ce dont vous voulez vous souvenir ; les notes sont conservées lors des fusions. **Enregistrer** sauvegarde les changements ; **Annuler** les abandonne.

Vos modifications sont conservées, même quand ses informations sont consultées à nouveau, ainsi qu’après **Fusionner** et **Annuler**. Videz un champ pour réutiliser la valeur consultée. Si vous videz le nom, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus : **Importer une photo**, choisissez-en une trouvée pour cette personne, ou **Retirer la photo**. Elle reste sur votre Machine.

## Fusionner deux personnes

Quand deux profils correspondent peut-être à la même personne, leur page vous pose la question et Personnes les affiche sous **Même personne ?**. **Fusionner** les regroupe avec tous leurs messages, notes, rôles et projets. **Pas la même** les sépare définitivement. Votre réponse apparaît brièvement sur la paire, qui quitte ensuite la liste. La liste disparaît quand il n’y a plus de question.

Une personne dont l’adresse ressemble simplement à celle d’une personne connue, comme acme-corp.example par rapport à acmecorp.example, n’est jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel externe à votre entreprise et un chat personnel qui n’ont qu’un nom en commun ne sont pas associés automatiquement : ils apparaissent sous forme de question.

**Tout fusionner** fusionne toutes les paires de la liste d’un coup, sauf celles que vous avez marquées **Pas la même**. **Annuler**, juste après, les sépare toutes à nouveau.

Pour associer vous-même deux personnes, ouvrez l’une d’elles, puis **⋯**, **Même personne que…** et choisissez l’autre. La page de la personne fusionnée indique la raison sous **Associée depuis**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. La personne et tout ce que votre Machine sait à son sujet sont supprimés : sa fiche, ses adresses, les informations consultées, les messages échangés uniquement entre vous deux et vos notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom est supprimé. Elle ne sera pas ajoutée à nouveau, même par une importation ou une tâche d’anniversaire Facebook portant son nom ou son adresse. Cette action est irréversible.

## E-mail non distribué

Quand un e-mail envoyé à une personne n’est pas distribué, son adresse porte la mention **Non distribué** et la date, et une autre de ses adresses apparaît en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si une autre est connue. Si c’est sa seule adresse, la fenêtre d’envoi vous avertit, mais vous pouvez quand même envoyer le message.

Une adresse est considérée comme non distribuable quand le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires sur une semaine. La mention disparaît quand la personne vous écrit à nouveau depuis cette adresse ou qu’un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse professionnelle obtiennent un poste, une photo, un profil LinkedIn et une ville, consultés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche ne transmet que leur nom et le domaine de leur entreprise. Pour les photos, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Quand ces informations sont disponibles, leur page affiche aussi leur présentation, la date de début de leur poste actuel et leurs deux postes précédents. Les préparations les consultent également, mais n’utilisent la présentation que si la personne n’a pas sa propre biographie.

Vos connexions se complètent avec les informations qu’elles consultent déjà : un poste, un numéro de téléphone et un fuseau horaire depuis Slack, une biographie et un lieu depuis X, un titre de profil et une photo depuis LinkedIn, des postes depuis Google contacts et Salesflare, et la photo d’un contact depuis Salesflare si le service en conserve une. Passez la souris sur la ligne sous son nom pour voir sa source.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont importées par votre synchronisation WhatsApp et votre connexion aux chats Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé. Une importation d’anniversaires Facebook ajoute la photo de profil d’une personne sans photo quand vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Graph d’équipe](team-graph.md) d’un Fleet professionnel, une petite copie de la photo professionnelle accompagne la fiche partagée d’une personne. Les photos provenant de Google contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours les vôtres et ne correspondent jamais à une autre personne dans votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre. Une importation ignore votre propre ligne.

La page À propos de vous liste vos adresses et leur source ; modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Ce qu’elle représente pour vous

Les rôles que votre Machine repère dans vos messages s’affichent sur sa page, sous **Pour vous**, avec la ligne qui a permis de les repérer. Rien n’attend votre confirmation. Une erreur ? **Modifier** sur sa page permet de la corriger, ou utilisez **⋯** sur la ligne dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce qu’elle sait sur une personne

Les informations sur cette personne se trouvent sur sa page, sous **Informations connues** ; Apprentissage conserve les informations générales. **Ajouter** permet d’en ajouter une autre avec vos propres mots. Chaque information a son menu :

- **Modifier** la change directement.
- **Ne la concerne pas** la transforme à nouveau en information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

**Modifications récentes**, repliées juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorient ce que votre Machine a modifié ou appris à leur sujet : un rôle, leur lieu de travail, le lien entre deux personnes, une information ou le déplacement d’un projet. Chaque ligne indique sa date et sa source ; touchez la source pour lire le message.

Si une ligne est incorrecte, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Ne la concerne pas** ou **Annuler** pour remettre un projet à sa place. Trois lignes s’affichent ; **Afficher plus** montre les autres.

Une personne dont votre Machine a mis à jour les informations aujourd’hui est signalée par un petit point dans la liste Personnes. **4 personnes mises à jour aujourd’hui** s’affiche en haut de la liste pour les nommer. Voir [Le Graph](graph.md).

## Une tâche concernant une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet crée une tâche à leur sujet.
