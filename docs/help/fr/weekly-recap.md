---
title: Récap de la semaine
area: weekly
summary: Une fois par semaine, le bilan de votre Machine : tâches, promesses, personnes et projets, et ce qu’elle a remarqué. Désactivé par défaut.
covers: weekly-recap
code: assistant.py, config.example.json
order: 1
---
## Ce qu’il contient

- Votre semaine avec The Machine, et combien de tâches en valaient la peine, comparé à la semaine précédente.
- Tâches : nouvelles, faites, écartées et mises en attente, et la rapidité de vos réponses.
- Promesses : les vôtres tenues et en cours, celles des autres qui ont abouti ou sont encore attendues.
- Apprentissages à partager avec l’équipe The Machine, s’il y en a qui vous attendent. Voir [Partager des apprentissages avec l’équipe](share-learnings.md).
- Personnes et projets, comme qui ne donne plus de nouvelles.
- Ce que j’ai remarqué : brouillons envoyés tels quels ou modifiés, tâches écartées en quelques minutes, tâches mises en attente plus d’une fois.
- En coulisses : ce qu’elle a passé en revue, et ce que cela a coûté.

## Quand et où

Une fois par semaine, par défaut le vendredi après 16:00 dans votre fuseau horaire. Il arrive sur [Telegram](telegram.md), ou comme notification intitulée « Votre semaine » depuis l’[app mobile](phone-app.md).

## L’activer

Il est désactivé par défaut, et le tableau de bord n’a pas encore d’interrupteur pour lui, donc une Machine hébergée ne peut pas l’activer aujourd’hui. Sur votre propre ordinateur, réglez `weekly_recap` dans le config.json de votre Machine : `enabled` à true, et en option `weekday` (de 1 à 7, le vendredi est 5) et `at` ("16:00"). Voir le [guide de configuration](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
