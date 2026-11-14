---
title: L’application mobile
area: getting-started
summary: The Machine sous forme d’application sur iPhone et Android : des notifications pour vos tâches, et le partage vers The Machine depuis n’importe quelle application.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: 3865fe910a5427fb
---
L’application mobile ouvre votre propre tableau de bord, avec la même session que sur le Web. Téléchargez-la sur l’[App Store](https://apps.apple.com/app/id6829875215) pour iPhone et iPad, ou sur [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) pour Android.

La tâche **Tirez le meilleur de The Machine**, en haut de la page Tâches, vous le suggère. Dans le navigateur d’un téléphone, **Obtenir** ouvre la boutique. Sur un téléphone configuré pour afficher les sites pour ordinateur, les liens vers les deux boutiques s’affichent. Sur un ordinateur, un code QR à scanner avec votre téléphone et les liens vers les deux boutiques s’affichent.

Sur n’importe quel téléphone, [themachine.computer/app](https://themachine.computer/app) ouvre la bonne boutique. **Paramètres**, **Applis** affiche les deux boutiques en haut, ou uniquement celle de votre téléphone si vous êtes sur un téléphone. Sur un ordinateur, **Ordinateur** installe le tableau de bord comme une application : consultez [Installer l’application](phone-app.md).

## Connexion

Sur une Machine hébergée, l’application se connecte avec votre compte. Sur une Machine auto-hébergée, ouvrez **Paramètres**, puis **Applis** sur un ordinateur : sous les boutiques, **Pas sur le Network ?** affiche un code. Installez l’application, puis scannez le code avec l’appareil photo de votre téléphone, ou saisissez dans l’application l’adresse affichée sous le code. L’application vous demande votre accord avant de se connecter, et la connexion à votre Machine reste nécessaire.

## Notifications

À son premier lancement, l’application vous demande l’autorisation d’envoyer des notifications. Touchez-en une pour ouvrir son contenu : une tâche ouvre son chat, le briefing du matin ouvre l’**Agenda** du jour, le briefing de l’équipe ouvre les Tâches et une question de Fleet ouvre sa tâche. Le texte d’une tâche ne transite jamais par Apple, Google ou le service de The Machine : ils ne transmettent qu’un message fixe, comme « Une tâche a besoin de vous ».

L’application demande ensuite à votre Machine le titre de la tâche et l’étape suivante, par exemple « Répondre à Sam » avec « Envoyer à Sam : mardi à 10 h, ça marche ». Le briefing du matin indique ce qui vous attend et l’heure de votre première réunion, le briefing de l’équipe ses premiers éléments et une mise à jour de Fleet ce qui s’est passé. Si elle ne parvient pas à joindre votre Machine, le message fixe reste affiché. Sur Android, la notification indique le nombre de tâches en attente, par exemple « 2 tâches ont besoin de vous ».

Une notification propose **Mettre en attente** (jusqu’à demain) et **Marquer comme fait**, ainsi que **Faire** pour une tâche qui n’a pas encore commencé. Ces actions fonctionnent après le déverrouillage du téléphone, sans ouvrir l’application. L’envoi et les étapes finales ouvrent toujours l’application. Une seule notification par tâche : « Préparation » devient « Prête », puis la notification disparaît une fois la tâche terminée ou mise en attente, ici ou ailleurs.

Lorsqu’une étape que vous avez confirmée est effectuée, sa notification indique **Fait** et ce qui s’est passé, jusqu’à ce que vous touchiez **Compris** dans les Tâches. Sur iPhone, vous pouvez attendre d’ouvrir l’application pour le faire.

Si vous désactivez **Texte dans les notifications** dans **Paramètres**, puis **Sécurité**, le message fixe reste affiché. C’est également le cas si votre écran verrouillé masque le contenu des notifications. Lorsqu’il n’y a rien à afficher, le message « Touchez pour ouvrir » apparaît. Si votre téléphone ne parvient pas à joindre votre Machine à la réception d’une notification, les détails s’affichent dès que la connexion est rétablie.

Les mêmes règles que pour les notifications push sur le Web s’appliquent : vos choix pour chaque type dans [Notifications](notifications.md), vos [heures de travail](work-hours.md) et aucune notification lorsque vous utilisez un tableau de bord.

Chaque téléphone équipé de l’application apparaît dans **Paramètres**, **Notifications**, sous **Téléphone avec l’app**. **Retirer** désactive ses notifications. Une Machine auto-hébergée doit être connectée au The Machine Network pour les recevoir ; l’application fonctionne sans elles.

## Partager vers The Machine

Dans n’importe quelle application, touchez Partager et choisissez The Machine. Une **Nouvelle tâche** s’ouvre avec le texte, le lien ou les fichiers partagés. Vérifiez-les, ajoutez une date si vous le souhaitez, puis ajoutez la tâche. Rien n’est ajouté avant cette étape.

Un fichier seul suffit, comme une facture ou une lettre. Votre Machine lit le texte d’un PDF et remplit la tâche : son objet, l’étape suivante et sa date. Le fichier est envoyé directement à votre Machine et y reste.

Sur Android, le tableau de bord installé comme application accepte aussi les partages : choisissez-le dans le menu de partage de la même manière.

Les forfaits et la facturation ne s’affichent pas dans l’application. **Ouvrir le compte** reste disponible dans **Paramètres** pour supprimer votre compte.
