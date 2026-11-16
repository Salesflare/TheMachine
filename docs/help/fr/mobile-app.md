---
title: L’application mobile
area: getting-started
summary: The Machine sur iPhone et Android : des notifications pour vos tâches et le partage vers The Machine depuis n’importe quelle appli.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
translated: f622bdc266f69965
---
L’application mobile ouvre votre propre tableau de bord, avec le même compte que sur le web. Téléchargez-la sur l’[App Store](https://apps.apple.com/app/id6829875215) pour iPhone et iPad, ou sur [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) pour Android.

La tâche **Tirez le meilleur de The Machine**, en haut de la section Tâches, vous la recommande. Dans le navigateur d’un téléphone, **Obtenir** ouvre la boutique. Sur un téléphone configuré pour afficher les sites pour ordinateur, les liens vers les deux boutiques s’affichent. Sur un ordinateur, un code QR à scanner avec votre téléphone s’affiche, avec les liens vers les deux boutiques.

Sur n’importe quel téléphone, [themachine.computer/app](https://themachine.computer/app) ouvre la bonne boutique. **Paramètres**, **Applis** affiche les deux boutiques en haut, ou seulement celle de votre téléphone si vous êtes sur un téléphone. Sur un ordinateur, **Ordinateur** installe le tableau de bord comme une appli : consultez [Installer l’appli](phone-app.md).

## Connecter l’appli

Sur une Machine hébergée, l’appli se connecte avec votre compte. Sur une Machine auto-hébergée, ouvrez **Paramètres**, puis **Applis** sur un ordinateur : sous les boutiques, **Pas sur le Network ?** affiche un code. Installez l’appli, puis scannez le code avec l’appareil photo de votre téléphone ou saisissez dans l’appli l’adresse affichée en dessous. L’appli vous demande votre autorisation avant de se connecter, et la connexion à votre Machine reste nécessaire.

**Se connecter avec** un service sous **Connexions** (Shortcut, Notion, Slack, Zoom et les autres) ouvre l’écran de connexion de votre téléphone. Une fois connecté, vous retrouvez l’appli, et la nouvelle connexion apparaît automatiquement dans **Connexions**.

## Notifications

À sa première ouverture, l’appli vous demande l’autorisation d’envoyer des notifications. Touchez-en une pour ouvrir le contenu correspondant : une tâche s’affiche en surbrillance dans votre liste, le briefing du matin ouvre la journée du jour dans **Agenda**, le brief d’équipe ouvre la section Tâches et une question de Fleet ouvre la tâche correspondante. Le texte d’une tâche ne transite jamais par Apple, Google ou le service de The Machine : ces services ne transmettent qu’un message fixe, comme « Une tâche vous attend ».

L’appli demande ensuite à votre propre Machine le titre de la tâche et l’étape suivante, par exemple « Répondre à Sam » avec « Envoyer à Sam : mardi à 10 h, ça marche ». Le briefing du matin indique ce qui vous attend et l’heure de votre première réunion, le brief d’équipe ses premiers éléments, et une mise à jour de Fleet ce qui s’est passé. Si l’appli ne parvient pas à joindre votre Machine, le message fixe reste affiché. Sur Android, le message indique le nombre de tâches en attente, comme « 2 tâches vous attendent ».

Une notification propose **Mettre en attente** (jusqu’au lendemain) et **Marquer comme fait**, ainsi que **Faire** pour une tâche qui n’a pas encore commencé. Ces actions fonctionnent après le déverrouillage du téléphone, sans ouvrir l’appli. L’envoi et les étapes finales ouvrent toujours l’appli. Une seule notification est envoyée par tâche : « En préparation » devient « Prête », puis la notification disparaît dès que la tâche est terminée ou mise en attente, dans l’appli ou ailleurs.

Quand une étape que vous avez confirmée est effectuée, sa notification indique **Fait** et précise ce qui s’est passé, jusqu’à ce que vous touchiez **Compris** dans la section Tâches. Sur iPhone, vous pouvez attendre la prochaine ouverture de l’appli.

Si **Texte dans les notifications** est désactivé dans **Paramètres**, puis **Sécurité**, le message fixe reste affiché. C’est aussi le cas si l’écran verrouillé masque le contenu des notifications. Quand rien ne peut être affiché, le message « Touchez pour ouvrir » apparaît. Si votre téléphone ne parvient pas à joindre votre Machine à l’arrivée d’une notification, les détails s’affichent dès qu’il est de nouveau en ligne.

Les notifications suivent les mêmes règles que les notifications push sur le web : vos choix pour chaque type dans [Notifications](notifications.md), vos [heures de travail](work-hours.md), et aucune notification lorsque vous utilisez un tableau de bord.

Chaque téléphone avec l’appli apparaît dans **Paramètres**, puis **Notifications**, sous **Téléphone avec l’app**. **Retirer** désactive ses notifications. Une Machine auto-hébergée doit être connectée à The Machine Network pour les recevoir. L’appli fonctionne sans elles.

## Partager vers The Machine

Dans n’importe quelle appli, touchez Partager et choisissez The Machine. Une **Nouvelle tâche** s’ouvre avec le texte, le lien ou les fichiers que vous avez partagés. Vérifiez le contenu, ajoutez une date si vous le souhaitez, puis ajoutez la tâche. Rien n’est ajouté avant cette étape.

Un fichier seul suffit, par exemple une facture ou une lettre. Votre Machine lit le texte d’un PDF et remplit la tâche : son objet, l’étape suivante et sa date. Le fichier est envoyé directement à votre Machine et y reste.

Sur Android, vous pouvez aussi partager des éléments vers le tableau de bord installé comme une appli : choisissez-le dans la feuille de partage, comme d’habitude.

Les forfaits et la facturation ne s’affichent pas dans l’appli. **Ouvrir le compte** reste disponible dans **Paramètres** pour supprimer votre compte.
