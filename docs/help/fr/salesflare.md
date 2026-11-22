---
title: Salesflare CRM
area: connections
summary: Comptes, contacts et opportunités pour savoir qui compte. La lecture se fait avec votre clé API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## Ce qu’elle lit

Vos comptes, vos contacts et vos opportunités dans Salesflare, ainsi que le fil d’activité de chaque compte : les e-mails de vos collègues auxquels vous n’étiez pas en copie et les réunions avec leurs notes.

## Ce qu’elle peut modifier

Rien. (Sur votre ordinateur, le paramètre `join_pipelines` peut l’autoriser à vous ajouter aux comptes des pipelines sélectionnés. Cette option est désactivée par défaut.)

## La connecter

1. Dans Salesflare, ouvrez [Paramètres, clés API](https://app.salesflare.com/#/settings/apikeys) et créez une clé.
2. Sur une Machine hébergée : ouvrez votre page de configuration à l’adresse app.themachine.computer/setup, allez dans **Plus de sources**, ouvrez Salesflare CRM, collez la clé et cliquez sur **Se connecter**.
3. Dans le tableau de bord : **Connexions**, **Clients**, Salesflare CRM, collez la clé et cliquez sur **Se connecter**. La carte indique ensuite l’avancement.

## Détails de la synchronisation

Dans **Connexions**, **Clients**, Salesflare indique l’avancement : le nombre de comptes lus lors de cette synchronisation et ceux qui ont été ignorés parce que Salesflare a répondu trop lentement. Si une synchronisation dure plusieurs heures, un message indique qu’elle est peut-être bloquée.

Les compteurs indiquent le nombre de comptes auxquels elle a pu accéder et le nombre d’e-mails et de réunions importés. Si votre clé API ne permet d’accéder à aucun compte dans Salesflare, la carte affiche **Attend votre aide** : utilisez la clé d’un utilisateur qui peut les consulter. Si Salesflare dépasse régulièrement le délai d’attente, mais que chaque nouvelle tentative aboutit, la carte indique que Salesflare est **parfois lent**.

Si Salesflare n’a pas activé l’accès au fil d’activité pour les clés API de votre équipe, la carte vous l’indique : aucun e-mail ni aucune réunion n’est importé tant que le support de Salesflare ne l’a pas activé. Une nouvelle vérification a lieu toutes les 10 minutes le premier jour, puis environ toutes les heures. La synchronisation reprend automatiquement dès que l’accès fonctionne.

- **Arrêter** : aucun nouvel élément n’est importé jusqu’à ce que vous cliquiez sur **Démarrer**. La synchronisation reprend là où elle en était.
- **Relancer la synchro** : recommence la synchronisation et lit à nouveau les données de la dernière semaine. Rien de ce qui a déjà été importé n’est perdu.
- **Clés API** : ouvre la page des clés API de Salesflare pour en créer une nouvelle.

## La supprimer

- Dans le tableau de bord : **Connexions**, ouvrez Salesflare, puis **Détails** et **Déconnecter**. Les données déjà importées sont conservées.
- Sur une Machine hébergée, vous pouvez aussi cliquer sur **Retirer** à côté de Salesflare sur votre page de configuration.

## Révoquer l’accès dans Salesflare

Supprimez la clé API dans Salesflare, sous Paramètres, clés API.
