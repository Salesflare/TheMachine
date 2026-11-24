---
title: Envoyer plus tard
area: cards
summary: Validez un message maintenant et choisissez quand l’envoyer. Si la personne vous écrit d’abord, le message attend à nouveau votre validation.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
translated: 29860e4848acce2e
---
## Planifier l’envoi d’un message

Dans la fenêtre où vous consultez un message, cliquez sur **Envoyer plus tard** à côté de **Envoyer maintenant**. Choisissez **Dans 2 heures**, **Demain**, **lundi** ou **Choisir une date**, puis **Enregistrer l’heure**. Le message sera envoyé exactement comme vous l’avez vu, à l’heure prévue dans votre fuseau horaire.

Cette option fonctionne pour les e-mails, Slack, WhatsApp, Telegram, Signal, Teams et Intercom. Elle ne fonctionne pas pour LinkedIn et X, car votre Machine ne peut pas vérifier si un nouveau message est arrivé juste avant l’envoi, ni pour une réponse dans un document.

L’option est aussi disponible dans **Nouvel e-mail**. Si vous consultez plusieurs messages à la fois, ils seront tous envoyés à l’heure choisie.

## Pendant l’attente

La tâche apparaît dans **Revient plus tard** et à la date prévue dans l’[Agenda](calendar.md), avec le message et son heure d’envoi : « Envoi jeu. 26 nov. à 09:30 ». **Envoyer maintenant** l’envoie immédiatement, **Changer l’heure** permet de choisir une autre heure et **Annuler** le transforme à nouveau en brouillon. Le chat affiche la même information.

Si vous modifiez le brouillon, terminez la tâche, l’écartez ou la réactivez, le message ne sera pas envoyé. Vous devrez le valider à nouveau.

## Si la personne vous écrit d’abord

Si la personne vous écrit avant l’envoi, votre Machine n’envoie pas le message. La tâche réapparaît avec son message, par exemple « Non envoyé : Sam Lee vous a écrit d’abord. », et vous recevez la notification habituelle d’une tâche en attente. Pour un e-mail, cela vaut pour toutes les adresses que votre Machine connaît pour cette personne, dans toutes les boîtes mail que vous avez connectées. La réponse d’une autre personne dans la conversation compte aussi.

Une réponse automatique, comme un message d’absence, ne bloque pas l’envoi. Vos propres messages non plus.

Juste avant l’envoi, votre Machine relit la conversation. Si elle n’y arrive pas, la tâche indique « Impossible de vérifier si un nouveau message est arrivé. » et elle réessaie pendant une heure. Ensuite, elle vous demande quoi faire au lieu d’envoyer le message.

Sur WhatsApp, votre Machine vérifie les messages reçus jusque-là par votre propre compte WhatsApp associé.

## Si The Machine est éteinte

Si votre Machine est éteinte, en veille ou déconnectée à l’heure prévue, le message sera envoyé quand elle sera de nouveau disponible, avec un retard pouvant aller jusqu’à une heure. Au-delà, la tâche réapparaît avec le message « Non envoyé : le retard dépasse une heure. » et vous décidez quoi faire.

Quand vous passez sur un autre ordinateur, les messages programmés vous redemandent votre accord. Consultez [Changer d’ordinateur](moving.md).

## Qui peut programmer un envoi

Vous seul pouvez le faire, depuis le tableau de bord ou l’application. Votre Machine, son chat, une IA que vous avez connectée et les autres Machines ne peuvent pas programmer l’envoi d’un message. L’[Activité](activity.md) indique quand un message a été programmé, modifié, annulé, envoyé ou non envoyé.
