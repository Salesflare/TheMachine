---
title: Promesses
area: cards
summary: Ce que vous avez promis de faire et ce que les autres vous ont promis. Tout est suivi automatiquement.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Dans **Promesses**, sur la page Tâches :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Promis à vous**.

Chaque promesse comporte un menu **⋯** :

- **Faire** pour les vôtres : elles deviennent immédiatement des tâches et votre Machine les prépare. **Relancer** pour les leurs : votre Machine rédige un bref message de relance dans le fil où la promesse a été faite, sans vous faire quitter la liste. Une courte note indique que le message est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « une tâche maintenant ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, cette tâche s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue. Votre Machine arrête alors de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche à la date prévue, la veille au matin pour les vôtres, pour vous laisser une journée pour la réaliser, et le lendemain matin pour celles des autres, si elles sont toujours ouvertes. Elle apparaît à la date prévue dans le [Calendrier](calendar.md). Si elle devient une tâche, un lien mène à celle-ci, et **Marquer comme fait** ou **N’aura pas lieu** clôt également cette tâche. Quand votre Machine constate que la promesse a été tenue, les deux sont clôturées et une ligne l’indique.

Une réponse qui ne fait que promettre le travail, comme « Je vous enverrai les fichiers d’ici mardi », ne termine pas la tâche. Celle-ci reste ouverte avec cette date, et la promesse y renvoie. L’écran de vérification avant envoi vous le signale.

La promesse a déjà été tenue, par exemple dans une réponse que vous avez envoyée ou lors d’une réunion ? Elle est clôturée automatiquement, sans créer de tâche.

Une nouvelle date est donnée plus tard, comme « plutôt la semaine prochaine » ? La même promesse est déplacée, ainsi que sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit une date de **relance** : trois jours après que vous l’avez faite, une semaine après que l’autre personne l’a faite. Si elle est toujours ouverte à cette date, elle devient une tâche.

Les promesses venant de Slack indiquent le nom de la personne.

Les promesses reçues par e-mail de personnes à qui vous n’avez jamais écrit sont également suivies, avec la mention **expéditeur non vérifié** : elles reposent uniquement sur leur parole. La tâche commence par « Non vérifié : vous ne lui avez jamais écrit auparavant. »

## Remboursements

Quand un commerçant, une compagnie aérienne, un propriétaire ou un assureur vous promet un remboursement, par exemple pour une commande annulée ou une demande d’indemnisation acceptée, votre Machine enregistre le montant, la personne qui doit payer et la date prévue du versement. Le remboursement apparaît dans **Promis à vous**. Seulement si le message indique clairement ces trois éléments.

Si l’argent est versé d’abord, par exemple si vous recevez un e-mail indiquant que le « remboursement a été traité », une notification d’un service de paiement ou une notification de votre application bancaire sur votre téléphone, la promesse est clôturée automatiquement, sans créer de tâche.

L’argent n’est pas arrivé à cette date ? Une tâche discrète apparaît : « Réclamer le remboursement de 42 € auprès de … », accompagnée d’un bref e-mail qui indique le numéro de commande ou de dossier. Rien n’est envoyé tant que vous ne l’envoyez pas. Si l’argent arrive finalement, la tâche est clôturée automatiquement. **Annuler** la rouvre pendant une journée.

Le [récapitulatif hebdomadaire](weekly-recap.md) compte les promesses tenues et encore ouvertes. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
