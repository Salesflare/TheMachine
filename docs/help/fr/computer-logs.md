---
title: Problèmes sur votre ordinateur
area: troubleshooting
summary: Votre Machine lit les journaux de son propre ordinateur et vous signale les vrais problèmes, avec leur cause et une solution. Une solution ne s’exécute que lorsque vous appuyez sur **Faire**.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## Journaux consultés

Sous Linux avec systemd, votre Machine lit le journal de votre propre session utilisateur : vos propres services et les rapports de plantage de vos propres programmes. Sur Omarchy, elle vérifie aussi Hyprland et la barre. Elle ne lit jamais le journal de tout le système et ne demande jamais d’accès supplémentaire.

Elle lit quel service s’est arrêté, comment il s’est terminé et quel programme a planté. Elle ne lit jamais le contenu des lignes du journal : aucun texte de journal n’est donc conservé ni transmis depuis votre ordinateur.

## Ce qui constitue un problème

Un service qui ne cesse de redémarrer, qui a échoué plusieurs fois dans la journée ou qui reste arrêté, un service à court de mémoire et un programme qui a planté. Sur Omarchy, un plantage de Hyprland ou de la barre, ainsi que des erreurs dans vos paramètres Hyprland.

Un seul redémarrage ou un seul échec est normal et ne donne lieu à aucune alerte. C’est aussi le cas d’un service qui a échoué quelques fois, puis a fonctionné correctement, et d’un service que rien ne tente de lancer : il n’est pas activé et aucun autre service ni minuteur ne le démarre.

Les navigateurs pilotés par des tests et des agents (headless, Playwright, Puppeteer, CI) ne donnent lieu à aucune alerte. C’est aussi le cas d’un programme qui s’arrête pendant l’arrêt ou le redémarrage de son service. Les exécutions de développement ne donnent pas non plus lieu à des alertes : ce qu’exécute un agent de programmation, les tests et les programmes lancés depuis un dossier temporaire ou de cache. Un programme qui plante sans cesse crée une seule tâche indiquant à quelle fréquence et quand cela s’est produit.

Un script est désigné par son propre nom, comme backup.py, et non par python3 ou node.

## Ce que vous recevez

Une tâche qui explique en termes simples ce qui s’est passé, pourquoi c’est important et ce que vous pouvez faire. Les commandes qui permettent de comprendre la cause se trouvent sous **Afficher plus**. Posez vos questions dans le chat de la tâche et The Machine cherchera la cause. Elle attend votre accord avant d’effectuer le moindre changement, comme avec **Faire**.

Lorsqu’une solution sans risque existe, la tâche propose **Faire**. Pour relancer un de vos services qui reste arrêté, elle le redémarre. Sur Omarchy, elle rétablit la barre. Le bouton **Faire** n’exécute que cette commande, et le résultat s’affiche dans le chat de la tâche. Elle ne touche jamais aux services de The Machine ni à OpenClaw Gateway.

Pour un même problème, une seule tâche au maximum est créée toutes les deux semaines, et jamais tant que la tâche est encore ouverte. Deux nouvelles tâches au maximum sont créées par jour. Une tâche concernant un service arrêté se ferme automatiquement dès qu’il redémarre ou que son état est réinitialisé.

## Dans un terminal

`assistant doctor` affiche les mêmes problèmes survenus au cours de la dernière journée.

## Autres ordinateurs

Sur macOS, Windows et les ordinateurs sans systemd, elle ne lit rien et le précise dans `assistant doctor`.

Sur une Machine hébergée, c’est à nous d’assurer le fonctionnement du serveur : les problèmes sont signalés à l’équipe The Machine, pas à vous sous forme de tâches.

## Désactiver cette fonction

Définissez `"computer_logs": false` dans config.json et redémarrez le service.
