---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les notifications qui ne peuvent pas attendre vous dérangent, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4f777fac22dba7c0
---
Vous voulez moins de notifications, ou en recevoir d’autres ? Dans **Paramètres**, ouvrez **Notifications** et choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement celles qui ne peuvent pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion, une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, lorsqu’elles reviennent.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type dispose d’une option pour les notifications **Push** (sur l’application de votre téléphone ou ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou sur The Machine Network. Toutes les options sont activées, sauf les récaps sur Telegram.

Vos **Heures de travail** se règlent dans le même onglet : jours travaillés, plages horaires d’envoi des notifications, heure de retour des tâches mises en attente, horaires des récaps et fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, un message Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse attendue, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et silencieusement sur Telegram) et attend le récap du matin. Un jour de congé, seules les tâches urgentes ou à échéance aujourd’hui vous alertent. Vous recevrez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevrez que le récap du matin jusqu’à votre retour.

## Quand les notifications sont envoyées

The Machine vérifie si vous utilisez vraiment le tableau de bord, et pas seulement s’il est ouvert :

- Vous l’utilisez (il est au premier plan et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune notification ne vous dérange. Les messages Telegram arrivent silencieusement. Le simple fait de l’ouvrir ou de le recharger ne compte pas.
- Vous êtes absent (le tableau de bord est en arrière-plan, fermé ou inactif depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- La notification n’a toujours pas été vue 15 minutes plus tard et ne peut pas attendre : un e-mail vous est envoyé, au maximum un par heure. Les tâches que vous avez déjà traitées sont exclues. La plupart du temps, le récap du matin est le seul e-mail que vous recevez.
- Un coéquipier vous confie une tâche et votre Machine ne peut pas vous joindre par téléphone ou sur Telegram : un e-mail contenant son titre et un lien vous est envoyé si vous ne l’avez toujours pas vue 15 minutes plus tard. Désactivez **E-mail** pour **Résultats et questions** pour ne plus en recevoir.
- En dehors de vos heures de travail : aucune notification. La tâche figurera dans le récap du matin.
- Une nouvelle tâche professionnelle reçue un jour de congé attend l’heure du récap de votre prochain jour travaillé. La tâche indique quand elle vous sera envoyée, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Si un nouveau résultat est ajouté à une tâche que vous n’avez pas encore vue, il la met à jour sans envoyer de nouvelle notification. Une série de notifications n’en déclenche qu’une seule. L’icône de l’application indique combien de tâches nécessitent votre attention.

## Boutons des notifications

Chaque notification comporte des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Question, blocage ou connexion requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez-le pour l’ouvrir.

Le navigateur et Telegram affichent deux de ces boutons. Pour les questions de Fleet, vous avez toujours les boutons **Répondre** et **Refuser**.

Aucun message n’est envoyé, aucun paiement n’est effectué et rien n’est envoyé depuis une notification. Un brouillon s’ouvre toujours d’abord, pour que vous puissiez le voir avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste avec son brouillon complet. **Faire** lance le travail sur une nouvelle tâche.

Dans l’application mobile, les boutons **Mettre en attente** et **Marquer comme fait** vous demandent d’abord de déverrouiller votre téléphone. Dans un navigateur, ils ouvrent le tableau de bord, où l’action est effectuée et où l’option Annuler s’affiche. Une tâche mise en attente revient au bout de deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens **Ouvrir** (et **Mettre en attente** pour les tâches en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou le lien **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’est pas encore à jour, elle suit la tâche dès qu’elle le devient.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure définie pour **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure précède **Les mises en attente reviennent à**, il attend 5 minutes après cette heure afin d’inclure les tâches qui reviennent ce matin-là. **Aperçu** affiche le récap sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail. Il est assez court pour être lu en un coup d’œil :

- une formule d’accueil suivie de l’essentiel pour la journée, par exemple « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, en attente de votre accord : envoyer le bon de commande » ;
- les tâches mentionnées dans la formule d’accueil, chacune avec un lien **Ouvrir**, ainsi que celles à échéance aujourd’hui ; sinon, jusqu’à trois tâches à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre attention, quel que soit le nombre indiqué dans la formule d’accueil ;
- le nombre d’autres tâches en attente et le temps nécessaire pour les traiter à votre rythme, par exemple « 12 autres tâches en attente, environ 5 min pour les traiter ». Les tâches qui attendent votre réponse ne sont pas incluses dans ce temps, et une tâche mise en attente à échéance aujourd’hui n’est comptée qu’à son retour ;
- vos réunions sur une seule ligne.

**Ouvrir** affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou mise en attente. Une promesse ouvre sa tâche, ou sa propre page si elle n’en a pas encore.

La notification push contient le même texte, sans liens. Touchez-la, ou utilisez le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure définie dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les modes d’envoi choisis dans sa ligne ci-dessus. Vous ne le recevez pas un jour où aucune tâche n’a été terminée et aucune réunion n’a eu lieu. Il commence par un bilan chiffré de la journée, par exemple « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis présente une partie **Travail** et une partie **Perso**. Les parties sans contenu sont omises. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, par exemple « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé, si nous sommes vendredi) : les premières réunions et les tâches à échéance.

Il se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le relire, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez sa ligne.

## Confidentialité

Les notifications push sont envoyées directement de votre Machine à votre appareil, où elles sont chiffrées. Les e-mails passent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Quand le mode [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que les nombres. Désactivez **E-mail** pour un type de notification pour ne plus le recevoir par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) reçoit d’abord une ligne de texte via Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
