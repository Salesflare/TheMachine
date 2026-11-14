---
title: Mistral
area: connections
summary: Faites tourner votre Machine sur les modèles de Mistral, avec une clé API de Mistral. Le Chat Pro inclut des crédits API.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
translated: 5d782f28fb69efef
---
## À quoi ça sert

Mistral est un fournisseur d’IA européen. Avec une clé API de Mistral, votre Machine lit et rédige avec les modèles de Mistral. The Machine n’a pas d’IA à elle : les requêtes vont directement à Mistral, sous votre compte et selon ses conditions.

## Obtenir une clé

Mistral n’a pas de connexion pour les autres apps, donc cela passe par une clé API. Dans la [console Mistral](https://console.mistral.ai/), ouvrez API keys et créez-en une. Le Chat Pro inclut des crédits API chaque mois ; ensuite, Mistral facture à l’usage.

## Connecter

Sur une Machine hébergée, ouvrez votre page de configuration, allez à Votre IA et ouvrez **Autres services d’IA**. Choisissez Mistral comme fournisseur, collez la clé et appuyez sur **Enregistrer la clé**. Votre Machine essaie d’abord la clé avec une toute petite requête. Une clé erronée s’affiche tout de suite, et rien n’est enregistré.

Mistral Large devient le modèle principal. Mistral Small est là aussi, un choix moins cher pour les chats ou comme modèle de secours.

Sur votre propre ordinateur, voyez le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Utilisation

**Paramètres**, **Modèle** indique "Utilise votre clé API Mistral". Une clé API n’a pas de limites d’utilisation, donc le travail en arrière-plan ne fait jamais de pause pour elle. Voir [Modèle](model.md).

## Le retirer

Sur votre page de configuration, sous Votre IA, appuyez sur **Retirer** à côté de Mistral dans **Clés**. La clé est supprimée de votre Machine, et si Mistral était votre modèle principal, un autre modèle connecté prend le relais. Pour annuler la clé elle-même, supprimez-la dans la console Mistral.
