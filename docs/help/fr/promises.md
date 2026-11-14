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

- **Faire** pour les vôtres : la promesse devient une tâche et votre Machine la prépare. **Relancer** pour les leurs : votre Machine rédige un court message de relance là où la promesse a été faite, tandis que vous restez dans la liste. Une courte note indique que le message est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « maintenant une tâche ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, elle ouvre cette tâche.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : elle ne se réalisera pas. Votre Machine cesse alors de la suivre, sans créer de tâche.

Une promesse en cours devient aussi automatiquement une tâche à son échéance (la veille au matin pour les vôtres, afin de vous laisser une journée pour vous en occuper) et apparaît à la date correspondante dans le [Calendrier](calendar.md). Si elle est déjà devenue une tâche, un lien y mène, et **Marquer comme fait** ou **N’aura pas lieu** clôt aussi cette tâche. Quand votre Machine détecte que la promesse a été tenue, les deux sont clôturées, avec une note qui l’indique.

Une promesse déjà tenue, par exemple une réponse que vous avez envoyée ou une réunion qui y a donné suite ? Elle est clôturée automatiquement, sans créer de tâche.

Une nouvelle date est donnée plus tard, par exemple « plutôt la semaine prochaine » ? La même promesse est déplacée, ainsi que sa tâche, sans en créer une deuxième. Sa page indique la nouvelle date et le message le plus récent.

Une promesse sans date reçoit une date de **relance** : trois jours après que vous l’avez faite, une semaine après que l’autre personne l’a faite. Si elle est toujours en cours à cette date, elle devient une tâche.

Les promesses provenant de Slack affichent le nom de la personne.

Les promesses envoyées par e-mail par une personne à qui vous n’avez jamais écrit sont également suivies, avec la mention **expéditeur non vérifié** : il n’y a que sa parole. La tâche correspondante commence par « Non vérifié : vous ne lui avez jamais écrit. »

Le [récapitulatif hebdomadaire](weekly-recap.md) compte les promesses tenues et celles en cours. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
