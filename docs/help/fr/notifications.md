---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les notifications urgentes vous font vibrer. Le reste figure dans un seul récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3faac166e8f9fa3d
---
Vous voulez moins de notifications ou en recevoir d’autres ? Dans **Paramètres**, puis **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement celles qui ne peuvent pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion ou une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, quand elles reviennent.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qu’il reste à faire demain. Voir ci-dessous.

Chaque type dispose d’un interrupteur pour les **Push** (l’app sur votre téléphone ou votre ordinateur), **Telegram** une fois configuré et **E-mail** sur une Machine hébergée ou sur The Machine Network. Tout est activé, sauf les récapitulatifs sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les heures auxquelles les notifications peuvent arriver, le moment où les tâches en attente reviennent, les heures des récapitulatifs et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, une notification Telegram ou un e-mail vous est envoyé uniquement dans les cas suivants :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse attendue par quelqu’un, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et sans son sur Telegram), en attendant le récap du matin. Les jours de repos, seules les tâches urgentes ou à échéance aujourd’hui vous font vibrer. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récap du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

L’app vérifie si vous utilisez vraiment le tableau de bord, et pas seulement s’il est ouvert :

- Si vous l’utilisez (il est au premier plan et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes), rien ne vibre. Les notifications Telegram arrivent sans son. Ouvrir ou actualiser le tableau de bord ne suffit pas.
- Si vous êtes absent (l’app est en arrière-plan, fermée ou inactive depuis 10 minutes), une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Si la notification n’a toujours pas été vue 15 minutes plus tard et que la tâche ne peut pas attendre, un e-mail vous est envoyé, à raison d’un maximum par heure. Les tâches dont vous vous êtes déjà occupé sont exclues. Chaque tâche y figure une seule fois, dans son état actuel. La plupart du temps, le récap du matin est le seul e-mail envoyé.
- Si un collègue vous confie une tâche et que votre Machine ne peut pas vous joindre par téléphone ou sur Telegram, un e-mail contenant son titre et un lien vous est envoyé si elle n’a toujours pas été vue au bout de 15 minutes. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- En dehors de vos heures de travail, aucune notification n’est envoyée. La tâche figure dans le récap du matin.
- Une nouvelle tâche de travail un jour de repos attend l’heure du récap de votre prochain jour travaillé. La tâche indique quand elle vous sera envoyée, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Si un nouveau résultat est disponible pour une tâche que vous n’avez pas encore vue, il remplace le précédent sans générer de nouvelle notification. Plusieurs notifications rapprochées n’en déclenchent qu’une seule. L’icône de l’app indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’app mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Une réponse est nécessaire, une tâche est bloquée ou une connexion est requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez la notification pour l’ouvrir.

Un navigateur et Telegram en affichent deux. Pour les questions de Fleet, les boutons **Répondre** et **Refuser** restent toujours disponibles.

Aucun message n’est envoyé, aucun paiement n’est effectué et rien n’est soumis depuis une notification. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le vérifier avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste avec le brouillon complet. **Faire** lance le travail uniquement pour une nouvelle tâche.

Dans l’app mobile, les boutons **Mettre en attente** et **Marquer comme fait** vous demandent d’abord de déverrouiller l’app. Dans un navigateur, ils ouvrent le tableau de bord, qui effectue l’action et affiche **Annuler**. Une tâche mise en attente revient au bout de deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens **Ouvrir** (et **Mettre en attente** pour les tâches en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou le lien **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve désormais : **Tout juste fait**, **Fait**, **Revient plus tard** ou dans une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle affiche la tâche dès qu’elle l’est.

## Le récap du matin

Il est envoyé les jours travaillés, à l’heure de votre **Récap du matin**, sauf si rien n’est à signaler. Si cette heure précède celle de **Les mises en attente reviennent à**, il attend 5 minutes après cette dernière pour inclure les tâches qui reviennent ce matin-là. **Aperçu** permet de le consulter sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail, dans un format assez court pour être lu en un coup d’œil :

- un message d’accueil avec les informations importantes de la journée, comme « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, en attente de votre accord : envoyer le bon de commande ». Seules les tâches avec un brouillon ou un résultat à approuver sont considérées comme prêtes. Une tâche qui nécessite d’abord votre réponse ne l’est pas ;
- les tâches mentionnées dans le message d’accueil, chacune avec un lien **Ouvrir**, ainsi que celles à échéance aujourd’hui ; sinon, trois tâches à faire au maximum ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre intervention, quel que soit le nombre indiqué dans le message d’accueil ;
- le nombre d’autres tâches en attente et le temps qu’il vous faudra pour les traiter à votre rythme, par exemple : « 12 autres tâches en attente, environ 5 min pour les traiter ». Les tâches qui attendent votre réponse ne sont pas incluses dans ce délai. Une tâche à échéance aujourd’hui, mais mise en attente jusqu’à plus tard, ou sur laquelle The Machine travaille encore, n’est comptée que lorsqu’elle attend votre intervention. Le nombre indiqué correspond aux tâches en attente dans votre liste.
- vos réunions sur une seule ligne.

Le lien **Ouvrir** affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou en attente. Une promesse ouvre la tâche correspondante, ou sa propre page si elle n’en a pas encore.

La notification push reprend le même contenu, sans liens. Touchez-la, ou utilisez le lien à la fin de l’e-mail, pour consulter de nouveau le récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure indiquée dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les modes choisis sur sa ligne ci-dessus. Il est envoyé uniquement les jours où vous avez été actif : vous avez utilisé le tableau de bord ou choisi une action pour une tâche, sur Telegram, dans le chat ou par commande vocale. Il n’est pas envoyé les jours où aucune tâche n’a été terminée et aucune réunion n’a eu lieu.

Il commence par un décompte de la journée, par exemple : « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis affiche une partie **Travail** et une partie **Perso**. Les parties sans contenu sont omises. Chacune comprend :

- **Fait aujourd’hui** : jusqu’à trois tâches que vous ou votre Machine avez terminées, puis « +12 autres » et les réunions de la journée, par exemple : « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé, si nous sommes vendredi) : les prochaines réunions et les tâches à échéance.

Il indique enfin le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le consulter de nouveau, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez sa ligne.

## Confidentialité

La notification push est envoyée directement de votre Machine à votre appareil, où elle est chiffrée. Les e-mails transitent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque [Mode prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que des décomptes. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’app](phone-app.md). L’[app mobile](mobile-app.md) envoie une ligne de texte non chiffrée via Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
