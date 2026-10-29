---
title: Journal de la Machine
area: connections
summary: Le journal de votre Machine, pour qu’elle repère ses propres problèmes. Il ne fait que lire.
covers: connector:gateway
code: onboarding.py
site: More sources, Remove
---
## Ce qu’il lit

Le journal de votre OpenClaw Gateway : exécutions échouées, transferts refusés, messages Telegram qui ne sont pas partis, et erreurs de The Machine elle-même. Une tâche vous prévient quand quelque chose doit être réparé.

## Ce qu’il peut faire

Rien. Il ne fait que lire le journal sur votre propre Machine.

## Le connecter

- Sur une Machine hébergée, il se trouve sur votre page de configuration, sous **Plus de sources**, sous le nom OpenClaw Gateway log. Un par Machine.
- Sur votre propre ordinateur : lancez `assistant connect gateway`.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez-le, **Détails**, puis **Déconnecter**.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

Il n’y a rien à désinstaller ailleurs.
