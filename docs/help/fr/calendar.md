---
title: Calendrier
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 93fe9794660b0ab2
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches à échéance ce jour-là et les tâches en attente qui reviennent ce jour-là,
- les points de suivi sur le travail que vous avez confié,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) issus des e-mails de réservation et de billetterie.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda partagé avec vous affiche les événements de son propriétaire en couleur atténuée, avec son prénom. Ces événements ne génèrent jamais de tâche. Les événements sur une journée entière et ceux qui durent plusieurs jours s’affichent comme événements sur toute la journée, pour chaque jour concerné. Dans Agenda, un voyage apparaît en premier chaque jour. Dans Semaine et Mois, il apparaît sous forme d’une seule bande sur les jours concernés, par exemple « Voyage à Lisbonne ».

Un projet convenu ensemble constitue une seule promesse, indiquée par « Avec » et son nom. Une promesse concernant une réunion prévue ce jour-là avec la même personne apparaît sur la ligne de cette réunion.

**En retard** apparaît en premier. Une réunion avec une tâche ouverte affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche les jours les uns à la suite des autres. Faites défiler vers le bas pour voir les jours à venir, ou vers le haut (ou appuyez sur **Afficher les jours précédents**) pour voir les jours passés. L’affichage remonte à la semaine précédant la connexion de votre agenda, avec une ligne en haut qui indique le premier jour affiché. Une fois son [historique](history.md) ajouté, il remonte à environ un an.
- **Semaine** affiche une grille, du lundi au dimanche. Sur un téléphone, elle affiche trois jours.
- **Mois** affiche le mois entier. Sur un ordinateur, jusqu’à trois éléments s’affichent par jour. Sur un téléphone, des points s’affichent, et un appui liste les éléments du jour.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. Le mode d’affichage choisi est mémorisé sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte tout en restant lisibles. Les autres sont indiqués par **+N**. Appuyez dessus pour ouvrir ce jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de sa tâche, la promesse, le voyage ou l’événement, ou la réunion. Une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, affiche ses détails : quand, où et qui. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, sont des liens vers leurs pages. **Ouvrir dans Google Calendar** (ou **Ouvrir dans Outlook**) en dessous permet de l’ouvrir dans le service concerné. La consultation ne modifie rien.

Une salle réservée pour une réunion apparaît sous Où, jamais comme une personne ni dans votre Graph.

Un lien de réunion indique le service utilisé, par exemple Zoom, Google Meet ou Teams, ou s’affiche comme **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage s’affiche sous forme d’une seule bande sur les jours concernés. Ouvrez-le pour consulter le code de réservation, le siège et le billet de chaque réservation, dans l’ordre chronologique.

Les billets pour un concert, un match, un festival ou une conférence créent un événement par événement, avec le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est marqué comme professionnel, sinon comme personnel.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche a été créée à partir de l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** permet de l’afficher.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.

The Machine lit les informations présentes dans les e-mails de confirmation des compagnies aériennes, hôtels, sites de réservation et billetteries, sans recourir à l’IA. Un e-mail qui ne contient pas ces informations ne crée rien. Les e-mails de réservation de l’année couverte par l’[historique](history.md) conservé par votre Machine sont lus en arrière-plan une fois cet historique ajouté.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à mener. **Transcription** reprend mot pour mot les propos échangés. Elle est repliée au départ et indique sa durée. **Afficher** permet de l’ouvrir.

Si elles ne se chargent pas, une nouvelle tentative est lancée automatiquement pendant environ une demi-minute. Ensuite, appuyez sur **Réessayer**.

Chaque partie a ses propres boutons **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (appuyez deux fois). Le contenu de l’une ne modifie pas l’autre. Pour une réunion que vous pouvez modifier, **Notes** sous son formulaire permet de les ouvrir.

Lorsque [Zoom](zoom.md) ou [Google Meet](google-meet.md) est connecté, les notes du service apparaissent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom** ou **De Google Meet**. Elles ne remplacent jamais celles que vous avez ajoutées : si les deux sont présentes, elles s’affichent toutes les deux.

Des notes peuvent aussi être ajoutées à l’événement de calendrier de la réunion après son début, ou être envoyées par e-mail par Zoom ou Gemini. Après la réunion, The Machine en crée des tâches uniquement pour les prochaines étapes clairement définies. Si les mêmes notes arrivent par deux moyens, elles ne créent qu’une tâche, dont la source est la réunion : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à mener avec les personnes qui en sont responsables, dans la langue de la réunion.

Le message **Rédaction des notes…** s’affiche, et la rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela prend quelques minutes et utilise votre propre modèle. Les notes indiquent **Rédigées par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « ajoute cette transcription à la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcript, un résumé dans Notes. Dans le Calendrier, une réunion qui en contient affiche **Notes** ou **Transcription**.

The Machine lit les deux pour repérer les tâches de suivi de la réunion. Elles sont professionnelles ou personnelles comme la réunion, et ne sont envoyées à votre équipe que si la réunion l’est aussi.

Les détails de la réunion s’ouvrent de la même façon partout où vous la trouvez : sur une chronologie, dans une recherche de messages ou comme source d’une tâche. **Invitation d’origine** en bas affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un (sur un téléphone, appuyez sur **+** dans la barre supérieure) : choisissez l’agenda, un titre et l’heure. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (appuyez deux fois).

**Où** suggère des lieux pendant la saisie : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses issues d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour trouver des résultats. Choisissez une suggestion ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option n’est disponible que dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous appuyez sur le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un rendez-vous de retrait. Les changements sont indiqués précisément, et seule votre action **Ajouter**, **Enregistrer** ou **Supprimer** les applique.

Aucune réunion pour le moment ? Si vous n’avez pas d’agenda, **Connecter votre agenda** ouvre Connexions. Vous pouvez connecter [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Chevauchements avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou l’inverse, The Machine crée une tâche concernant l’événement le plus récent. Elle peut rédiger un bref message pour proposer de le déplacer, ou proposer de le décliner. Rien n’est envoyé tant que vous ne l’avez pas approuvé.

Les événements sur une journée entière, les événements indiqués comme libres et ceux à confirmer ne sont jamais pris en compte. Chaque chevauchement n’est signalé qu’une fois. Une tâche professionnelle indique seulement qu’il y a un conflit, afin que votre équipe ne voie jamais l’événement personnel. Vous seul voyez avec quel événement il y a un chevauchement.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer la réunion**. Elle contient un bref aperçu :

- **Qui :** qui sont ces personnes, d’après votre Graph.
- **Dernier contact :** votre dernier échange avec elles. Ce message devient la source de la tâche après la réunion.
- **Promesses en attente :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** ce qu’il faut régler ou apporter.

La tâche arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle utilise uniquement les informations déjà présentes sur votre Machine. Elle sert uniquement à la consultation : appuyez sur **Fait** une fois que vous l’avez lue. Toute promesse ou question qui nécessite une action a sa propre tâche.

Sans historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou déclinées n’en génèrent pas. Si une réunion est déplacée, sa tâche unique est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**, à un appui de son chat.
