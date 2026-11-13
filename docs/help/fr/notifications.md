---
title: Notifications
area: settings
summary: Ce qui vous parvient, où et quand : seul ce qui ne peut pas attendre vous notifie, le reste est dans un seul récap du matin.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Dans **Paramètres**, **Notifications**, choisissez pour chaque type où il vous parvient :

- **Nouvelles tâches** : seulement ce qui ne peut pas attendre, comme une échéance aujourd’hui ou une urgence.
- **Résultats et questions** : une réponse prête à envoyer, une connexion qu’une tâche demande, une question de la Fleet.
- **Rappels** : les mises en attente et les attentes qui reviennent.
- **Récap du matin** : un court résumé de votre journée. Voir plus bas.
- **Récap du soir** : ce qui a été fait aujourd’hui et ce qui reste pour demain. Voir plus bas.

Chacun a un interrupteur pour **Push** (l’app sur votre téléphone ou votre ordinateur), **Telegram** quand il est configuré, et **E-mail** sur une Machine hébergée ou sur une Machine du The Machine Network. Tous sont activés, sauf les récaps sur Telegram.

Les **Heures de travail** se trouvent dans le même onglet : vos jours de travail, les heures où les notifications peuvent partir, l’heure de retour des mises en attente, l’heure du récap et votre fuseau horaire. Voir [Heures de travail](work-hours.md).

## Seulement ce qui ne peut pas attendre

Un push, une notification Telegram ou un e-mail part seulement pour :

- une tâche à faire aujourd’hui, ou marquée urgente ;
- une réponse que quelqu’un attend, rédigée et prête à envoyer ;
- une tâche qui demande que vous vous connectiez ;
- une mise en attente qui revient à l’heure choisie.

Tout le reste arrive sans bruit sur le tableau de bord (et sans son dans Telegram) et attend le récap du matin. Un jour de repos, seul ce qui est urgent ou à faire aujourd’hui vous notifie. Au plus 8 push par jour. Après 3 jours sans ouvrir le tableau de bord, seul le récap du matin arrive, jusqu’à votre retour.

## Quand les notifications partent

Comme Slack, il regarde si vous utilisez le tableau de bord, pas seulement s’il est ouvert :

- En cours d’utilisation : le tableau de bord est devant vous, au premier plan, et vous avez cliqué, tapé, fait défiler ou touché l’écran dans les 10 dernières minutes. Rien ne vibre. Telegram arrive sans son.
- Absent : le tableau de bord est en arrière-plan, réduit, fermé ou inactif depuis 10 minutes. Un push part une minute après que vous l’avez quitté, sauf si vous revenez et le voyez avant.
- Toujours pas vu 15 minutes plus tard, et cela ne peut pas attendre : un e-mail pour cela, au plus un par heure. Ce que vous avez déjà traité n’y figure pas. La plupart des jours, le récap du matin est le seul e-mail.
- En dehors de vos heures de travail : rien. Le récap du matin contient ce qui est arrivé.
- Une nouvelle tâche de travail arrivée un jour de repos attend l’heure du récap de votre prochain jour de travail. La tâche indique où et quand elle vous parviendra, par exemple Notification lun. 2 nov. · 08:30, selon la ligne **Nouvelles tâches**. Avec Push et Telegram tous deux désactivés, elle n’indique rien.

Seul ce qui a besoin de vous envoie une notification. Pas les avancées ni les modifications. Un résultat plus récent sur une tâche que vous n’avez pas encore vue la met à jour sans nouvelle notification. Une rafale ne vibre qu’une fois. L’icône de l’app montre combien de tâches ont besoin de vous.

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

Il arrive les jours de travail à l’heure du **Récap du matin**, sauf s’il n’y a rien à dire. Si elle est avant **Les mises en attente reviennent à**, il attend 5 minutes après, pour inclure les tâches qui reviennent ce matin-là. **Aperçu**, sur sa ligne, l’affiche sans l’envoyer. Par défaut, c’est un push et un e-mail, assez courts pour se lire d’un coup d’œil :

- un bonjour avec ce qui compte aujourd’hui, comme "Bonjour Sam, 2 réponses sont prêtes à envoyer" ou, pour une tâche, "Bonjour Sam, à valider : Envoyer le bon de commande" ;
- au plus trois choses à faire, chacune avec un lien Ouvrir : d’abord les brouillons prêts et les promesses du jour ;
- combien d’autres peuvent attendre, et le temps qu’elles vous prennent, comme "12 autres peuvent attendre, environ 5 min pour tout traiter." Les tâches qui attendent votre réponse ne comptent pas dans ce temps.
- vos réunions en une ligne.

Ouvrir affiche la tâche en surbrillance dans votre liste. Si elle est faite, mise en attente ou dans une autre vue, son chat s’ouvre. Une promesse ouvre sa tâche, ou sa propre page si elle n’en a pas encore.

Le push dit la même chose sans liens. Touchez-le, ou le lien à la fin de l’e-mail, pour relire ce récap dans **Tâches**.

À la fin viennent vos récaps **Travail** et **Perso**, le même texte que copie **Récap** dans les tâches. Quand le texte des tâches est masqué dans les notifications, ils sont omis.

## Le récap du soir

Il arrive une fois les jours de travail à son heure dans **Heures de travail**, par défaut 15 minutes avant **Jusqu’à**, par les moyens choisis dans sa ligne ci-dessus. Un jour sans tâche faite ni réunion tenue n’en reçoit pas. Il commence par votre journée en un chiffre, comme "Bonsoir Sam, 4 tâches faites aujourd’hui", puis une partie **Travail** et une partie **Perso**. Une partie vide est omise. Chacune contient :

- les réunions du jour sur une ligne à part, comme "3 réunions : Appel tarifs et 2 autres." ;
- **Fait aujourd’hui** : jusqu’à trois tâches que vous ou votre Machine avez terminées, et combien d’autres ;
- **À faire demain** (un vendredi, votre prochain jour de travail) : les premières réunions et ce qui arrive à échéance.

Il se termine par le nombre de tâches qui vous attendent encore. Touchez la notification push, ou le lien à la fin de l’e-mail, pour le relire, avec **Copier Travail** et **Copier Perso**. Pour ne plus le recevoir, désactivez sa ligne.

## Confidentialité

Le push va directement de votre Machine à votre appareil, chiffré pour cet appareil. Le plan de contrôle ne le voit jamais. L’e-mail est envoyé par le serveur mail de The Machine à l’adresse de votre compte, donc le texte passe par lui et par votre fournisseur de messagerie. Quand [Prudent](security-levels.md) masque le texte des tâches dans les notifications, les e-mails ne contiennent que des chiffres. Désactivez **E-mail** pour un type afin de le tenir entièrement à l’écart de l’e-mail.

Activez le push pour un appareil dans **Cet appareil**, ou voir [Installer l’app](phone-app.md).
