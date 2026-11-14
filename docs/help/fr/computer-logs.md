---
title: Problèmes sur votre ordinateur
area: troubleshooting
summary: Votre Machine lit ses propres journaux système et vous signale les vrais problèmes, avec leur cause et une solution. Une solution ne s’exécute que si vous appuyez sur **Faire**.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## Ce que votre Machine lit

Sous Linux avec systemd, votre Machine lit le journal de votre propre session utilisateur : vos services et les rapports de plantage de vos programmes. Sur Omarchy, elle vérifie aussi Hyprland et la barre. Elle ne lit jamais le journal système complet et ne demande jamais d’accès supplémentaire.

Elle lit quel service s’est arrêté, comment il s’est terminé et quel programme a planté. Elle ne lit jamais le contenu des lignes du journal, qui n’est donc ni conservé ni transmis depuis votre ordinateur.

## Ce qui est considéré comme un problème

Un service qui redémarre sans cesse, qui a échoué plusieurs fois dans la journée ou qui reste arrêté, qui a manqué de mémoire, ainsi qu’un programme qui a planté. Sur Omarchy, cela inclut aussi les plantages de Hyprland ou de la barre, ainsi que les erreurs dans vos paramètres Hyprland.

Un seul redémarrage ou un seul échec est normal et ne donne lieu à aucune alerte. Il en va de même pour un service qui échoue quelques fois, puis fonctionne à nouveau correctement.

Les navigateurs pilotés par des tests et des agents (headless, Playwright, Puppeteer, CI) ne donnent lieu à aucune alerte. Il en va de même pour un programme qui s’arrête pendant l’arrêt ou le redémarrage de son service. Les exécutions de développement restent également silencieuses : ce qu’exécute un agent de programmation, les tests et les programmes lancés depuis un dossier temporaire ou de cache. Un programme qui plante à répétition donne lieu à une seule tâche indiquant combien de fois et quand cela s’est produit.

Un script est nommé d’après son propre nom, comme backup.py, et non d’après python3 ou node.

## Ce que vous recevez

Une tâche qui explique en termes simples ce qui s’est passé, pourquoi c’est important et ce que vous pouvez faire. Les commandes qui permettent de comprendre pourquoi se trouvent sous **Afficher plus**. Posez une question dans le chat associé et The Machine cherchera à en savoir plus. Tout changement attend votre accord, comme avec **Faire**.

Lorsqu’une solution sans risque est disponible, la tâche comporte le bouton **Faire**. Si l’un de vos services reste arrêté, elle le redémarre. Sur Omarchy, elle relance aussi la barre. **Faire** n’exécute que cette commande, et le résultat s’affiche dans le chat de la tâche. Elle ne touche jamais aux propres services de The Machine ni à l’OpenClaw Gateway.

Un même problème donne lieu à une seule tâche au maximum toutes les deux semaines, et jamais tant que sa tâche est encore ouverte. Vous ne recevrez pas plus de deux nouvelles tâches par jour. Une tâche concernant un service arrêté se ferme automatiquement dès que le service redémarre ou que son état est effacé.

## Dans un terminal

`assistant doctor` répertorie les mêmes problèmes survenus au cours de la dernière journée.

## Autres ordinateurs

Sur macOS, Windows et les ordinateurs sans systemd, votre Machine ne lit rien et vous l’indique dans `assistant doctor`.

Sur une Machine hébergée, c’est à notre serveur de rester opérationnel : ses problèmes sont transmis à l’équipe The Machine, et non à vous sous forme de tâches.

## Désactiver cette fonction

Définissez `"computer_logs": false` dans config.json, puis redémarrez le service.
