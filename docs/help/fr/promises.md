---
title: Promesses
area: cards
summary: Ce que vous avez promis et ce que les autres vous ont promis. Le suivi se fait automatiquement.
covers: promises
code: dashboard.html, assistant.py, refunds.py
order: 6
translated: 176831c86d0a382a
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Sous **Promesses**, sur la page Tâches :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Promis à vous**.

Chaque promesse a un menu **⋯** :

- **Faire** pour les vôtres : elle devient une tâche, et votre Machine la prépare. **Relancer** pour les leurs : votre Machine prépare un court message de relance là où la promesse a été faite, tandis que vous restez sur la liste. Une courte note indique que le message est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « maintenant une tâche ». Rien n’est envoyé avant que vous l’envoyiez. Si elle est déjà une tâche, celle-ci s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : elle ne se réalisera pas, votre Machine cesse donc de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche à l’approche de sa date (la veille au matin pour les vôtres, pour vous laisser une journée pour agir ; le lendemain matin pour les leurs, si elle est toujours ouverte), et apparaît à la date correspondante dans le [Calendrier](calendar.md). Si elle est déjà une tâche, la promesse y renvoie, et **Marquer comme fait** ou **N’aura pas lieu** clôt aussi cette tâche. Quand votre Machine voit qu’elle est accomplie, les deux sont clôturées et une ligne l’indique.

Une réponse qui ne fait que promettre le travail, comme « Je vous enverrai les fichiers d’ici mardi », ne termine pas la tâche. Celle-ci reste ouverte avec cette date, et la promesse y renvoie. L’écran de vérification avant l’envoi vous le signale.

La promesse a déjà été tenue, par exemple dans une réponse que vous avez envoyée ou lors d’une réunion ? Elle se clôt automatiquement, sans créer de tâche.

Une nouvelle date est donnée plus tard, par exemple « plutôt la semaine prochaine » ? La date de la même promesse est modifiée, ainsi que celle de sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit une date de **relance** : trois jours après que vous l’avez faite, une semaine après qu’ils l’ont faite. Si elle est toujours ouverte à cette date, elle devient une tâche.

Les promesses venant de Slack affichent le nom de la personne.

Les promesses reçues par e-mail de personnes à qui vous n’avez jamais écrit sont aussi conservées. Elles sont marquées **expéditeur non vérifié** : seule leur parole en témoigne. La tâche commence par « Non vérifié : vous ne lui avez jamais écrit. »

## Remboursements

Quand un magasin, une compagnie aérienne, un propriétaire ou un assureur vous promet un remboursement, par exemple pour une commande annulée ou une demande approuvée, votre Machine conserve le montant, le nom du payeur et la date prévue du versement. La promesse apparaît sous **Promis à vous**. Elle n’est enregistrée que si le message précise ces trois éléments.

Si l’argent est versé avant cette date, par exemple à la réception d’un e-mail indiquant que le remboursement a été traité, d’une notification d’un service de paiement ou d’une notification de votre application bancaire sur votre téléphone, la promesse se clôt automatiquement, sans créer de tâche.

L’argent n’est pas arrivé à cette date ? Une tâche discrète apparaît : « Réclamer le remboursement de 42 € auprès de … », avec un court e-mail mentionnant le numéro de commande ou de dossier. Rien n’est envoyé avant que vous l’envoyiez. Si l’argent arrive finalement, la tâche se clôt automatiquement. **Annuler** la réactive pendant une journée.

Le [Récap hebdo](weekly-recap.md) compte les promesses tenues et ouvertes. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
