---
title: Flux RSS
area: connections
summary: Publications d’un flux RSS ou Atom que vous suivez.
covers: connector:rss
code: connectors/rss.py
site: More sources
translated: efeb27dadc6163e9
---
## Ce qu’elle lit

Les nouvelles publications d’un flux RSS ou Atom par connexion. Ajoutez une connexion distincte pour chaque flux.

Elle consulte le flux toutes les 30 minutes, et jamais à moins de 15 minutes d’intervalle. Elle ne consulte que les adresses https:// publiques.

## Ce qu’elle peut faire

Rien. Elle se contente de consulter le flux.

## Connecter le flux

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Autres**, et choisissez **Flux RSS**. Sur une Machine hébergée, la page de configuration propose aussi cette option, sous **Plus de sources**. Sur votre propre ordinateur, vous pouvez aussi exécuter `assistant connect rss`.
2. Collez l’adresse du flux.

## Supprimer la connexion

Dans le tableau de bord : ouvrez le flux depuis **Connexions**, puis **Détails**, et enfin **Déconnecter**. Rien d’autre n’est à désinstaller.
