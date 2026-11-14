---
title: Une connexion a besoin de votre aide
area: troubleshooting
summary: Une source affiche **Attend votre aide** ou n'importe plus rien. Voici quoi essayer.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: 1c530fc2b291d640
---
## Vérifier son état

Ouvrez **Connexions**. Chaque source indique son état :

- **Reconnexion automatique** : un petit problème temporaire. La source réessaie toute seule.
- **En attente de la première synchro** : la connexion vient d'être établie. Patientez quelques minutes.
- **Reprise de la lecture à** 07:00 : X et LinkedIn ne récupèrent des données que pendant la journée. Rien à faire.
- **Attend votre aide** : ouvrez **Détails**. Vous y trouverez la cause du problème et la marche à suivre.
- **Téléphone déconnecté** : votre téléphone Android ne parvient pas à joindre votre Machine. Ouvrez l'application OpenClaw sur votre téléphone.

Une source qui n'importe rien pendant plus longtemps que d'habitude n'apparaît plus comme connectée. Le problème disparaît automatiquement dès que de nouveaux éléments arrivent.

Le nombre affiché sur **Connexions** correspond uniquement aux sources qui nécessitent votre aide.

## Résoudre les problèmes courants

- « Reconnectez-vous à Google » (ou Microsoft) : un clic sur **Reconnecter** rétablit toutes les sources de ce compte, comme Gmail et Calendar.
- « Vous devez vous reconnecter » : appuyez sur **Reconnecter**, puis connectez-vous.
- Microsoft configure encore l'accès : la connexion réessaie automatiquement.
- Slack : appuyez sur **Reconnecter**. Vous êtes connecté avec une clé Maton ? Vérifiez la clé et la connexion Slack dans Maton.
- Android : ouvrez l'application OpenClaw sur votre téléphone et autorisez-la à accéder aux notifications.

Sur votre propre ordinateur, `assistant doctor` vérifie chaque source et indique comment résoudre chaque problème.

Vous êtes toujours bloqué ? Consultez [Obtenir de l'aide](get-support.md).
