---
title: L’installer sur votre propre ordinateur
area: getting-started
summary: Installez l’app open source sur Linux, macOS ou Windows. Gratuite, avec votre propre modèle et vos propres données.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
The Machine est open source (AGPL). Sur votre propre ordinateur, elle est gratuite, et vos données y restent.

## Ce qu’il faut

- OpenClaw 2026.10.7 ou plus récent. L’installateur propose de l’installer.
- Python 3.12 ou plus récent, et Node.js 24 (24.22.1 ou plus récent) ou 26.12.1 ou plus récent, pas 25.
- Tailscale, pour accéder à votre tableau de bord depuis votre téléphone.
- Votre propre compte utilisateur, pas root.

## L’installer

Sur Linux ou macOS (macOS est en bêta) :

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Sur Windows (bêta), elle tourne dans WSL2. Dans PowerShell, lancez `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Cela installe WSL2 avec Ubuntu et tout ce dont l’app a besoin, puis lance `./install.sh`.

L’installateur trouve vos comptes, les connecte un par un et montre un aperçu de la semaine passée avant que quoi que ce soit ne s’active.

## Après l’installation

- Ajoutez des sources avec `assistant connect`, ou **Connexions**, puis **+ Ajouter**, dans le tableau de bord.
- Vérifiez tout avec `assistant doctor`. Il affiche une solution pour chaque problème.
- Les mises à jour arrivent sous forme de versions signées.

Le guide complet est dans le dépôt : [Getting started](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
