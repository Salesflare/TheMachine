---
title: Promesses
area: cards
summary: Ce que vous avez dit que vous feriez et ce que les autres vous ont promis. Suivi automatiquement.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 0779d3fc9d3f3407
---
Suivez les promesses que vous avez faites et celles que les autres vous ont faites. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Sur la page Tâches, sous **Promesses** :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Promis à vous**.

Chaque promesse a un menu **⋯** :

- **Faire** pour les vôtres : elle devient immédiatement une tâche, et votre Machine la prépare. **Relancer** pour les leurs : votre Machine prépare un bref message de relance là où la promesse a été faite, sans vous faire quitter la liste. Une courte note vous indique que le message est en préparation, avec **Ouvrir la tâche**, et la promesse affiche « une tâche à faire maintenant ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, elle ouvre cette tâche.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue. Votre Machine cesse alors de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche à son échéance (les vôtres la veille au matin, pour vous laisser une journée pour vous en occuper) et apparaît à la date prévue dans le [Calendrier](calendar.md). Si la promesse est maintenant une tâche, un lien y mène, et **Marquer comme fait** ou **N’aura pas lieu** ferme aussi cette tâche. Quand votre Machine voit qu’elle est tenue, les deux sont clôturées et une note l’indique.

Une promesse déjà tenue, par exemple avec une réponse que vous avez envoyée ou une réunion qui y a donné suite ? Elle est clôturée automatiquement, sans créer de tâche.

Une nouvelle date est donnée plus tard, par exemple « plutôt la semaine prochaine » ? La même promesse est reportée, ainsi que sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit une date de **relance** : trois jours après que vous l’avez faite, une semaine après qu’ils l’ont faite. Toujours ouverte à cette date ? Elle devient une tâche.

Les promesses venant de Slack affichent le nom de la personne.

Le [récapitulatif hebdomadaire](weekly-recap.md) indique le nombre de promesses tenues et ouvertes. Sur votre propre ordinateur, `assistant promises` les liste dans un terminal.
