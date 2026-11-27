---
title: L’application mobile
area: getting-started
summary: The Machine sur iPhone et Android : recevez des notifications pour vos tâches et partagez du contenu avec The Machine depuis n’importe quelle appli.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: aaf34f864dadf180
---
L’application mobile ouvre votre propre tableau de bord, avec la même session que sur le Web. Téléchargez-la sur l’[App Store](https://apps.apple.com/app/id6829875215) pour iPhone et iPad, ou sur [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) pour Android.

La tâche **Tirez le meilleur de The Machine**, en haut de la liste des tâches, vous la recommande. Dans le navigateur d’un téléphone, **Obtenir** ouvre la boutique. Sur un téléphone configuré pour afficher les sites pour ordinateur, les liens vers les deux boutiques s’affichent. Sur un ordinateur, un QR code à scanner avec votre téléphone s’affiche, ainsi que les liens vers les deux boutiques.

Sur n’importe quel téléphone, [themachine.computer/app](https://themachine.computer/app) ouvre la boutique appropriée. Dans **Paramètres**, **Applis**, les deux boutiques s’affichent en haut de la page, ou seule la boutique de votre téléphone s’affiche sur un téléphone. Sur un ordinateur, vous y trouverez aussi l’application de bureau pour Windows, Mac et Linux : consultez [L’application de bureau](desktop-app.md).

## Connecter l’application

Sur une Machine hébergée, l’application se connecte avec votre compte. Sur une Machine auto-hébergée, ouvrez **Paramètres**, puis **Applis** sur un ordinateur : sous les boutiques, **Pas sur le Network ?** affiche un code. Installez l’application, puis scannez le code avec l’appareil photo de votre téléphone ou saisissez dans l’application l’adresse affichée en dessous. L’application vous demande votre accord avant de se connecter, et la connexion à votre Machine reste soumise à son propre système de connexion.

**Se connecter avec** un service dans **Connexions** (Shortcut, Notion, Slack, Zoom et les autres) ouvre la fenêtre de connexion de votre téléphone. Une fois la connexion établie, vous revenez dans l’application et la nouvelle connexion apparaît automatiquement dans **Connexions**.

Quand l’application n’arrive pas à joindre votre Machine, elle vous le signale et réessaie automatiquement. Sur un Mac, l’application recharge aussi automatiquement la page si sa fenêtre est vide après la sortie de veille. Le message de chat que vous étiez en train d’écrire réapparaît également. Sur un Mac ou un iPad avec un clavier, Cmd+R recharge la page.

## Notifications

L’application vous demande l’autorisation d’envoyer des notifications à sa première ouverture. Touchez-en une pour ouvrir l’élément concerné : une tâche s’affiche en surbrillance dans votre liste, la notification du matin ouvre la journée dans l’**Agenda**, le brief d’équipe ouvre les tâches et une question de Fleet ouvre la tâche correspondante. Aucun texte de tâche ne transite par Apple, Google ou le service de The Machine : ces services ne transmettent qu’un message prédéfini, comme « Une tâche vous attend ».

L’application demande ensuite à votre Machine le titre de la tâche et la prochaine étape, par exemple « Répondre à Sam » avec « Envoyer à Sam : mardi à 10 h, ça marche ». La notification du matin indique ce qui vous attend et l’heure de votre première réunion, le brief d’équipe présente ses premiers éléments et une mise à jour de Fleet indique ce qui s’est passé. Si l’application n’arrive pas à joindre votre Machine, le message prédéfini reste affiché. Sur Android, elle indique le nombre de tâches en attente, par exemple « 2 tâches vous attendent ».

Une notification propose **Mettre en attente** (jusqu’à demain) et **Marquer comme fait**, ainsi que **Faire** pour une tâche qui n’a pas encore commencé. Ces actions fonctionnent après le déverrouillage du téléphone, sans ouvrir l’application. L’envoi et les dernières étapes ouvrent toujours l’application. Une seule notification est envoyée par tâche : « Préparation » devient « Prête », puis la notification disparaît quand la tâche est terminée ou mise en attente, dans l’application ou ailleurs.

Lorsqu’une étape que vous avez confirmée est effectuée, sa notification indique **Fait** et ce qui s’est passé. Elle reste affichée jusqu’à ce que vous touchiez **Compris** dans la liste des tâches. Sur iPhone, vous pouvez attendre votre prochaine ouverture de l’application pour le faire.

Si l’option **Texte dans les notifications** est désactivée dans **Paramètres**, puis **Sécurité**, le message prédéfini reste affiché. C’est aussi le cas si l’écran verrouillé masque le contenu des notifications. Quand il n’y a rien à afficher, le message « Touchez pour ouvrir » apparaît. Si votre téléphone n’arrive pas à joindre votre Machine à l’arrivée d’une notification, les détails s’affichent dès que la connexion est rétablie.

Les notifications suivent les mêmes règles que les notifications push sur le Web : vos choix pour chaque type dans [Notifications](notifications.md), vos [heures de travail](work-hours.md), et aucune notification lorsque vous utilisez un tableau de bord.

Chaque téléphone sur lequel l’application est installée apparaît dans **Paramètres**, **Notifications**, sous **Téléphone avec l’app**. **Retirer** désactive ses notifications. Une Machine auto-hébergée a besoin de The Machine Network pour envoyer ces notifications. L’application fonctionne sans elles.

## Partager avec The Machine

Dans n’importe quelle appli, touchez Partager et choisissez The Machine. Une **Nouvelle tâche** s’ouvre avec le texte, le lien ou les fichiers que vous avez partagés. Vérifiez son contenu, ajoutez une date si vous le souhaitez, puis ajoutez la tâche. Rien n’est ajouté avant que vous le fassiez.

Vous pouvez partager un fichier seul, comme une facture ou une lettre. Votre Machine lit le texte d’un PDF et remplit la tâche : de quoi il s’agit, la prochaine étape et sa date. Le fichier est envoyé directement à votre Machine et y reste.

Le tableau de bord installé comme application sur Android accepte aussi les partages : choisissez-le dans la feuille de partage, comme pour les autres applis.

Les forfaits et la facturation ne s’affichent pas dans l’application. **Ouvrir le compte** reste disponible dans **Paramètres** pour supprimer votre compte.
