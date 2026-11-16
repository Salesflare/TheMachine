---
title: Calendrier
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches arrivant à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 970b39054ae39543
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches arrivant à échéance ce jour-là et les tâches en attente le jour où elles reviennent,
- les suivis concernant le travail que vous avez confié,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) repérés dans les e-mails de réservation et de billets.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ces événements ne génèrent jamais de tâche. Les événements d’une journée entière ou de plusieurs jours s’affichent comme événements d’une journée entière pour chaque jour concerné. Dans **Agenda**, un voyage apparaît en premier pour chacun de ses jours. Dans **Semaine** et **Mois**, il apparaît sous la forme d’une bande qui couvre ces jours, par exemple « Voyage à Lisbonne ».

Un projet élaboré ensemble correspond à une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse concernant une réunion prévue ce jour-là avec cette même personne apparaît sur la ligne de la réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche en cours affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a marquée comme terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. L’affichage remonte jusqu’à la semaine précédant la connexion de votre agenda, et une ligne en haut indique le jour de début. Une fois que l’[historique](history.md) est chargé, l’affichage remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur un téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur un ordinateur, jusqu’à trois éléments s’affichent par jour. Sur un téléphone, des points s’affichent et un toucher affiche la liste du jour.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu à la même heure s’affichent côte à côte, tout en restant lisibles. Les autres apparaissent sous la forme **+N**. Touchez-les pour afficher ce jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, ses détails s’affichent : quand, où et qui. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, sont des liens vers leurs pages. **Ouvrir dans Google Calendar** (ou **Ouvrir dans Outlook**) permet de l’ouvrir dans le service correspondant. Le fait de la consulter ne change rien.

Une salle de réunion réservée pour une réunion s’affiche sous le lieu. Elle n’apparaît jamais comme une personne ni dans votre Graph.

Un lien de réunion s’affiche sous le nom de son service, par exemple Zoom, Google Meet ou Teams, ou sous la forme **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand un e-mail de réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage apparaît sous la forme d’une seule bande qui couvre les jours concernés. Ouvrez-le pour consulter, dans l’ordre chronologique, le code de réservation, le siège et le billet de chaque réservation.

Les billets de concert, de match, de festival ou de conférence créent un événement, un par événement, avec le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est classé comme professionnel, sinon il est personnel.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche a été créée à partir de l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.

Les détails sont lus directement dans les e-mails de confirmation envoyés par les compagnies aériennes, les hôtels, les sites de réservation et les vendeurs de billets, sans IA. Un e-mail qui ne contient pas ces détails ne crée rien. Les e-mails de réservation datant de l’année couverte par l’[historique](history.md) conservé par votre Machine sont lus en arrière-plan une fois cet historique chargé.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux sections. **Notes** contient le résumé : les décisions et les actions à réaliser. **Transcription** reprend les propos mot à mot. Elle est repliée par défaut et indique sa durée. **Afficher** permet de l’ouvrir.

Si elles ne se chargent pas, une nouvelle tentative est lancée automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque section dispose de ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à une section y reste. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais ce que vous avez ajouté : si les deux versions sont disponibles, elles s’affichent toutes les deux.

Des notes peuvent également être ajoutées à l’événement de calendrier de la réunion après son début, ou envoyées par e-mail depuis Zoom ou Gemini. Après la réunion, The Machine ne crée des tâches à partir de ces notes que si elles indiquent clairement les prochaines étapes. Si les mêmes notes arrivent de deux façons, elles ne créent qu’une tâche, dont la source est la réunion : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à réaliser avec les personnes chargées de les mener, dans la langue de la réunion.

Le message **Rédaction des notes…** s’affiche, et la rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela prend quelques minutes et utilise votre propre modèle. Les notes indiquent **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple « ajoute cette transcription à la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcript, un résumé dans Notes. Une réunion qui en contient affiche **Notes** ou **Transcription** dans le Calendrier.

The Machine lit les deux pour trouver les tâches de suivi de la réunion. Elles sont classées comme professionnelles ou personnelles, comme la réunion, et ne sont partagées avec votre équipe que si la réunion l’est aussi.

Les détails d’une réunion s’affichent quel que soit l’endroit où vous l’ouvrez : dans une chronologie, une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre agenda Google personnel ici. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** en ajoute un (sur un téléphone, touchez **+** dans la barre supérieure) : choisissez l’agenda, un titre et une heure. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

**Où** propose des lieux au fil de votre saisie : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses issues d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour rechercher des lieux. Sélectionnez un résultat ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes qui recevront une invitation sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un rendez-vous pour récupérer quelque chose. Le détail des changements s’affiche, et seule votre action **Ajouter**, **Enregistrer** ou **Supprimer** les applique.

Pas encore de réunion ? Si vous n’avez pas d’agenda, **Connecter votre agenda** ouvre les Connexions : connectez [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche au sujet de l’événement le plus récent. Elle peut rédiger un bref message pour le déplacer ou proposer de le refuser. Rien n’est envoyé avant votre approbation.

Les événements d’une journée entière, les événements où votre disponibilité est indiquée comme libre et les événements provisoires ne sont jamais pris en compte. Chaque conflit n’est signalé qu’une fois. Une tâche professionnelle indique seulement qu’il y a un conflit, pour que votre équipe ne voie jamais l’événement personnel. Vous seul voyez avec quel événement il entre en conflit.

## Bien préparer vos réunions

Avant une réunion avec des personnes externes à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref compte rendu :

- **Qui :** qui sont ces personnes, d’après votre Graph.
- **Dernier contact :** votre dernier échange avec elles. Après la réunion, ce message devient la source de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** ce qu’il reste à régler ou à apporter.

La tâche est créée le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle utilise uniquement les informations déjà présentes sur votre Machine. Elle sert uniquement à consulter ces informations : marquez-la **Fait** après l’avoir lue. Toute promesse ou question qu’elle contient et qui nécessite une action fait l’objet de sa propre tâche.

Sans historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles et refusées n’en génèrent pas. Si une réunion est déplacée, sa tâche unique est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée est fermée automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour ouvrir son chat.
