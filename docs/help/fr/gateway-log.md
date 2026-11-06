---
title: Santé de votre Machine
area: connections
summary: Le journal de votre Machine, pour qu’elle repère ses propres problèmes. Il ne fait que lire.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Ce qu’il lit

Le journal de votre Machine : exécutions échouées, transferts refusés, messages Telegram qui ne sont pas partis, et erreurs de The Machine elle-même. Une tâche vous prévient quand quelque chose doit être réparé.

## Correctifs mis de côté par une mise à jour

Quand The Machine se met à jour et qu’un de ses propres correctifs ne convient plus à la nouvelle version, la mise à jour met ce correctif de côté et continue, pour que votre Machine ne reste jamais sur une ancienne version. Une tâche, **Refaire un correctif mis de côté par la mise à jour**, nomme le correctif. Demandez à le refaire sur la nouvelle version, ou fermez la tâche.

## Vos propres fichiers gardés par une mise à jour

Quand une nouvelle version apporte un fichier portant le même nom qu’un fichier que vous avez ajouté vous-même, la mise à jour renomme le vôtre au lieu de l’écraser et continue. Une tâche indique combien elle en a gardé et donne chaque ancien et nouveau nom. Fermez-la une fois que vous les avez vérifiés.

## Ce qu’il peut faire

Rien. Il ne fait que lire le journal sur votre propre Machine.

## Le connecter

- Sur une Machine hébergée, il se trouve sur votre page de configuration, sous **Plus de sources**, sous le nom Santé de votre Machine. Un par Machine.
- Sur votre propre ordinateur : lancez `assistant connect gateway`.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez-le, **Détails**, puis **Déconnecter**.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

Il n’y a rien à désinstaller ailleurs.
