---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses qui ne peuvent pas attendre vous alertent, le reste figure dans un seul récapitulatif matinal.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 2146426abe3eaa50
---
Vous voulez moins de notifications, ou en recevoir d’autres ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : seulement celles qui ne peuvent pas attendre, par exemple une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion, une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez.
- **Récap du matin** : un bref récapitulatif de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type dispose d’un bouton pour **Push** (l’application sur votre téléphone ou ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine sur The Machine Network. Tout est activé, sauf les récapitulatifs sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les heures auxquelles les notifications peuvent être envoyées, le moment où les tâches mises en attente reviennent, les horaires des récapitulatifs et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Seules les choses qui ne peuvent pas attendre

Une notification push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse que quelqu’un attend, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche qui revient après sa mise en attente, à l’heure choisie.

Tout le reste apparaît discrètement dans le tableau de bord (et sans alerte sur Telegram) et attend le récapitulatif du matin. Les jours de congé, seules les choses urgentes ou à échéance aujourd’hui vous alertent. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récapitulatif du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

The Machine vérifie si vous utilisez vraiment le tableau de bord, et pas seulement s’il est ouvert :

- En cours d’utilisation (au premier plan, et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune alerte. Les notifications Telegram arrivent sans alerte. Ouvrir ou recharger le tableau de bord ne suffit pas.
- Si vous êtes absent (l’application est en arrière-plan, fermée ou inactive depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Si la notification n’a toujours pas été vue 15 minutes plus tard et que la tâche ne peut pas attendre : un e-mail est envoyé, au maximum un par heure. Les tâches que vous avez déjà traitées sont exclues. La plupart du temps, le récapitulatif du matin est le seul e-mail envoyé.
- Si un collègue vous attribue une tâche et que votre Machine ne peut pas vous joindre par téléphone ou sur Telegram : un e-mail contenant son titre et un lien est envoyé 15 minutes plus tard si la tâche n’a toujours pas été vue. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- En dehors de vos heures de travail : aucune notification. La tâche figure dans le récapitulatif du matin.
- Une nouvelle tâche professionnelle reçue un jour de congé attend l’heure du récapitulatif de votre prochain jour travaillé. La tâche indique quand elle vous sera envoyée, par exemple Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Si un nouveau résultat arrive pour une tâche que vous n’avez pas encore vue, il la met à jour sans envoyer de nouvelle notification. Une série de notifications déclenche une seule alerte. L’icône de l’application indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : Faire, Mettre en attente, Marquer comme fait.
- Brouillon prêt : Ouvrir le brouillon, Mettre en attente, Marquer comme fait.
- Résultat prêt : Ouvrir, Marquer comme fait, Mettre en attente.
- Question, blocage ou connexion requise : Répondre, Ouvrir ou Se connecter, puis Mettre en attente et Marquer comme fait.
- Rappel : Marquer comme fait, Mettre en attente, Ouvrir.
- Récapitulatif du matin : touchez-le pour l’ouvrir.

Un navigateur et Telegram affichent deux de ces boutons. Pour les questions de Fleet, les boutons Répondre une fois et Refuser restent disponibles.

Une notification ne permet jamais d’envoyer, de payer ou de soumettre quoi que ce soit. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le vérifier avant son envoi. Ouvrir le brouillon affiche la tâche dans votre liste et son brouillon complet. Faire démarre uniquement le travail sur une nouvelle tâche.

Dans l’application mobile, Mettre en attente et Marquer comme fait vous demandent d’abord de déverrouiller l’application. Dans un navigateur, ces boutons ouvrent le tableau de bord, qui effectue l’action et affiche Annuler. Une tâche mise en attente revient dans deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens Ouvrir (et Mettre en attente pour les tâches en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou le lien Ouvrir dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle retrouve la tâche dès qu’elle l’est.

## Le récapitulatif du matin

Il est envoyé les jours travaillés à l’heure définie dans **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure est antérieure à **Les mises en attente reviennent à**, l’envoi est reporté jusqu’à 5 minutes après cet horaire, pour inclure les tâches qui reviennent ce matin-là. **Aperçu** vous permet de le consulter sans l’envoyer. Par défaut, il est envoyé sous forme de notification push et d’e-mail, et tient en quelques lignes :

- un message d’accueil qui indique ce qui compte aujourd’hui, par exemple « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, à valider : Envoyer le formulaire de commande » ;
- les tâches mentionnées dans le message d’accueil, chacune accompagnée d’un lien Ouvrir, ainsi que celles qui arrivent à échéance aujourd’hui ; sinon, jusqu’à trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre attention, quel que soit le nombre indiqué dans le message d’accueil ;
- le nombre de tâches supplémentaires qui peuvent attendre et le temps qu’il vous faudra pour les traiter à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour tout régler. » Les tâches qui attendent votre réponse ne sont pas incluses dans ce temps. Une tâche à échéance aujourd’hui mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est comptée que lorsqu’elle attend votre attention. Le nombre correspond aux tâches en attente dans votre liste.
- vos réunions, sur une seule ligne.

Ouvrir affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou en attente. Une promesse ouvre la tâche correspondante, ou sa propre page si elle n’en a pas encore.

La notification push affiche le même contenu, sans liens. Touchez-la, ou le lien à la fin de l’e-mail, pour relire ce récapitulatif dans **Tâches**.

## Le récapitulatif du soir

Il est envoyé une fois les jours travaillés à l’heure définie dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les modes choisis dans la ligne ci-dessus. Il n’est pas envoyé les jours où aucune tâche n’a été terminée et aucune réunion n’a eu lieu. Il commence par un bilan de la journée, par exemple « Bonsoir Sam, 4 tâches faites aujourd’hui », puis présente une partie **Travail** et une partie **Perso**. Les parties vides sont omises. Chaque partie comprend :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, par exemple « +3 réunions : Appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé, si nous sommes vendredi) : les premières réunions et les tâches à échéance.

Le récapitulatif se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push, ou le lien à la fin de l’e-mail, pour le relire, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez la ligne correspondante.

## Confidentialité

Les notifications push sont envoyées directement de votre Machine à votre appareil, et chiffrées pour celui-ci. Les e-mails passent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque [Précautionneux](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que les nombres. Désactivez **E-mail** pour un type de notification afin de ne plus le recevoir par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) reçoit une ligne de texte via Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
