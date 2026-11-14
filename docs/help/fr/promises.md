---
title: Promesses
area: cards
summary: Ce que vous avez dit que vous feriez et ce que les autres vous ont promis. Le suivi se fait automatiquement.
covers: promises
code: dashboard.html, assistant.py
order: 6
translated: 8e5ce7b371ab7fd0
---
Suivez ce que vous avez promis et ce que les autres vous ont promis. Votre Machine repère automatiquement les promesses dans vos messages.

## Où les trouver

Dans **Promesses**, sur la page des tâches :

- Ce que vous avez dit que vous feriez, et pour qui : **Votre promesse**.
- Ce que les autres ont dit qu’ils feraient : **Promis à vous**.

Chaque promesse a un menu **⋯** :

- **Faire** pour les vôtres : elle devient une tâche, et votre Machine la prépare. **Relancer** pour les leurs : votre Machine rédige une courte relance dans le fil où la promesse a été faite, et vous restez sur la liste. Une courte note indique que la relance est en cours, avec **Ouvrir la tâche**, et la promesse affiche « une tâche maintenant ». Rien n’est envoyé tant que vous ne l’envoyez pas. Si la promesse est déjà une tâche, celle-ci s’ouvre.
- **Marquer comme fait** : la promesse a été tenue.
- **N’aura pas lieu** : la promesse ne sera pas tenue. Votre Machine arrête alors de la suivre, sans créer de tâche.

Une promesse ouverte devient aussi automatiquement une tâche aux alentours de la date prévue : les vôtres le matin de la veille, pour vous laisser une journée pour vous en occuper ; les leurs le matin suivant, si elle est toujours ouverte. Elle apparaît à la date prévue dans le [Calendrier](calendar.md). Si elle est déjà une tâche, la promesse renvoie vers celle-ci. **Marquer comme fait** ou **N’aura pas lieu** clôt aussi cette tâche. Quand votre Machine voit que la promesse est tenue, les deux sont clôturées, avec une note qui l’indique.

La promesse a déjà été tenue, par exemple avec une réponse de votre part ou une réunion qui a permis de la tenir ? Elle est clôturée automatiquement, sans créer de tâche.

Une nouvelle date est donnée plus tard, par exemple « plutôt la semaine prochaine » ? La promesse est déplacée, tout comme sa tâche, sans en créer une deuxième. Sa page affiche la nouvelle date et le message le plus récent.

Une promesse sans date reçoit un jour de relance : trois jours après que vous l’avez faite, ou une semaine après que l’autre personne l’a faite. Si elle est toujours ouverte à cette date, elle devient une tâche.

Les promesses de Slack affichent le nom de la personne.

Les promesses reçues par e-mail d’une personne à qui vous n’avez jamais écrit sont aussi suivies, mais marquées comme **expéditeur non vérifié** : elles reposent uniquement sur sa parole. La tâche commence par « Non vérifié : vous ne lui avez jamais écrit. »

Le [récapitulatif hebdomadaire](weekly-recap.md) indique le nombre de promesses tenues et ouvertes. Sur votre propre ordinateur, `assistant promises` les affiche dans un terminal.
