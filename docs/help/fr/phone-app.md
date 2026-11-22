---
title: Installer l’app et activer les notifications
area: getting-started
summary: Installez The Machine sur votre téléphone ou votre ordinateur pour recevoir une notification pour chaque tâche. Telegram est facultatif.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
translated: 3c10a121b1cfb06d
---
Installez The Machine comme une appli sur votre téléphone ou votre ordinateur pour recevoir une notification pour chaque tâche, résultat et rappel, pendant vos [heures de travail](work-hours.md). Choisissez ce qu’elle envoie dans **Notifications** ([Notifications](notifications.md)).

La tâche **Tirez le meilleur de The Machine**, en haut de la liste Tâches, comporte une ligne pour chaque option : **Télécharger l’app mobile** (voir [L’app mobile](mobile-app.md)), **Activer les notifications** et **Installer sur cet ordinateur**. Seules les options qui ne sont pas encore disponibles sur cet appareil s’affichent. Le × sur une ligne la ferme. Ces mêmes options restent disponibles dans **Paramètres**, **Général**, **Cet appareil**.

Dans l’application mobile, le message **Recevez une alerte quand quelque chose a besoin de vous.** s’affiche lorsque les notifications sont désactivées. **Activer** demande l’autorisation au téléphone ou ouvre ses paramètres. **×** masque le message pendant 7 jours.

## Sur ordinateur (Chrome ou Edge)

1. Ouvrez votre tableau de bord, puis cliquez sur **Installer** dans la ligne correspondante de cette tâche, sur **Installer l’app** dans **Paramètres**, **Général**, ou sur **Installer** à côté de **Ordinateur** dans **Paramètres**, **Applis**.
2. The Machine s’ouvre dans sa propre fenêtre. Épinglez-la à la barre des tâches ou au Dock.
3. Cliquez sur **Activer** dans la ligne correspondante et autorisez les notifications. Une notification de test s’affiche immédiatement.

## Sur Mac (Safari)

1. Dans la barre de menus de Safari, choisissez **Fichier**, puis **Ajouter au Dock**.
2. Ouvrez The Machine depuis le Dock, puis cliquez sur **Activer**.

## Dans Firefox

Firefox ne permet pas d’installer l’application. Les notifications fonctionnent dans l’onglet : cliquez sur **Activer** dans la ligne correspondante ou sur la cloche à côté de **Notifications** dans les paramètres.

## Sur iPhone ou iPad

1. Ouvrez votre tableau de bord dans Safari. iOS 16.4 ou une version ultérieure est nécessaire.
2. Touchez **Partager**, puis **Sur l’écran d’accueil**.
3. Ouvrez The Machine depuis l’écran d’accueil, puis touchez **Activer**.

Les notifications fonctionnent uniquement depuis l’application sur l’écran d’accueil, pas dans un onglet Safari.

## Sur Android

1. Ouvrez votre tableau de bord dans Chrome, ouvrez le menu, puis touchez **Installer l’app**.
2. Ouvrez l’application depuis l’écran d’accueil, puis touchez **Activer**.

## Vérifier ou modifier les paramètres

Dans **Paramètres**, **Général**, **Cet appareil**, la cloche à côté de **Notifications** permet d’activer ou de désactiver les notifications pour cet appareil uniquement. **Envoyer un test** en envoie une sur cet appareil.

Vous ne recevez pas les notifications ? Sur un ordinateur, cliquez sur l’icône à gauche de l’adresse et autorisez les notifications. Sur iPhone, ouvrez l’app Réglages, puis Notifications et The Machine.

## Ouverture rapide

L’application affiche tout de suite vos dernières tâches, puis les actualise. Cette copie reste sur l’appareil, chiffrée, pendant 7 jours maximum, et est supprimée lorsque vous vous déconnectez.

## Hors ligne ou Wi-Fi instable

Dans l’avion ou le train, le tableau de bord continue de fonctionner. Une barre en haut indique **Hors ligne** et la date de la dernière actualisation. Vos tâches, leurs chats, l’agenda et les listes Graph s’ouvrent depuis l’appareil.

- **Mettre en attente**, **Pas nécessaire**, **Marquer comme fait**, **Rouvrir** et les messages de chat destinés à The Machine restent en attente sur l’appareil, avec **Annuler**. Ils sont envoyés automatiquement dès que vous êtes de nouveau en ligne.
- Les messages destinés à d’autres personnes ne sont jamais mis en attente. Renvoyez-les lorsque vous êtes de nouveau en ligne.
- Le texte que vous saisissez dans un chat reste sur l’appareil jusqu’à son envoi, même après le rechargement de la page.
- L’application réessaie automatiquement. **Essayer maintenant** relance immédiatement la tentative.
- Votre propre Machine est accessible par Tailscale, et un téléphone peut désactiver Tailscale en arrière-plan. Lorsque votre Machine est inaccessible de cette façon, la barre indique **Tailscale est peut-être désactivé sur cet appareil**. Sur un téléphone, **Ouvrir Tailscale** ouvre l’application ou sa page dans la boutique pour vous permettre de la réactiver.
- Une Machine très sollicitée peut mettre du temps à répondre. L’application affiche alors **Votre Machine met du temps à répondre** et conserve ce qui est à l’écran. Cela ne signifie pas que vous êtes hors ligne.

## Autres appareils

Connectez-vous de la même manière sur chaque appareil. Sur une Machine hébergée, une clé d’accès par appareil accélère la connexion : dans **Paramètres** › **Compte**, appuyez sur **Gérer** à côté de **Connexion**.

Pour lire les notifications de votre téléphone Android comme source, consultez [Notifications Android](android.md).
