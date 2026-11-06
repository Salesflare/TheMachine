---
title: Passer sur un autre ordinateur
area: getting-started
summary: Exportez tout ce que votre Machine sait dans un seul fichier chiffré et importez-le sur une autre Machine, hébergée ou la vôtre.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Tout ce que votre IA apprend vous appartient : messages, conversations, tâches avec leur historique, brouillons, le Graph, souvenirs, compétences et tâches d’agent. Vous pouvez tout emporter, même si vous arrêtez d’utiliser The Machine.

## Exporter

Sur votre propre ordinateur :

1. Dans **Paramètres** › **Général** › **Exporter**, appuyez sur **Exporter** à côté de Tout.
2. Si vous voulez, choisissez une phrase secrète. Sans elle, vous recevez un code d’export : notez-le, l’import en a besoin.
3. Si vous voulez, activez **Inclure les clés et jetons** (demande une phrase secrète) pour ne pas reconnecter vos sources.
4. Appuyez sur **Lancer l’export**, puis sur **Télécharger**. Le fichier est supprimé après 24 heures, ou tout de suite avec **Supprimer**.

Sur une Machine hébergée, **Exporter** à côté de Tout ouvre la page de votre compte. Appuyez sur **Tout exporter**, puis sur **Télécharger**. Votre Machine supprime le fichier après 24 heures, ou tout de suite avec **Le supprimer maintenant**.

Le fichier est toujours chiffré. Après un export, les Paramètres montrent ce qu’il contient, avec les nombres, et ce qu’il ne contient pas, avec la raison. Les connexions à Google et Microsoft via le service hébergé demandent toujours une nouvelle connexion de l’autre côté.

## Importer

1. Dans **Paramètres** › **Général** › **Exporter**, appuyez sur **Choisir un fichier** à côté d’Importer et choisissez l’export.
2. Saisissez sa phrase secrète ou son code d’export et appuyez sur **Ouvrir**. The Machine vérifie d’abord tout le fichier.
3. Hébergée : appuyez sur **Importer maintenant**. The Machine redémarre avec dans quelques minutes. Sur votre propre ordinateur : appuyez sur **Remplacer par cet export**, puis sur **Remplacer**. The Machine redémarre avec dans une minute ou deux, et les Réglages affichent **Importée**.

L’import remplace ce que cette Machine contient et en garde d’abord une copie. Rien de ce qui attendait ne part tout seul : les envois en file attendent que vous les renvoyiez.

Avancé : sur un ordinateur où The Machine tourne sans gestionnaire de services, les Réglages affichent les commandes. Vous pouvez aussi les lancer vous-même : `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

Sur un nouvel ordinateur, [installez d’abord The Machine](self-hosted-setup.md). Résiliez ensuite votre abonnement hébergé si vous n’en avez plus besoin : voir [Résilier ou supprimer](cancel-and-delete.md).
