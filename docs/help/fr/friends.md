---
title: Les amis et le Network
area: fleet
summary: Ajoutez des amis par nom d’utilisateur, trouvez des connaissances qui ont une Machine et associez une Machine sur votre propre ordinateur.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 70a39b4999d112b7
---
## Amis

Ajoutez quelqu’un avec son nom d’utilisateur exact, dans l’onglet **Fleet**, sous **Amis**. Vos amis peuvent demander qui connaît quelqu’un, obtenir du contexte sur une réunion et des mises en relation, et voir quand vous êtes occupé (uniquement les périodes où vous êtes occupé, jamais la raison). Les jours dont l’agenda ne donne aucune information apparaissent comme inconnus, jamais comme libres. Vous pouvez supprimer ou bloquer un ami à tout moment.

## Trouver les personnes que vous connaissez

Dans **Fleet**, sous **Network** :

- « Vérifier lesquels de mes contacts ont une Machine » vous suggère des personnes que vous connaissez.
- « Permettre aux personnes qui ont mon adresse e-mail de me trouver » leur permet de vous trouver.

Les deux options sont activées par défaut et désactivées au niveau de sécurité Prudent. Vous pouvez désactiver l’une ou l’autre à tout moment. Votre choix est conservé. Les personnes peuvent vous trouver avec l’adresse e-mail de connexion à votre compte (toujours activée) et vos adresses connectées. Chacune a son propre interrupteur sous **Trouvable par**, à l’exception des adresses partagées, comme info@, qui restent désactivées tant que vous ne les activez pas.

Les personnes que vous connaissez apparaissent immédiatement comme une tâche quand vous activez l’option, puis au fur et à mesure qu’elles rejoignent le Network. Pour chacune, vous pouvez choisir **Ami** et **Famille** (**Connecter** pour un collègue), **Pas maintenant** ou **Ne jamais suggérer** dans le menu ⋯. Une fois que vous êtes amis, la personne ne vous est plus suggérée. **Quitter le Network** vous retire du Network.

Les personnes trouvées apparaissent dans votre liste de personnes avec la mention **A une Machine**. La recherche vérifie les adresses dans vos messages et celles que vous avez ajoutées à une personne avec **Modifier**. Si quelqu’un s’est inscrit avec une autre adresse, ajoutez-la à sa fiche. Sur la page d’une personne trouvée, **Ajouter comme ami** envoie la même demande que Connecter (**Ajouter comme famille** se trouve dans le menu ⋯).

Pour une personne qui n’a pas de Machine, l’option **Inviter sur The Machine** ouvre le brouillon de l’e-mail qu’elle recevra, dans **Envoyer cet e-mail ?**. C’est le même e-mail que pour n’importe quelle tâche, et vous pouvez le modifier. Rien n’est envoyé avant que vous appuyiez sur **Envoyer maintenant**. Si vous fermez la fenêtre, l’invitation reste une tâche. Si aucune boîte mail ne permet l’envoi : **Copier** ou **Ouvrir dans votre messagerie**.

Les numéros de téléphone sont aussi pris en compte : ceux des conversations WhatsApp avec les personnes à qui vous avez écrit ou que vous avez rencontrées, et ceux que vous avez ajoutés avec **Modifier**. Votre numéro WhatsApp associé et les numéros indiqués dans À propos de vous permettent aux autres de vous trouver. Chacun a son propre interrupteur sous **Trouvable par**. Un numéro permet de trouver quelqu’un uniquement si cette personne vous a aussi recherché ou si vous êtes amis. Personne ne peut donc essayer des numéros pour vérifier qui a une Machine.

## Planifier avec d’autres Machines

Quand une personne qui a une Machine écrit « Retrouvons-nous la semaine prochaine », votre Machine demande à la sienne ses disponibilités et en trouve une qui vous convient à tous les deux, pendant vos heures de travail. Vous recevez chacun une tâche, par exemple « Rencontrer Alex Example », avec l’heure indiquée en dessous. Appuyez sur **Réserver**, **Autre horaire** ou **Pas nécessaire**. L’invitation n’est envoyée qu’une fois que vous avez tous les deux appuyé sur « Réserver ».

Seules les disponibilités sont transmises, de manière chiffrée de bout en bout, sur une période maximale de 14 jours et par tranches de 15 minutes. Les événements privés sont considérés comme occupés. Une Machine ne peut faire une demande que si vous vous êtes envoyé des e-mails tous les deux. Choisissez une option sous **Ce que d’autres Machines peuvent demander à la mienne** : **Libre/occupé pour planifier** ou **Désactivé**, puis définissez la durée de vos réunions, la marge entre elles et vos horaires préférés. Chaque demande apparaît dans **Activité**, sous **Agenda**.

Une période est considérée comme libre uniquement si votre agenda l’indique. Votre Machine ne propose aucune disponibilité si aucun agenda n’est connecté, s’il est impossible de le lire pendant une journée ou si la date est à plus de 30 jours. Les événements sur toute la journée sont considérés comme occupés s’ils sont marqués comme tels. Ceux qui sont marqués comme libres ne le sont jamais. Un événement sur toute la journée ajouté par une tâche est considéré comme libre, sauf si vous êtes absent ou avez réservé ces jours. Dans ce cas, il est indiqué comme « occupé » avant que vous l’ajoutiez.

Si la personne n’a pas de Machine ou ne répond pas, le brouillon de l’e-mail contient un lien qui lui permet de choisir une de vos disponibilités. Son choix apparaît comme une tâche avec l’option **Réserver**. Rien n’est réservé avant que vous appuyiez dessus.

Le lien affiche uniquement les disponibilités, selon les mêmes règles, et aucune autre information sur vous. Il expire une fois la réunion réservée ou au bout de 14 jours. Dans l’e-mail, il apparaît sous le nom « Choisir une heure ». En bas de la page, le texte indique « La Machine d’Alex a trouvé ces horaires. Lancez la vôtre. », avec votre prénom. Désactivez cette option avec **Pied de page des liens de réservation**. Chaque lien et chaque choix apparaissent dans **Activité**.

## Une Machine sur votre propre ordinateur

Pour rejoindre le Network depuis une Machine que vous hébergez vous-même :

1. Dans le tableau de bord de votre Machine, ouvrez **Paramètres** et appuyez sur **Rejoindre le Network**.
2. Sur la page qui s’ouvre, connectez-vous (ou créez votre compte), puis confirmez. Votre Machine prend en compte le changement automatiquement, sans redémarrage.

La méthode avec le code fonctionne toujours : appuyez sur **Associer une Machine auto-hébergée** sur la page de votre compte, à l’adresse app.themachine.computer, puis exécutez `assistant fleet-pair` avec le code sur votre ordinateur et redémarrez. Le code ne fonctionne qu’une fois et expire au bout de 15 minutes.

Vous pouvez avoir jusqu’à 5 Machines par compte. Vous pouvez déconnecter chacune d’elles depuis cette page.
