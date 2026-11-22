---
title: Promesses
area: cards
summary: Ce que vous avez promis de faire et ce que les autres vous ont promis. Le suivi est automatique.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: ba0e2190e1b8b791
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Sous **Promesses**, sur la page Tâches :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Vous a été promis**.

Chaque promesse a un menu **⋯** :

- **Faire** pour vos promesses : elle devient immédiatement une tâche, et votre Machine la prépare. **Relancer** pour celles des autres : votre Machine rédige une courte relance là où la promesse a été faite, sans vous faire quitter la liste. Une courte note indique que la relance est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « une tâche est créée ». Rien n’est envoyé avant que vous l’envoyiez. Si une tâche existe déjà, elle s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue. Votre Machine cesse donc de la suivre, sans créer de tâche.

Une promesse en cours devient aussi automatiquement une tâche autour de sa date (la vôtre le matin précédent, pour vous laisser une journée pour vous en occuper ; celle des autres le matin suivant, si elle est toujours en cours), et s’affiche à la date correspondante dans l’[Agenda](calendar.md). Si une tâche existe déjà, la promesse y renvoie. **Marquer comme fait** ou **N’aura pas lieu** clôt aussi cette tâche. Quand votre Machine voit qu’elle est terminée, les deux sont clôturées et une note l’indique.

Une réponse qui promet seulement de faire le travail, comme « Je vous enverrai les fichiers d’ici mardi », ne termine pas la tâche. La tâche reste ouverte avec cette date, et la promesse y renvoie. Un message vous le signale dans l’écran de vérification avant l’envoi.

La promesse a déjà été tenue, par exemple dans une réponse que vous avez envoyée ou une réunion qui l’a réglée ? Elle est clôturée automatiquement, sans créer de tâche.

Quand quelqu’un répond à une promesse qu’il a faite, elle reste ouverte jusqu’à ce que la réponse montre qu’elle a été tenue. Un « D’accord », une réponse automatique ou une partie du travail ne suffit pas. Si une relance était en attente d’envoi, elle est annulée et la tâche reste ouverte avec la mention « La personne a répondu ».

La personne donne une nouvelle date, par exemple « plutôt la semaine prochaine » ? La même promesse est reportée, tout comme sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit un jour de **relance** : trois jours après que vous l’avez faite, une semaine après que l’autre personne l’a faite. Si elle est toujours en cours à cette date, elle devient une tâche.

Les promesses venant de Slack affichent le nom de la personne.

Les promesses reçues par e-mail d’une personne à qui vous n’avez jamais écrit sont aussi suivies, mais marquées **expéditeur non vérifié** : elles reposent uniquement sur sa parole. La tâche commence par « Non vérifié : vous ne lui avez jamais écrit auparavant. »

## Remboursements

Quand un commerçant, une compagnie aérienne, un propriétaire ou un assureur vous promet un remboursement, par exemple pour une commande annulée ou une demande acceptée, votre Machine note le montant, la personne qui paie et la date prévue du versement. Le remboursement apparaît sous **Vous a été promis**. Seulement si le message indique clairement ces trois éléments.

Si l’argent est remboursé avant cette date, par exemple dans un e-mail indiquant que le remboursement a été traité, une notification d’un service de paiement ou une notification de votre application bancaire sur votre téléphone, la promesse est clôturée automatiquement, sans créer de tâche.

Vous n’avez toujours pas reçu l’argent à cette date ? Une tâche discrète apparaît : « Relancer le remboursement de 42 € auprès de … », avec un court e-mail qui précise le numéro de commande ou de dossier. Rien n’est envoyé avant que vous l’envoyiez. Si l’argent arrive finalement, la tâche est clôturée automatiquement. **Annuler** la rétablit pendant une journée.

Le [récap hebdo](weekly-recap.md) compte les promesses tenues et celles qui sont en cours. Sur votre ordinateur, `assistant promises` les affiche dans un terminal.
