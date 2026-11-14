---
title: Récap de la semaine
area: weekly
summary: Une fois par semaine, le bilan de votre Machine : tâches, promesses, personnes et projets, et ce qu’elle a remarqué. Activé par défaut.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
translated: 936df3d624aba2d7
---
## Ce qu’il contient

- Votre semaine avec The Machine, et combien de tâches en valaient la peine, comparé à la semaine précédente.
- Tâches : nouvelles, faites, écartées et mises en attente, et la rapidité de vos réponses.
- Promesses : les vôtres tenues et en cours, celles des autres qui ont abouti ou sont encore attendues.
- Apprentissages à partager avec l’équipe The Machine, s’il y en a qui vous attendent. Voir [Partager des apprentissages avec l’équipe](share-learnings.md).
- Personnes et projets, comme qui ne donne plus de nouvelles.
- Ce que j’ai remarqué : brouillons envoyés tels quels ou modifiés, tâches écartées en quelques minutes, tâches mises en attente plus d’une fois.
- En coulisses : combien de signaux elle a vérifiés cette semaine, et combien attendent encore.
- Des choix, chacun dans son propre message après le récapitulatif : une source très active sans résultat (**Ne plus vérifier** ou **Continuer à vérifier**) et une tâche mise en attente plus d’une fois (**Pas nécessaire**, **Faire** ou **Garder**). Rien ne change tant que vous ne touchez pas.

## Quand et où

Une fois par semaine, par défaut le vendredi après 16:00 dans votre fuseau horaire. Il arrive sur [Telegram](telegram.md), ou comme notification intitulée « Votre semaine » depuis l’[app mobile](phone-app.md) et l’app du tableau de bord. Il arrive aussi par e-mail quand l’e-mail est activé pour **Récap du matin** dans Paramètres › Notifications. Avec [Prudent](security-levels.md), il n’arrive pas par e-mail.

## Le désactiver

Il est activé par défaut. Désactivez-le dans Paramètres › Notifications avec l’interrupteur **Récap hebdo**. Si vous l’avez désactivé, il reste désactivé. Sur votre propre ordinateur, vous pouvez aussi régler `weekly_recap` dans le config.json : `enabled` à false avec `chosen` à true, et en option `weekday` (de 1 à 7, le vendredi est 5) et `at` ("16:00"). Voir le [guide de configuration](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
