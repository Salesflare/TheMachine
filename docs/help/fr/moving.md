---
title: Passer sur votre propre ordinateur
area: getting-started
summary: Exportez tout depuis une Machine hébergée dans un seul fichier chiffré et importez-le sur votre propre ordinateur.
covers: moving
code: moving.py, cli.py
site: Export everything, Delete it now, Download
order: 5
---
## Exporter

1. Sur la page de votre compte, ouvrez Données et appuyez sur **Tout exporter**.
2. Si vous voulez, définissez une phrase secrète pour emporter vos clés. Sans phrase secrète, l’export reçoit un code et ces sources devront être reconnectées.
3. Appuyez sur **Télécharger**. Le fichier vient directement de votre serveur, qui le supprime après 24 heures, ou tout de suite avec **Le supprimer maintenant**.

Le fichier est toujours chiffré. Google demande toujours une nouvelle connexion de l’autre côté. La connexion à votre modèle et l’historique de vos chats restent sur place.

## Importer

Sur votre propre ordinateur, [installez The Machine](self-hosted-setup.md), puis lancez `assistant import` avec le fichier.

Résiliez ensuite votre forfait hébergé si vous n’en avez plus besoin : voir [Résilier ou supprimer](cancel-and-delete.md).
