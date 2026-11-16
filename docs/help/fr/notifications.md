---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses qui ne peuvent pas attendre vous alertent, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: ee3ba81a8441704f
---
Moins de notifications, ou d’autres notifications ? Dans **Paramètres**, **Notifications**, choisissez où recevoir chaque type :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche due aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion, une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, lorsqu’elles reviennent.
- **Récap du matin** : un bref récap de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type dispose d’un bouton pour **Push** (l’application sur votre téléphone ou votre ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine sur The Machine Network. Tout est activé, sauf les récaps sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les horaires auxquels les notifications peuvent être envoyées, l’heure de retour des tâches mises en attente, les horaires des récaps et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, une alerte Telegram ou un e-mail est envoyé uniquement pour :

- une tâche due aujourd’hui ou marquée comme urgente ;
- une réponse attendue par quelqu’un, rédigée et prête à envoyer ;
- une tâche qui nécessite que vous vous connectiez ;
- une tâche mise en attente qui revient à l’heure que vous avez choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et silencieusement dans Telegram) et attend le récap du matin. Un jour non travaillé, seules les tâches urgentes ou dues aujourd’hui vous alertent. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, seul le récap du matin vous est envoyé jusqu’à votre retour.

## Quand les notifications sont envoyées

The Machine vérifie si vous utilisez réellement le tableau de bord, et pas seulement s’il est ouvert :

- En cours d’utilisation (au premier plan, avec un clic, une saisie ou un défilement au cours des 10 dernières minutes) : aucune alerte. Les notifications Telegram arrivent silencieusement.
- Inactif (en arrière-plan, fermé ou sans activité depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenu et l’avez vue.
- Toujours pas vue 15 minutes plus tard, et elle ne peut pas attendre : un seul e-mail est envoyé, au maximum un par heure. Les éléments que vous avez déjà traités sont ignorés. La plupart du temps, le récap du matin est le seul e-mail envoyé.
- Si un collègue vous confie une tâche et que votre Machine ne peut pas vous joindre par téléphone ou Telegram : un e-mail avec son titre et un lien est envoyé 15 minutes plus tard si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour ne plus recevoir ces e-mails.
- En dehors de vos heures de travail : aucune notification. Le récap du matin inclut la tâche.
- Une nouvelle tâche professionnelle un jour non travaillé attend l’heure du récap de votre prochain jour travaillé. La tâche indique quand elle vous sera envoyée, par exemple : Notification lun. 2 nov. · 08:30.

Les mises à jour de progression et les modifications ne déclenchent jamais de notification. Un nouveau résultat concernant une tâche que vous n’avez pas encore vue la met à jour sans envoyer de nouvelle notification. Une série de notifications n’en déclenche qu’une seule. L’icône de l’application indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Question, blocage ou connexion requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez la notification pour l’ouvrir.

Dans un navigateur et dans Telegram, deux boutons sont affichés. Pour les questions de Fleet, les boutons **Répondre une fois** et **Refuser** restent disponibles.

Aucun message n’est envoyé, aucun paiement n’est effectué et rien n’est soumis depuis une notification. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le voir avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste avec son brouillon complet. **Faire** lance uniquement le travail sur une nouvelle tâche.

Dans l’application mobile, vous devez d’abord déverrouiller votre téléphone pour utiliser **Mettre en attente** ou **Marquer comme fait**. Dans un navigateur, le tableau de bord s’ouvre et effectue l’action, avec la possibilité de l’annuler. Une tâche mise en attente revient après deux heures, ou le lendemain matin s’il s’agit d’un rappel.

Les e-mails contiennent des liens **Ouvrir** (et **Mettre en attente** pour les éléments en attente). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche dans votre liste, mise en évidence, où qu’elle se trouve : **Tout juste fait**, **Fait**, **Revient plus tard** ou une autre vue. Le chat ne s’ouvre jamais. Si la page n’était pas encore à jour, elle suit la tâche dès qu’elle l’est.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure de votre **Récap du matin**, sauf si vous n’avez rien à signaler. Si cet horaire est antérieur à celui de **Les mises en attente reviennent à**, l’envoi attend jusqu’à 5 minutes après, afin d’inclure les tâches qui reviennent ce matin-là. **Aperçu** affiche le récap sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail, dans un format assez court pour être lu d’un coup d’œil :

- un message d’accueil indiquant l’essentiel du jour, comme « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, en attente de votre accord : envoyer le bon de commande » ;
- les tâches mentionnées dans le message d’accueil, chacune avec un lien **Ouvrir**, ainsi que les tâches dues aujourd’hui ; sinon, jusqu’à trois choses à faire ;
- jusqu’à cinq tâches que vous avez ajoutées vous-même et qui attendent votre attention, quel que soit le nombre indiqué dans le message d’accueil ;
- le nombre d’autres tâches en attente et le temps qu’il vous faudra à votre rythme pour les traiter, comme « 12 autres peuvent attendre, environ 5 min pour les traiter ». Les tâches qui attendent votre réponse ne sont pas incluses dans ce temps, et une tâche mise en attente qui est due aujourd’hui n’est comptée qu’à son retour ;
- vos réunions sur une seule ligne.

**Ouvrir** affiche la tâche dans votre liste, mise en évidence, même si elle est terminée ou mise en attente. Une promesse ouvre sa tâche, ou sa propre page si elle n’en a pas encore.

La notification push reprend le même contenu, sans liens. Touchez-la, ou le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés à l’heure définie dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les moyens choisis dans sa ligne ci-dessus. Il n’est pas envoyé si aucune tâche n’a été terminée et qu’aucune réunion n’a eu lieu. Il commence par un bilan chiffré de la journée, comme « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis affiche une partie **Travail** et une partie **Perso**. Les parties vides sont omises. Chacune contient :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, comme « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé si nous sommes vendredi) : les premières réunions et les tâches dues.

Le récap se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le relire, avec **Copier Travail** et **Copier Perso**. Pour le désactiver, désactivez sa ligne.

## Confidentialité

La notification push est envoyée directement de votre Machine à votre appareil, où elle est chiffrée. Les e-mails passent par le serveur de messagerie de The Machine et par votre fournisseur de messagerie. Lorsque [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’indiquent que des nombres. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) reçoit une ligne sans détails via Apple ou Google, puis demande à votre Machine le titre et l’étape suivante.
