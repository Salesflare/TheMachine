---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses urgentes vous alertent, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: dc56a77907df5da0
---
Vous voulez moins de notifications ou des notifications différentes ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion, une question sur Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, lorsqu’elles reviennent.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type dispose d’un interrupteur pour **Push** (l’app sur votre téléphone ou ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine sur The Machine Network. Tout est activé, sauf les récaps sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : jours de travail, horaires d’envoi des notifications, heure de retour des tâches mises en attente, horaires des récaps et fuseau horaire. Voir [Heures de travail](work-hours.md).

## Seules les choses urgentes

Une notification Push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse que quelqu’un attend, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche qui revient à l’heure que vous avez choisie après avoir été mise en attente.

Tout le reste apparaît discrètement sur le tableau de bord (et sans alerte sur Telegram) et attend le récap du matin. Un jour de congé, seules les choses urgentes ou à échéance aujourd’hui déclenchent une alerte. Vous recevez au maximum 8 notifications Push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, seul le récap du matin vous est envoyé jusqu’à votre retour.

## Quand les notifications sont envoyées

L’app vérifie si vous utilisez vraiment le tableau de bord, pas seulement s’il est ouvert :

- En cours d’utilisation (au premier plan, avec un clic, une saisie ou un défilement au cours des 10 dernières minutes) : aucune alerte. Telegram arrive sans alerte. Ouvrir ou actualiser le tableau de bord ne suffit pas.
- Absente (en arrière-plan, fermée ou inactive depuis 10 minutes) : une notification Push est envoyée une minute après votre départ, sauf si vous êtes revenue et l’avez vue.
- Si vous n’avez rien reçu 15 minutes plus tard et que ça ne peut pas attendre : un e-mail est envoyé, au maximum un par heure. Les éléments que vous avez vus ou traités sont exclus, et chaque tâche n’y figure qu’une fois, dans son état actuel. La plupart du temps, le récap du matin est le seul e-mail.
- Une notification est considérée comme reçue si elle s’est affichée sur votre téléphone ou dans votre navigateur, ou si Telegram a accepté le message. Un téléphone éteint, hors ligne ou dont les notifications sont désactivées ne compte pas. Telegram ne compte pas non plus lorsque le tableau de bord est utilisé. Si la notification s’est affichée uniquement sur un ordinateur, les éléments urgents ou à échéance aujourd’hui sont tout de même envoyés par e-mail : vous êtes peut-être absente.
- Vous n’avez pas d’app mobile, de notifications du navigateur ni de Telegram ? L’e-mail est envoyé pour tous les éléments ci-dessus.
- Telegram est injoignable : la notification Push est tout de même envoyée, une fois, et l’app réessaie automatiquement sur Telegram.
- Un collègue vous confie une tâche et votre Machine ne peut pas vous joindre par téléphone ni sur Telegram : un e-mail avec son titre et un lien est envoyé 15 minutes plus tard si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- Votre connexion à Claude expire dans les 3 jours ou a expiré : un e-mail avec **Se reconnecter** est envoyé une fois par connexion. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- En dehors de vos heures de travail : aucune notification. Le récap du matin vous en informera.
- Une nouvelle tâche de travail créée un jour de congé attend l’heure du récap de votre prochain jour de travail. La tâche indique quand la notification vous parviendra, par exemple : Notification lun. 2 nov. · 08:30.

Les modifications et la progression ne déclenchent jamais de notification. Si un nouveau résultat concerne une tâche que vous n’avez pas encore vue, il la met à jour sans envoyer de nouvelle notification. Une série de notifications déclenche une seule alerte. L’icône de l’app indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’app mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Réponse nécessaire, tâche bloquée ou connexion requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez-le pour l’ouvrir.

Le navigateur et Telegram en affichent deux. Pour les questions Fleet, les boutons **Répondre** et **Refuser** restent disponibles.

Aucune notification ne permet d’envoyer, de payer ou de soumettre quoi que ce soit. Un brouillon s’ouvre toujours d’abord, pour que vous puissiez le vérifier avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste avec le brouillon complet. **Faire** lance simplement le travail sur une nouvelle tâche.

Dans l’app mobile, vous devez d’abord déverrouiller votre téléphone pour utiliser **Mettre en attente** ou **Marquer comme fait**. Dans un navigateur, ces boutons ouvrent le tableau de bord, où l’action est effectuée et où l’option d’annulation s’affiche. **Mettre en attente** fait revenir la tâche dans deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens **Ouvrir** (et **Mettre en attente** pour les éléments en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche en surbrillance dans votre liste, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle affiche la tâche dès qu’elle l’est.

## Le récap du matin

Il est envoyé les jours de travail à l’heure définie dans **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure est antérieure à **Les mises en attente reviennent à**, le récap attend 5 minutes après cette heure, afin d’inclure les tâches qui reviennent ce matin-là. **Aperçu** permet de le consulter sans l’envoyer. Par défaut, il est envoyé par notification Push et par e-mail, dans un format assez court pour être lu en un coup d’œil :

- une salutation qui résume l’essentiel de la journée, comme « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, en attente de votre accord : envoyer le bon de commande ». Seules les tâches avec un brouillon ou un résultat à approuver sont considérées comme prêtes. Une tâche qui nécessite d’abord votre réponse ne l’est pas ;
- les tâches comptabilisées dans la salutation, chacune avec un lien **Ouvrir**, ainsi que celles à échéance aujourd’hui. Sinon, jusqu’à trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre intervention, quel que soit le nombre indiqué dans la salutation ;
- le nombre d’autres tâches qui peuvent attendre, et le temps nécessaire à votre rythme, par exemple : « 12 autres peuvent attendre, environ 5 min pour les traiter. » Les tâches qui attendent votre réponse ne sont pas comptées dans ce temps. Une tâche à échéance aujourd’hui mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est pas comptée tant qu’elle n’attend pas votre intervention. Le nombre correspond aux tâches en attente dans votre liste.
- vos réunions sur une seule ligne.

**Ouvrir** affiche la tâche en surbrillance dans votre liste, même si elle est terminée ou mise en attente. Une promesse ouvre sa tâche ou, si elle n’en a pas encore, sa propre page.

La notification Push contient le même texte, sans liens. Touchez-la, ou le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours de travail, à l’heure définie dans **Heures de travail**, 15 minutes avant **Jusqu’à** par défaut, selon les modes choisis dans la ligne ci-dessus. Il est envoyé uniquement les jours où vous avez été présente : vous avez utilisé le tableau de bord ou fait un choix concernant une tâche, sur le tableau de bord, dans Telegram, dans le chat ou à la voix. Il n’y a pas de récap les jours où aucune tâche n’a été terminée et où aucune réunion n’a eu lieu.

Il commence par un bilan de la journée, comme « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis affiche une partie **Travail** et une partie **Perso**. Les parties vides ne sont pas affichées. Les alertes concernant votre Machine ne figurent dans aucune des deux parties. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, par exemple « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou votre prochain jour de travail si c’est vendredi) : les premières réunions et les tâches à échéance.

Le récap se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification Push ou le lien à la fin de l’e-mail pour le relire, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez sa ligne.

## Confidentialité

La notification Push est envoyée directement de votre Machine à votre appareil, où elle est chiffrée. L’e-mail passe par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que les nombres. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications Push pour un appareil dans **Cet appareil**, ou consultez [Installer l’app](phone-app.md). L’[app mobile](mobile-app.md) envoie une simple ligne via Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
