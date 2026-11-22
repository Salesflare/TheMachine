---
title: Une connexion nécessite votre aide
area: troubleshooting
summary: Une source affiche **Attend votre aide** ou cesse d’importer des données. Voici quoi essayer.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: c07a7f214b1e4deb
---
## Vérifier son état

Ouvrez **Connexions**. Chaque source indique son état :

- **Reconnexion automatique** : un petit problème passager. La source réessaie automatiquement.
- **En attente de la première synchro** : la connexion vient d’être établie. Patientez quelques minutes.
- **Reprend la lecture à** 07:00 : X et LinkedIn ne lisent les données que pendant la journée. Rien à faire.
- **Attend votre aide** : ouvrez **Détails**. Vous y trouverez la cause du problème et la marche à suivre.
- **Téléphone déconnecté** : votre téléphone Android n’arrive pas à joindre votre Machine. Ouvrez l’application OpenClaw sur votre téléphone.

Une source qui n’importe plus rien depuis plus longtemps que d’habitude affiche **En attente d’une nouvelle synchro**. Le statut disparaît automatiquement dès qu’une synchronisation aboutit.

Le nombre affiché sur **Connexions** compte uniquement les sources qui nécessitent votre aide.

## Solutions courantes

- « Connectez-vous à Google à nouveau » (ou Microsoft) : une seule action sur **Reconnecter** rétablit toutes les sources de ce compte, comme Gmail et Agenda.
- « vous devez vous reconnecter » : appuyez sur **Reconnecter**, puis connectez-vous.
- Microsoft est encore en train de configurer l’accès : une nouvelle tentative se fait automatiquement.
- Slack : appuyez sur **Reconnecter**. Vous êtes connecté avec une clé Maton ? Vérifiez la clé et la connexion Slack dans Maton.
- Android : ouvrez l’application OpenClaw sur le téléphone et autorisez-la à accéder aux notifications.

Sur votre ordinateur, `assistant doctor` vérifie chaque source et indique comment résoudre chaque problème.

Vous êtes toujours bloqué ? Consultez [Contacter le support](get-support.md).
