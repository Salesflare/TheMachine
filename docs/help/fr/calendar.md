---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py
order: 1
---
## Ce qu’il affiche

Les 7 prochains jours, avec :

- les réunions des agendas que vous avez connectés,
- les tâches dues ce jour-là, et les tâches en attente le jour où elles reviennent,
- les relances sur le travail que vous avez transféré,
- les promesses avec une date.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda que quelqu’un a partagé avec vous affiche ses événements en grisé, avec son prénom ; ceux-ci ne créent jamais de tâche. Les événements d’une journée entière ou de plusieurs jours s’affichent comme journée entière, sur chaque jour qu’ils couvrent.

Un projet prévu ensemble est une seule promesse, marquée « Avec » et le nom de la personne. Une promesse liée à une réunion du même jour avec la même personne se place sur la ligne de cette réunion.

**En retard** vient en premier. Une réunion avec une tâche ouverte l’affiche : **Préparation prête**, **En préparation** ou **Tâche**.

## Agenda ou semaine

**Agenda** liste chaque jour. Sur un ordinateur, **Semaine** affiche une grille. Votre choix est mémorisé sur cet appareil.

Dans la grille, les événements à la même heure se placent côte à côte tant que chacun reste lisible. Les autres s’affichent en **+N**, qui ouvre ce jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de sa tâche, la promesse, ou la réunion dans son propre agenda. Dans une réunion, une personne que votre Graph connaît, ainsi que les organisations et projets dont parle la réunion, sont des liens vers leur page. Regarder ne change rien.

Une salle de réunion réservée apparaît dans le lieu, jamais comme une personne ni dans votre Graph.

## Notes et transcription de réunion

Les détails d’une réunion ont deux parties. **Notes** est le résumé : décisions et actions. **Transcription** est ce qui a été dit, mot pour mot. Elle est d’abord repliée, avec sa durée ; **Afficher** l’ouvre.

Chacune a son propre **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** pour un fichier Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Ce qui est dans l’une y reste. Sur une réunion que vous pouvez modifier, **Notes** sous son formulaire les ouvre.

Avec [Zoom](zoom.md) connecté, son résumé apparaît dans Notes et sa transcription dans Transcription, marqués **De Zoom**. Zoom ne remplace jamais ce que vous avez ajouté : quand les deux existent, les deux s’affichent.

The Machine peut aussi les ajouter. Demandez-le sur une tâche, par exemple "ajoute cette transcription au conseil d’administration d’aujourd’hui". Une transcription va dans Transcription, un résumé dans Notes. Une réunion qui en a affiche **Notes** ou **Transcription** dans le calendrier.

The Machine lit les deux pour les suites de la réunion. Elles sont Travail ou Personnel comme la réunion, et ne vont à votre équipe que si la réunion y va.

## Ajouter ou modifier un événement

Quand un agenda peut être modifié d’ici, **Nouvel événement** en ajoute un (sur un téléphone, il est sous **+** dans la barre du haut) : choisissez l’agenda, un titre et l’heure. Cliquez sur un événement sans invités de cet agenda pour le modifier, ou pour le **Supprimer** (touchez deux fois).

**Où** propose des lieux pendant que vous tapez : d’abord ceux que vous avez déjà utilisés et vos organisations, puis des adresses d’[OpenStreetMap](https://www.openstreetmap.org) via Photon, une recherche de cartes gratuite. Votre Machine l’interroge avec seulement les mots que vous avez tapés. Choisissez-en un ou gardez votre propre texte.

**Inviter** ajoute des personnes de votre Graph, ou n’importe quelle adresse e-mail. Ce n’est disponible que sur votre propre agenda. Les personnes invitées sont listées au-dessus du bouton, et le bouton indique combien : **Ajouter et inviter 2**. Google envoie les invitations quand vous appuyez, pas avant. Sans invités, personne n’est invité ni ne reçoit de mise à jour.

Une tâche peut aussi proposer un changement, comme un trajet à ajouter. Elle montre exactement ce qui change, et seul votre **Ajouter**, **Enregistrer** ou **Supprimer** le fait.

Pas encore de réunions ? Sans agenda, **Connecter votre agenda** ouvre Connexions : connectez [Google Agenda](google-calendar.md) ou [Outlook Calendar](microsoft.md).
