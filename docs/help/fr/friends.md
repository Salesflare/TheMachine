---
title: Les amis et le Network
area: fleet
summary: Ajoutez des amis avec leur nom d’utilisateur exact, trouvez les personnes que vous connaissez qui ont une Machine et associez une Machine installée sur votre ordinateur.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 637784bf811800bb
---
## Amis

Ajoutez quelqu’un avec son nom d’utilisateur exact dans l’onglet **Fleet**, sous Amis. Vos amis peuvent demander qui connaît quelqu’un, obtenir du contexte sur une réunion et des mises en relation, et voir quand vous êtes occupé (uniquement vos périodes d’indisponibilité, jamais leur contenu). Vous pouvez supprimer un ami ou le bloquer à tout moment.

## Trouver les personnes que vous connaissez

Dans **Fleet**, sous **Network** :

- **« Vérifier lesquels de mes contacts ont une Machine »** vous suggère des personnes que vous connaissez.
- **« Laisser les personnes qui ont mon e-mail me trouver »** leur permet de vous trouver.

Les deux options sont activées par défaut et désactivées au niveau de sécurité Prudent. Vous pouvez désactiver l’une ou l’autre à tout moment. Votre choix est conservé. Les personnes peuvent vous trouver avec l’adresse e-mail utilisée pour vous connecter (toujours activée) et vos adresses connectées, chacune avec son propre interrupteur sous **Trouvable par**, sauf les adresses partagées comme info@, qui restent désactivées jusqu’à ce que vous les activiez.

Les personnes que vous connaissez apparaissent immédiatement comme une tâche lorsque vous activez cette option, puis au fur et à mesure qu’elles rejoignent le Network. Pour chacune, vous pouvez choisir **Ami** ou **Famille** (**Connecter** pour un collègue), **Pas maintenant** ou **Ne jamais suggérer** dans le menu ⋯. Une fois que vous êtes amis, elles ne vous sont plus suggérées. **Quitter le Network** vous retire du Network.

Les personnes trouvées apparaissent avec le statut **A une Machine** dans votre liste de personnes. The Machine vérifie les adresses dans vos messages et celles que vous avez ajoutées à une personne avec **Modifier**. Si quelqu’un s’est inscrit avec une autre adresse, ajoutez-la à sa fiche. Sur la page d’une personne trouvée, **Ajouter comme ami** envoie la même demande que **Connecter** (**Ajouter comme famille** se trouve dans le menu ⋯).

Pour quelqu’un qui n’a pas de Machine, choisissez **Inviter sur The Machine**. Cela ouvre l’e-mail qu’il recevra dans **Envoyer cet e-mail ?**, comme pour n’importe quelle tâche. Vous pouvez le modifier si vous le souhaitez. Rien n’est envoyé avant que vous choisissiez **Envoyer maintenant**. Si vous fermez la fenêtre, l’invitation reste sous forme de tâche. Si aucune boîte mail ne permet l’envoi : **Copier** ou **Ouvrir dans votre messagerie**.

Les numéros de téléphone sont aussi pris en compte : ceux des conversations WhatsApp avec les personnes à qui vous avez écrit ou que vous avez rencontrées, ainsi que ceux que vous avez ajoutés avec **Modifier**. Votre numéro WhatsApp associé et les numéros indiqués dans la section À propos de vous permettent aux autres de vous trouver, chacun avec son propre interrupteur sous **Trouvable par**. Un numéro ne permet de trouver quelqu’un que si cette personne vous a aussi recherché ou si vous êtes amis. Ainsi, personne ne peut essayer des numéros pour savoir qui a une Machine.

## Planifier avec d’autres Machines

Quand une personne qui a une Machine écrit « Retrouvons-nous la semaine prochaine », votre Machine demande à la sienne les créneaux disponibles et en trouve un qui vous convient à tous les deux, pendant vos heures de travail. Vous recevez chacun une tâche, par exemple « Rencontrer Alex Example », avec l’heure indiquée dessous. Choisissez **Réserver**, **Autre horaire** ou **Pas nécessaire**. L’invitation est envoyée uniquement après que vous avez tous les deux choisi **Réserver**.

Seules vos disponibilités sont partagées, avec un chiffrement de bout en bout, pour une période maximale de 14 jours et par tranches de 15 minutes. Les événements privés sont considérés comme des périodes d’indisponibilité. Une Machine ne peut faire une demande que si vous vous êtes envoyé des e-mails l’un à l’autre. Réglez cette option sous **Ce que d’autres Machines peuvent demander à la mienne** : **Libre/occupé pour planifier** ou **Désactivé**, ainsi que la durée de vos réunions, le temps de battement et vos horaires préférés. Chaque demande apparaît dans Activité, sous Agenda.

Si la personne n’a pas de Machine ou ne répond pas, le brouillon d’e-mail contient un lien qui lui permet de choisir l’un de vos créneaux disponibles. Son choix apparaît sous forme de tâche avec **Réserver**. Rien n’est réservé avant que vous appuyiez sur ce bouton.

Le lien affiche uniquement vos créneaux disponibles, selon les mêmes règles, et ne révèle rien d’autre à votre sujet. Il expire dès que la réunion est réservée ou au bout de 14 jours. Dans l’e-mail, il apparaît sous la mention « Choisir un horaire ». En bas de la page, on lit : « La Machine d’Alex a trouvé ces horaires. Obtenez la vôtre. », avec votre prénom. Désactivez cette option avec **Pied de page des liens de réservation**. Chaque lien et chaque choix apparaissent dans Activité.

## Une Machine sur votre ordinateur

Pour rejoindre le Network depuis une Machine que vous hébergez vous-même :

1. Dans le tableau de bord de votre Machine, ouvrez **Paramètres**, puis appuyez sur **Rejoindre le Network**.
2. Sur la page qui s’ouvre, connectez-vous (ou créez votre compte), puis confirmez. Votre Machine détecte l’association automatiquement, sans redémarrage.

La méthode avec code fonctionne toujours : appuyez sur **Associer une Machine auto-hébergée** sur la page de votre compte à l’adresse app.themachine.computer, puis exécutez `assistant fleet-pair` avec le code sur votre ordinateur et redémarrez. Le code ne fonctionne qu’une seule fois et expire au bout de 15 minutes.

Vous pouvez avoir jusqu’à 5 Machines par compte. Vous pouvez déconnecter chacune d’elles depuis cette page.
