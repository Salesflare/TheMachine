---
title: Installer l’app et activer les notifications
area: getting-started
summary: Installez The Machine sur votre téléphone ou votre ordinateur pour recevoir une notification pour chaque tâche. Telegram est facultatif.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
translated: c1ead6181c38a6d8
---
Installez The Machine comme une application sur votre téléphone ou votre ordinateur pour recevoir une notification pour chaque tâche, résultat et rappel, pendant vos [heures de travail](work-hours.md). Choisissez ce qu’elle envoie dans **[Notifications](notifications.md)**.

La tâche **Tirez le meilleur de The Machine**, en haut de la liste des tâches, propose une ligne pour chaque action : **Télécharger l’app mobile** (voir [L’application mobile](mobile-app.md)), **Télécharger l’app de bureau** (voir [L’application de bureau](desktop-app.md)), **Activer les notifications** et **Installer sur cet ordinateur**. Seuls les éléments qui manquent sur l’appareil s’affichent. La croix × ferme une ligne. Vous retrouverez les mêmes commandes dans **Paramètres**, **Général**, **Cet appareil**.

**Installer sur cet ordinateur** s’affiche uniquement sur un ordinateur sans l’app de bureau, comme un Chromebook.

Dans l’app mobile, le message **Recevez une notification quand quelque chose nécessite votre attention.** s’affiche lorsque les notifications sont désactivées. **Activer** demande l’autorisation au téléphone ou ouvre ses réglages. **×** masque le message pendant 7 jours.

## Sur un ordinateur (Chrome ou Edge)

1. Ouvrez votre tableau de bord, puis cliquez sur **Installer l’app** dans Paramètres, **Général**, **Cet appareil**, ou sur **Installer** dans la ligne de cette tâche sur un Chromebook.
2. The Machine s’ouvre dans sa propre fenêtre. Épinglez-la à votre barre des tâches ou à votre Dock.
3. Cliquez sur **Activer** dans sa ligne et autorisez les notifications. Une notification de test s’affiche immédiatement.

## Sur un Mac (Safari)

1. Dans la barre des menus de Safari, choisissez Fichier, puis Ajouter au Dock.
2. Ouvrez The Machine depuis le Dock, puis cliquez sur **Activer**.

## Dans Firefox

Firefox ne permet pas de l’installer comme une application. Les notifications fonctionnent dans l’onglet : cliquez sur **Activer** dans sa ligne ou sur la cloche à côté de **Notifications** dans les paramètres.

## Sur un iPhone ou un iPad

1. Ouvrez votre tableau de bord dans Safari. iOS 16.4 ou une version ultérieure est nécessaire.
2. Touchez Partager, puis Ajouter à l’écran d’accueil.
3. Ouvrez The Machine depuis l’écran d’accueil, puis touchez **Activer**.

Les notifications fonctionnent uniquement depuis l’app installée sur l’écran d’accueil, pas dans un onglet Safari.

## Sur Android

1. Ouvrez votre tableau de bord dans Chrome, ouvrez le menu, puis touchez Installer l’app.
2. Ouvrez l’app depuis votre écran d’accueil et touchez **Activer**.

## Vérifier ou modifier les réglages

Dans **Paramètres**, **Général**, **Cet appareil**, la cloche à côté de **Notifications** active ou désactive les notifications sur cet appareil uniquement, et **Envoyer un test** lui envoie une notification.

L’accès est bloqué ? Sur un ordinateur, cliquez sur l’icône à gauche de l’adresse et autorisez les notifications. Sur un iPhone, ouvrez l’app Réglages, puis Notifications, puis The Machine.

## Accès rapide

L’app s’ouvre immédiatement sur vos dernières tâches, puis les actualise. Cette copie reste sur l’appareil, chiffrée, pendant 7 jours maximum, et disparaît lorsque vous vous déconnectez.

## Hors ligne ou connexion Wi-Fi instable

Dans un avion ou un train, le tableau de bord reste accessible. Une barre en haut indique **Hors ligne** et la date de la dernière mise à jour. Vos tâches, leurs chats, l’Agenda et les listes Graph s’ouvrent depuis l’appareil.

- **Mettre en attente**, **Pas nécessaire**, **Marquer comme fait**, **Rouvrir** et les messages de chat adressés à The Machine restent en attente sur l’appareil, avec l’option **Annuler**. Ils sont envoyés automatiquement dès que vous êtes de nouveau en ligne.
- Les messages adressés à d’autres personnes ne sont jamais mis en attente : renvoyez-les lorsque vous êtes de nouveau en ligne.
- Ce que vous saisissez dans un chat reste sur l’appareil jusqu’à l’envoi, même après une actualisation.
- L’app réessaie automatiquement. **Essayer maintenant** relance la tentative immédiatement.
- Votre Machine est accessible via Tailscale, et un téléphone peut désactiver Tailscale en arrière-plan. Si votre Machine n’est plus accessible de cette façon, la barre indique **Tailscale est peut-être désactivé sur cet appareil**. Sur un téléphone, **Ouvrir Tailscale** ouvre l’app, ou sa page dans la boutique, pour vous permettre de la réactiver.
- Une Machine occupée peut mettre du temps à répondre. L’app affiche alors **Votre Machine répond lentement** et conserve ce qui est affiché. Cela ne signifie pas que vous êtes hors ligne.

## Autres appareils

Connectez-vous de la même manière sur chaque appareil. Sur une Machine hébergée, une clé d’accès par appareil accélère la connexion : dans **Paramètres** › **Compte**, cliquez sur **Gérer** à côté de Connexion.

Pour consulter les notifications de votre téléphone Android comme source, voir [Notifications Android](android.md).
