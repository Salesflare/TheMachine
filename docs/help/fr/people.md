---
title: Personnes
area: graph
summary: Toutes les personnes avec qui vous êtes en contact : leur page, leur résumé et leur chronologie, ainsi que les façons d’ajouter, de modifier, de fusionner ou de supprimer une personne.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 26845dd199228f90
---
Toutes les personnes avec qui vous êtes en contact, en commençant par les plus proches, d’après vos messages et vos réunions. Les newsletters, reçus et autres envois ne créent pas de contact tant que vous n’y répondez pas. Ils apparaissent sous Expéditeurs masqués, au bas de la liste : **Afficher comme une personne** en ajoute un. Les champs, tags et importations fonctionnent de la même façon dans les trois listes, et chaque liste a ses propres filtres : voir [The Graph](graph.md).

Une boîte de réception partagée (info@, service client, nom d’un magasin) est associée à son organisation, et non à une personne, même si vous lui écrivez.

## Page d’une personne

La page commence par sa photo, son nom, son poste, son organisation et son lieu, puis une ligne résume vos échanges (« Échanges quotidiens · dernier contact hier · prochaine réunion mar. 27 oct. »). Le dernier contact est indiqué par « à l’instant », « il y a 3 heures », « hier » ou « il y a 3 jours ». Pour les contacts plus anciens, la date s’affiche. Survolez-la pour voir la date exacte. En dessous :

