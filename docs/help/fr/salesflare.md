---
title: Salesflare CRM
area: connections
summary: Comptes, contacts et deals, pour savoir qui compte. Il lit avec votre clé API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## Ce qu’il lit

Vos comptes, contacts et deals dans Salesflare, et les fils des comptes : les e-mails de collègues qui ne vous concernent pas, et les réunions avec leurs notes.

## Ce qu’il peut changer

Rien, sauf si vous définissez `join_pipelines` dans le fichier de paramètres de votre Machine. Il vous ajoute alors de lui-même aux comptes de ces pipelines. C’est vide par défaut.

## Le connecter

1. Dans Salesflare, ouvrez [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) et créez une clé.
2. Sur une Machine hébergée : ouvrez votre page de configuration sur app.themachine.computer/setup, allez dans **Plus de sources**, ouvrez Salesflare CRM, collez la clé et appuyez sur **Se connecter**.
3. Sur votre propre ordinateur : lancez `assistant connect crm`, ou **Connexions**, **+ Ajouter**, Salesflare CRM. Après **Se connecter**, votre Machine redémarre et ouvre la carte Salesflare, qui indique d’abord qu’elle cherche les comptes avec des e-mails et des réunions récents, puis combien elle en a lu.

## Détails de la synchro

Sa carte sous **Connexions**, **Autres sources** montre où il en est : combien de comptes il a lus dans ce tour, et combien il en a sautés parce que Salesflare répondait trop lentement. Un tour qui dure des heures indique qu’il est peut-être bloqué.

- **Arrêter** : plus rien de nouveau n’arrive jusqu’à ce que vous appuyiez sur **Démarrer**. Il reprend là où il en était.
- **Relancer la synchro** : abandonne le tour en cours, avec ses erreurs, et relit tout de suite la dernière semaine. Rien de ce qu’il a récupéré n’est perdu.
- **Clés API** : ouvre la page des clés API de Salesflare, pour créer une nouvelle clé.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Salesflare, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de lui sur votre page de configuration.

## Le révoquer dans Salesflare

Supprimez la clé API dans Salesflare, sous Settings, API keys.
