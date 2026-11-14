---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seules les choses urgentes vous alertent, le reste est regroupé dans un récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 334224e0b479ef47
---
Vous préférez recevoir moins de notifications ou en recevoir d’autres ? Dans **Paramètres**, **Notifications**, choisissez où recevoir chaque type de notification :

- **Nouvelles tâches** : uniquement ce qui ne peut pas attendre, comme une tâche à échéance aujourd’hui ou urgente.
- **Résultats et questions** : une réponse prête à envoyer, une tâche qui nécessite une connexion, une question de Fleet.
- **Rappels** : les tâches mises en attente et les réponses que vous attendez, quand elles reviennent.
- **Récap du matin** : un bref résumé de votre journée. Voir ci-dessous.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste à faire demain. Voir ci-dessous.

Chaque type de notification dispose d’un bouton pour activer ou désactiver les notifications **Push** (sur l’application de votre téléphone ou ordinateur), **Telegram** une fois configuré, et **E-mail** sur une Machine hébergée ou une Machine du The Machine Network. Tout est activé, sauf les récaps sur Telegram.

Vos **Heures de travail** se trouvent dans le même onglet : les jours travaillés, les heures auxquelles les notifications peuvent être envoyées, le retour des mises en attente, les heures des récaps et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Uniquement ce qui ne peut pas attendre

Une notification push, un message Telegram ou un e-mail est envoyé uniquement pour :

- une tâche à échéance aujourd’hui ou marquée comme urgente ;
- une réponse attendue, rédigée et prête à être envoyée ;
- une tâche qui nécessite que vous vous connectiez ;
- une mise en attente qui revient à l’heure que vous avez choisie.

Tout le reste apparaît discrètement sur le tableau de bord (et sans alerte sur Telegram) et attend le récap du matin. Les jours de congé, seules les choses urgentes ou à échéance aujourd’hui vous alertent. Vous recevez au maximum 8 notifications push par jour. Si vous n’ouvrez pas le tableau de bord pendant 3 jours, vous ne recevez que le récap du matin, jusqu’à votre retour.

## Quand vous recevez une notification

The Machine vérifie si vous utilisez vraiment le tableau de bord, et pas seulement s’il est ouvert :

- En cours d’utilisation (au premier plan, et vous avez cliqué, saisi du texte ou fait défiler la page au cours des 10 dernières minutes) : aucune alerte. Les notifications Telegram arrivent sans alerte.
- Absente (en arrière-plan, fermée ou inactive depuis 10 minutes) : une notification push est envoyée une minute après votre départ, sauf si vous êtes revenue et l’avez vue.
- Toujours pas vue 15 minutes plus tard et elle ne peut pas attendre : un seul e-mail vous est envoyé, au maximum une fois par heure. Les tâches déjà traitées sont exclues. La plupart du temps, le récap du matin est le seul e-mail que vous recevez.
- Un membre de l’équipe vous confie une tâche et votre Machine ne peut pas vous joindre par téléphone ou sur Telegram : un seul e-mail avec son titre et un lien vous est envoyé 15 minutes plus tard si vous ne l’avez toujours pas vue. Désactivez **E-mail** pour **Résultats et questions** pour désactiver cette notification.
- En dehors de vos heures de travail : aucune notification. La tâche figurera dans le récap du matin.
- Une nouvelle tâche professionnelle un jour de congé attend l’heure de votre récap le prochain jour travaillé. La tâche indique quand vous la recevrez, par exemple Notification Mon 2 Nov · 08:30.

Les progrès et les modifications ne déclenchent jamais de notification. Si un nouveau résultat apparaît pour une tâche que vous n’avez pas encore vue, il la met à jour sans nouvelle notification. Une série de notifications rapprochées ne déclenche qu’une seule alerte. L’icône de l’application indique le nombre de tâches qui nécessitent votre attention.

## Boutons des notifications

Chaque notification propose des boutons pour passer à l’étape suivante. Dans l’application mobile :

- Nouvelle tâche : **Faire**, **Mettre en attente**, **Marquer comme fait**.
- Brouillon prêt : **Ouvrir le brouillon**, **Mettre en attente**, **Marquer comme fait**.
- Résultat prêt : **Ouvrir**, **Marquer comme fait**, **Mettre en attente**.
- Question, blocage ou connexion requise : **Répondre**, **Ouvrir** ou **Se connecter**, puis **Mettre en attente** et **Marquer comme fait**.
- Rappel : **Marquer comme fait**, **Mettre en attente**, **Ouvrir**.
- Récap du matin : touchez la notification pour l’ouvrir.

