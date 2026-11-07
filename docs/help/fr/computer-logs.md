---
title: Problèmes sur votre ordinateur
area: troubleshooting
summary: Votre Machine lit les journaux de son ordinateur et vous signale les vrais problèmes, avec la cause et une solution. Elle ne fait que lire.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## Ce qu’elle lit

Sous Linux avec systemd, votre Machine lit le journal de votre propre session : vos propres services et les rapports de plantage de vos propres programmes. Sous Omarchy, elle vérifie aussi Hyprland et la barre. Elle ne lit jamais le journal de tout le système et ne demande jamais plus d’accès.

Elle lit quel service s’est arrêté, comment il s’est terminé et quel programme a planté. Jamais le contenu d’une ligne de journal : aucun texte de journal n’est gardé ni ne quitte votre ordinateur.

## Ce qui compte comme problème

Un service qui redémarre sans cesse, un service qui a échoué plusieurs fois dans la journée ou reste arrêté, un service à court de mémoire, et un programme qui a planté. Sous Omarchy aussi un plantage de Hyprland ou de la barre, et des erreurs dans vos réglages Hyprland.

Un seul redémarrage ou une seule exécution ratée, c’est normal : rien ne s’affiche.

## Ce que vous recevez

Une tâche qui dit en mots simples ce qui s’est passé, pourquoi c’est important et la commande qui le montre ou le répare. Demandez dans son chat et The Machine s’en occupe. Tout ce qu’elle modifie attend votre accord, comme avec Do it.

Un même problème donne au plus une tâche toutes les deux semaines, et jamais tant que sa tâche est ouverte. Au plus deux nouvelles par jour.

## Dans un terminal

`assistant doctor` liste les mêmes problèmes du dernier jour.

## Autres ordinateurs

Sous macOS, Windows et sur les ordinateurs sans systemd, elle ne lit rien et le dit dans `assistant doctor`.

## La désactiver

Mettez `"computer_logs": false` dans config.json et redémarrez le service.
