---
title: Lancer The Machine sur votre propre ordinateur
area: getting-started
summary: Installez l’app open source sur Linux, macOS ou Windows. C’est gratuit, et vous utilisez votre propre modèle et vos propres données.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
Lancez The Machine gratuitement sur votre ordinateur. Le code est open source (AGPL) et vos données restent chez vous. Il vous faut un terminal pour l’installer, mais pas pour connecter vos comptes.

## Configuration requise

- OpenClaw 2026.11.2 ou version ultérieure, l’agent open source sur lequel The Machine s’appuie. L’installateur vous propose de l’installer.
- Python 3.12 ou version ultérieure, et Node.js 24 (24.22.1 ou version ultérieure) ou 26.12.1 ou version ultérieure, mais pas la version 25.
- Tailscale, pour accéder à votre tableau de bord depuis votre téléphone.
- Un compte utilisateur standard, pas root.

## Installation

Sous Linux ou macOS (macOS est en version bêta) :

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Sous Windows (version bêta), l’application s’exécute dans WSL2. Dans PowerShell, exécutez `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Cette commande configure WSL2 avec Ubuntu et tous les éléments nécessaires à l’application, puis exécute `./install.sh`.

L’installateur repère vos comptes, les connecte un par un et affiche un aperçu de la semaine dernière avant toute activation.

## Après l’installation

- Connectez votre messagerie : en haut de **Tâches**, cliquez sur **Gmail** (ou **Outlook**), puis sur **Associer cette Machine** pour l’associer à votre compte. Si vous n’avez pas de compte, **Utiliser votre propre app** se trouve juste en dessous.
- Cliquez ensuite sur **Se connecter avec Google** (ou **Se connecter avec Microsoft** pour Outlook). La messagerie et l’agenda se connectent ensemble.
- Pour les autres sources, cliquez sur **Connexions**, puis sur le type de source. Pour utiliser votre propre client Google ou votre app Entra : exécutez `assistant connect` dans un terminal.
- Vérifiez que tout fonctionne avec `assistant doctor`. Cette commande affiche une solution pour chaque problème.
- L’installateur installe la dernière version signée. Les mises à jour sont également publiées sous forme de versions signées.
- Associez-la à votre compte : l’app mobile l’ouvrira après votre connexion. La dissociation supprime ce lien.

Le guide complet se trouve dans le dépôt : [Premiers pas](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