- **Contact** : ses numéros de téléphone et ses adresses e-mail. Touchez l’un d’eux pour appeler ou écrire, ou **Copier** pour le copier. Son **Anniversaire** apparaît aussi ici, avec sa source (Google Contacts, Google Calendar, Facebook, vos notes ou vous) : voir [The Graph](graph.md#birthday).
- **Avec vous** : son rôle dans votre vie, son type de contact (pro ou personnel), ainsi que votre famille ou votre Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous échangez avec cette personne. **Slack** ouvre son profil dans Slack ou votre conversation Slack la plus récente avec elle.
- Les **Personnes** et **Projets** dont elle fait partie, les **En cours entre vous** (promesses dans les deux sens, avec **Marquer comme fait** et **Abandonner**) et sa **Chronologie**.

Les adresses et chats d’une personne sont associés automatiquement lorsqu’il est clair qu’ils lui appartiennent, par exemple une adresse e-mail professionnelle en copie d’un e-mail envoyé depuis sa propre adresse.

Si la page affiche **Impossible de charger cette page.**, touchez **Réessayer**. Si le message s’affiche toujours, touchez **Un problème ?** en bas de la page.

## Résumé

Quelques lignes en haut de la page d’une personne résument les décisions, demandes, projets ou promesses, et nomment toutes les personnes concernées. The Machine le réécrit lorsqu’il y a du nouveau, uniquement pour les personnes avec qui vous êtes vraiment en contact, et vérifie chaque ligne au préalable. En général, une fois par jour ; sous quelques heures si un élément concernant cette personne change, comme une nouvelle échéance ou une demande retirée.

Les lignes vagues sont omises. S’il n’y a rien de précis à dire, aucun résumé ne s’affiche. Chaque ligne renvoie à sa source : les messages d’une même journée partagent une date et leur nombre, et s’ouvrent ensemble.

**Modifier** le résumé pour le reformuler à votre façon. En cas de nouveauté, The Machine affiche une **Mise à jour suggérée**, avec les options **L’utiliser** et **Garder la mienne**. **Laisser The Machine l’écrire** lui confie à nouveau le résumé.

Les préparatifs de réunion l’utilisent, mais uniquement les lignes associées au type de la tâche concernée (pro ou personnel). Ils restent sur votre Machine ; votre équipe ne les voit jamais.

## Chronologie

Chaque page de personne et d’organisation a une chronologie, de la plus récente à la plus ancienne : e-mails, réunions et résumés Zoom, conversations Intercom (avec **Ouvrir dans Intercom**), chats WhatsApp, Telegram, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut affichent une source à la fois. **Afficher plus** charge les éléments plus anciens.

Les réunions à venir apparaissent en haut, sous **À venir**, de la plus proche à la plus éloignée. **Afficher tout ce qui est à venir** affiche les autres. Une réunion indique qui y a participé, chaque personne une seule fois. Les réunions avec des notes ou une transcription portent la mention **Notes** ou **Transcription** ; cliquez dessus pour les consulter.

Vos chronologies vous appartiennent : le Graph de l’équipe n’affiche que ce qu’autorisent vos règles de partage. Sur une page, l’option **Équipe** au-dessus de la chronologie ajoute les éléments partagés par vos collègues, en indiquant leur auteur ; **Les miens** n’affiche que les vôtres.

## Travail et perso

Les onglets **Travail** et **Perso** affichent les personnes selon leur type, indiqué sur leur page. Votre choix (**Modifier**) est prioritaire. Sinon, les membres de votre famille et vos amis, ainsi que les personnes qui sont de la famille ou des amis pour vous (une épouse, un père), sont classés comme personnels, quelle que soit l’adresse depuis laquelle ils écrivent. Votre équipe ne voit jamais vos contacts personnels.

## Ajouter une personne

Touchez **Nouvelle personne** en haut de Personnes, ou **+** dans la barre supérieure sur un téléphone. Indiquez un nom, ainsi qu’une adresse e-mail et une organisation si vous les connaissez. Si une personne qui lui ressemble figure déjà dans votre Graph, le formulaire l’affiche en premier pour que vous puissiez ouvrir sa fiche. **Ajouter** ouvre la nouvelle page.

La personne que vous ajoutez reste dans votre liste, même si vous n’avez encore aucun message avec elle. Son premier message sera associé à sa fiche.

## Modifier une personne

L’option **Modifier**, en haut de sa page, permet de changer son nom, son poste, son organisation, son lieu, son profil LinkedIn, ses numéros de téléphone et ses adresses e-mail, son rôle dans votre vie, ainsi que son type (pro ou personnel). Le champ **Notes** permet d’ajouter tout ce que vous voulez retenir ; les notes sont conservées lors des fusions. **Enregistrer** garde les modifications ; **Annuler** les abandonne.

Vos modifications sont conservées, même lorsque ses informations sont recherchées à nouveau, ainsi qu’après **Fusionner** et **Annuler**. Effacez le contenu d’un champ pour réutiliser la valeur trouvée automatiquement. Si vous effacez le nom, celui de ses messages réapparaît.

Pour changer sa photo, cliquez dessus, puis choisissez **Importer une photo**, sélectionnez une photo trouvée pour cette personne ou choisissez **Retirer la photo**. La photo reste sur votre Machine.

## Fusionner deux personnes

Lorsque deux fiches pourraient correspondre à la même personne, leur page vous demande si c’est le cas et Personnes les affiche sous **Même personne ?**. **Fusionner** associe leurs messages, notes, rôles et projets. **Pas la même** les garde séparées définitivement. Votre réponse reste affichée sur la paire un instant, puis celle-ci disparaît de la liste. La liste disparaît lorsqu’il n’y a plus de question à poser.

Une personne dont l’adresse ressemble seulement à celle d’un contact connu, comme acme-corp.example par rapport à acmecorp.example, ne sera jamais proposée comme étant la même personne. Vous seul pouvez lui attribuer un rôle.

Une adresse partagée, comme info@ ou une liste de diffusion, n’est jamais associée aux personnes qui l’utilisent pour écrire. Un contact professionnel extérieur à votre entreprise et un contact personnel qui n’ont qu’un nom en commun ne sont pas associés automatiquement : ils sont affichés comme une question.

**Tout fusionner** associe toutes les paires de la liste en une fois, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après les sépare à nouveau.

Pour associer vous-même deux personnes, ouvrez l’une de leurs pages, puis choisissez **⋯**, **Même personne que…** et sélectionnez l’autre personne. La page d’une personne associée indique pourquoi sous **Associée depuis**, avec l’option **Annuler** pour les séparer à nouveau.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. Cela supprime la personne et tout ce que votre Machine sait à son sujet : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et les notes à son sujet.

Les tâches qui la concernent sont conservées, mais son nom en est retiré. Elle ne sera pas ajoutée à nouveau, y compris par une importation ou une tâche d’anniversaire Facebook portant son nom ou son adresse. Cette action est irréversible.

## E-mail renvoyé

Lorsqu’un e-mail envoyé à une personne est renvoyé, son adresse porte la mention **Renvoyé**, accompagnée de la date, et une autre de ses adresses apparaît en premier. Les nouveaux brouillons ne sont jamais envoyés à cette adresse si une autre est connue. Si c’est sa seule adresse, l’écran d’envoi vous avertit, mais vous pouvez tout de même envoyer l’e-mail.

Une adresse est considérée comme renvoyée si le serveur de messagerie indique qu’elle n’existe pas ou après 3 échecs temporaires en une semaine. La mention disparaît lorsque la personne écrit à nouveau depuis cette adresse ou lorsqu’un e-mail lui est envoyé avec succès.

## Poste et photo

Les personnes qui ont une adresse professionnelle reçoivent un poste, une photo, un profil LinkedIn et une ville, recherchés comme les [informations sur les organisations](organization-data.md). Sur une Machine hébergée, la recherche utilise uniquement leur nom et le domaine de leur entreprise. Pour trouver une photo, Gravatar reçoit une empreinte de leur adresse professionnelle, jamais l’adresse elle-même. Désactivez cette option dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Lorsque la recherche trouve des informations, la page affiche aussi leur présentation, la date depuis laquelle la personne occupe son poste actuel et ses deux postes précédents. Les préparatifs les consultent également, mais n’utilisent la présentation que si la personne n’a pas de biographie.

Vos connexions s’enrichissent aussi des informations déjà consultées par The Machine : un poste, un numéro de téléphone et un fuseau horaire provenant de Slack ; une biographie et un lieu venant de X ; un titre et une photo venant de LinkedIn ; des postes venant de Google Contacts et de Salesflare ; et la photo d’un contact venant de Salesflare lorsque le service en conserve une. Survolez la ligne sous son nom pour voir d’où viennent les informations.

Outlook ajoute les photos des collègues de votre organisation et de vos contacts Outlook, ainsi que les postes et les entreprises de vos contacts ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

Les photos WhatsApp et Telegram sont récupérées via la synchronisation WhatsApp et la connexion à vos chats Telegram : jusqu’à 50 par jour pour chaque service, et uniquement pour les personnes déjà dans votre Graph. Aucun message ne leur est envoyé. Une importation des anniversaires Facebook ajoute la photo de profil des personnes qui n’en ont pas lorsque vous l’enregistrez ([Routines](routines.md)). Tout reste sur votre Machine.

Dans le [Team Graph](team-graph.md) d’un Work Fleet, une petite copie de la photo professionnelle accompagne la fiche partagée d’une personne. Les photos de Google Contacts, WhatsApp, Telegram ou Facebook, ainsi que celles que vous avez modifiées ou supprimées, ne sont jamais partagées.

## À propos de vous

Vos propres adresses et numéros, y compris vos alias, sont toujours associés à vous, jamais à une personne de votre Graph. Si vous vous recherchez ou ajoutez une personne avec l’une de vos adresses, **À propos de vous** s’ouvre. Une importation ignore votre propre ligne.

La page À propos de vous répertorie vos adresses et indique leur source. Vous pouvez les modifier dans **Paramètres**, sous Compte. Pour envoyer vos coordonnées à un collègue ou à un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Votre rôle auprès de cette personne

Les rôles que votre Machine repère dans vos messages apparaissent sur sa page, sous **Pour vous**, avec la phrase dans laquelle ils ont été repérés. Vous n’avez rien à confirmer. Une erreur ? L’option **Modifier** sur sa page permet de corriger le rôle, tout comme **⋯** sur sa ligne dans **Modifications récentes**. The Machine apprend de vos modifications.

## Ce que The Machine sait sur une personne

Les informations à son sujet apparaissent sur sa page, sous **Informations connues** ; les informations générales se trouvent dans **Apprentissage**. **Ajouter** permet d’en ajouter une autre avec vos propres mots. Chaque information a un menu :

- **Modifier** permet de la changer directement.
- **Pas à son sujet** la redevient générale et la déplace dans **Apprentissage**, sous **Faits**.
- **Retirer** la supprime partout.

## Modifications récentes

**Modifications récentes**, dans la section repliée juste au-dessus de la chronologie d’une personne, d’une organisation ou d’un projet, répertorie les informations que votre Machine a modifiées ou apprises à son sujet : un rôle, son lieu de travail, le lien entre deux personnes, un fait ou un changement de projet. Chaque ligne indique sa date et sa source. Touchez la source pour lire le message.

Si une ligne est incorrecte, son menu **⋯** permet de la corriger directement : **Modifier**, **Retirer**, **Pas à son sujet** ou **Annuler** pour remettre un projet à sa place. Trois lignes s’affichent ; **Afficher plus** révèle les autres.

Une personne dont votre Machine a mis la fiche à jour aujourd’hui est signalée par un petit point dans la liste Personnes. Le message **4 personnes mises à jour aujourd’hui** en haut de la liste indique lesquelles. Voir [The Graph](graph.md).

## Une tâche concernant une personne

**Nouvelle tâche** dans le menu **⋯** d’une personne, d’une organisation ou d’un projet permet de créer une tâche à leur sujet.
