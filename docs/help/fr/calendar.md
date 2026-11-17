---
title: Calendrier
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: c1941aa6ca09b134
---
## Ce qu’il affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des calendriers que vous avez connectés,
- les tâches qui arrivent à échéance ce jour-là et les tâches en attente qui reviennent ce jour-là,
- les suivis du travail que vous avez délégué,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) repérés dans vos e-mails de réservation et de billetterie.

Une réunion présente dans deux calendriers ne s’affiche qu’une fois. Un calendrier partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ces événements ne génèrent jamais de tâche. Les événements sur toute la journée ou sur plusieurs jours s’affichent comme des événements sur toute la journée, pour chacun des jours concernés. Dans Agenda, un voyage apparaît en premier chaque jour. Dans Semaine et Mois, il s’affiche sous la forme d’une bande sur toute sa durée, par exemple « Voyage à Lisbonne ».

Un projet commun constitue une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion qui a lieu ce jour-là avec la même personne apparaît sur la ligne de cette réunion.

**En retard** apparaît en premier. Une réunion associée à une tâche ouverte l’indique : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. L’affichage remonte jusqu’à une semaine avant la connexion de votre calendrier, avec une ligne en haut qui indique le jour de début. Une fois son [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours sont affichés.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et › en haut vous permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille hebdomadaire, les événements qui ont lieu en même temps s’affichent côte à côte, tout en restant lisibles. Les autres sont regroupés sous **+N**. Sélectionnez cette ligne pour ouvrir le jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, ses détails s’affichent : quand, où et qui. Les personnes que votre Graph connaît, ainsi que les organisations et projets associés à la réunion, sont des liens vers leur page. **Ouvrir dans Google Calendar** (ou **Ouvrir dans Outlook**) sous ces liens ouvre la réunion dans le calendrier correspondant. La consultation n’entraîne aucune modification.

Une salle réservée pour une réunion apparaît sous « Où », jamais comme une personne ni dans votre Graph.

Le lien d’une réunion affiche le nom du service, comme Zoom, Google Meet ou Teams, ou **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking d’aéroport arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un seul voyage, quel que soit le compte de messagerie concerné : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet de retour. Les réservations sont regroupées lorsque leurs dates se chevauchent ou que l’une commence au moment où l’autre se termine.

Le voyage s’affiche sous la forme d’une bande sur toute sa durée. Ouvrez-le pour voir chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre place.

Les billets pour un concert, un match, un festival ou une conférence créent un événement, un par événement, avec son lieu, le code de réservation, la place et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à celui-ci. Un événement réservé depuis votre compte professionnel est classé comme professionnel, sinon comme personnel. Les billets pour un événement pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et votre hôtel. Ces lignes sont en grisé et portent l’étiquette **Aucune réservation**. Si aucun hébergement n’est prévu pour le voyage, rien n’est indiqué concernant les nuits.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si l’e-mail a généré une tâche, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.
- Une réservation pour quelqu’un d’autre, comme le vol d’un collègue qui vous a été transféré, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour les autres, comme un e-mail transféré ou provenant d’un petit site de réservation, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques-uns à la fois, et attend si vous approchez de votre limite d’utilisation. Les e-mails de réservation de l’année incluse dans l’[historique](history.md) conservé par votre Machine sont lus en arrière-plan une fois cet historique chargé.

## Notes et transcription des réunions

Les détails d’une réunion comprennent deux parties. **Notes** est le résumé : décisions et actions à réaliser. **Transcription** reprend mot pour mot ce qui a été dit. Elle est repliée au départ et indique sa durée. **Afficher** permet de l’ouvrir.

Si le chargement échoue, une nouvelle tentative se lance automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque partie dispose de ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, l’option **Notes** sous son formulaire permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes apparaissent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais ce que vous avez ajouté. Si les deux versions sont présentes, elles s’affichent toutes les deux.

Des notes peuvent aussi être ajoutées à l’événement de calendrier de la réunion, après son début, ou envoyées par e-mail depuis Zoom ou Gemini. Après la réunion, The Machine ne crée des tâches à partir de ces notes que si elles contiennent des prochaines étapes claires. Si les mêmes notes arrivent de deux façons, elles ne génèrent qu’une seule tâche, dont la réunion est la source : « Source : notes de » la réunion.

Une réunion avec une transcription, mais sans notes, propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à réaliser, dans la langue de la réunion.

L’indication **Rédaction des notes…** s’affiche, et la rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela peut prendre quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « ajoute cette transcription aux notes de la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcription, un résumé dans Notes. Dans le Calendrier, les réunions qui en contiennent affichent **Notes** ou **Transcription**.

The Machine consulte les deux pour trouver les suivis de la réunion. Ils sont classés comme professionnels ou personnels, comme la réunion, et ne sont transmis à votre équipe que si la réunion l’est aussi.

Les détails d’une réunion sont accessibles partout où vous la trouvez : sur une chronologie, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre calendrier Google ici. Outlook et les autres calendriers sont uniquement consultables. **Nouvel événement** permet d’en ajouter un (sur téléphone, l’option se trouve sous **+** dans la barre supérieure) : choisissez le calendrier, un titre et l’horaire. Cliquez sur un événement sans invités de ce calendrier pour le modifier ou le **Supprimer** (touchez deux fois).

**Où** suggère des lieux à mesure que vous tapez : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses provenant d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour rechercher des lieux. Choisissez une suggestion ou conservez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre calendrier. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple un lieu de prise en charge à ajouter. Les changements sont indiqués précisément. Ils ne sont appliqués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Vous n’avez pas encore de réunions ? Sans calendrier connecté, **Connecter votre agenda** ouvre Connexions. Vous pouvez connecter [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre calendrier](other-calendars.md).

## Conflits avec votre autre calendrier

Lorsqu’une réunion professionnelle chevauche un événement de votre calendrier personnel, ou l’inverse, The Machine crée une tâche à propos de l’événement le plus récent. Elle peut rédiger un court message pour le déplacer ou proposer de le décliner. Rien n’est envoyé avant votre approbation.

Les événements sur toute la journée, libres ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Une tâche professionnelle indique uniquement qu’il y a un conflit, afin que votre équipe ne voie jamais l’événement personnel. Vous seule voyez avec quel événement il entre en conflit.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer la réunion**. Elle contient un bref résumé :

- **Qui :** leur identité, d’après votre Graph.
- **Dernier contact :** votre dernier échange avec ces personnes. Après la réunion, ce message apparaît comme source de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** les points à régler ou les choses à emporter.

La tâche arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle utilise uniquement les informations déjà présentes sur votre Machine. Elle sert uniquement à la consultation. Sélectionnez **Fait** une fois que vous l’avez lue. Les promesses ou les questions qu’elle contient et qui nécessitent une action ont leur propre tâche.

S’il n’y a pas d’historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou déclinées n’en génèrent pas. Si une réunion est déplacée, sa tâche est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée est fermée automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour ouvrir son chat.
