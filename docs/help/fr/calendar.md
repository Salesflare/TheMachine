---
title: Calendrier
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 7187a83e373922b3
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des calendriers que vous avez connectés,
- les tâches dont l’échéance tombe ce jour-là et les tâches en attente, le jour où elles réapparaissent,
- les points de suivi sur le travail que vous avez délégué,
- les promesses avec une date.

Une réunion présente dans deux calendriers ne s’affiche qu’une fois. Les événements d’un calendrier partagé avec vous s’affichent en gris, avec le prénom de la personne qui l’a partagé. Ils ne donnent jamais lieu à une tâche. Les événements sur une journée entière ou plusieurs jours s’affichent comme des événements d’une journée entière, pour chaque jour concerné.

Un plan que vous avez établi ensemble compte comme une seule promesse, marquée « Avec » et son nom. Une promesse liée à une réunion prévue ce jour-là avec cette même personne s’affiche sur la ligne de la réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche en cours affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque journée. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut (ou sélectionnez **Afficher les jours précédents**) pour voir les jours précédents. L’agenda remonte à une semaine avant la connexion de votre calendrier, et une ligne en haut indique à partir de quel jour. Une fois son [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent : touchez-en un pour afficher la liste de cette journée.

**Aujourd’hui**, ‹ et › en haut vous permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu à la même heure s’affichent côte à côte, tout en restant lisibles. Les autres sont regroupés sous la forme **+N**. Sélectionnez-les pour ouvrir cette journée dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, comme celle d’une autre personne ou une réunion avec des invités, ses détails s’affichent : la date et l’heure, le lieu et les participants. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, sont des liens vers leur page. **Ouvrir dans Google Calendar** (ou **Ouvrir dans Outlook**) en dessous permet de l’ouvrir dans le calendrier correspondant. Le fait de la consulter ne change rien.

Une salle de réunion réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Un lien de réunion s’affiche sous le nom du service correspondant, comme Zoom, Google Meet ou Teams, ou sous la forme **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à effectuer. **Transcription** reprend les propos mot pour mot. Elle est d’abord repliée et indique sa durée. Sélectionnez **Afficher** pour la développer.

Si elles ne se chargent pas, une nouvelle tentative se lance automatiquement pendant environ une demi-minute. Ensuite, sélectionnez **Réessayer**.

Les notes et la transcription ont chacune leurs propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu de l’une reste séparé de l’autre. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet de les ouvrir.

Si [Zoom](zoom.md) ou [Google Meet](google-meet.md) est connecté, les notes de la réunion s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom** ou **De Google Meet**. Elles ne remplacent jamais ce que vous avez ajouté : si les deux sont présentes, elles s’affichent toutes les deux.

Des notes peuvent aussi être ajoutées à l’événement de calendrier de la réunion, après son début, ou être envoyées par e-mail par Zoom ou Gemini. Une fois la réunion terminée, The Machine n’en crée des tâches que pour les prochaines étapes clairement définies. Si les mêmes notes arrivent par deux moyens, elles ne créent qu’une seule tâche, dont la réunion est la source : **Notes de** la réunion.

Une réunion avec une transcription et sans notes propose l’option **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à effectuer, en précisant qui s’en charge, dans la langue de la réunion.

Le statut **Rédaction des notes…** s’affiche. La rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela peut prendre quelques minutes et utilise votre propre modèle. Les notes indiquent **Rédigées par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple « ajoute cette transcription au point d’équipe d’aujourd’hui ». La transcription est ajoutée dans Transcription et le résumé dans Notes. Dans le Calendrier, une réunion avec l’un de ces éléments affiche **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les actions de suivi de la réunion. Elles sont classées Travail ou Personnel, comme la réunion, et ne sont transmises à votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails où que vous la trouviez : sur une chronologie, dans une recherche de messages ou comme source d’une tâche. L’option **Invitation d’origine** en bas affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Les événements d’Outlook et des autres calendriers sont en lecture seule. **Nouvel événement** en ajoute un (sur téléphone, l’option se trouve sous **+** dans la barre supérieure) : choisissez le calendrier, un titre et une heure. Cliquez sur un événement sans invités de ce calendrier pour le modifier ou le **Supprimer** (touchez deux fois).

**Où** suggère des lieux au fur et à mesure de la saisie : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses de [OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour effectuer la recherche. Choisissez une suggestion ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option n’est disponible que dans votre propre calendrier. Les personnes qui recevront une invitation sont listées au-dessus du bouton, qui indique leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un lieu de prise en charge. Les changements sont indiqués précisément et ne sont appliqués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Aucune réunion pour le moment ? Si aucun calendrier n’est connecté, **Connecter votre agenda** ouvre Connexions. Connectez [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre calendrier](other-calendars.md).

## Chevauchements avec votre autre calendrier

Lorsqu’une réunion de travail chevauche un événement de votre calendrier personnel, ou inversement, The Machine crée une seule tâche au sujet de l’événement le plus récent. Elle peut rédiger un court message pour le déplacer ou proposer de le décliner. Rien n’est envoyé tant que vous ne l’avez pas approuvé.

Les événements sur une journée entière, les événements indiqués comme libres et ceux indiqués comme provisoires ne sont jamais pris en compte. Chaque chevauchement n’est signalé qu’une fois. Une tâche Travail indique seulement qu’il y a un conflit, de sorte que votre équipe ne voit jamais l’événement personnel. Vous seul voyez l’événement avec lequel il y a un chevauchement.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer la réunion**. Il s’agit d’un bref résumé :

- **Qui :** qui sont ces personnes, d’après votre Graph.
- **Dernier contact :** votre dernier échange avec elles. Après la réunion, ce message est la source de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** ce qu’il faut régler ou apporter.

La tâche est créée le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle utilise uniquement les informations déjà présentes sur votre Machine. Elle sert uniquement à la lecture : sélectionnez **Fait** une fois que vous l’avez lue. Toute promesse ou question qu’elle contient et qui nécessite une action a sa propre tâche.

S’il n’y a pas d’historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou déclinées n’en génèrent pas. Si l’heure d’une réunion change, sa tâche est conservée et mise à jour. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**, accessible d’une seule pression depuis son chat.
