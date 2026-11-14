---
title: Promesses
area: cards
summary: Ce que vous avez dit que vous feriez et ce que les autres vous ont promis. Le suivi se fait automatiquement.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: dbac0241c54b0ec6
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Sur la page Tâches, sous **Promesses** :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Promis à vous**.

Chaque promesse a un menu **⋯** :

- **Faire** pour les vôtres : elles deviennent des tâches et votre Machine les prépare. **Relancer** pour celles des autres : votre Machine rédige une courte relance dans le fil où la promesse a été faite, sans vous faire quitter la liste. Une courte note indique qu’elle est en cours d’envoi, avec **Ouvrir la tâche**, et la promesse affiche « une tâche maintenant ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, elle ouvre cette tâche.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue. Votre Machine arrête alors de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche à son échéance. Pour les vôtres, cela se fait la veille au matin, pour vous laisser une journée pour vous en occuper. Elle apparaît aussi à la date prévue dans le [Calendrier](calendar.md). Une promesse devenue une tâche renvoie vers celle-ci, et **Marquer comme fait** ou **N’aura pas lieu** clôture aussi la tâche. Lorsque votre Machine voit qu’elle est terminée, les deux sont clôturées et une ligne l’indique.

Une promesse déjà tenue, par exemple avec une réponse que vous avez envoyée ou une réunion qui y a donné suite, est clôturée automatiquement, sans créer de tâche.

Si une nouvelle date est donnée plus tard, par exemple « plutôt la semaine prochaine », la même promesse est déplacée, ainsi que sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit une journée de **relance** : trois jours après que vous l’avez faite, ou une semaine après que l’autre personne l’a faite. Si elle est toujours ouverte à cette date, elle devient une tâche.

Les promesses venant de Slack affichent le nom de la personne.

Les promesses reçues par e-mail d’une personne à qui vous n’avez jamais écrit sont aussi enregistrées, avec la mention **expéditeur non vérifié** : elles reposent uniquement sur sa parole. La tâche commence par « Non vérifié : vous ne lui avez jamais écrit auparavant. »

Le [récapitulatif hebdomadaire](weekly-recap.md) compte les promesses tenues et ouvertes. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
