---
title: État de Machine
area: connections
summary: Le journal de votre Machine, pour qu’elle repère elle-même ses problèmes. Elle ne fait que le lire.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
translated: 3a06400a28396465
---
## Ce qu’elle lit

Le journal de votre Machine : les exécutions échouées, les transferts refusés, les messages Telegram non envoyés et les erreurs de The Machine. Une tâche vous indique quand quelque chose doit être corrigé. Sur votre propre ordinateur, cela inclut **Terminer l’installation de la dernière mise à jour** : une partie d’une mise à jour nécessite un bref redémarrage pendant la nuit, mais cela n’a pas été possible certaines nuits. Demandez-le dans son chat et The Machine terminera l’installation. La tâche se ferme automatiquement une fois cette étape terminée.

## Correctifs mis de côté par une mise à jour

Quand The Machine se met à jour et que l’un de ses propres correctifs ne s’applique plus à la nouvelle version, la mise à jour le met de côté et continue, pour que votre Machine ne reste jamais sur une ancienne version. Une tâche, **Refaire un correctif mis de côté par la mise à jour**, indique de quel correctif il s’agit.

Avec **Refaire**, votre Machine recrée le correctif dans la nouvelle version, comme pour n’importe lequel de ses propres correctifs : vous voyez la modification et appuyez sur **Fusionner le correctif**. Une fois le correctif fusionné, l’ancienne copie est supprimée. Vous pouvez aussi fermer la tâche.

## Vos fichiers conservés lors d’une mise à jour

Quand une nouvelle version inclut un fichier portant le même nom qu’un fichier que vous avez ajouté, la mise à jour renomme votre fichier au lieu de l’écraser, puis continue. Une tâche indique combien de fichiers ont été conservés et donne, pour chacun, son ancien et son nouveau nom. Fermez-la une fois que vous les avez vérifiés.

## Ce qu’elle peut faire

Rien. Elle ne fait que lire le journal de votre Machine.

## La connecter

- Sur une Machine hébergée, elle apparaît sur votre page de configuration, sous **Plus de sources**, sous le nom **État de Machine**. Une par Machine.
- Sur votre propre ordinateur : exécutez `assistant connect gateway`.

## La supprimer

- Dans le tableau de bord : **Connexions**, ouvrez-la, puis sélectionnez **Détails** et **Déconnecter**.
- Sur une Machine hébergée, vous pouvez aussi sélectionner **Retirer** à côté de celle-ci sur votre page de configuration.

Il n’y a rien d’autre à désinstaller.
