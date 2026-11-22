---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches mises en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 24033419578a8c8f
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches qui arrivent à échéance ce jour-là et celles mises en attente, le jour où elles reviennent,
- les suivis sur le travail que vous avez confié à quelqu’un,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) trouvés dans les e-mails de réservation et de billets.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Les événements d’un agenda partagé avec vous sont estompés et affichent le prénom de la personne qui l’a partagé. Ils ne donnent jamais lieu à une tâche. Les événements sur une journée entière ou plusieurs jours s’affichent comme tels pour chaque jour concerné. Dans **Agenda**, un voyage apparaît en premier chaque jour. Dans **Semaine** et **Mois**, il s’affiche sous forme de bande sur toute sa durée, par exemple « Voyage à Lisbonne ».

Un projet élaboré à plusieurs correspond à une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion prévue ce jour-là avec la même personne apparaît sur la ligne de cette réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche en cours affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque journée. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. L’affichage remonte jusqu’à une semaine avant la connexion de votre agenda, avec une ligne en haut indiquant le premier jour affiché. Une fois son [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu à la même heure s’affichent côte à côte et restent lisibles. Les autres sont regroupés sous **+N**. Sélectionnez-le pour afficher ce jour dans l’agenda.

## Ouvrir un élément

Sélectionnez une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : date et heure, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et projets associés à la réunion, renvoient vers leur page. Sélectionnez **Ouvrir dans Google Agenda** (ou **Ouvrir dans Outlook**) sous leurs noms pour ouvrir la réunion dans l’agenda correspondant. La consultation ne modifie rien.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ou dans votre Graph.

Un lien de réunion affiche le nom de son service, comme Zoom, Google Meet ou Teams, ou **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture, de taxi ou de stationnement à l’aéroport arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un voyage, quelle que soit votre boîte mail : le train pour l’aéroport, les vols, la voiture, l’hébergement et le trajet de retour. Les réservations sont regroupées si leurs dates se chevauchent ou si l’une commence là où l’autre se termine.

Le voyage s’affiche sous forme d’une bande sur toute sa durée. Ouvrez-le pour voir chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre siège.

Un billet pour un concert, un match, un festival ou une conférence crée un événement, un par événement, avec son lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à celui-ci. Un billet acheté dans votre boîte mail professionnelle est classé dans Travail, sinon dans Personnel. Les billets pour un événement pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine signale ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits** ou l’absence de réservation pour le trajet entre l’aéroport et l’hôtel. Ces lignes sont estompées et marquées **Aucune réservation**. Si aucun hébergement n’est réservé pour un voyage, aucune information sur les nuits ne s’affiche.

- Chaque ligne indique la provenance de la réservation, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si l’e-mail a créé une tâche, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée est retirée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est également retiré.
- Une réservation pour quelqu’un d’autre, comme le vol d’un collègue qui vous a été transféré, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour les autres, comme un e-mail transféré ou un petit site de réservation, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques-uns à la fois, et attend si vous êtes proche de votre limite d’utilisation. Les e-mails de réservation de l’année couverte par l’[historique](history.md) conservé par votre Machine sont lus en arrière-plan une fois l’historique chargé.

## Notes et transcription des réunions

Les détails d’une réunion comprennent deux parties. **Notes** est le résumé : décisions et actions à suivre. **Transcription** restitue mot pour mot ce qui a été dit. Elle est repliée au départ, avec sa durée. **Afficher** permet de l’ouvrir.

Si le contenu ne se charge pas, une nouvelle tentative est lancée automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Les notes et la transcription ont chacune leurs propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** au format Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet de les ouvrir.

Lorsque [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais le contenu que vous avez ajouté. Si les deux sont disponibles, les deux s’affichent.

Les notes peuvent aussi être ajoutées à l’événement de la réunion dans l’agenda, une fois celle-ci commencée, ou être envoyées par e-mail par Zoom ou Gemini. Après la réunion, The Machine crée des tâches à partir de ces notes uniquement si elles indiquent clairement les prochaines étapes. Si les mêmes notes arrivent de deux façons, une seule tâche est créée, avec la réunion comme source : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à suivre avec les personnes responsables, dans la langue de la réunion.

Le message **Rédaction des notes…** s’affiche, et la rédaction continue même si vous fermez la réunion. Une réunion longue peut prendre quelques minutes. Cette opération utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais les notes que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « Ajoute cette transcription à la réunion du conseil d’administration d’aujourd’hui ». Une transcription est ajoutée dans Transcription, un résumé dans Notes. Une réunion avec des notes ou une transcription affiche **Notes** ou **Transcription** dans l’Agenda.

The Machine lit les deux pour trouver les actions à suivre après la réunion. Elles sont classées dans Travail ou Personnel comme la réunion, et ne sont transmises à votre équipe que si la réunion l’est aussi.

Les détails d’une réunion sont accessibles partout où elle apparaît : sur une chronologie, dans une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont uniquement consultables. **Nouvel événement** permet d’en ajouter un (sur téléphone, l’option se trouve sous **+** dans la barre supérieure) : choisissez l’agenda, un titre et un horaire. Sélectionnez un événement sans invités dans cet agenda pour le modifier, ou **Supprimer** pour le supprimer (touchez deux fois).

**Où** suggère des lieux au fur et à mesure de votre saisie : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses fournies par [OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots saisis sont envoyés pour rechercher un lieu. Choisissez une suggestion ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’une prise en charge. Les changements sont indiqués précisément. Ils ne sont effectués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Vous n’avez encore aucune réunion ? Si aucun agenda n’est connecté, **Connecter votre agenda** ouvre Connexions. Vous pouvez y connecter [Google Agenda](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Chevauchements avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche concernant l’événement le plus récent. Elle peut rédiger un court message pour le déplacer ou proposer de le refuser. Rien n’est envoyé sans votre approbation.

Les événements sur une journée entière, marqués comme disponibles ou provisoires ne sont jamais pris en compte, et chaque chevauchement n’est signalé qu’une fois. Une tâche Travail indique seulement qu’il y a un conflit, pour que votre équipe ne voie jamais l’événement personnel. Vous seul voyez avec quel événement il entre en conflit.

## Préparez vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer la réunion**. Il s’agit d’un bref résumé :

- **Qui :** qui sont ces personnes, d’après votre Graph, avec des informations sur leur parcours lorsqu’elles sont disponibles.
- **Organisation :** les activités de leur entreprise qui comptent pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les offres faites, ainsi que leur état d’avancement. Après la réunion, ces messages sont les sources de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** les points à régler ou les éléments à apporter, ainsi que ce qui les intéressera probablement.

La tâche est créée le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle sert uniquement à consulter les informations : sélectionnez **Fait** une fois la lecture terminée. Une promesse ou une question qui nécessite une action fait l’objet de sa propre tâche.

The Machine utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne d’une entreprise, elle effectue également une brève recherche sur le Web à partir de son nom et de celui de l’entreprise, et affiche un lien à côté des informations trouvées. Seuls son nom public, le nom de l’entreprise et son site Web sont transmis à la recherche, jamais vos messages. Les résultats de recherche sont réutilisés pendant 30 jours. Si l’option **Rechercher les contacts pro** est désactivée dans Paramètres, sous Sécurité, aucune recherche n’est effectuée.

En l’absence d’historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou refusées n’en génèrent pas. Si l’horaire d’une réunion change, sa tâche unique est conservée et mise à jour. Une tâche écartée ne réapparaît pas. La tâche d’une réunion annulée est fermée automatiquement.

Si une mise à jour modifie le contenu d’un résumé, les résumés des réunions à venir sont rédigés une seule fois à nouveau, sous leur nouvelle forme. Leur titre, leurs sources et leur place dans votre liste restent les mêmes. Un résumé que vous avez modifié, mis en attente ou fermé reste inchangé, tout comme celui d’une réunion qui commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**, accessible d’une seule pression depuis son chat.
