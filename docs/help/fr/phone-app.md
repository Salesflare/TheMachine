---
title: Installer l’app et activer les notifications
area: getting-started
summary: Installez The Machine sur votre téléphone ou votre ordinateur et recevez une notification pour chaque tâche. Telegram est facultatif.
covers: phone-app
code: manifest.webmanifest, sw.js, dashboard.html
order: 3
---
Le tableau de bord s’installe comme une app sur un téléphone ou un ordinateur. Il envoie alors une notification pour chaque tâche, résultat et rappel quand vous n’êtes pas sur le tableau de bord, pendant vos [heures de travail](work-hours.md). Choisissez ce qu’il envoie dans [Notifications](notifications.md).

Une note discrète en haut de Tâches propose les deux, l’un après l’autre : d’abord l’app, puis les notifications. **Pas maintenant** la masque pendant 14 jours, et un second **Pas maintenant** l’arrête sur cet appareil. Les mêmes réglages restent dans **Paramètres**, **Général**, **Cet appareil**.

## Sur un ordinateur (Chrome ou Edge)

1. Ouvrez votre tableau de bord et cliquez sur **Installer** dans cette note, ou sur **Installer l’app** dans les Paramètres.
2. The Machine s’ouvre dans sa propre fenêtre. Épinglez-la à votre barre des tâches ou à votre Dock.
3. Cliquez sur **Activer** dans la note suivante et autorisez les notifications. Une notification de test s’affiche tout de suite.

## Sur un Mac (Safari)

1. Dans la barre de menus de Safari, choisissez Fichier, puis Ajouter au Dock.
2. Ouvrez The Machine depuis le Dock et cliquez sur **Activer**.

## Dans Firefox

Firefox ne peut pas l’installer comme app. Les notifications fonctionnent dans l’onglet : cliquez sur **Activer** dans cette note, ou sur la cloche à côté de **Notifications** dans les Paramètres.

## Sur un iPhone ou un iPad

1. Ouvrez votre tableau de bord dans Safari. Il faut iOS 16.4 ou plus récent.
2. Touchez Partager, puis Sur l’écran d’accueil.
3. Ouvrez The Machine depuis votre écran d’accueil et touchez **Activer**.

Les notifications ne fonctionnent que depuis l’app de l’écran d’accueil, pas dans un onglet Safari.

## Sur Android

1. Ouvrez votre tableau de bord dans Chrome et touchez **Installer** dans cette note, ou ouvrez le menu et touchez Installer l’application.
2. Ouvrez-la depuis votre écran d’accueil et touchez **Activer**.

## Vérifier ou modifier

Dans **Paramètres**, **Général**, **Cet appareil**, la cloche à côté de **Notifications** les active ou les désactive pour cet appareil seulement, et **Envoyer un test** lui en envoie une.

Si les notifications sont bloquées, la ligne indique où les autoriser à nouveau : sur un ordinateur, cliquez sur l’icône à gauche de l’adresse et autorisez les notifications. Sur un iPhone, ouvrez l’app Réglages, Notifications, The Machine.

## Ouverture rapide

L’app s’ouvre tout de suite avec vos dernières tâches, puis les met à jour. Sans connexion, elle affiche ce qu’elle avait, marqué **Hors ligne** avec l’heure de la dernière mise à jour. Cette copie reste sur l’appareil 7 jours au plus, chiffrée, et disparaît quand vous vous déconnectez.

## Hors ligne et Wi-Fi capricieux

Dans un avion ou un train, le tableau de bord continue de fonctionner. Une barre en haut indique **Hors ligne** et l’heure de la dernière mise à jour de ce que vous voyez. Vos tâches, leurs chats, l’Agenda et les listes du Graph s’ouvrent depuis l’appareil.

- **Mettre en attente**, **Pas nécessaire**, **Marquer comme fait**, **Rouvrir** et les notes ou messages de chat à The Machine attendent sur l’appareil. La tâche indique que ce sera enregistré dès votre retour en ligne, avec **Annuler** d’ici là. Dès que votre Machine répond de nouveau, ils partent d’eux-mêmes, dans l’ordre, une seule fois chacun.
- Les messages à d’autres personnes n’attendent jamais. **Envoyer** indique que vous êtes hors ligne : renvoyez une fois de retour.
- Ce que vous tapez dans un chat reste sur l’appareil jusqu’à l’envoi, même après un rechargement.
- L’app réessaie d’elle-même, un peu plus tard à chaque fois. **Essayer maintenant** réessaie tout de suite.

## Plus d’appareils

Connectez-vous sur chaque appareil de la même façon. Sur une Machine hébergée, une clé d’accès par appareil rend la connexion plus rapide : ajoutez-en une sous Sécurité, sur la page de votre compte.

Pour lire les notifications de votre téléphone Android comme source, voir [Notifications Android](android.md).
