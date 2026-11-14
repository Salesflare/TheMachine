---
title: Passer sur un autre ordinateur
area: getting-started
summary: Exportez tout ce que votre Machine sait dans un seul fichier chiffré, puis importez-le sur une autre Machine, hébergée ou installée sur votre ordinateur.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
translated: a08d8cd091c7d47b
---
Tout ce que votre Machine apprend vous appartient : messages, tâches, brouillons, Graph, souvenirs et compétences. Emportez tout sur une autre Machine ou gardez-en une copie.

## Exporter

Sur votre ordinateur :

1. Dans **Paramètres** › **Général** › **Exporter**, cliquez sur **Exporter** à côté de **Tout**.
2. Vous pouvez choisir une phrase secrète. Sinon, un code d’export vous sera fourni : notez-le, vous en aurez besoin pour l’importation.
3. Vous pouvez aussi activer **Inclure les clés et jetons** (une phrase secrète est nécessaire), pour ne pas avoir à reconnecter vos sources.
4. Cliquez sur **Lancer l’export**, puis sur **Télécharger**. Le fichier est supprimé après 24 heures, ou immédiatement si vous cliquez sur **Supprimer**.

Sur une Machine hébergée, cliquez sur **Exporter** à côté de **Tout** pour ouvrir la page de votre compte. Cliquez sur **Tout exporter**, puis sur **Télécharger**. Votre Machine supprime le fichier après 24 heures, ou immédiatement si vous cliquez sur **Supprimer maintenant**.

Le fichier est toujours chiffré. Les **Paramètres** indiquent ensuite ce qu’il contient et ce qu’il ne contient pas. Vous devrez vous reconnecter à vos comptes Google et Microsoft connectés via notre système de connexion hébergé.

## Importer

1. Dans **Paramètres** › **Général** › **Exporter**, cliquez sur **Choisir un fichier** à côté d’Import, puis sélectionnez l’export.
2. Saisissez la phrase secrète ou le code d’export, puis cliquez sur **Ouvrir**. The Machine vérifie d’abord l’intégralité du fichier.
3. Sur une Machine hébergée : cliquez sur **Importer maintenant**. Sur votre ordinateur : cliquez sur **Remplacer par cet export**, puis sur **Remplacer**. The Machine redémarre avec les données de l’export en quelques minutes, et les **Paramètres** affichent **Importée**.

L’importation remplace le contenu actuel de cette Machine, après en avoir conservé une copie. Rien n’est envoyé automatiquement : les envois en attente attendent votre action.

Si les **Paramètres** ne parviennent pas à redémarrer The Machine sur votre ordinateur, ils vous indiquent les commandes à exécuter.

Sur un nouvel ordinateur, [installez The Machine](self-hosted-setup.md) d’abord. Ensuite, annulez votre forfait hébergé si vous n’en avez plus besoin : consultez [Annuler ou supprimer](cancel-and-delete.md).
