---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, et comment ajouter, modifier, fusionner ou supprimer quelqu’un.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Toutes les personnes avec qui vous êtes en contact, les plus proches en premier, à partir de vos messages et réunions. Les newsletters, reçus et autres envois ne créent pas de fiche tant que vous n’y répondez pas. Ils apparaissent sous **Expéditeurs masqués**, sous la liste : **Afficher comme une personne** les ajoute. Les champs, tags et imports fonctionnent de la même façon dans les trois listes, et chacune a ses propres filtres : voir [The Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom propre d’une boutique) est associée à son organisation, et non à une personne, même après que vous lui avez écrit.

## Page d’une personne

En haut, vous trouverez sa photo, son nom, son poste, son organisation et sa ville, ainsi qu’une ligne sur vos échanges (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour un contact plus ancien, la date s’affiche. Survolez-la pour voir la date exacte. Plus bas :

- **Contact** : ses numéros de téléphone et adresses e-mail. Touchez l’un d’eux pour appeler ou écrire, ou **Copier** pour le copier. Son **Anniversaire** apparaît aussi ici, avec sa source (Google contacts, Google Calendar, Facebook ou vous) : voir [The Graph](graph.md#birthday).
- **Avec vous** : son rôle auprès de vous, contact professionnel ou personnel, et votre famille ou Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres services où vous échangez avec cette personne. **Slack** ouvre son profil dans Slack ou votre dernière conversation Slack avec elle.
- Les **Personnes** et **Projets** auxquels elle est liée, les **En cours entre vous** (promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et conversations d’une personne sont automatiquement regroupées lorsqu’il est évident qu’elles lui appartiennent, par exemple une adresse e-mail professionnelle mise en copie avec son adresse personnelle.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message réapparaît, touchez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes courtes en haut de la page d’une personne : ce qui a été décidé, demandé, planifié ou promis, avec le nom de toutes les personnes concernées. The Machine le réécrit dès qu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; dans les quelques heures qui suivent un changement important, comme une nouvelle échéance ou une demande retirée.

Les lignes vagues sont ignorées. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée sont regroupés sous une seule date avec leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le formuler à votre façon. En cas de nouveauté, The Machine affiche une **Mise à jour suggérée**, avec **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui rend la main.

Les préparations de réunion l’utilisent, mais uniquement les lignes du type de cette tâche (Travail ou Perso). Le résumé reste sur votre Machine ; votre équipe ne le voit jamais.

## Chronologie

Chaque page de personne ou d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et leurs résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), discussions WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir s’affichent en haut, dans **À venir**, de la plus proche à la plus éloignée. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique les personnes qui y ont participé, chacune une seule fois. Les réunions avec des notes ou une transcription affichent **Notes** ou **Transcription** ; cliquez dessus pour les lire.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que ce que vos règles de partage autorisent. Sur une page, **Équipe**, au-dessus de la chronologie, ajoute les éléments partagés par vos coéquipiers, avec le nom de la personne qui a partagé chaque élément. **Les miens** n’affiche que les vôtres.

## Travail et Perso

Les onglets **Travail** et **Perso** affichent les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les personnes qui sont de votre famille ou vos amies (votre femme, votre père), sont classés dans Perso, quelle que soit l’adresse utilisée pour vous écrire. Votre équipe ne voit jamais les contacts personnels.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de Personnes, ou **+** dans la barre supérieure sur un téléphone. Saisissez un nom, puis une adresse e-mail et une organisation si vous les connaissez. Si une personne similaire existe déjà dans votre Graph, le formulaire l’affiche en premier pour que vous puissiez ouvrir sa fiche. Touchez **Ajouter** pour ouvrir la nouvelle fiche.

La personne que vous ajoutez reste dans votre Graph, même si vous n’avez encore aucun message avec elle. Son premier message la relie à sa fiche.

## Modifier une personne

**Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, sa ville, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, son rôle auprès de vous, ainsi que son classement Travail ou Perso. Le champ **Notes** vous permet de noter ce dont vous voulez vous souvenir ; les notes sont conservées lors des fusions. **Enregistrer** sauvegarde les changements, tandis que **Annuler** rétablit les valeurs précédentes.

Vos modifications sont conservées, y compris lorsque les informations de la personne sont recherchées à nouveau, ainsi qu’après une **Fusionner** ou une **Annuler**. Videz un champ pour utiliser à nouveau la valeur trouvée lors de la recherche. Si le nom est vide, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus : **Importer une photo**, choisissez-en une trouvée pour cette personne ou **Retirer la photo**. Elle reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux fiches pourraient désigner la même personne, une question s’affiche sur leur page et Personnes les regroupe sous **Même personne ?**. **Fusionner** réunit leurs messages, notes, rôles et projets. **Pas la même** les garde séparées définitivement. Votre choix s’affiche quelque temps sur la paire, puis elle disparaît de la liste. La liste disparaît lorsqu’il n’y a plus rien à vérifier.

Une personne dont l’adresse ressemble seulement à une adresse connue, par exemple acme-corp.example au lieu de acmecorp.example, ne vous sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel extérieur à votre entreprise et une conversation personnelle qui n’ont qu’un nom en commun ne sont pas automatiquement fusionnés : ils apparaissent comme une question à vérifier.

**Tout fusionner** fusionne toutes les paires de la liste en une fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après les sépare à nouveau.

Pour fusionner vous-même deux personnes, ouvrez l’une de leurs fiches, puis **⋯**, **Même personne que…** et choisissez l’autre. La page de la personne fusionnée indique la raison sous **Fusionnée à partir de**, avec **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. Cela supprime la personne et tout ce que votre Machine sait à son sujet : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et les notes la concernant.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, y compris lors d’un import ou d’une tâche d’anniversaire Facebook contenant son nom ou son adresse. Cette action est irréversible.

## E-mails rejetés

Lorsqu’un e-mail envoyé à une personne est rejeté, son adresse porte la mention **Rejetée**, avec la date. Si elle a une autre adresse, celle-ci s’affiche en premier. Les nouveaux brouillons ne sont jamais envoyés à l’adresse rejetée lorsqu’une autre adresse est connue. Si c’est sa seule adresse, une alerte s’affiche avant l’envoi, mais vous pouvez tout de même envoyer le message.

Une adresse est considérée comme rejetée lorsque le serveur de messagerie indique qu’elle n’existe pas, ou après 3 échecs temporaires en une semaine. Le statut est effacé lorsque la personne vous écrit à nouveau depuis cette adresse ou qu’un e-mail envoyé à celle-ci est distribué.

## Poste et photo

Les personnes qui ont une adresse professionnelle reçoivent un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, seules leur nom et le domaine de leur entreprise sont transmis lors de la recherche. Pour la photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Lorsque ces informations sont trouvées, leur page affiche aussi leur présentation, la date depuis laquelle elles occupent leur poste actuel et les deux postes précédents. Les préparations les consultent également, mais n’utilisent leur présentation que si elles n’ont pas de biographie.

Vos connexions ajoutent des informations qu’elles ont déjà consultées : un poste, un numéro de téléphone et un fuseau horaire depuis Slack, une biographie et une ville depuis X, un titre de profil et une photo depuis LinkedIn, des postes depuis Google contacts et Salesflare, et la photo d’un contact depuis Salesflare si le service en conserve une. Survolez la ligne sous son nom pour voir d’où viennent ces informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont ajoutées via la synchronisation WhatsApp et la connexion à vos conversations Telegram : jusqu’à 50 par jour pour chaque service, uniquement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé. Un import des anniversaires Facebook ajoute la photo de profil d’une personne qui n’en a pas, lorsque vous enregistrez sa fiche ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Team Graph](team-graph.md) d’un Fleet professionnel, une petite copie de la photo professionnelle est jointe à la fiche partagée de la personne. Les photos de Google contacts, WhatsApp, Telegram ou Facebook, ainsi que les photos que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours associés à vous, jamais à une autre personne de votre Graph. Si vous vous recherchez vous-même ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre. Lors d’un import, votre propre ligne est ignorée.

La page À propos de vous répertorie vos adresses et leur source. Modifiez-les dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un coéquipier ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre rôle auprès de cette personne

Les rôles que votre Machine repère dans vos messages apparaissent sur sa page sous **Pour vous**, avec la phrase où ils ont été détectés. Vous n’avez pas besoin de les confirmer. Une erreur ? **Modifier** sur sa page permet de la corriger, ou utilisez **⋯** sur la ligne correspondante dans **Modifications récentes**. Votre Machine apprend de vos modifications.

## Ce que votre Machine sait sur une personne

Les informations sur une personne figurent sur sa page, sous **Informations connues** ; **Apprentissage** regroupe les informations générales. **Ajouter** vous permet d’en ajouter une avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la changer directement.
- **Ne concerne pas** cette personne pour en faire à nouveau une information générale, sous **Apprentissage**, **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

**Modifications récentes**, dans la section repliable juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie ce que votre Machine a changé ou appris à leur sujet : un rôle, leur lieu de travail, le lien entre deux personnes, une information ou le changement d’étape d’un projet. Chaque ligne indique sa date et sa source. Touchez la source pour lire le message.

Si une ligne est incorrecte, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Ne concerne pas** cette personne ou **Annuler** pour remettre un projet à son étape précédente. Trois lignes s’affichent ; **Afficher plus** donne accès aux autres.

Une personne dont votre Machine a mis à jour les informations aujourd’hui est marquée d’un petit point dans la liste Personnes. Le message **4 personnes mises à jour aujourd’hui** en haut de la liste indique leurs noms. Voir [The Graph](graph.md).

## Une tâche concernant une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet crée une tâche à leur sujet.
