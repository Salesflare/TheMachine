---
title: Une connexion a besoin d’aide
area: troubleshooting
summary: Une source indique Attend votre aide, ou ne récupère plus rien. Ce qu’il faut essayer.
covers: 
code: onboarding.py, dashboard.html
order: 1
---
## Vérifier son état

Ouvrez **Connexions**. Chaque source indique son état :

- **Reconnexion automatique** : un petit accroc. Elle réessaie d’elle-même.
- **En attente de la première synchro** : tout juste connectée. Laissez-lui quelques minutes.
- **Lit à nouveau à** 07:00 : X et LinkedIn ne lisent qu’en journée. Rien à faire.
- **Attend votre aide** : ouvrez **Détails**. Elle dit ce qui n’a pas marché et quoi faire.

Le nombre sur **Connexions** ne compte que les sources qui attendent votre aide.

## Solutions courantes

- « doit être reconnecté » : appuyez sur **Reconnecter** et connectez-vous. Sur une Machine hébergée, Google et Microsoft se reconnectent depuis votre page de configuration.
- Microsoft prépare encore l’accès : il réessaie de lui-même.
- Slack : vérifiez votre clé API Maton et la connexion Slack dans Maton.
- Android : ouvrez l’app OpenClaw sur le téléphone, et autorisez-lui l’accès aux notifications.

Sur votre propre ordinateur, `assistant doctor` vérifie chaque source et affiche la solution pour chaque problème.

Toujours bloqué ? Voir [Obtenir de l’aide](get-support.md).
