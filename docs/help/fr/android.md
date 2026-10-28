---
title: Notifications Android
area: connections
summary: Les notifications de votre téléphone Android, via l’app OpenClaw. Il se contente de lire.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, More sources, Remove
---
## Ce qu’il lit

Les notifications qui arrivent sur votre téléphone Android, via l’app OpenClaw. Les codes à usage unique sont exclus, ainsi que les notifications WhatsApp, Telegram, Signal et Discord.

## Ce qu’il peut faire

Rien sur votre téléphone. Il se contente de lire les notifications.

## Le connecter

Sur une Machine hébergée :

1. Installez l’app OpenClaw sur votre téléphone.
2. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, choisissez Téléphone Android et appuyez sur **Afficher un code de configuration**.
3. Scannez-le dans l’app OpenClaw, puis appuyez sur **Approuver** pour l’association.
4. Dans l’app OpenClaw, activez Forward Notification Events, et autorisez l’accès aux notifications quand Android le demande.

Sur votre propre ordinateur, associez le téléphone à votre OpenClaw Gateway, puis lancez `assistant connect android`.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Android, **Détails**, puis **Déconnecter**.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le retirer sur le téléphone

Désactivez l’accès aux notifications pour l’app OpenClaw dans les paramètres d’Android, ou dissociez le téléphone dans l’app OpenClaw.