Le navigateur et Telegram n’affichent que deux de ces boutons. Pour les questions de Fleet, les boutons **Répondre** et **Refuser** restent toujours disponibles.

Aucune notification ne permet d’envoyer, de payer ou de soumettre quoi que ce soit. Un brouillon s’ouvre toujours d’abord pour que vous puissiez le voir avant son envoi. **Ouvrir le brouillon** affiche la tâche dans votre liste et le brouillon en entier. **Faire** lance uniquement le travail sur une nouvelle tâche.

Dans l’application mobile, vous devez d’abord déverrouiller votre téléphone pour **Mettre en attente** ou **Marquer comme fait**. Dans un navigateur, ces boutons ouvrent le tableau de bord, où l’action est effectuée et où vous pouvez l’annuler. **Mettre en attente** fait revenir la tâche dans deux heures ou, pour un rappel, le lendemain matin.

Les e-mails contiennent des liens **Ouvrir** (et **Mettre en attente** pour ce qui attend). Ils ouvrent uniquement le tableau de bord.

Si vous touchez une notification, ou le lien **Ouvrir** dans un e-mail ou sur Telegram, la tâche s’affiche en surbrillance dans votre liste. Si elle est terminée, mise en attente ou affichée dans une autre vue, son chat s’ouvre.

## Le récap du matin

Il est envoyé les jours travaillés à l’heure de votre **Récap du matin**, sauf s’il n’y a rien à signaler. Si cette heure est antérieure à **Les mises en attente reviennent à**, le récap attend 5 minutes après cette heure, pour inclure les tâches qui reviennent ce matin-là. **Aperçu** vous permet de le consulter sans l’envoyer. Par défaut, il est envoyé par notification push et par e-mail, dans un format assez court pour être lu en un coup d’œil :

- un message d’accueil qui résume l’essentiel de la journée, comme « Bonjour Sam, 2 réponses sont prêtes à envoyer » ou, pour une seule tâche, « Bonjour Sam, prêt pour votre accord : envoyer le bon de commande » ;
- les tâches mentionnées dans le message d’accueil, chacune avec un lien **Ouvrir**, ainsi que celles à échéance aujourd’hui ; sinon, trois choses à faire au maximum ;
- le nombre de tâches qui peuvent attendre et le temps nécessaire à votre rythme, par exemple « 12 autres peuvent attendre, environ 5 min pour les terminer ». Les tâches qui attendent votre réponse ne sont pas prises en compte dans ce temps ;
- vos réunions, sur une seule ligne.

Le lien **Ouvrir** affiche la tâche en surbrillance dans votre liste. Si elle est terminée, mise en attente ou affichée dans une autre vue, son chat s’ouvre. Une promesse ouvre la tâche correspondante ou, si elle n’en a pas encore, sa propre page.

La notification push reprend le même contenu, sans les liens. Touchez-la, ou le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

## Le récap du soir

Il est envoyé une fois les jours travaillés, à l’heure définie dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, selon les moyens de réception que vous avez choisis dans la ligne ci-dessus. Vous n’en recevez pas les jours où aucune tâche n’a été terminée et où aucune réunion n’a eu lieu. Il commence par un bilan de la journée, comme « Bonsoir Sam, 4 tâches terminées aujourd’hui », puis comporte une partie **Travail** et une partie **Perso**. Les parties vides sont omises. Chacune comprend :

- **Fait aujourd’hui** : jusqu’à trois tâches terminées par vous ou votre Machine, puis « +12 autres » et les réunions de la journée, comme « +3 réunions : appel sur les tarifs et 2 autres » ;
- **À faire demain** (ou le prochain jour travaillé si c’est vendredi) : les premières réunions et les tâches à échéance.

Le récap se termine par le nombre de tâches qui nécessitent encore votre attention. Touchez la notification push ou le lien à la fin de l’e-mail pour le relire et accéder à **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez la ligne correspondante.

## Confidentialité

Les notifications push sont envoyées directement de votre Machine vers votre appareil, où elles sont chiffrées. Les e-mails passent par le serveur de messagerie de The Machine et votre fournisseur de messagerie. Lorsque [Mode prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails n’affichent que des nombres. Désactivez **E-mail** pour un type de notification pour qu’il ne soit plus envoyé par e-mail.

Activez les notifications push pour un appareil dans **Cet appareil**, ou consultez [Installer l’application](phone-app.md). L’[application mobile](mobile-app.md) reçoit une ligne de texte simple via Apple ou Google, puis demande le titre et l’étape suivante à votre Machine.
