---
title: Amis et le Network
area: fleet
summary: Ajoutez des amis par nom d’utilisateur, trouvez des personnes que vous connaissez qui ont une Machine, et associez une Machine sur votre propre ordinateur.
covers: friends
code: friends.py, network.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Amis

Ajoutez quelqu’un par son nom d’utilisateur exact, dans l’onglet **Fleet** sous Amis. Les amis peuvent demander qui connaît quelqu’un, obtenir le contexte d’une réunion et des présentations, et voir quand vous êtes occupé (uniquement les créneaux occupés, jamais ce que vous faites). Retirez ou bloquez un ami à tout moment.

## Trouver des personnes que vous connaissez

Dans le volet Network :

- « Vérifier lesquels de mes contacts ont une Machine » suggère des personnes que vous connaissez.
- « Laisser les personnes qui ont mon e-mail me trouver » leur permet de vous trouver.

Les personnes que vous connaissez et qui sont sur le Network sont suggérées dès que vous l’activez, et quand quelqu’un le rejoint plus tard. Une correspondance propose Se connecter, Pas maintenant ou **Ne jamais suggérer**. **Quitter le Network** vous en retire.

## Une Machine sur votre propre ordinateur

Pour rejoindre le Network depuis une Machine que vous faites tourner vous-même :

1. Sur la page de votre compte sur app.themachine.computer, appuyez sur **Associer une Machine auto-hébergée**. Le code fonctionne une fois, pendant 15 minutes.
2. Sur votre ordinateur, lancez `assistant fleet-pair` avec le code, puis redémarrez.

Jusqu’à 5 Machines par compte. Chacune peut y être déconnectée.
