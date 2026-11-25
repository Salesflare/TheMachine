---
title: Une connexion a besoin de votre aide
area: troubleshooting
summary: Une source a besoin de votre aide ou cesse d’importer des données. Voici quoi essayer.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: cc4b227abd053022
---
## Vérifier son état

Ouvrez **Connexions**. Chaque source affiche son état :

- **Reconnexion automatique** : un petit problème passager. La source réessaie toute seule.
- **En attente de la première synchro** : la source vient d’être connectée. Patientez quelques minutes.
- **Prochaine lecture à** 07:00 : X et LinkedIn ne lisent les données que pendant la journée. Vous n’avez rien à faire.
- **Pas encore configuré** : personne ne s’y est encore connecté. Appuyez sur **Connecter**. La source démarre dans la minute qui suit.
- **Attend votre aide** : ouvrez **Détails**. Vous y trouverez la cause du problème et la marche à suivre.
- **Téléphone déconnecté** : votre téléphone Android ne communique plus avec votre Machine. Ouvrez l’app OpenClaw sur votre téléphone.

Une source qui n’importe rien depuis plus longtemps que d’habitude affiche **En attente d’une nouvelle synchro**. Le statut disparaît tout seul dès qu’une synchro aboutit.

Le nombre affiché sur **Connexions** ne compte que les sources qui nécessitent votre aide.

## Solutions courantes

- « Se reconnecter à Google » (ou à Microsoft) : une seule fois sur **Reconnecter** suffit pour rétablir toutes les sources de ce compte, comme Gmail et Agenda.
- « vous demande de vous reconnecter » : appuyez sur **Reconnecter**, puis connectez-vous.
- « nécessite un programme qui n’est pas installé sur cet ordinateur » : exécutez la commande indiquée sur sa fiche dans un terminal sur cet ordinateur. Elle précise quoi installer ou détecte un programme qui a changé d’emplacement.
- Microsoft configure encore l’accès : la source réessaie toute seule.
- Slack : appuyez sur **Reconnecter**. Vous vous êtes connecté avec une clé Maton ? Vérifiez la clé et la connexion Slack dans Maton.
- Android : ouvrez l’app OpenClaw sur le téléphone et autorisez-la à accéder aux notifications.

Sur votre propre ordinateur, `assistant doctor` vérifie chaque source et indique comment résoudre chaque problème.

Vous êtes toujours bloqué ? Consultez [Contacter le support](get-support.md).
