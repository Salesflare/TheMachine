---
title: Envoyer plus tard
area: cards
summary: Appuyez sur **Envoyer plus tard**, à côté de **Envoyer maintenant**, pour programmer l’envoi d’un e-mail ou d’un message. Vous l’approuvez maintenant et choisissez quand l’envoyer. Si la personne vous écrit d’abord, la tâche revient vers vous.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, schedule an email, send at a time, delay, tomorrow morning, unsend, take back
translated: 6fa6af155c337981
---
## Programmer un message

Dans la fenêtre où vous vérifiez un message, appuyez sur **Envoyer plus tard**, à côté de **Envoyer maintenant**. Choisissez **Dans 2 heures**, **Demain**, **lundi** ou **Choisir une date**, puis **Enregistrer l’heure**. Le message sera envoyé exactement comme vous l’avez vu, à l’heure choisie dans votre fuseau horaire.

Cette option fonctionne pour les e-mails, Slack, WhatsApp, Telegram, Signal, Teams et Intercom. Elle ne fonctionne pas pour LinkedIn ni X, car votre Machine ne peut pas vérifier si vous avez reçu un nouveau message juste avant l’envoi, ni pour les réponses dans un document.

L’option est aussi disponible dans **Nouvel e-mail**. Si vous vérifiez plusieurs messages à la fois, ils seront tous envoyés à l’heure choisie.

## Pendant l’attente

La tâche apparaît sous **Revient plus tard** et à la date prévue dans [Agenda](calendar.md), avec le message et son heure d’envoi : « Envoi jeu. 26 nov., 9 h 30 ». **Envoyer maintenant** envoie le message tout de suite, **Changer l’heure** permet d’en choisir une autre, et **Annuler** le transforme de nouveau en brouillon. Le chat affiche la même chose.

Si vous modifiez le brouillon, terminez ou écartez la tâche, ou la réactivez, le message ne sera pas envoyé : vous devrez l’approuver à nouveau.

## Si la personne vous écrit d’abord

Si la personne vous écrit avant l’envoi, votre Machine n’envoie pas le message. La tâche revient avec son message, par exemple « Non envoyé : Sam Lee vous a écrit d’abord. », et vous recevez la notification habituelle d’une tâche mise en attente. Pour un e-mail, cela concerne toutes les adresses que votre Machine connaît pour cette personne, dans toutes les boîtes e-mail connectées. Une autre personne qui répond dans la conversation compte aussi.

Une réponse automatique, comme un message d’absence, ne bloque pas l’envoi. Vos propres messages non plus.

Juste avant l’envoi, votre Machine vérifie de nouveau la conversation. Si elle n’y arrive pas, la tâche indique « Impossible de vérifier si un nouveau message a été reçu. » et elle réessaie pendant une heure. Ensuite, elle vous demande quoi faire au lieu d’envoyer le message.

Sur WhatsApp, elle vérifie les messages reçus jusqu’ici par le compte WhatsApp que vous avez lié.

## Si The Machine est éteinte

Si votre Machine est éteinte, en veille ou déconnectée à l’heure prévue, le message sera envoyé lorsqu’elle sera de nouveau disponible, avec un retard maximal d’une heure. Au-delà, la tâche revient avec le message « Non envoyé : l’envoi a eu plus d’une heure de retard. » et vous décidez quoi faire.

Si vous passez à un autre ordinateur, les messages programmés vous demanderont à nouveau votre approbation sur celui-ci. Consultez l’article [Changer d’ordinateur](moving.md).

## Qui peut programmer un envoi

Vous seule pouvez le faire, depuis le tableau de bord ou l’application. Votre Machine, son chat, une IA que vous avez connectée et les autres Machines ne peuvent pas programmer de message. [Activité](activity.md) indique quand un message a été programmé, modifié, annulé, envoyé ou non envoyé.
