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
- **Récap du matin** : les réunions du jour, ce qui arrive à échéance et ce qui est arrivé pendant la nuit.

Chacun a un interrupteur pour **Push** (l’app sur votre téléphone ou votre ordinateur), **Telegram** quand il est configuré, et **E-mail** sur une Machine hébergée ou sur une Machine du The Machine Network. Tous sont activés, sauf le récap sur Telegram.

Les **Heures de travail** se trouvent dans le même onglet : vos jours de travail, les heures où les notifications peuvent partir, l’heure de retour des mises en attente, l’heure du récap et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Quand les notifications partent

Comme Slack, il regarde si vous utilisez le tableau de bord, pas seulement s’il est ouvert :

- En cours d’utilisation : le tableau de bord est devant vous, au premier plan, et vous avez cliqué, tapé, fait défiler ou touché l’écran dans les 10 dernières minutes. Rien ne vibre. Telegram arrive sans son.
- Absent : le tableau de bord est en arrière-plan, réduit, fermé ou inactif depuis 10 minutes. Un push part une minute après que vous l’avez quitté, sauf si vous revenez et le voyez avant.
- Toujours pas vu 15 minutes plus tard : un seul e-mail avec tout ce qui vous attend encore. Au plus un par heure. Ce que vous avez traité entre-temps, sur Telegram ou ailleurs, n’y figure pas. Utiliser le tableau de bord après l’arrivée d’un élément compte comme l’avoir vu : une journée passée sur le tableau de bord peut donc n’envoyer aucun e-mail.
- En dehors de vos heures de travail : rien. Le récap du matin contient ce qui est arrivé.

Seul ce qui a besoin de vous envoie une notification. Pas les avancées ni les modifications. Une rafale ne vibre qu’une fois. L’icône de l’app montre combien de tâches ont besoin de vous.

## Le récap du matin

Il arrive les jours de travail à l’heure du **Récap du matin**, et il est sauté quand il n’y a rien à dire. **Aperçu**, sur sa ligne, l’affiche sur la page sans l’envoyer. Par défaut, c’est un push et un e-mail.

## Confidentialité

Le push va directement de votre Machine à votre appareil, chiffré pour cet appareil. Le plan de contrôle ne le voit jamais. L’e-mail est envoyé par le serveur mail de The Machine à l’adresse de votre compte, donc le texte passe par lui et par votre fournisseur de messagerie. Quand [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails ne contiennent que des chiffres. Désactivez **E-mail** pour un type afin de le tenir entièrement à l’écart de l’e-mail.

Activez le push pour un appareil dans **Cet appareil**, ou voir [Installer l’app](phone-app.md).
