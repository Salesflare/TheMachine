---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : push, Telegram ou e-mail par type, vos heures de travail et le récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Dans **Paramètres**, **Notifications**, choisissez pour chaque type où il vous parvient :

- **Nouvelles tâches** : une réponse que quelqu’un attend, une demande, tout ce qui est urgent.
- **Résultats et questions** : un brouillon prêt à approuver ou à envoyer, une tâche bloquée ou qui demande une connexion, une question de la Fleet.
- **Rappels** : les mises en attente et les attentes qui reviennent.
- **Récap du matin** : les réunions du jour, ce qui arrive à échéance, ce qui est arrivé pendant la nuit et les premières tâches en attente, dans l’ordre de votre liste de tâches.

Chacun a un interrupteur pour **Push** (l’app sur votre téléphone ou votre ordinateur), **Telegram** quand il est configuré, et **E-mail** sur une Machine hébergée ou sur une Machine du The Machine Network. Tous sont activés, sauf le récap sur Telegram.

Les **Heures de travail** se trouvent dans le même onglet : vos jours de travail, les heures où les notifications peuvent partir, l’heure de retour des mises en attente, l’heure du récap et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Quand les notifications partent

Comme Slack, il regarde si vous utilisez le tableau de bord, pas seulement s’il est ouvert :

- En cours d’utilisation : le tableau de bord est devant vous, au premier plan, et vous avez cliqué, tapé, fait défiler ou touché l’écran dans les 10 dernières minutes. Rien ne vibre. Telegram arrive sans son.
- Absent : le tableau de bord est en arrière-plan, réduit, fermé ou inactif depuis 10 minutes. Un push part une minute après que vous l’avez quitté, sauf si vous revenez et le voyez avant.
- Toujours pas vu 15 minutes plus tard : un seul e-mail avec tout ce qui vous attend encore. Au plus un par heure. Ce que vous avez traité entre-temps, sur Telegram ou ailleurs, n’y figure pas. Utiliser le tableau de bord après l’arrivée d’un élément compte comme l’avoir vu : une journée passée sur le tableau de bord peut donc n’envoyer aucun e-mail.
- En dehors de vos heures de travail : rien. Le récap du matin contient ce qui est arrivé.
- Une nouvelle tâche de travail arrivée un jour de repos attend l’heure du récap de votre prochain jour de travail. La tâche indique où et quand elle vous parviendra, par exemple Notification lun. 2 nov. · 08:30, selon la ligne **Nouvelles tâches**. Avec Push et Telegram tous deux désactivés, elle n’indique rien.

Seul ce qui a besoin de vous envoie une notification. Pas les avancées ni les modifications. Une rafale ne vibre qu’une fois. L’icône de l’app montre combien de tâches ont besoin de vous.

## Boutons sur les notifications

Chaque notification a des boutons pour l’étape suivante. Dans l’app sur le téléphone :

- Nouvelle tâche : Faire, Mettre en attente, Marquer comme fait.
- Brouillon prêt : Ouvrir le brouillon, Mettre en attente, Marquer comme fait.
- Résultat prêt : Ouvrir, Marquer comme fait, Mettre en attente.
- Question, bloquée ou connexion requise : Répondre, Ouvrir ou Se connecter, puis Mettre en attente et Marquer comme fait.
- Rappel : Marquer comme fait, Mettre en attente, Ouvrir.
- Récap du matin : touchez-le pour l’ouvrir.

Un navigateur et Telegram en affichent deux. Les questions du Fleet gardent Répondre une fois et Refuser.

Rien n’est envoyé, payé ou soumis depuis une notification. Un brouillon s’ouvre toujours d’abord, pour que vous le voyiez avant qu’il parte. Ouvrir le brouillon montre la tâche dans votre liste avec le brouillon en entier. Faire lance seulement le travail sur une nouvelle tâche.

Dans l’app, Mettre en attente et Marquer comme fait demandent d’abord de déverrouiller. Dans un navigateur, ils ouvrent le tableau de bord, qui le fait et propose Annuler. Mettre en attente fait revenir la tâche dans deux heures, ou demain matin sur un rappel.

Les e-mails qui listent ce qui vous attend ont des liens Ouvrir et Mettre en attente. Ils ouvrent seulement le tableau de bord.

## Le récap du matin

Il arrive les jours de travail à l’heure du **Récap du matin**, et il n’est sauté que quand il n’y a rien à dire : pas de réunion, rien d’échu ni de nouveau, et aucune tâche en attente. **Aperçu**, sur sa ligne, l’affiche sur la page sans l’envoyer. Par défaut, c’est un push et un e-mail. Le push indique combien de tâches attendent, les deux premières et l’heure de votre première réunion. Toucher le push ouvre aujourd’hui dans l’**Agenda**.

## Confidentialité

Le push va directement de votre Machine à votre appareil, chiffré pour cet appareil. Le plan de contrôle ne le voit jamais. L’e-mail est envoyé par le serveur mail de The Machine à l’adresse de votre compte, donc le texte passe par lui et par votre fournisseur de messagerie. Quand [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails ne contiennent que des chiffres. Désactivez **E-mail** pour un type afin de le tenir entièrement à l’écart de l’e-mail. Il dit aussi combien de temps les tâches en attente vous prennent, comme "4 prêts · environ 2 min".

Activez le push pour un appareil dans **Cet appareil**, ou voir [Installer l’app](phone-app.md).
