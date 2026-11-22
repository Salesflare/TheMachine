---
title: L’app mobile
area: getting-started
summary: The Machine sous forme d’app sur iPhone et Android : des notifications pour vos tâches et le partage vers The Machine depuis n’importe quelle app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 672364a90f92ef8f
---
L’app mobile ouvre votre tableau de bord, connecté au même compte que sur le web. Téléchargez-la sur l’[App Store](https://apps.apple.com/app/id6829875215) pour iPhone et iPad, ou sur [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) pour Android.

La tâche **Tirez le meilleur de The Machine**, en haut de la liste des tâches, vous la recommande. Dans le navigateur d’un téléphone, **Obtenir** ouvre la boutique d’apps. Sur un téléphone configuré pour afficher les sites pour ordinateur, les liens vers les deux boutiques s’affichent. Sur un ordinateur, un QR code à scanner avec votre téléphone apparaît, ainsi que les liens vers les deux boutiques.

Sur n’importe quel téléphone, [themachine.computer/app](https://themachine.computer/app) ouvre la bonne boutique. Dans **Paramètres**, **Applis**, les deux boutiques s’affichent en haut sur ordinateur, et seule la boutique de votre téléphone s’affiche sur téléphone. Sur ordinateur, **Ordinateur** installe le tableau de bord comme une app : consultez [Installer l’app](phone-app.md).

## Connecter l’app

Sur une Machine hébergée, l’app se connecte avec votre compte. Sur une Machine auto-hébergée, ouvrez **Paramètres**, puis **Applis** sur un ordinateur : sous les boutiques, **Pas sur le Network ?** affiche un code. Installez l’app, puis scannez le code avec l’appareil photo de votre téléphone, ou saisissez dans l’app l’adresse affichée en dessous. L’app vous demande confirmation avant de se connecter, et vous devez toujours vous connecter à votre Machine comme d’habitude.

**Se connecter avec** un service sous **Connexions** (Shortcut, Notion, Slack, Zoom et les autres) ouvre la fenêtre de connexion de votre téléphone. Une fois la connexion terminée, vous revenez dans l’app, et la nouvelle connexion apparaît automatiquement dans **Connexions**.

Quand l’app n’arrive pas à joindre votre Machine, elle vous le signale et réessaie automatiquement. Sur un Mac ou un iPad avec un clavier, Cmd+R recharge la page.

## Notifications

L’app vous demande l’autorisation d’envoyer des notifications à sa première ouverture. Touchez-en une pour voir son contenu : une tâche s’affiche dans votre liste et est mise en évidence, le point du matin ouvre l’**Agenda** du jour, le récapitulatif d’équipe ouvre la liste des tâches, et une question de Fleet ouvre sa tâche. Le texte d’une tâche ne passe jamais par Apple, Google ni le service de The Machine : ces services ne transmettent qu’un message fixe, comme « Une tâche nécessite votre attention ».

L’app demande ensuite à votre Machine le titre de la tâche et la prochaine étape, par exemple « Répondre à Sam » et « Envoyer à Sam : mardi à 10 h, ça marche ». Le point du matin affiche ce qui vous attend et l’heure de votre premier rendez-vous, le récapitulatif d’équipe affiche ses premiers éléments, et une mise à jour de Fleet indique ce qui s’est passé. Si l’app n’arrive pas à joindre votre Machine, le message fixe reste affiché. Sur Android, le message indique le nombre de tâches en attente, par exemple « 2 tâches nécessitent votre attention ».

Une notification propose **Mettre en attente** (jusqu’à demain) et **Marquer comme fait**, ainsi que **Faire** pour une tâche qui n’a pas encore commencé. Ces actions fonctionnent après le déverrouillage du téléphone, sans ouvrir l’app. L’envoi et les étapes finales ouvrent toujours l’app. Il n’y a qu’une notification par tâche : « En préparation » devient « Prête », puis la notification disparaît quand la tâche est terminée ou mise en attente, ici ou ailleurs.

Quand une étape que vous avez confirmée est effectuée, sa notification indique **Fait** et précise ce qui s’est passé, jusqu’à ce que vous touchiez **Compris** dans la liste des tâches. Sur iPhone, vous pouvez attendre la prochaine ouverture de l’app.

Si **Texte dans les notifications** est désactivé dans **Paramètres**, puis **Sécurité**, le message fixe reste affiché. C’est aussi le cas si votre écran verrouillé masque le contenu des notifications. Quand il n’y a rien à afficher, le message « Touchez pour ouvrir » apparaît. Si votre téléphone n’arrive pas à joindre votre Machine à l’arrivée d’une notification, son contenu s’affiche dès que la connexion est rétablie.

Les notifications suivent les mêmes règles que les notifications push sur le web : vos choix pour chaque type dans [Notifications](notifications.md), vos [heures de travail](work-hours.md), et aucune notification pendant que vous utilisez un tableau de bord.

Chaque téléphone avec l’app apparaît dans **Paramètres**, puis **Notifications**, sous **Téléphone avec l’app**. **Retirer** désactive ses notifications. Une Machine auto-hébergée a besoin de The Machine Network pour les envoyer, mais l’app fonctionne sans elles.

## Partager vers The Machine

Dans n’importe quelle app, touchez Partager et choisissez The Machine. Une **Nouvelle tâche** s’ouvre avec le texte, le lien ou les fichiers partagés. Vérifiez le contenu, ajoutez une date si vous le souhaitez, puis ajoutez la tâche. Rien n’est ajouté avant cette dernière étape.

Un fichier seul suffit, comme une facture ou une lettre. Votre Machine lit le texte d’un PDF et remplit la tâche : ce que c’est, la prochaine étape et sa date. Le fichier est envoyé directement à votre Machine et y reste.

Sur Android, vous pouvez aussi partager vers le tableau de bord installé comme une app : sélectionnez-le dans le menu de partage, comme d’habitude.

Les forfaits et la facturation ne s’affichent pas dans l’app. **Ouvrir le compte** dans **Paramètres** reste disponible pour supprimer votre compte.
