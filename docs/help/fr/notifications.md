---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses urgentes déclenchent une alerte, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: aab523e3a774400b
---
Vous voulez moins de notifications, ou en recevoir d’autres ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion ou une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, lorsqu’elles reviennent.
- **Récap du matin** : un bref récap de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type a un bouton pour **Push** (l’app sur votre téléphone ou votre ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou sur une Machine du The Machine Network. Tout est activé, sauf les récapitulatifs sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les heures auxquelles les notifications peuvent être envoyées, le moment où les tâches mises en attente reviennent, les heures des récapitulatifs et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse attendue par quelqu’un, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et sans alerte sur Telegram) et attend le récap du matin. Un jour de congé, seules les choses urgentes ou à échéance aujourd’hui déclenchent une alerte. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récap du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

L’application vérifie si vous utilisez réellement le tableau de bord, et pas seulement s’il est ouvert :

- Vous l’utilisez (il est au premier plan et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune alerte. Les messages Telegram arrivent sans alerte. Le simple fait d’ouvrir ou de recharger le tableau de bord ne compte pas.
- Vous êtes absent (l’application est en arrière-plan, fermée ou inactive depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Si la notification est toujours sans réponse 15 minutes plus tard et ne peut pas attendre, un seul e-mail est envoyé, au maximum un par heure. Les choses dont vous vous êtes déjà occupé sont exclues. La plupart du temps, le récap du matin est le seul e-mail envoyé.
- Si un membre de l’équipe vous confie une tâche et que votre Machine ne peut pas vous joindre par téléphone ou sur Telegram, un e-mail avec son titre et un lien est envoyé 15 minutes plus tard si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- En dehors de vos heures de travail : aucune notification. La tâche apparaîtra dans le récap du matin.
- Une nouvelle tâche professionnelle reçue un jour de congé attend l’heure du récap de votre prochain jour travaillé. La tâche indique quand vous la recevrez, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Si un nouveau résultat arrive pour une tâche que vous n’avez pas encore vue, il la met à jour sans envoyer de nouvelle notification. Une série de notifications rapprochées ne déclenche qu’une seule alerte. L’icône de l’application indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : Faire, Mettre en attente, Marquer comme fait.
- Brouillon prêt : Ouvrir le brouillon, Mettre en attente, Marquer comme fait.
- Résultat prêt : Ouvrir, Marquer comme fait, Mettre en attente.
- Question, blocage ou connexion nécessaire : Répondre, Ouvrir ou Se connecter, puis Mettre en attente et Marquer comme fait.
- Rappel : Marquer comme fait, Mettre en attente, Ouvrir.
- Récap du matin : touchez-le pour l’ouvrir.

Le navigateur et Telegram affichent deux de ces boutons. Pour les questions de Fleet, les boutons Répondre et Refuser restent disponibles.

Aucun contenu n’est envoyé, payé ou soumis depuis une notification. Un brouillon s’ouvre toujours en premier, pour que vous puissiez le vérifier avant son envoi. Ouvrir le brouillon affiche la tâche dans votre liste et son brouillon en entier. Faire lance le travail uniquement pour une nouvelle tâche.

Dans l’application mobile, Mettre en attente et Marquer comme fait vous demandent d’abord de déverrouiller l’appareil. Dans un navigateur, ces boutons ouvrent le tableau de bord, qui effectue l’action et affiche Annuler. Mettre en attente fait revenir la tâche dans deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens Ouvrir (et Mettre en attente pour les tâches en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou le lien Ouvrir dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou dans une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle affiche la tâche dès qu’elle le sera.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure définie pour **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure précède celle de **Les mises en attente reviennent à**, il est envoyé 5 minutes après cette dernière, pour inclure les tâches qui reviennent ce matin-là. **Aperçu** permet de le consulter sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail, dans un format assez court pour être lu d’un coup d’œil :

- un message d’accueil avec les éléments importants du jour, par exemple « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, à valider : Envoyer le bon de commande » ;
- les tâches mentionnées dans le message d’accueil, chacune avec un lien Ouvrir, ainsi que les tâches à échéance aujourd’hui ; s’il n’y en a pas, jusqu’à trois tâches à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui nécessitent votre attention, qu’elles soient mentionnées ou non dans le message d’accueil ;
- le nombre d’autres tâches qui peuvent attendre et le temps nécessaire à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour les traiter ». Les tâches qui attendent votre réponse ne sont pas incluses dans cette durée. Une tâche à échéance aujourd’hui, mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est pas comptée tant qu’elle ne nécessite pas votre attention. Le nombre correspond aux tâches en attente dans votre liste ;
- vos réunions, sur une seule ligne.

Ouvrir affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou mise en attente. Une promesse ouvre sa tâche, ou sa propre page si elle n’a pas encore de tâche.

La notification push reprend les mêmes informations sans les liens. Touchez-la, ou le lien à la fin de l’e-mail, pour relire le récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure définie dans **Heures de travail**, soit par défaut 15 minutes avant **Jusqu’à**, selon les modes choisis dans la ligne correspondante ci-dessus. Il n’est envoyé que les jours où vous avez été actif : vous avez utilisé le tableau de bord ou fait un choix concernant une tâche, sur le tableau de bord, dans Telegram, dans le chat ou à la voix. Il n’est pas envoyé les jours où aucune tâche n’a été terminée et aucune réunion n’a eu lieu.

Il commence par un bilan de la journée, par exemple « Bonsoir Sam, 4 tâches faites aujourd’hui », puis comporte une partie **Travail** et une partie **Perso**. Les parties vides sont omises. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, par exemple « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou votre prochain jour travaillé, si c’est vendredi) : les premières réunions et les tâches à échéance.

Le récap se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le relire, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez la ligne correspondante.

## Confidentialité

Les notifications push sont envoyées directement par votre Machine à votre appareil, où elles sont chiffrées. Les e-mails passent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque le niveau [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que le nombre de tâches. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) envoie une ligne de texte à Apple ou Google, puis demande le titre et l’étape suivante à votre Machine.
