---
title: Notifications Android
area: connections
summary: Les notifications de votre téléphone Android, via l’application OpenClaw. Elle se contente de les lire.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
translated: 5b08b093662393a1
---
## Ce qu’elle lit

Les notifications de votre téléphone Android, via l’application OpenClaw. Les codes à usage unique sont exclus, tout comme les notifications de WhatsApp, Telegram, Signal et Discord.

## Ce qu’elle peut faire

Rien sur votre téléphone. Elle se contente de lire les notifications.

## La connecter

Sur une Machine hébergée :

1. Installez OpenClaw depuis Google Play sur votre téléphone.
2. Dans le tableau de bord, ouvrez **Connexions**, puis **Autres**, choisissez Notifications Android et appuyez sur **Afficher un code de configuration**.
3. Dans l’application OpenClaw, ajoutez un Gateway et scannez le code. De retour dans le tableau de bord, appuyez sur **Approuver**.
4. Autorisez l’accès aux notifications lorsque l’application vous le demande. Activez ensuite Transférer les événements de notification dans les paramètres de l’application, pour recevoir les notifications au fur et à mesure, et pas seulement lors de la vérification toutes les 10 minutes.

Sur votre propre ordinateur, associez le téléphone dans l’application OpenClaw, puis exécutez `assistant connect android`.

## La retirer

- Dans le tableau de bord : **Connexions**, ouvrez Android, **Détails**, puis **Déconnecter**.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de l’appareil sur votre page de configuration.

## La retirer du téléphone

Désactivez l’accès aux notifications de l’application OpenClaw dans les paramètres Android, ou dissociez le téléphone dans l’application OpenClaw.
