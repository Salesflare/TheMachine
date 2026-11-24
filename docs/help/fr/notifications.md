---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les notifications urgentes vous alertent, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3c469ec1032f6bea
---
Vous préférez recevoir moins de notifications, ou des notifications différentes ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche due aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion ou une question dans Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, lorsqu’elles reviennent.
- **Récap du matin** : un récap succinct de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type comporte une option pour **Push** (l’application sur votre téléphone ou ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine sur The Machine Network. Toutes ces options sont activées, sauf les récaps sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les heures auxquelles les notifications peuvent être envoyées, le moment où les tâches mises en attente reviennent, les heures des récaps et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Vous recevez une notification Push, une alerte Telegram ou un e-mail uniquement pour :

- une tâche dont l’échéance est aujourd’hui ou qui est marquée comme urgente ;
- une réponse attendue par quelqu’un, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient au moment choisi.

Tout le reste apparaît discrètement sur le tableau de bord (et silencieusement sur Telegram) et attend le récap du matin. Un jour de congé, seules les tâches urgentes ou dues aujourd’hui vous alertent. Vous recevez au maximum 8 notifications Push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récap du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

L’application vérifie si vous utilisez vraiment le tableau de bord, pas seulement s’il est ouvert :

- Vous l’utilisez (il est au premier plan et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune alerte. Les notifications Telegram arrivent silencieusement. Le simple fait d’ouvrir ou de recharger la page ne compte pas.
- Vous êtes absent (l’application est en arrière-plan, fermée ou inactive depuis 10 minutes) : une notification Push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Vous n’avez rien reçu au bout de 15 minutes et la notification ne peut pas attendre : un seul e-mail est envoyé, au maximum une fois par heure. Les éléments que vous avez vus ou traités sont exclus, et chaque tâche n’y figure qu’une fois, dans son état actuel. La plupart du temps, le récap du matin est le seul e-mail envoyé.
- Une notification est considérée comme reçue lorsqu’elle s’affiche sur votre téléphone ou dans votre navigateur, ou lorsque Telegram reçoit le message. Un téléphone éteint, hors ligne ou dont les notifications sont désactivées ne compte pas. Les notifications Telegram ne comptent pas non plus lorsque vous utilisez le tableau de bord. Si la notification s’affiche uniquement sur un ordinateur, les éléments urgents ou dus aujourd’hui vous sont tout de même envoyés par e-mail : vous êtes peut-être absent.
- Vous n’avez pas d’application mobile, de notifications dans le navigateur ni Telegram ? Vous recevez un e-mail pour tous les éléments ci-dessus.
- Telegram est inaccessible : la notification Push est tout de même envoyée, une seule fois, et l’application réessaie d’envoyer le message sur Telegram automatiquement.
- Un collègue vous confie une tâche et votre Machine n’a ni téléphone ni Telegram pour vous joindre : vous recevez un seul e-mail avec son titre et un lien, après 15 minutes si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour ne plus le recevoir.
- En dehors de vos heures de travail : aucune notification. Le récap du matin inclut la tâche.
- Une nouvelle tâche professionnelle ajoutée un jour de congé attend l’heure de votre récap du prochain jour travaillé. La tâche indique quand vous la recevrez, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Si un nouveau résultat concerne une tâche que vous n’avez pas encore vue, il la met à jour sans envoyer de nouvelle notification. Plusieurs notifications rapprochées n’en déclenchent qu’une seule. L’icône de l’application indique combien de tâches attendent votre attention.

## Boutons des notifications

Chaque notification comporte des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Une réponse est nécessaire, une tâche est bloquée ou une connexion est requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez-le pour l’ouvrir.

Le navigateur et Telegram affichent deux de ces boutons. Pour les questions Fleet, les boutons **Répondre** et **Refuser** restent disponibles une seule fois.

Aucune notification ne permet d’envoyer, de payer ou de soumettre quoi que ce soit. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le vérifier avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste avec le brouillon complet. **Faire** lance le travail uniquement pour une nouvelle tâche.

Dans l’application mobile, **Mettre en attente** et **Marquer comme fait** vous demandent d’abord de déverrouiller l’application. Dans un navigateur, ils ouvrent le tableau de bord, qui effectue l’action et affiche **Annuler**. **Mettre en attente** fait revenir la tâche dans deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens **Ouvrir** (et **Mettre en attente** pour les tâches en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’est pas encore à jour, elle suit la tâche dès qu’elle l’est.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure indiquée dans **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure précède celle de **Les mises en attente reviennent à**, il attend 5 minutes après cette dernière pour inclure les tâches qui reviennent ce matin-là. **Aperçu** permet de le consulter sans l’envoyer. Par défaut, il est envoyé par Push et par e-mail, dans un format assez court pour être lu d’un coup d’œil :

- un message d’accueil qui indique ce qui compte aujourd’hui, par exemple « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, en attente de votre accord : envoyer le bon de commande ». Seules les tâches avec un brouillon ou un résultat à approuver sont considérées comme prêtes. Une tâche qui nécessite d’abord votre réponse ne l’est pas ;
- les tâches mentionnées dans le message d’accueil, chacune avec un lien **Ouvrir**, et celles qui sont dues aujourd’hui. Sinon, au maximum trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre attention, quel que soit le nombre indiqué dans le message d’accueil ;
- le nombre d’autres tâches qui peuvent attendre et le temps nécessaire pour les traiter à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour tout régler ». Les tâches qui attendent votre réponse ne sont pas incluses dans ce temps. Une tâche due aujourd’hui, mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est pas comptabilisée tant qu’elle n’attend pas votre attention. Le nombre correspond aux tâches en attente dans votre liste ;
- vos réunions, sur une seule ligne.

Le lien **Ouvrir** affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou mise en attente. Une promesse ouvre sa tâche, ou sa propre page si elle n’en a pas encore.

La notification Push contient le même texte, sans liens. Touchez-la, ou le lien en bas de l’e-mail, pour consulter à nouveau ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure indiquée dans **Heures de travail**. Par défaut, il est envoyé 15 minutes avant **Jusqu’à**, selon les méthodes choisies dans la ligne ci-dessus. Vous le recevez uniquement les jours où vous avez été actif : vous avez utilisé le tableau de bord ou fait un choix sur une tâche, sur Telegram, dans le chat ou par la voix. Vous n’en recevez pas les jours où aucune tâche n’a été terminée et aucune réunion n’a eu lieu.

Il commence par un récapitulatif de la journée, par exemple « Bonsoir Sam, 4 tâches faites aujourd’hui », puis comporte une partie **Travail** et une partie **Perso**. Les parties vides sont omises. Les alertes concernant votre Machine n’apparaissent dans aucune des deux. Chaque partie comprend :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions du jour, par exemple « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé si le récap est envoyé un vendredi) : les premières réunions et les tâches dues.

Il se termine par le nombre de tâches qui attendent encore votre attention. Touchez la notification Push, ou le lien en bas de l’e-mail, pour le consulter à nouveau, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez la ligne correspondante.

## Confidentialité

Les notifications Push sont envoyées directement de votre Machine à votre appareil et chiffrées pour celui-ci. Les e-mails passent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque le mode [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’indiquent que leur nombre. Désactivez **E-mail** pour un type de notification afin de ne plus le recevoir par e-mail.

Activez les notifications Push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) envoie d’abord une ligne de texte brut par Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
