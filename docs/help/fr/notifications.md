---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses qui ne peuvent pas attendre vous alertent, le reste figure dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: febea6f9eb2c331a
---
Moins de notifications, ou des notifications différentes ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une connexion nécessaire à une tâche ou une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez qui reviennent.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type a un bouton pour **Push** (l’application sur votre téléphone ou votre ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou sur The Machine Network. Tout est activé, sauf les récaps sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les horaires d’envoi des notifications, le retour des tâches mises en attente, les horaires des récaps et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse attendue, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et sans alerte sur Telegram) et attend le récap du matin. Un jour de congé, seules les choses urgentes ou à échéance aujourd’hui déclenchent une alerte. Vous recevrez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevrez que le récap du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

The Machine vérifie si vous utilisez vraiment le tableau de bord, pas seulement s’il est ouvert :

- Si vous l’utilisez (il est au premier plan et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes), aucune alerte n’est envoyée. Les notifications Telegram arrivent sans alerte. Le simple fait d’ouvrir ou de recharger le tableau de bord ne compte pas.
- Si vous êtes absent (le tableau de bord est en arrière-plan, fermé ou inactif depuis 10 minutes), une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Si la notification n’a toujours pas été vue 15 minutes plus tard et que la tâche ne peut pas attendre, un seul e-mail est envoyé, au maximum une fois par heure. Les éléments que vous avez déjà traités sont exclus, et chaque tâche n’y figure qu’une fois, dans son état actuel. La plupart du temps, le récap du matin est le seul e-mail envoyé.
- Si un collègue vous confie une tâche et que votre Machine ne peut pas vous joindre par téléphone ou sur Telegram, un e-mail contenant son titre et un lien est envoyé 15 minutes plus tard si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour empêcher cela.
- En dehors de vos heures de travail, aucune notification n’est envoyée. La tâche figure dans le récap du matin.
- Une nouvelle tâche professionnelle reçue un jour non travaillé attend l’heure d’envoi du récap de votre prochain jour travaillé. La tâche indique quand elle vous parviendra, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Si un nouveau résultat apparaît pour une tâche que vous n’avez pas encore vue, il est ajouté sans nouvelle notification. Une série de notifications déclenche une seule alerte. L’icône de l’application indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : Faire, Mettre en attente, Marquer comme fait.
- Brouillon prêt : Ouvrir le brouillon, Mettre en attente, Marquer comme fait.
- Résultat prêt : Ouvrir, Marquer comme fait, Mettre en attente.
- Question, blocage ou connexion nécessaire : Répondre, Ouvrir ou Se connecter, puis Mettre en attente et Marquer comme fait.
- Rappel : Marquer comme fait, Mettre en attente, Ouvrir.
- Récap du matin : touchez-le pour l’ouvrir.

Un navigateur et Telegram en affichent deux. Pour les questions Fleet, les boutons Répondre une fois et Refuser restent disponibles.

Aucun contenu n’est envoyé, payé ou soumis depuis une notification. Un brouillon s’ouvre toujours d’abord, pour que vous puissiez le voir avant son envoi. Ouvrir le brouillon affiche la tâche dans votre liste avec son brouillon complet. Faire lance le travail uniquement pour une nouvelle tâche.

Dans l’application mobile, Mettre en attente et Marquer comme fait vous demandent d’abord de déverrouiller l’application. Dans un navigateur, ces boutons ouvrent le tableau de bord, qui effectue l’action et affiche Annuler. Mettre en attente fait revenir la tâche dans deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens Ouvrir (et Mettre en attente pour les éléments en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou Ouvrir dans un e-mail ou sur Telegram, la tâche apparaît dans votre liste, en surbrillance, où qu’elle se trouve maintenant : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle suit la tâche dès qu’elle le devient.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure définie dans **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure précède **Les mises en attente reviennent à**, il attend 5 minutes après cet horaire pour inclure les tâches qui reviennent ce matin-là. **Aperçu** affiche le récap sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail. Il est assez court pour être lu en un coup d’œil :

- un message d’accueil indiquant l’essentiel de la journée, par exemple « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, votre accord est attendu : Envoyer le bon de commande ». Seules les tâches avec un brouillon ou un résultat à approuver comptent comme prêtes. Une tâche qui attend d’abord votre réponse ne compte pas ;
- les tâches comptabilisées dans le message d’accueil, chacune avec un lien Ouvrir, ainsi que celles à échéance aujourd’hui. Sinon, jusqu’à trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre intervention, quel que soit le nombre indiqué dans le message d’accueil ;
- le nombre de tâches qui peuvent attendre et le temps qu’il vous faudra pour les traiter à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour tout régler. » Les tâches qui attendent votre réponse ne sont pas incluses dans ce temps. Une tâche à échéance aujourd’hui mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est comptée que lorsqu’elle attend votre intervention. Le nombre correspond aux tâches en attente dans votre liste ;
- vos réunions, sur une seule ligne.

Ouvrir affiche la tâche dans votre liste, en surbrillance, même si elle est terminée ou mise en attente. Une promesse ouvre la tâche correspondante, ou sa propre page si elle n’a pas encore de tâche.

La notification push contient le même texte, sans liens. Touchez-la, ou utilisez le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure définie dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les modes choisis dans sa ligne ci-dessus. Il est envoyé uniquement les jours où vous étiez présent : vous avez utilisé le tableau de bord ou pris une décision sur une tâche, là, sur Telegram, dans le chat ou par la voix. Il n’y a pas de récap pour une journée sans tâche terminée ni réunion tenue.

Il commence par un bilan chiffré de la journée, par exemple « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis une partie **Travail** et une partie **Perso**. Les parties vides sont omises. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, par exemple « +3 réunions : Appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou votre prochain jour travaillé si nous sommes vendredi) : les premières réunions et les tâches à échéance.

Il se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le relire, avec **Copier Travail** et **Copier Perso**. Pour arrêter de le recevoir, désactivez sa ligne.

## Confidentialité

La notification push est envoyée directement de votre Machine à votre appareil, où elle est chiffrée. Les e-mails transitent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque [Mode prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que des nombres. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) envoie une ligne de texte simple par Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
