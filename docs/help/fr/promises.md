---
title: Promesses
area: cards
summary: Ce que vous avez dit que vous feriez et ce que les autres vous ont promis. Le suivi est automatique.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 22b81ed3f7c4801f
---
Gardez une trace de ce que vous avez promis et de ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Sur la page des tâches, sous **Promesses** :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Promis à vous**.

Chaque promesse a un menu **⋯** :

- **Faire** sur les vôtres : elles deviennent immédiatement des tâches, et votre Machine les prépare. **Relancer** sur les leurs : votre Machine prépare un court message de relance dans le fil où la promesse a été faite, sans vous faire quitter la liste. Une brève note indique que le message est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « une tâche maintenant ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, celle-ci s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue, votre Machine arrête donc de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche autour de sa date (la vôtre la veille au matin, pour vous laisser une journée pour vous en occuper ; la leur le lendemain matin, si elle est toujours ouverte) et apparaît à la date correspondante dans le [Calendrier](calendar.md). Une promesse devenue une tâche y renvoie, et **Marquer comme fait** ou **N’aura pas lieu** clôt aussi cette tâche. Quand votre Machine voit que la promesse est tenue, les deux sont clôturées et une ligne l’indique.

Si la promesse a déjà été tenue, par exemple grâce à une réponse que vous avez envoyée ou à une réunion qui a réglé la question, elle se clôt automatiquement, sans créer de tâche.

Si une nouvelle date est communiquée plus tard, par exemple « plutôt la semaine prochaine », la même promesse est déplacée, ainsi que sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit une **date de relance** : trois jours après que vous l’avez faite, une semaine après que l’autre personne l’a faite. Si elle est toujours ouverte à ce moment-là, elle devient une tâche.

Les promesses venant de Slack affichent le nom de la personne.

Une promesse reçue par e-mail d’une personne à qui vous n’avez jamais écrit est également enregistrée, avec la mention **expéditeur non vérifié** : elle repose uniquement sur sa parole. La tâche commence par « Non vérifié : vous ne lui avez jamais écrit. »

## Remboursements

Quand un commerçant, une compagnie aérienne, un propriétaire ou un assureur vous promet de vous rembourser, par exemple pour une commande annulée ou un sinistre accepté, votre Machine enregistre le montant, la personne ou l’entreprise qui paie et la date à laquelle le remboursement devrait arriver. La promesse apparaît sous **Promis à vous**. Seulement si le message précise clairement ces trois éléments.

Si le remboursement arrive avant cette date, par exemple avec un e-mail indiquant que le remboursement a été traité, une notification du service de paiement ou une notification de l’application bancaire sur votre téléphone, la promesse se clôt automatiquement, sans créer de tâche.

Le remboursement n’est pas arrivé à cette date ? Une tâche discrète apparaît : « Réclamer le remboursement de 42 € auprès de … », avec un court e-mail à lui envoyer qui mentionne le numéro de commande ou de dossier. Rien n’est envoyé tant que vous ne l’envoyez pas. Si le remboursement arrive finalement, la tâche se clôt automatiquement. **Annuler** la réactive pendant un jour.

Le [récapitulatif hebdomadaire](weekly-recap.md) compte les promesses tenues et celles encore ouvertes. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
