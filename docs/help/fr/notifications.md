---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses urgentes vous alertent, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
Vous voulez moins de notifications, ou des notifications différentes ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une connexion nécessaire à une tâche ou une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, lorsqu’elles reviennent.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type de notification a une option pour **Push** (l’app sur votre téléphone ou votre ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine sur The Machine Network. Tout est activé, sauf les récapitulatifs sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : jours travaillés, plages horaires d’envoi des notifications, heure de retour des tâches mises en attente, horaires des récapitulatifs et fuseau horaire. Voir [Heures de travail](work-hours.md).

## Seulement ce qui ne peut pas attendre

Une notification push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse que quelqu’un attend, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et sans alerte sur Telegram) et attend le récap du matin. Un jour de congé, seules les tâches urgentes ou à échéance aujourd’hui vous alertent. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récap du matin, jusqu’à votre retour.

## Quand les notifications arrivent

L’app vérifie si vous utilisez réellement le tableau de bord, et pas seulement s’il est ouvert :

- En cours d’utilisation (au premier plan, et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune alerte. Les notifications Telegram arrivent sans alerte. Le simple fait d’ouvrir ou d’actualiser le tableau de bord ne compte pas.
- Absent (en arrière-plan, fermée ou inactive depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Si la notification n’a toujours pas été vue 15 minutes plus tard et que la tâche ne peut pas attendre, un e-mail est envoyé, au maximum un par heure. Les éléments que vous avez déjà traités sont exclus. La plupart du temps, le récap du matin est le seul e-mail envoyé.
- Si un membre de l’équipe vous confie une tâche et que votre Machine ne peut pas vous joindre par téléphone ou sur Telegram, un e-mail contenant son titre et un lien est envoyé 15 minutes plus tard, si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour empêcher l’envoi de cet e-mail.
- En dehors de vos heures de travail : aucune notification. La tâche apparaît dans le récap du matin.
- Une nouvelle tâche professionnelle reçue un jour non travaillé attend l’heure du récap de votre prochain jour travaillé. La tâche indique quand elle vous sera transmise, par exemple Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications n’envoient jamais de notification. Un nouveau résultat pour une tâche que vous n’avez pas encore vue la met à jour sans envoyer de nouvelle notification. Une série de notifications déclenche une seule alerte. L’icône de l’app indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’app mobile :

- Nouvelle tâche : Faire, Mettre en attente, Marquer comme fait.
- Brouillon prêt : Ouvrir le brouillon, Mettre en attente, Marquer comme fait.
- Résultat prêt : Ouvrir, Marquer comme fait, Mettre en attente.
- Question, blocage ou connexion nécessaire : Répondre, Ouvrir ou Se connecter, puis Mettre en attente et Marquer comme fait.
- Rappel : Marquer comme fait, Mettre en attente, Ouvrir.
- Récap du matin : touchez-le pour l’ouvrir.

Un navigateur et Telegram en affichent deux. Pour les questions de Fleet, les boutons Répondre et Refuser restent disponibles.

Aucun envoi, paiement ou envoi de formulaire n’est effectué depuis une notification. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le consulter avant son envoi. Ouvrir le brouillon affiche la tâche dans votre liste et son brouillon en entier. Faire lance le travail uniquement pour une nouvelle tâche.

Dans l’app mobile, Mettre en attente et Marquer comme fait vous demandent d’abord de déverrouiller l’app. Dans un navigateur, ils ouvrent le tableau de bord, qui effectue l’action et affiche Annuler. Mettre en attente fait revenir la tâche dans deux heures, ou le lendemain matin pour un rappel.

Les e-mails contiennent des liens Ouvrir (et Mettre en attente pour les éléments en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou le lien Ouvrir dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou dans une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle suit la tâche dès qu’elle l’est.

## Le récap du matin

Il arrive les jours travaillés à l’heure de votre **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure précède **Les mises en attente reviennent à**, le récap attend 5 minutes après cette heure pour inclure les tâches qui reviennent ce matin-là. **Aperçu** affiche le récap sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail, et suffisamment court pour être lu d’un coup d’œil :

- un message d’accueil indiquant l’essentiel de la journée, par exemple « Bonjour Sam, 2 réponses sont prêtes à être envoyées » ou, pour une seule tâche, « Bonjour Sam, en attente de votre accord : Envoyer le bon de commande ». Seules les tâches avec un brouillon ou un résultat à approuver sont considérées comme prêtes ; une tâche qui attend d’abord votre réponse ne l’est pas ;
- les tâches comptées dans le message d’accueil, chacune avec un lien Ouvrir, ainsi que les tâches à échéance aujourd’hui ; sinon, au maximum trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre intervention, quel que soit le nombre indiqué dans le message d’accueil ;
- le nombre d’autres tâches qui peuvent attendre et le temps nécessaire pour les traiter à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour les traiter ». Le temps indiqué ne comprend pas les tâches qui attendent votre réponse. Une tâche à échéance aujourd’hui, mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est comptée que lorsqu’elle attend votre intervention. Le nombre correspond aux tâches en attente dans votre liste ;
- vos réunions sur une seule ligne.

Ouvrir affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou mise en attente. Une promesse ouvre sa tâche, ou sa propre page si elle n’en a pas encore.

La notification push reprend le même contenu sans les liens. Touchez-la, ou le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

## Le récap du soir

Il arrive une fois par jour travaillé, à l’heure définie dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les moyens choisis dans sa ligne ci-dessus. Il n’est envoyé que les jours où vous avez été actif : vous avez utilisé le tableau de bord ou pris une décision sur une tâche, sur Telegram, dans le chat ou à la voix. Vous ne le recevez pas un jour sans tâche terminée ni réunion tenue.

Il commence par un bilan de la journée, par exemple « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis comporte une partie **Travail** et une partie **Perso**. Les parties sans contenu sont omises. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, par exemple « +3 réunions : Appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé, si nous sommes vendredi) : les premières réunions et les tâches à échéance.

Le récap indique ensuite le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push, ou le lien à la fin de l’e-mail, pour le relire avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez sa ligne.

## Confidentialité

Les notifications push sont envoyées directement de votre Machine à votre appareil, où elles sont chiffrées. Les e-mails transitent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque le niveau [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que le nombre de tâches. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’app](phone-app.md). L’[app mobile](mobile-app.md) envoie une ligne de texte simple par Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
