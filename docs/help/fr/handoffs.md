---
title: Transferts
area: fleet
summary: Transférez une tâche à la Machine d’un coéquipier avec les informations dont il a besoin. Faites le point plus tard ou reprenez-la.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: acb60a24ef374625
---
## Transférer une tâche

1. Dans la tâche, ouvrez **…**, puis **Transférer…**, et choisissez **Un coéquipier**.
2. Choisissez la personne, vérifiez ce qui est inclus (× exclut une partie) et ajoutez une note. Rien provenant d’un compte personnel ou d’une autre entreprise n’est transmis.
3. Envoyez la tâche. Sa Machine la lui présente comme une tâche.

Sa Machine lui envoie une notification sur son téléphone ou dans Telegram. Si aucune de ces options n’est configurée, un e-mail lui est envoyé une seule fois, avec le nom de la personne qui lui a transféré la tâche, son titre et un lien. Consultez [Notifications](notifications.md).

Une conversation Intercom est également transmise. Si sa Machine lit le même espace de travail Intercom, **Lire le message** l’ouvre et sa réponse est renvoyée dans Intercom. Sinon, un lien vers la conversation apparaît dans sa tâche.

En attendant, la tâche indique ce que vous avez demandé et quand (« Demande envoyée à Pat le mar. 3 nov. : … »), uniquement si cela apporte une précision par rapport à son titre. Elle se trouve dans **Revient plus tard**, avec la mention « Avec Pat · en attente » et une date de relance. **Relancer maintenant** prépare un petit rappel pour Pat que vous pouvez envoyer. **Changer l’heure** modifie la date de relance.

Si la Machine de Pat ne peut pas lui envoyer de notification, la tâche indique « Pat ne recevra pas de notification. Prévenez-le. » Prévenez Pat vous-même. Ce message disparaît dès que Pat active les notifications.

La tâche revient en haut uniquement lorsqu’une décision est nécessaire : Pat a répondu, refusé ou terminé la tâche, le transfert a échoué ou une échéance est arrivée. La date de relance dépend de l’échéance : quelques heures pour une tâche à échéance aujourd’hui, le jour ouvré précédent si elle est proche, le lendemain matin si elle est urgente, et sinon dans 3 jours ouvrés.

Lorsqu’elle revient pour une relance, la tâche indique « Toujours chez Pat ». **Relancer maintenant** prépare un petit rappel pour Pat, dans le chat où vous lui avez écrit (Slack, WhatsApp, Telegram ou e-mail), directement depuis la tâche. Rien n’est envoyé tant que vous n’avez pas choisi **Envoyer**. La tâche reste alors en attente de Pat. Si aucun des services que vous avez connectés ne permet de lui écrire, le chat s’ouvre et vous l’indique. **Reprendre** et **Transférer à quelqu’un d’autre** se trouvent sous **…**, puis **Transférer…**.

Le chat de la tâche indique quand elle a été transférée (« Transférée à la Machine de Pat · 14:02 ») et la réponse reçue : acceptée, refusée (avec sa note) ou terminée. En l’absence de réponse, les options **Marquer comme fait**, **Mettre en attente** et **Pas nécessaire** sont proposées. Pour lui envoyer un rappel ou reprendre la tâche, dites-le dans le chat.

Si le transfert n’a pas été envoyé, la tâche et son chat l’indiquent, avec l’option **Réessayer**.

## La transférer à quelqu’un d’autre

Tant qu’un coéquipier s’en occupe, la tâche l’indique sur une ligne (« Avec Pat · en attente »). **Reprendre** et **Transférer à quelqu’un d’autre** se trouvent sous **…**, puis **Transférer…**. **Reprendre** vous rend la tâche : la Machine de Pat en est informée et sa réponse ne la fera plus avancer.

**Transférer à quelqu’un d’autre** ouvre le formulaire de transfert. Vous pouvez aussi le dire dans le chat de la tâche (« cette tâche devrait être confiée à Kim »). La tâche indique alors « Toujours chez Pat jusqu’à ce que vous la transfériez à Kim », avec l’option **Vérifier le transfert à** Kim.

Chaque tâche ne peut être transférée qu’une seule fois à chaque coéquipier : tant que Pat s’en occupe, choisir Pat à nouveau dans le formulaire de transfert permet de faire le point. **Faire le point** prépare le même rappel, avec une ligne de votre part si vous en ajoutez une.

L’option **Reprendre** à Pat est activée par défaut. Désactivez-la pour que les deux personnes s’en occupent. Rien n’est envoyé tant que vous n’avez pas choisi **Transférer**. La Machine de Pat en est informée et sa copie de la tâche est retirée.

## S’ils refusent

Ils peuvent expliquer pourquoi : la tâche ne leur revient pas, elle est déjà terminée ou ils n’ont pas le temps cette semaine. Choisissez ensuite **Le faire moi-même**, **Transférer à quelqu’un d’autre** ou **Marquer comme fait**. La même chose s’applique s’ils ne répondent pas à temps. **Le faire moi-même** vous rend la tâche, qui réapparaît dans Pour vous.

## Une personne en dehors du Network

Choisissez **Par e-mail** : votre Machine prépare un e-mail à envoyer. Au fil de votre saisie, elle vous suggère d’abord les membres de votre Fleet, puis les personnes de votre entreprise. Ajoutez une page de tâche pour qu’ils puissent répondre en un seul geste : consultez [Pages de tâche](task-pages.md).

Cette option est disponible uniquement pour les tâches Work. Cochez les éléments à inclure : quelques lignes sur la tâche, son brouillon, des liens et des fichiers. Le contenu Personnel et Vous uniquement reste exclu. **Préparer l’e-mail** ajoute l’e-mail à la tâche. Lisez-le, puis envoyez-le depuis votre propre boîte mail. Aucun suivi n’est effectué.

Une tâche provenant d’Intercom ou de Slack n’a pas de boîte mail associée. L’e-mail est donc envoyé depuis votre boîte mail Work.

La tâche suit ensuite la promesse jusqu’à ce que la personne réponde qu’elle l’a terminée ou que vous la marquiez comme faite. L’e-mail se termine par « Confiez cette tâche à votre propre Machine » : si la personne s’inscrit avec ce lien, elle peut rejoindre votre Fleet et la tâche est transférée à sa Machine. Désactivez cette ligne dans **Paramètres**, sous Fleet.
