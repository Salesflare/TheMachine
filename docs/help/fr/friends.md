---
title: Amis et Network
area: fleet
summary: Ajoutez des amis avec leur nom d’utilisateur exact, trouvez les personnes que vous connaissez qui ont une Machine et associez une Machine sur votre propre ordinateur.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 3565b3898b234575
---
## Amis

Ajoutez quelqu’un avec son nom d’utilisateur exact, dans l’onglet **Fleet**, sous Amis. Vos amis peuvent demander qui connaît quelqu’un, obtenir du contexte sur les réunions et être mis en relation par des connaissances. Ils peuvent aussi voir quand vous êtes occupé (uniquement les horaires, jamais le contenu). Vous pouvez supprimer un ami ou le bloquer à tout moment.

## Trouver des personnes que vous connaissez

Dans **Fleet**, sous **Network** :

- « Vérifier lesquels de mes contacts ont une Machine » vous suggère des personnes que vous connaissez.
- « Permettre aux personnes qui ont mon adresse e-mail de me trouver » leur permet de vous trouver.

Ces deux options sont activées par défaut et désactivées au niveau de sécurité Prudent. Vous pouvez désactiver l’une ou l’autre à tout moment, et votre choix est conservé. On peut vous trouver avec l’adresse e-mail utilisée pour vous connecter (toujours activée) et vos adresses connectées, chacune avec son propre interrupteur sous **Trouvable par**. Les adresses partagées comme info@ restent désactivées jusqu’à ce que vous les activiez.

Les personnes que vous connaissez apparaissent dès que vous activez l’option, puis au fur et à mesure qu’elles rejoignent le Network. Pour chacune, vous pouvez choisir **Ajouter comme ami**, **Pas maintenant** ou **Ne jamais suggérer**. Une fois que vous êtes amis, cette personne ne vous est plus suggérée. **Quitter le Network** vous en retire.

Les personnes trouvées portent la mention **A une Machine** dans votre liste de personnes. The Machine vérifie les adresses dans vos messages et celles que vous avez ajoutées à une personne avec **Modifier**. Si quelqu’un s’est inscrit avec une autre adresse, ajoutez-la à sa fiche. Sur la page d’une personne trouvée, **Ajouter comme ami** envoie la même demande que l’option Ajouter comme ami (**Ajouter comme famille** se trouve dans le menu ⋯).

Pour une personne sans Machine, l’option **Inviter sur The Machine** ouvre l’e-mail qu’elle recevra dans **Envoyer cet e-mail ?**. C’est le même e-mail que pour n’importe quelle tâche, et vous pouvez le modifier. Rien n’est envoyé avant que vous choisissiez **Envoyer maintenant**. Si vous fermez la fenêtre, l’invitation reste dans vos tâches. Si aucune boîte mail ne peut envoyer de message, choisissez **Copier** ou **Ouvrir dans votre messagerie**.

Les numéros de téléphone sont également pris en compte : ceux des personnes avec qui vous avez discuté sur WhatsApp, écrit ou que vous avez rencontrées, ainsi que ceux que vous avez ajoutés avec **Modifier**. Votre numéro WhatsApp associé et les numéros indiqués dans **À propos de vous** permettent de vous trouver. Chacun a son propre interrupteur sous **Trouvable par**. Un numéro ne permet de trouver quelqu’un que si cette personne vous a aussi recherché ou si vous êtes amis. Personne ne peut donc essayer des numéros pour vérifier qui a une Machine.

## Planifier avec d’autres Machines

Quand une personne qui a une Machine vous écrit « retrouvons-nous la semaine prochaine », votre Machine demande à la sienne vos disponibilités et trouve un horaire qui convient à vous deux, pendant vos heures de travail. Vous recevez chacun une tâche, par exemple « Rencontrer Alex Example », avec l’horaire indiqué en dessous. Choisissez **Réserver**, **Autre horaire** ou **Pas nécessaire**. L’invitation est envoyée uniquement quand vous avez tous les deux choisi Réserver.

Seules vos disponibilités, libre ou occupé, sont transmises, chiffrées de bout en bout, pour une durée maximale de 14 jours et par tranches de 15 minutes. Les événements privés sont considérés comme occupés. Une Machine peut faire une demande uniquement si vous vous êtes écrit tous les deux. Configurez cette option sous **Ce que d’autres Machines peuvent demander à la mienne** : **Libre/occupé pour planifier** ou **Désactivée**, puis définissez la durée de vos réunions, la marge entre elles et vos horaires préférés. Chaque demande apparaît dans **Activité**, sous **Calendrier**.

Si l’autre personne n’a pas de Machine ou ne répond pas, le brouillon d’e-mail contient un lien qui lui permet de choisir l’une de vos disponibilités. Son choix devient une tâche avec l’option **Réserver**. Rien n’est réservé avant que vous la sélectionniez.

Le lien affiche uniquement vos disponibilités, selon les mêmes règles, et ne révèle rien d’autre à votre sujet. Il expire une fois la réunion réservée ou au bout de 14 jours. Dans l’e-mail, il apparaît sous le texte « Choisir un horaire ». En bas de la page, le texte « Votre Machine a trouvé ces horaires. Obtenez la vôtre. » apparaît avec votre prénom. Désactivez-le avec **Pied de page des liens de réservation**. Chaque lien et chaque choix apparaissent dans **Activité**.

## Une Machine sur votre propre ordinateur

Pour rejoindre le Network depuis une Machine que vous gérez vous-même :

1. Dans le tableau de bord de votre Machine, ouvrez **Paramètres** et cliquez sur **Rejoindre le Network**.
2. Sur la page qui s’ouvre, connectez-vous (ou créez votre compte), puis confirmez. Votre Machine se connecte automatiquement, sans redémarrage.

La méthode avec code fonctionne toujours : cliquez sur **Associer une Machine auto-hébergée** dans la page de votre compte sur app.themachine.computer, puis exécutez `assistant fleet-pair` avec le code sur votre ordinateur et redémarrez. Le code ne fonctionne qu’une fois, pendant 15 minutes.

Vous pouvez avoir jusqu’à 5 Machines par compte. Vous pouvez déconnecter chacune d’elles depuis cette page.
