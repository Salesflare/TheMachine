---
title: Récap hebdo
area: weekly
summary: Chaque semaine, découvrez comment votre Machine s’en est sortie : tâches, promesses, personnes et projets, et ce qu’elle a remarqué. Activé par défaut.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 223b143a6efd5692
---
## Ce qu’il contient

- Vous attend : les promesses qu’on vous a faites et qui sont en retard, ainsi que les vôtres qui sont en retard ou arrivent à échéance dans les deux prochaines semaines.
- La semaine prochaine : vos réunions (avec un lien quand la préparation est prête), les tâches à échéance et les promesses faites par d’autres pour cette période.
- Ce qui a changé : le nombre de tâches qui en valaient la peine, par rapport à la semaine précédente, la fréquence à laquelle **Faire** a été juste du premier coup, les ajustements apportés à votre façon d’écrire et à ses filtres, et le nombre de brouillons envoyés tels quels.
- Pour l’équipe The Machine : les apprentissages à partager, s’il y en a qui vous attendent. Consultez [Partager les apprentissages avec l’équipe](share-learnings.md).
- Personnes et projets : les projets qui prennent de l’ampleur ou ralentissent, les nouvelles personnes et celles qui se font discrètes.
- En coulisses : le nombre de signaux vérifiés cette semaine et le nombre de ceux qui sont encore en attente.
- Sur [Telegram](telegram.md), vous recevez ensuite des choix, chacun dans son propre message : une source très active sans résultat (**Ne plus vérifier** ou **Continuer à vérifier**) et une tâche mise en attente plusieurs fois (**Pas nécessaire**, **Faire** ou **Garder**). Rien ne change tant que vous n’avez pas appuyé sur un choix.

## Quand et où

Par défaut, une fois par semaine, le vendredi après 16 h dans votre fuseau horaire. Vous le recevez sur [Telegram](telegram.md), ou sous forme de notification intitulée « Votre semaine » depuis l’[application mobile](phone-app.md) et l’application de tableau de bord. Vous le recevez aussi par e-mail si les e-mails sont activés pour le **Récap du matin** dans Paramètres › Notifications. Avec le niveau [Prudent](security-levels.md), ou si l’option **Texte dans les notifications** est désactivée, vous ne le recevez pas par e-mail.

## Désactiver

Cette option est activée par défaut. Pour la désactiver, allez dans Paramètres › Notifications et désactivez **Récap hebdo**. Si vous l’avez désactivée, elle reste désactivée. Sur votre propre ordinateur, vous pouvez aussi définir `weekly_recap` dans config.json : `enabled` false avec `chosen` true, et éventuellement `weekday` (1 à 7, vendredi correspond à 5) et `at` ("16:00"). Consultez le [guide de configuration](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
