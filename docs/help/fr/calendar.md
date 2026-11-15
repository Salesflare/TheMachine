---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches arrivant à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 9da7909bce253806
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions de vos agendas connectés,
- les tâches arrivant à échéance ce jour-là et les tâches en attente le jour où elles réapparaissent,
- les suivis du travail que vous avez délégué,
- les promesses avec une date.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ces événements ne donnent jamais lieu à une tâche. Les événements sur une journée entière ou plusieurs jours s’affichent comme des événements sur une journée entière, pour chaque jour concerné.

Un plan établi ensemble compte comme une seule promesse, indiquée par « Avec » et son nom. Une promesse concernant une réunion ce jour-là avec la même personne apparaît sur la ligne de cette réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche en cours affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. L’affichage remonte jusqu’à la semaine précédant la connexion de votre agenda, et une ligne en haut indique à partir de quel jour. Une fois l’[historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent, et un toucher affiche la liste du jour.

**Aujourd’hui**, ‹ et › en haut permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte, tout en restant lisibles. Les autres apparaissent sous la forme **+N**. Sélectionnez-les pour afficher le jour dans l’agenda.

## Ouvrir un élément

Sélectionnez une ligne pour ouvrir le chat de la tâche, la promesse ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : quand, où et qui. Les personnes connues de votre Graph, ainsi que les organisations et projets associés à la réunion, sont des liens vers leur page. **Ouvrir dans Google Calendar** ou **Ouvrir dans Outlook**, sous ces liens, permet d’ouvrir la réunion dans le calendrier correspondant. La consultation ne modifie rien.

Une salle de réunion réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Un lien de réunion s’affiche avec le nom de son service, comme Zoom, Google Meet ou Teams, ou sous la forme **Appel vidéo**. Ouvrez la réunion pour y participer.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à mener. **Transcription** reprend mot pour mot ce qui a été dit. Elle est repliée au départ, avec sa durée. **Afficher** permet de l’ouvrir.

Si elles ne se chargent pas, The Machine réessaie automatiquement pendant environ une demi-minute. Ensuite, sélectionnez **Réessayer**.

Chacune propose ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet de les ouvrir.

Si [Zoom](zoom.md) ou [Google Meet](google-meet.md) est connecté, les notes du service s’affichent dans Notes et sa transcription dans Transcription, avec l’indication **De Zoom** ou **De Google Meet**. Elles ne remplacent jamais ce que vous avez ajouté. Si les deux sont présentes, elles s’affichent toutes les deux.

Les notes peuvent aussi être ajoutées à l’événement de réunion dans l’agenda, après le début de la réunion, ou envoyées par e-mail par Zoom ou Gemini. Après la réunion, The Machine en tire des tâches uniquement si elles décrivent clairement les prochaines étapes. Si les mêmes notes arrivent par deux moyens, elles ne créent qu’une seule tâche, dont la réunion est la source : « Source : notes de la réunion ».

Une réunion avec une transcription, mais sans notes, propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à mener avec les personnes chargées de les réaliser, dans la langue de la réunion.

L’indication **Rédaction des notes…** s’affiche et la rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela prend quelques minutes et utilise votre propre modèle. Les notes indiquent **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « Ajoute cette transcription au compte rendu de la réunion d’aujourd’hui ». Une transcription est ajoutée dans Transcription, un résumé dans Notes. Dans le calendrier, une réunion qui en contient affiche **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les suivis de la réunion. Ils sont classés comme Travail ou Personnel, selon la réunion, et ne sont transmis à votre équipe que si la réunion l’est aussi.

Les détails s’affichent à l’ouverture d’une réunion, où que vous la trouviez : sur une chronologie, dans une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un (sur téléphone, sélectionnez **+** dans la barre du haut) : choisissez l’agenda, un titre et l’heure. Sélectionnez un événement sans invités dans cet agenda pour le modifier, ou **Supprimer** pour l’effacer (touchez deux fois).

**Où** suggère des lieux au fur et à mesure de votre saisie : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses fournies par [OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour la recherche. Choisissez un lieu suggéré ou conservez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou toute adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes qui recevront une invitation sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un ramassage. Elle indique exactement ce qui va changer. Seule l’action **Ajouter**, **Enregistrer** ou **Supprimer** confirme la modification.

Pas encore de réunions ? Sans agenda, **Connecter votre agenda** ouvre Connexions. Vous pouvez connecter [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou l’inverse, The Machine crée une tâche concernant l’événement le plus récent. Elle peut rédiger un bref message pour le déplacer, ou proposer de le refuser. Rien n’est envoyé avant votre approbation.

Les événements sur une journée entière, libres ou provisoires ne sont jamais pris en compte, et chaque conflit ne s’affiche qu’une fois. Une tâche Travail indique seulement qu’il y a un conflit. Votre équipe ne voit donc jamais l’événement personnel. Vous seul voyez avec quel événement il entre en conflit.

## Prêt pour vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref dossier :

- **Qui :** leur identité, d’après votre Graph.
- **Dernier contact :** votre dernier échange avec elles. Après la réunion, ce message devient la source de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui reste sans réponse.
- **À décider ou à apporter :** les points à régler ou les éléments à apporter.

Le dossier est créé le matin d’un jour ouvré : le jour de la réunion si elle a lieu l’après-midi, sinon le jour ouvré précédent. Il utilise uniquement les informations déjà présentes sur votre Machine. Il sert uniquement à la lecture : sélectionnez **Fait** après l’avoir lu. Une promesse ou une question qui nécessite une action donne lieu à sa propre tâche.

Si l’historique ne contient rien d’utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou refusées ne donnent lieu à aucune tâche. Si l’heure d’une réunion change, sa tâche reste unique et est mise à jour. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour accéder à son chat.
