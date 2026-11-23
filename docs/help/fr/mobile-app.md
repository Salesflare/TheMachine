---
title: L’application mobile
area: getting-started
summary: The Machine sur iPhone et Android : des notifications pour vos tâches et le partage vers The Machine depuis n’importe quelle application.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 927fa395fe97f565
---
L’application mobile ouvre votre tableau de bord, avec la même session que sur le Web. Téléchargez-la sur l’[App Store](https://apps.apple.com/app/id6829875215) pour iPhone et iPad, ou sur [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) pour Android.

La tâche **Tirez le meilleur de The Machine**, en haut de la liste des tâches, vous la propose. Dans le navigateur d’un téléphone, **Obtenir** ouvre la boutique. Sur un téléphone configuré pour afficher les sites pour ordinateur, les liens vers les deux boutiques s’affichent. Sur un ordinateur, un QR code à scanner avec votre téléphone s’affiche, avec les liens vers les deux boutiques.

Sur n’importe quel téléphone, [themachine.computer/app](https://themachine.computer/app) ouvre la bonne boutique. Dans **Paramètres**, **Applis**, les deux boutiques s’affichent en haut, ou seule la boutique de votre téléphone si vous êtes sur un téléphone. Sur un ordinateur, **Ordinateur** installe le tableau de bord comme une application : consultez [Installer l’application](phone-app.md).

## Connecter l’application

Sur une Machine hébergée, l’application se connecte avec votre compte. Sur une Machine auto-hébergée, ouvrez **Paramètres**, puis **Applis** sur un ordinateur : sous les boutiques, **Pas sur le Network ?** affiche un code. Installez l’application, puis scannez le code avec l’appareil photo de votre téléphone, ou saisissez dans l’application l’adresse affichée dessous. L’application vous demande votre accord avant de se connecter, et la connexion à votre Machine nécessite toujours vos identifiants.

**Se connecter avec** un service dans **Connexions** (Shortcut, Notion, Slack, Zoom et les autres) ouvre la fenêtre de connexion de votre téléphone. Une fois la connexion terminée, vous revenez dans l’application, et la nouvelle connexion apparaît automatiquement dans **Connexions**.

Quand l’application ne parvient pas à joindre votre Machine, elle vous le signale et réessaie automatiquement. Sur Mac, l’application recharge aussi la page automatiquement si sa fenêtre est vide après la sortie de veille. Le message de chat que vous étiez en train de rédiger réapparaît lui aussi. Sur Mac ou sur iPad avec un clavier, Cmd+R recharge la page.

## Notifications

L’application vous demande l’autorisation d’envoyer des notifications lors de sa première ouverture. Touchez une notification pour ouvrir son contenu : une tâche apparaît en surbrillance dans votre liste, la notification du matin ouvre aujourd’hui dans l’**Agenda**, le brief de l’équipe ouvre les tâches, et une question de Fleet ouvre la tâche correspondante. Le texte d’une tâche ne passe jamais par Apple, Google ni le service de The Machine : ils ne transmettent qu’un message fixe, comme « Une tâche vous attend ».

L’application demande ensuite à votre Machine le titre de la tâche et la prochaine étape, par exemple « Répondre à Sam » avec « Envoyer à Sam : mardi à 10 h, ça marche ». La notification du matin indique ce qui vous attend et l’heure de votre première réunion, le brief de l’équipe présente ses premiers éléments, et une mise à jour de Fleet indique ce qui s’est passé. Si l’application ne parvient pas à joindre votre Machine, le message fixe reste affiché. Sur Android, elle indique le nombre de tâches en attente, par exemple « 2 tâches vous attendent ».

Une notification propose **Mettre en attente** (jusqu’au lendemain) et **Marquer comme fait**, ainsi que **Faire** pour une tâche qui n’a pas encore commencé. Ces actions fonctionnent après le déverrouillage du téléphone, sans ouvrir l’application. L’envoi et les étapes finales ouvrent toujours l’application. Une seule notification est envoyée par tâche : « En préparation » devient « Prête », puis disparaît une fois la tâche terminée ou mise en attente, dans l’application ou ailleurs.

Lorsqu’une étape que vous avez confirmée est effectuée, sa notification indique **Fait** et précise ce qui s’est passé, jusqu’à ce que vous touchiez **Compris** dans la liste des tâches. Sur iPhone, vous pouvez attendre la prochaine ouverture de l’application.

Si vous désactivez **Texte dans les notifications** dans **Paramètres**, puis **Sécurité**, le message fixe reste affiché. C’est aussi le cas si votre écran verrouillé masque le contenu des notifications. Quand aucune information ne peut s’afficher, le message « Touchez pour ouvrir » apparaît. Si votre téléphone ne parvient pas à joindre votre Machine à l’arrivée d’une notification, ses détails s’affichent dès que la connexion est rétablie.

Les notifications suivent les mêmes règles que les notifications push sur le Web : vos choix pour chaque type dans [Notifications](notifications.md), vos [heures de travail](work-hours.md), et aucune notification pendant que vous utilisez un tableau de bord.

Chaque téléphone avec l’application apparaît dans **Paramètres**, **Notifications**, sous **Téléphone avec l’app**. **Retirer** désactive ses notifications. Une Machine auto-hébergée a besoin de The Machine Network pour les envoyer ; l’application fonctionne sans elles.

## Partager avec The Machine

Dans n’importe quelle application, touchez Partager et choisissez The Machine. Une **Nouvelle tâche** s’ouvre avec le texte, le lien ou les fichiers partagés. Vérifiez-les, ajoutez une date si vous le souhaitez, puis ajoutez la tâche. Rien n’est ajouté avant que vous le fassiez.

Un fichier seul suffit, par exemple une facture ou une lettre. Votre Machine lit le texte d’un PDF et remplit la tâche : ce qu’est le document, la prochaine étape et sa date. Le fichier est envoyé directement à votre Machine et y reste.

Sur Android, vous pouvez aussi partager du contenu avec le tableau de bord installé comme application : choisissez-le dans la feuille de partage, comme n’importe quelle autre application.

Les abonnements et la facturation ne s’affichent pas dans l’application. **Ouvrir le compte** reste disponible dans **Paramètres** pour supprimer votre compte.
