---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses urgentes vous alertent, le reste arrive dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: bdb4ecec9446aa5e
---
Moins de notifications, ou d’autres notifications ? Dans **Paramètres**, ouvrez **Notifications** pour choisir où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion ou une question sur Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type de notification dispose d’une option pour **Push** (l’application sur votre téléphone ou votre ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine sur The Machine Network. Tout est activé, sauf les récaps sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les heures d’envoi des notifications, l’heure de retour des tâches mises en attente, les horaires des récaps et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse que quelqu’un attend, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure choisie.

Tout le reste apparaît discrètement sur le tableau de bord, et sans alerte dans Telegram, en attendant le récap du matin. Un jour de congé, seules les choses urgentes ou à échéance aujourd’hui déclenchent une alerte. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récap du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

L’application vérifie si vous utilisez réellement le tableau de bord, et pas seulement s’il est ouvert :

- Vous l’utilisez (il est au premier plan et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune alerte. Les notifications Telegram arrivent sans alerte. Ouvrir ou actualiser le tableau de bord ne suffit pas.
- Vous êtes absent·e (le tableau de bord est en arrière-plan, fermé ou inactif depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu·e et l’avez vue.
- Elle n’a toujours pas été vue 15 minutes plus tard et ne peut pas attendre : un seul e-mail est envoyé, à raison d’un maximum par heure. Les éléments que vous avez déjà traités sont exclus, et chaque tâche n’apparaît qu’une fois, dans son état actuel. La plupart du temps, le récap du matin est le seul e-mail que vous recevez.
- Un collègue vous confie une tâche et votre Machine ne peut pas vous joindre par téléphone ni sur Telegram : un e-mail contenant son titre et un lien est envoyé après 15 minutes si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- En dehors de vos heures de travail : aucune notification. Le récap du matin inclut ces éléments.
- Une nouvelle tâche professionnelle reçue un jour de congé attend l’heure du récap de votre prochain jour travaillé. La tâche indique quand vous la recevrez, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Un nouveau résultat sur une tâche que vous n’avez pas encore vue s’ajoute à la notification existante, sans en envoyer une nouvelle. Une série de notifications ne déclenche qu’une seule alerte. L’icône de l’application indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Votre réponse est nécessaire, une tâche est bloquée ou une connexion est requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez la notification pour l’ouvrir.

Un navigateur et Telegram n’en affichent que deux. Pour les questions Fleet, les boutons **Répondre** et **Refuser** restent disponibles.

Aucun envoi, paiement ni envoi de formulaire n’est effectué depuis une notification. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le consulter avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste et son brouillon en entier. **Faire** ne lance le travail que pour une nouvelle tâche.

Dans l’application mobile, **Mettre en attente** et **Marquer comme fait** vous demandent d’abord de déverrouiller votre téléphone. Dans un navigateur, ces boutons ouvrent le tableau de bord, qui effectue l’action et affiche l’option d’annulation. Une tâche mise en attente revient au bout de deux heures, ou le lendemain matin pour un rappel.

Les e-mails contiennent des liens **Ouvrir** et, pour les éléments en attente, **Mettre en attente**. Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche en surbrillance dans votre liste, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle affiche la tâche dès qu’elle l’est.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure définie pour **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure précède **Les mises en attente reviennent à**, l’envoi attend 5 minutes après cette heure afin d’inclure les tâches qui reviennent ce matin-là. **Aperçu** permet de le consulter sans l’envoyer. Par défaut, vous le recevez par notification push et par e-mail. Il est assez court pour être lu en un coup d’œil :

- une salutation qui résume l’essentiel de la journée, par exemple « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, il ne manque que votre accord : envoyer le bon de commande ». Seules les tâches avec un brouillon ou un résultat à approuver sont considérées comme prêtes. Une tâche qui nécessite d’abord votre réponse ne l’est pas ;
- les tâches mentionnées dans la salutation, chacune avec un lien **Ouvrir**, ainsi que les tâches à échéance aujourd’hui. Sinon, le récap présente au maximum trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre intervention, quel que soit le nombre indiqué dans la salutation ;
- le nombre de tâches supplémentaires qui peuvent attendre et le temps nécessaire pour les traiter à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour les traiter ». Les tâches qui attendent votre réponse ne sont pas comprises dans ce temps. Une tâche à échéance aujourd’hui, mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est comptée que lorsqu’elle attend votre intervention. Le nombre correspond aux tâches en attente dans votre liste ;
- vos réunions, sur une seule ligne.

**Ouvrir** affiche la tâche en surbrillance dans votre liste, même si elle est terminée ou mise en attente. Une promesse ouvre la tâche correspondante, ou sa propre page si elle n’en a pas encore.

La notification push reprend le même texte, sans les liens. Touchez-la, ou le lien à la fin de l’e-mail, pour retrouver ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure définie dans **Heures de travail**, 15 minutes avant **Jusqu’à** par défaut, selon les moyens choisis dans la ligne correspondante ci-dessus. Il est envoyé uniquement les jours où vous avez été actif·ve : vous avez utilisé le tableau de bord ou choisi une action pour une tâche, dans Telegram, dans le chat ou à la voix. Vous ne le recevez pas un jour sans tâche terminée ni réunion tenue.

Il commence par un bilan de la journée, par exemple « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis une section **Travail** et une section **Perso**. Les sections vides ne sont pas affichées. Les alertes concernant votre Machine n’apparaissent dans aucune des deux sections. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, suivies de « +12 autres » et des réunions de la journée, par exemple « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (le prochain jour travaillé si nous sommes vendredi) : les premières réunions et les tâches à échéance.

Il se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le consulter à nouveau, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez l’option correspondante.

## Confidentialité

Les notifications push sont envoyées directement de votre Machine à votre appareil, où elles sont chiffrées. Les e-mails passent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque le mode [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’indiquent que leur nombre. Désactivez **E-mail** pour un type de notification si vous ne souhaitez pas le recevoir par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) envoie une ligne de texte simple via Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
