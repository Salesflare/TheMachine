---
title: Santé de votre Machine
area: connections
summary: Le journal de votre Machine, pour qu’elle repère ses propres problèmes. Elle ne fait que le lire.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 7d66ff6a6a5d5b1d
---
## Ce qu’elle lit

Le journal de votre Machine : les exécutions échouées, les transferts refusés, les messages Telegram qui ne sont pas partis et les propres erreurs de The Machine. Une tâche vous indique quand quelque chose doit être corrigé. Sur votre ordinateur, cela inclut **Terminer l’installation de la dernière mise à jour** : une partie d’une mise à jour nécessite un bref redémarrage pendant la nuit, mais elle n’a pas pu le faire pendant plusieurs nuits. Demandez-le dans son chat et The Machine terminera l’installation. La tâche se ferme automatiquement une fois cette partie installée.

## Correctifs mis de côté par une mise à jour

Quand The Machine se met à jour et que l’un de ses correctifs ne fonctionne plus avec la nouvelle version, la mise à jour met ce correctif de côté et continue, pour que votre Machine ne reste jamais sur une ancienne version. Une tâche, **Refaire un correctif mis de côté par la mise à jour**, indique de quel correctif il s’agit.

Avec **Refaire**, votre Machine le recrée pour la nouvelle version, comme pour n’importe lequel de ses correctifs : vous voyez la modification et appuyez sur **Fusionner le correctif**. Une fois le correctif fusionné, l’ancienne copie est supprimée. Vous pouvez aussi fermer la tâche.

## Vos fichiers conservés lors d’une mise à jour

Quand une nouvelle version contient un fichier portant le même nom qu’un fichier que vous avez ajouté, la mise à jour renomme votre fichier au lieu de l’écraser, puis continue. Une tâche indique combien de fichiers ont été conservés et liste chaque ancien et nouveau nom. Fermez-la une fois que vous les avez vérifiés.

## Ce qu’elle peut faire

Rien. Elle ne fait que lire le journal de votre Machine.

## La connecter

- Sur une Machine hébergée, elle se trouve sur la page de configuration, sous **Plus de sources**, sous le nom **Santé de votre Machine**. Une par Machine.
- Sur votre ordinateur : **Connexions**, **Autres**, **Santé de votre Machine**. Ou exécutez `assistant connect gateway`.

## La supprimer

- Dans le tableau de bord : **Connexions**, ouvrez-la, puis **Détails** et **Déconnecter**.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur la page de configuration.

Il n’y a rien à désinstaller ailleurs.
