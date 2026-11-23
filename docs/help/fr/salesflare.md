---
title: Salesflare CRM
area: connections
summary: Comptes, contacts et opportunités, pour savoir qui compte. La connexion lit vos données avec votre clé API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## Ce qu’elle lit

Vos comptes, contacts et opportunités dans Salesflare, ainsi que le fil d’activité de chaque compte : les e-mails de collègues auxquels vous n’avez pas participé et les réunions avec leurs notes.

## Ce qu’elle peut modifier

Rien. (Sur votre ordinateur, le paramètre `join_pipelines` peut l’ajouter aux comptes des pipelines sélectionnés. Cette option est désactivée par défaut.)

## La connecter

1. Dans Salesflare, ouvrez [Paramètres, clés API](https://app.salesflare.com/#/settings/apikeys) et créez une clé.
2. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources**, ouvrez Salesflare CRM, collez la clé et appuyez sur **Connecter**.
3. Dans le tableau de bord : **Connexions**, **Clients**, Salesflare CRM, collez la clé et appuyez sur **Connecter**. Sa carte indique alors sa progression.

## Détails de la synchronisation

Dans **Connexions**, **Clients**, Salesflare indique sa progression : les comptes vérifiés pendant ce cycle, ceux qui ont été ignorés parce que Salesflare était trop lent et ceux auxquels votre clé API ne donne pas accès (**sans accès**). Si un cycle dure plusieurs heures, un message indique qu’il est peut-être bloqué.

Les vignettes indiquent le nombre de comptes lus cette semaine, ainsi que les e-mails et les réunions importés.

Quelques comptes sans accès ne nécessitent aucune intervention : le reste est importé normalement. Si votre clé API ne donne accès à aucun compte, la carte affiche **Attend votre aide** : utilisez la clé d’un utilisateur qui peut les consulter. Une nouvelle clé repart de zéro et relit la semaine écoulée. Si Salesflare expire souvent, mais que chaque nouvelle tentative aboutit, le statut indique que Salesflare est **parfois lent**.

Si Salesflare n’a pas activé l’accès au fil d’activité pour les clés API de votre équipe, la carte l’indique : aucun e-mail ni aucune réunion ne sera importé tant que le support Salesflare ne l’aura pas activé. La connexion vérifie à nouveau toutes les 10 minutes le premier jour, puis environ toutes les heures. Elle reprend automatiquement dès que l’accès fonctionne.

- **Arrêter** : rien de nouveau n’est importé tant que vous n’appuyez pas sur **Commencer**. La synchronisation reprend là où elle en était.
- **Relancer la synchro** : recommence la synchronisation et relit la semaine écoulée. Rien de ce qui a déjà été importé n’est perdu.
- **Clés API** : ouvre la page des clés API de Salesflare pour en créer une nouvelle.

## La retirer

- Dans le tableau de bord : **Connexions**, ouvrez Salesflare, puis **Détails** et **Déconnecter**. Les données déjà importées sont conservées.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Salesflare sur votre page de configuration.

## Révoquer l’accès dans Salesflare

Supprimez la clé API dans Salesflare, sous Paramètres, clés API.
