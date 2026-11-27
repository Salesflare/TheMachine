---
title: Promesses
area: cards
summary: Ce que vous avez dit que vous feriez et ce que les autres vous ont promis. Le suivi se fait automatiquement.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: b624394de7ff77b1
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Sous **Promesses**, sur la page Tâches :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Vous a été promis**.

Chaque promesse a un menu **⋯** :

- **Faire** pour les vôtres : elle devient immédiatement une tâche, et votre Machine la prépare. **Relancer** pour les leurs : votre Machine rédige une courte relance à l’endroit où la promesse a été faite, tandis que vous restez dans la liste. Une courte note indique qu’elle est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « une tâche maintenant ». Rien n’est envoyé avant que vous l’envoyiez. Si elle est déjà une tâche, cette tâche s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : elle n’aura pas lieu. Votre Machine arrête donc de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche à l’approche de sa date (les vôtres le matin précédent, pour vous laisser une journée pour vous en occuper ; les leurs le matin suivant, si elles sont toujours ouvertes). Elle apparaît également à la date prévue dans l’[Agenda](calendar.md). Si elle est déjà une tâche, un lien mène à celle-ci. **Marquer comme fait** ou **N’aura pas lieu** clôture aussi cette tâche. Quand votre Machine constate qu’elle est terminée, les deux sont clôturées et une ligne l’indique.

Une réponse qui ne fait que promettre le travail, comme « Je vous enverrai les fichiers d’ici mardi », ne termine pas la tâche. Elle reste ouverte avec cette date, et la promesse y est liée. L’écran de vérification avant envoi le signale. Si vous modifiez d’abord le texte, l’ancienne promesse et sa date sont supprimées : la tâche reste ouverte jusqu’à ce que votre Machine constate que le travail est terminé, et toute promesse dans le message envoyé y est associée.

La promesse a déjà été tenue, par exemple dans une réponse que vous avez envoyée ou lors d’une réunion ? Elle est clôturée automatiquement, sans créer de tâche.

Quand quelqu’un répond à une promesse qu’il a faite, elle reste ouverte jusqu’à ce que sa réponse montre qu’elle a été tenue. Un « Bien sûr » ou une réponse qui n’en réalise qu’une partie ne suffit pas. Si une relance était en attente d’envoi, elle est annulée et la tâche reste ouverte avec la mention « Cette personne a réécrit ». Une réponse d’absence ne change rien.

La personne donne une nouvelle date ultérieure, par exemple « plutôt la semaine prochaine » ? La même promesse est déplacée, ainsi que sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit un jour de relance : trois jours après que vous l’avez faite, ou une semaine après que l’autre personne l’a faite. Si elle est toujours ouverte à cette date, elle devient une tâche.

Les promesses provenant de Slack affichent le nom de la personne.

Une promesse reçue par e-mail d’une personne à qui vous n’avez jamais écrit est également suivie, avec la mention **expéditeur non vérifié** : elle repose uniquement sur sa parole. Sa tâche commence par « Non vérifié : vous ne lui avez jamais écrit auparavant. »

## Remboursements

Quand un magasin, une compagnie aérienne, un propriétaire ou un assureur vous promet un remboursement, par exemple pour une commande annulée ou une réclamation acceptée, votre Machine enregistre le montant, la personne qui doit vous payer et la date à laquelle le remboursement devrait arriver. La promesse apparaît sous **Vous a été promis**. Votre Machine ne l’ajoute que si le message précise ces trois éléments.

Si l’argent arrive d’abord, par exemple après un e-mail indiquant qu’un « remboursement a été traité », une notification d’un service de paiement ou une notification de votre application bancaire sur votre téléphone, la promesse est clôturée automatiquement, sans créer de tâche.

L’argent n’est pas arrivé à cette date ? Une seule tâche discrète apparaît : « Relancer le remboursement de 42 € auprès de … », avec un court e-mail mentionnant le numéro de commande ou de dossier. Rien n’est envoyé avant que vous l’envoyiez. Si l’argent arrive finalement, la tâche est clôturée automatiquement. **Annuler** la réactive pendant une journée.

Le [récap hebdo](weekly-recap.md) comptabilise les promesses tenues et ouvertes. Sur votre propre ordinateur, `assistant promises` les répertorie dans un terminal.
