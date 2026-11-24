---
title: Promesses
area: cards
summary: Ce que vous avez dit que vous feriez et ce que les autres vous ont promis. Le suivi se fait automatiquement.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 0bc6594bbd8f4c0b
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Dans **Promesses**, sur la page Tâches :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Vous a été promis**.

Chaque promesse a un menu **⋯** :

- **Faire** pour les vôtres : elle devient une tâche, et votre Machine la prépare. **Relancer** pour les leurs : votre Machine rédige une courte relance là où la promesse a été faite, et vous restez sur la liste. Une courte note indique que la relance est en cours, avec **Ouvrir la tâche**, et la promesse affiche « une tâche maintenant ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, celle-ci s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue. Votre Machine cesse alors de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche aux alentours de sa date (les vôtres la veille au matin, pour vous laisser une journée pour la faire ; les leurs le lendemain matin, si elle est toujours ouverte) et apparaît à la date correspondante dans [Agenda](calendar.md). Si elle est déjà devenue une tâche, un lien y mène. **Marquer comme fait** ou **N’aura pas lieu** clôt aussi cette tâche. Quand votre Machine voit que la tâche est terminée, elle clôt les deux et l’indique.

Une réponse qui fait seulement une promesse de travail, comme « Je vous enverrai les fichiers d’ici mardi », ne termine pas la tâche correspondante. La tâche reste ouverte avec cette date, et la promesse y renvoie. L’écran de vérification avant l’envoi vous le signale.

La promesse a déjà été tenue, par exemple dans une réponse que vous avez envoyée ou lors d’une réunion ? Elle se clôt automatiquement, sans créer de tâche.

Quand quelqu’un répond à une promesse qu’il a faite, celle-ci reste ouverte jusqu’à ce que la réponse montre qu’elle a été tenue. Un « Bien sûr » ou une réponse qui n’en réalise qu’une partie ne suffit pas. Si une relance était sur le point d’être envoyée, elle est annulée et la tâche reste ouverte avec la mention « Cette personne a répondu ». Une réponse automatique d’absence ne change rien.

La personne donne ensuite une nouvelle date, par exemple « plutôt la semaine prochaine » ? La même promesse est déplacée, ainsi que sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit un jour de **suivi** : trois jours après que vous l’avez faite, une semaine après que l’autre personne l’a faite. Si elle est toujours ouverte à cette date, elle devient une tâche.

Les promesses venant de Slack affichent le nom de la personne.

Une promesse par e-mail venant d’une personne à qui vous n’avez jamais écrit est également suivie, avec la mention **expéditeur non vérifié** : elle repose uniquement sur sa parole. Sa tâche commence par « Non vérifié : vous ne lui avez jamais écrit. »

## Remboursements

Quand un magasin, une compagnie aérienne, un propriétaire ou un assureur vous promet un remboursement, par exemple pour une commande annulée ou une demande d’indemnisation acceptée, votre Machine note le montant, la personne qui paie et la date à laquelle le remboursement doit arriver. Il apparaît dans **Vous a été promis**. Seulement si le message précise ces trois éléments.

Si le remboursement arrive d’abord, par exemple avec un e-mail indiquant « remboursement traité », une notification d’un service de paiement ou une notification de votre application bancaire sur votre téléphone, la promesse se clôt automatiquement, sans créer de tâche.

Le remboursement n’est pas arrivé à cette date ? Une seule tâche discrète apparaît : « Relancer pour le remboursement de €42 auprès de… », accompagnée d’un court e-mail qui mentionne le numéro de commande ou de dossier. Rien n’est envoyé tant que vous ne l’envoyez pas. Si le remboursement arrive finalement, la tâche se clôt automatiquement. **Annuler** la réactive pendant une journée.

Le [Récap hebdo](weekly-recap.md) compte les promesses tenues et celles qui sont encore ouvertes. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
