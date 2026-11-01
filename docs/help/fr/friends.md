---
title: Amis et le Network
area: fleet
summary: Ajoutez des amis par nom d’utilisateur, trouvez des personnes que vous connaissez qui ont une Machine, et associez une Machine sur votre propre ordinateur.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Amis

Ajoutez quelqu’un par son nom d’utilisateur exact, dans l’onglet **Fleet** sous Amis. Les amis peuvent demander qui connaît quelqu’un, obtenir le contexte d’une réunion et des présentations, et voir quand vous êtes occupé (uniquement les créneaux occupés, jamais ce que vous faites). Retirez ou bloquez un ami à tout moment.

## Trouver des personnes que vous connaissez

Dans le volet Network :

- « Vérifier lesquels de mes contacts ont une Machine » suggère des personnes que vous connaissez.
- « Laisser les personnes qui ont mon e-mail me trouver » leur permet de vous trouver.

Les deux sont activés par défaut, et désactivés au niveau de sécurité Prudent. Désactivez-les quand vous voulez ; votre choix est conservé. On peut vous trouver par votre e-mail de connexion et vos adresses connectées, sauf les adresses partagées comme info@, qui restent désactivées jusqu’à ce que vous les activiez.

Les personnes que vous connaissez et qui sont sur le Network sont suggérées dès que vous l’activez, et quand quelqu’un le rejoint plus tard. Une correspondance propose Se connecter, Pas maintenant ou **Ne jamais suggérer**. **Quitter le Network** vous en retire.

## Planifier avec d’autres Machines

Quand une personne qui a une Machine écrit « voyons-nous la semaine prochaine », votre Machine demande ses disponibilités à la sienne et trouve un horaire qui vous convient à tous les deux, dans vos heures de travail. Chacun reçoit une seule to-do, comme « Rendez-vous avec Alex Example », avec l’horaire en dessous. Touchez **Réserver**, **Autre horaire** ou **Pas nécessaire**. L’invitation ne part que lorsque vous avez tous les deux touché Réserver.

Seul libre ou occupé est transmis, chiffré de bout en bout, sur 14 jours au plus et arrondi à 15 minutes. Les événements privés comptent comme occupés. Une Machine ne peut demander que si vous vous êtes écrit dans les deux sens. Réglez-le dans le volet Network sous **Ce que d’autres Machines peuvent demander à la mienne** : **Libre/occupé pour planifier** ou **Désactivé**, avec la durée, la marge et les horaires préférés. Chaque demande apparaît dans Activité, sous Agenda.

Pas de Machine ou pas de réponse : le brouillon d’e-mail reçoit un lien où l’autre choisit un de vos horaires libres. Ce choix devient une to-do avec **Réserver** ; rien n’est réservé avant que vous ne touchiez.

Le lien ne montre que des horaires libres, selon les mêmes règles, et rien d’autre sur vous. Il prend fin dès que le rendez-vous est réservé, ou après 14 jours. Dans l’e-mail, il s’affiche comme "Pick a time". En bas, la page dit que votre Machine a trouvé ces horaires, avec "Get yours." et votre prénom. Désactivez cela avec **Pied de page des liens de réservation**. Chaque lien et chaque choix apparaît dans Activité.

## Une Machine sur votre propre ordinateur

Pour rejoindre le Network depuis une Machine que vous faites tourner vous-même :

1. Sur la page de votre compte sur app.themachine.computer, appuyez sur **Associer une Machine auto-hébergée**. Le code fonctionne une fois, pendant 15 minutes.
2. Sur votre ordinateur, lancez `assistant fleet-pair` avec le code, puis redémarrez.

Jusqu’à 5 Machines par compte. Chacune peut y être déconnectée.
