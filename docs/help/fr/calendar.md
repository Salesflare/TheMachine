---
title: Agenda
area: calendar
summary: La semaine à venir au même endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9f38e3718f3e8639
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches à échéance ce jour-là et les tâches en attente le jour où elles reviennent,
- les suivis du travail que vous avez délégué,
- les promesses associées à une date,
- les [voyages et événements](calendar.md#trips-and-events) issus des réservations et billets reçus par e-mail.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda qu’une personne a partagé avec vous affiche ses événements en grisé, avec son prénom. Ces événements ne génèrent jamais de tâche. Les événements sur toute la journée ou sur plusieurs jours s’affichent comme événements sur toute la journée, pour chaque jour concerné. Dans l’Agenda, un voyage apparaît en premier chaque jour. Dans les vues Semaine et Mois, il forme une seule bande sur les jours concernés, par exemple « Voyage à Lisbonne ».

Un projet commun est présenté comme une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion prévue ce jour-là avec cette même personne apparaît sur la ligne de la réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche ouverte affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son traitement a conclu qu’elle était terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque journée. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. La vue remonte jusqu’à la semaine précédant la connexion de votre agenda. Une ligne en haut indique à partir de quel jour. Une fois votre [historique](history.md) chargé, elle remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, elle affiche trois jours.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez-en un pour afficher la liste du jour.

**Aujourd’hui**, ‹ et › en haut de la page permettent de parcourir les semaines ou les mois. La vue sélectionnée est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte, tout en restant lisibles. Les autres sont regroupés sous **+N**. Touchez-le pour ouvrir cette journée dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : date et heure, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et projets associés à la réunion, sont des liens vers leur page. **Ouvrir dans Google Agenda** (ou **Ouvrir dans Outlook**) sous ces liens permet de l’ouvrir dans l’application correspondante. Consulter ces informations ne les modifie pas.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Le lien d’une réunion affiche le nom du service correspondant, comme Zoom, Google Meet ou Teams, ou **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand vous recevez par e-mail une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking à l’aéroport, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un seul voyage, quelle que soit la boîte mail concernée : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet du retour. Les réservations sont regroupées si leurs dates se chevauchent ou si l’une commence là où l’autre se termine.

Le voyage apparaît sous la forme d’une seule bande sur les jours concernés. Ouvrez-le pour consulter chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre place.

Les billets pour un concert, un match, un festival ou une conférence créent un événement par activité, avec le lieu, le code de réservation, la place et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est marqué Travail. Sinon, il est marqué Personnel. Les billets pour une activité qui a lieu pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et votre hôtel. Ces lignes sont grisées et portent la mention **Aucune réservation**. Un voyage sans aucun hébergement n’affiche aucune information sur les nuits.

- Chaque ligne indique l’origine de la réservation, par exemple **Depuis Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche a été créée à partir de l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** permet de l’afficher.
- Une réservation modifiée met à jour la ligne correspondante. Une réservation annulée est supprimée. Si toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.
- Une réservation au nom d’une autre personne, comme le vol d’un collègue qui vous a transféré l’e-mail, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour celles qui n’en contiennent pas, comme un e-mail transféré ou une réservation faite sur un petit site, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques-uns à la fois, et attend si vous êtes près de votre limite d’utilisation. Une fois l’[historique](history.md) chargé, les e-mails de réservation de l’année qu’il couvre sont aussi lus en arrière-plan.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à mener. **Transcription** reprend mot pour mot ce qui a été dit. Elle est d’abord repliée et indique sa durée. **Afficher** permet de l’ouvrir.

Si elles ne se chargent pas, l’application réessaie automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Les notes et la transcription ont chacune leurs commandes **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu de l’une reste dans cette partie. Pour une réunion que vous pouvez modifier, **Notes** sous son formulaire permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes apparaissent dans Notes et sa transcription dans Transcript, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais ce que vous avez ajouté. Si les deux sont présentes, les deux s’affichent.

Les notes peuvent aussi être ajoutées à l’événement de la réunion dans l’agenda, après son début, ou envoyées par e-mail depuis Zoom ou Gemini. Une fois la réunion terminée, The Machine n’en crée des tâches que pour les prochaines étapes clairement définies. Si les mêmes notes arrivent de deux façons, elles ne créent qu’une tâche, dont la réunion est la source : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine les rédige à partir de la transcription : un résumé court, les décisions et les actions à mener, avec les personnes responsables, dans la langue de la réunion.

Le statut **Rédaction des notes…** s’affiche. La rédaction continue même si vous fermez la réunion. Les réunions longues nécessitent quelques minutes et utilisent votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « ajoute cette transcription aux notes de la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcript et un résumé dans Notes. Dans l’Agenda, une réunion avec des notes ou une transcription porte la mention **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les tâches de suivi de la réunion. Elles sont marquées Travail ou Personnel comme la réunion et ne sont partagées avec votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails où que vous la trouviez : dans une chronologie, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas de page, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre agenda Google personnel depuis cette page. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un (sur téléphone, cette option se trouve sous **+** dans la barre supérieure) : choisissez l’agenda, le titre et l’heure. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

**Lieu** suggère des endroits à mesure que vous saisissez du texte : ceux que vous avez déjà utilisés et vos organisations d’abord, puis des adresses fournies par [OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour la recherche. Sélectionnez un lieu ou gardez le texte saisi.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les invités sont listés au-dessus du bouton, qui indique leur nombre : **Ajouter et inviter 2 personnes**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un lieu de prise en charge. Les changements sont détaillés. Ils ne sont appliqués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Pas encore de réunion ? Si vous n’avez pas d’agenda connecté, **Connecter votre agenda** ouvre Connexions. Vous pouvez y connecter [Google Agenda](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Quand une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche concernant l’événement le plus récent. Elle peut rédiger un court message pour proposer de le déplacer, ou vous proposer de le décliner. Rien n’est envoyé tant que vous ne l’avez pas approuvé.

Les événements sur toute la journée, libres ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Une tâche Travail indique seulement qu’il y a un conflit, afin que votre équipe ne voie jamais l’événement personnel. Vous seul pouvez voir avec quel événement il entre en conflit.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref dossier :

- **Qui :** leur identité, d’après votre Graph, avec des informations sur leur parcours si elles sont connues.
- **Organisation :** les activités de leur entreprise qui comptent pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les propositions faites, ainsi que la suite donnée. Après la réunion, ces messages deviennent les sources de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire, d’après les promesses présentes sur votre Machine.
- **Questions en suspens :** les questions qui restent sans réponse.
- **Décisions ou éléments à apporter :** ce qui reste à décider ou à apporter, et ce qui les intéressera probablement.

La tâche arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle sert uniquement à être consultée. Sélectionnez **Fait** une fois que vous l’avez lue. Toute promesse ou question qui nécessite une action a sa propre tâche.

The Machine utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne d’une entreprise, elle effectue aussi une brève recherche sur le Web à partir du nom de cette personne et de son entreprise, et affiche un lien à côté des résultats. Seuls son nom public, le nom de l’entreprise et son site Web sont envoyés pour la recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours. Si **Rechercher les contacts pro** est désactivé dans Paramètres, section Sécurité, aucune recherche n’est effectuée.

Sans historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou déclinées ne donnent pas lieu à une tâche. Si l’heure d’une réunion change, sa tâche unique est conservée et mise à jour. Une tâche écartée ne réapparaît pas. Celle d’une réunion annulée se ferme automatiquement.

Si une mise à jour modifie le contenu d’un dossier, les dossiers des réunions à venir sont réécrits une fois pour refléter les nouveaux éléments. Leur titre, leurs sources et leur position dans votre liste restent les mêmes. Un dossier que vous avez modifié, mis en attente ou fermé ne change pas. Il en va de même pour celui d’une réunion qui commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**, accessible d’un seul toucher depuis le chat.
