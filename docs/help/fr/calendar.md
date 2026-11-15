---
title: Calendrier
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: d85b3eff63ea503d
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches à échéance ce jour-là et les tâches en attente, le jour où elles reviennent,
- les points de suivi sur le travail que vous avez délégué,
- les promesses datées,
- les [notes](notes.md) avec une date, comme un voyage.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda qu’une personne a partagé avec vous affiche ses événements en estompé, avec son prénom ; ils ne créent jamais de tâche. Les événements d’une journée entière ou de plusieurs jours s’affichent comme événements d’une journée entière, pour chaque jour concerné. Dans Agenda, un voyage apparaît en premier chaque jour ; dans Semaine et Mois, une seule barre le couvre, par exemple « Voyage à Lisbonne ».

Un projet commun compte comme une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion du jour avec cette même personne apparaît sur la ligne de la réunion.

**En retard** apparaît en premier. Une réunion associée à une tâche ouverte l’indique : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée (vous avez déjà répondu, ou son exécution a conclu qu’elle l’était) ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** liste chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut (ou sélectionnez **Afficher les jours précédents**) pour voir les jours précédents. L’affichage remonte jusqu’à une semaine avant la connexion de votre agenda, avec une ligne en haut qui indique le jour de début. Une fois votre [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur un téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur un ordinateur, jusqu’à trois éléments s’affichent par jour ; sur un téléphone, des points s’affichent. Touchez un jour pour afficher la liste de ses événements.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu au même moment s’affichent côte à côte et restent lisibles. Les autres sont regroupés sous **+N**. Sélectionnez cette option pour ouvrir ce jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, la note ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : quand, où et qui. Les personnes connues de votre Graph, ainsi que les organisations et projets associés à la réunion, renvoient vers leur page. **Ouvrir dans Google Calendar** (ou **Ouvrir dans Outlook**) sous ces informations permet de l’ouvrir dans le service correspondant. La consultation ne change rien.

Une salle réservée pour une réunion apparaît sous « Où », jamais comme une personne ni dans votre Graph.

Le lien d’une réunion s’affiche sous le nom du service, par exemple Zoom, Google Meet ou Teams, ou sous la forme **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à entreprendre. **Transcription** reprend les propos mot pour mot. Elle est repliée au départ et indique sa durée ; sélectionnez **Afficher** pour l’ouvrir.

Si le chargement échoue, une nouvelle tentative est lancée automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque partie propose ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une ne se retrouve pas dans l’autre. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet de les ouvrir.

Si [Zoom](zoom.md) ou [Google Meet](google-meet.md) est connecté, les notes s’affichent dans Notes et la transcription dans Transcription, avec la mention **De Zoom** ou **De Google Meet**. Elles ne remplacent jamais ce que vous avez ajouté : si les deux existent, les deux s’affichent.

Des notes peuvent aussi être ajoutées à l’événement de la réunion dans l’agenda, après son début, ou envoyées par e-mail par Zoom ou Gemini. Une fois la réunion terminée, The Machine crée des tâches à partir de ces notes uniquement si elles indiquent clairement les prochaines étapes. Si les mêmes notes arrivent par deux moyens, elles ne créent qu’une seule tâche, dont la réunion est la source : « Source : notes de » la réunion.

Pour une réunion avec transcription mais sans notes, l’option **Générer les notes** s’affiche. The Machine les rédige à partir de la transcription : un résumé court, les décisions et les actions à entreprendre, avec le nom de la personne responsable, dans la langue de la réunion.

Le message **Rédaction des notes…** s’affiche et la rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela prend quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « ajoute cette transcription à la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcription, un résumé dans Notes. Dans le Calendrier, les réunions avec ces éléments portent la mention **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les actions à suivre après la réunion. Elles sont classées Travail ou Personnel selon la réunion et ne sont transmises à votre équipe que si la réunion l’est aussi.

Les détails d’une réunion sont accessibles partout où vous la trouvez : sur une chronologie, dans une recherche de messages ou comme source d’une tâche. L’option **Invitation d’origine** en bas de page affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont en lecture seule. L’option **Nouvel événement** permet d’en ajouter un (sur un téléphone, elle se trouve sous **+** dans la barre supérieure) : choisissez l’agenda, un titre et l’heure. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

L’option **Où** propose des lieux au fil de votre saisie : d’abord ceux que vous avez déjà utilisés et vos organisations, puis des adresses d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour la recherche. Choisissez une suggestion ou conservez votre propre texte.

L’option **Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Elle est disponible uniquement dans votre propre agenda. Les personnes qui recevront une invitation sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un retrait. Les changements sont indiqués précisément et ne sont effectués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Vous n’avez encore aucune réunion ? Si vous n’avez pas d’agenda, l’option **Connecter votre agenda** ouvre Connexions : connectez [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Chevauchements avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou l’inverse, The Machine crée une tâche au sujet de l’événement le plus récent. Elle peut rédiger un court message pour le déplacer ou proposer de le refuser. Rien n’est envoyé tant que vous ne l’avez pas approuvé.

Les événements d’une journée entière, les événements marqués comme libres et les événements provisoires ne sont jamais pris en compte. Chaque chevauchement n’est signalé qu’une fois. Une tâche Travail indique seulement qu’il y a un conflit, votre équipe ne voit donc jamais l’événement personnel. Vous seule voyez avec quel événement il chevauche.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref récapitulatif :

- **Qui :** qui sont ces personnes, d’après votre Graph.
- **Dernier contact :** votre dernier échange avec elles. Après la réunion, ce message devient la source de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** ce qu’il faut régler ou apporter.

La tâche est créée le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle utilise uniquement les informations déjà présentes sur votre Machine. C’est une tâche à consulter uniquement : sélectionnez **Fait** après l’avoir lue. Les promesses ou questions qui nécessitent une action ont leur propre tâche.

S’il n’y a pas d’historique utile, aucune tâche n’est créée. Aucune tâche n’est créée pour les réunions récurrentes, internes, personnelles ou refusées. Si l’horaire d’une réunion change, sa tâche unique est conservée et mise à jour. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la une fois pour ouvrir son chat.
