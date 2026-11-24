---
title: Transferts
area: fleet
summary: Partagez une tâche avec un collègue ou transférez-la à sa Machine avec **Transférer…**. Faites le point plus tard ou reprenez-la.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: d9b21c04fb0d34a6
---
## Transférer une tâche

1. Dans la tâche, ouvrez **…**, puis **Transférer…**, et choisissez **Un coéquipier**.
2. Choisissez la personne, vérifiez ce qui l’accompagne (× exclut un élément), puis ajoutez une note. Rien provenant d’un compte Personnel ou d’une autre entreprise ne l’accompagne.
3. Envoyez la tâche. Sa Machine la lui affiche comme une tâche.

Sa Machine l’avertit sur son téléphone ou dans Telegram. Si aucune de ces options n’est configurée, elle lui envoie un seul e-mail avec le nom de la personne qui a transféré la tâche, son titre et un lien. Consultez [Notifications](notifications.md).

Une conversation Intercom l’accompagne aussi. Si sa Machine lit le même espace de travail Intercom, **Lire le message** l’ouvre et sa réponse est renvoyée dans Intercom. Sinon, un lien vers la conversation apparaît dans sa tâche.

Pendant l’attente, la tâche indique ce que vous avez demandé et quand (« Demande à Pat le mar. 3 nov. : … »), uniquement si cela apporte une précision par rapport à son titre. Elle apparaît sous **Revient plus tard**, avec la mention « Avec Pat · en attente » et une date de relance. **Relancer maintenant** prépare une courte relance pour Pat, que vous pourrez envoyer. **Changer l’heure** modifie la date de relance.

Si la Machine de Pat ne peut pas l’avertir, la tâche affiche « Pat ne recevra pas de notification. Prévenez Pat. » Prévenez Pat vous-même. Ce message disparaît dès que Pat active les notifications.

La tâche ne revient en haut de la liste que lorsqu’il y a quelque chose à décider : Pat a répondu, a refusé ou a terminé la tâche, le transfert a échoué ou une échéance est arrivée. La date de relance dépend de l’échéance : quelques heures pour aujourd’hui, le jour ouvré précédent si elle approche, le lendemain matin si elle est urgente, sinon dans 3 jours ouvrés.

Quand la tâche revient pour une relance, elle indique « Toujours chez Pat ». **Relancer maintenant** prépare une courte relance à envoyer à Pat, dans le service où vous avez fait la demande (Slack, WhatsApp, Telegram ou e-mail), depuis la tâche. Rien n’est envoyé avant que vous choisissiez **Envoyer**. La tâche attend ensuite à nouveau la réponse de Pat. Si aucun des services connectés ne permet de lui envoyer un message, le chat s’ouvre et vous l’indique. **Reprendre** et **Transférer à quelqu’un d’autre** se trouvent sous **…**, puis **Transférer…**.

Le chat de la tâche indique quand elle a été transférée (« Transférée à la Machine de Pat · 14:02 ») et la réponse reçue : acceptée, refusée (avec sa note) ou terminée. Si Pat n’a pas encore répondu, les options **Marquer comme fait**, **Mettre en attente** et **Pas nécessaire** s’affichent. Pour relancer Pat ou reprendre la tâche, dites-le dans le chat.

Si le transfert n’a pas été envoyé, la tâche et son chat l’indiquent, avec l’option **Réessayer**.

## Ce que voit la personne

Uniquement cette tâche : votre demande, votre note, son échéance et son contact, ainsi que des copies des messages qui l’accompagnent (trois au maximum, sans pièces jointes). Pas votre boîte mail ni vos autres tâches. La personne choisit **Accepter** ou **Refuser**.

Une fois la tâche acceptée, elle lui appartient. La vôtre est terminée ou attend le résultat si elle comporte un **Terminé quand**. Vous ne travaillez pas tous les deux sur la même tâche. Pour demander l’avis de quelqu’un sans lui transférer la tâche, utilisez [Demander une relecture](ask-to-review.md).

## La transférer à quelqu’un d’autre

Tant qu’un collègue a la tâche, une ligne l’indique (« Avec Pat · en attente »). Les options **Reprendre** et **Transférer à quelqu’un d’autre** se trouvent sous **…**, puis **Transférer…**. **Reprendre** vous rend la tâche : la Machine de Pat en est informée et sa réponse ne la modifie plus.

**Transférer à quelqu’un d’autre** ouvre le formulaire de transfert. Vous pouvez aussi le demander dans le chat de la tâche (« cette tâche devrait aller à Kim »). La tâche indique alors « Toujours chez Pat jusqu’à ce que vous la transfériez à Kim », avec **Vérifier le transfert à** Kim.

Une tâche n’est transférée qu’une fois à chaque collègue. Tant que Pat l’a, choisir Pat à nouveau dans le formulaire de transfert permet de faire le point. **Faire le point** prépare la même relance, avec une phrase de votre part si vous en ajoutez une.

L’option **Reprendre à** Pat est activée par défaut. Désactivez-la pour que vous puissiez tous les deux avoir la tâche. Rien n’est envoyé avant que vous choisissiez **Transférer**. La Machine de Pat en est informée et sa copie de la tâche disparaît.

## En cas de refus

La personne peut indiquer pourquoi : la tâche ne lui revient pas, elle est déjà terminée ou elle n’a pas le temps cette semaine. Elle peut ensuite choisir **Le faire moi-même**, **Transférer à quelqu’un d’autre** ou **Marquer comme fait**. C’est aussi ce qui se passe si elle ne répond pas à temps. **Le faire moi-même** vous rend la tâche, dans la section Pour vous.

## Une personne en dehors du Network

Choisissez **Par e-mail** : votre Machine prépare un e-mail que vous pourrez envoyer. Pendant la saisie, elle suggère d’abord les personnes de votre Fleet, puis celles de votre entreprise. Ajoutez une page de tâche pour que la personne puisse répondre d’un seul geste : consultez [Pages de tâche](task-pages.md).

Réservé aux tâches Travail. Cochez les éléments à inclure : quelques lignes sur la tâche, son brouillon, des liens et des fichiers. Le contenu Personnel et Vous uniquement reste exclu. **Préparer l’e-mail** ajoute l’e-mail à la tâche : lisez-le, puis envoyez-le depuis votre propre boîte mail. Aucun suivi n’est effectué.

Une tâche provenant d’Intercom ou de Slack n’a pas de boîte mail propre. Son e-mail est donc envoyé depuis votre boîte mail Travail.

La tâche suit alors la promesse jusqu’à ce que la personne réponde que c’est fait ou que vous marquiez la tâche comme faite. L’e-mail se termine par « Prenez cette tâche en charge dans votre propre Machine ». Si la personne s’inscrit depuis ce lien, elle peut rejoindre votre Fleet et la tâche passe dans sa Machine. Désactivez cette ligne dans **Paramètres**, sous Fleet.
