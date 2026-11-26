---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: f34db396a7290252
---
**Paramètres**, **Modèle** indique quel modèle d’IA effectue votre **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

Sur une Machine hébergée avec une connexion à ChatGPT, le modèle principal est GPT-6.2 Sol : il répond plus vite que GPT-6.1 Sol, au même prix.

Par défaut, un forfait personnel ChatGPT ou Claude peut utiliser vos chats pour entraîner ses modèles. **Désactiver l’entraînement avec vos données** ouvre ce paramètre chez le fournisseur, et **Fait** masque la ligne.

## Modèle et réflexion pour les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats de tâches et l’aide. Vous ne voyez que les modèles et les niveaux proposés par votre connexion.

Un niveau de réflexion plus élevé améliore les réponses aux questions difficiles, mais les rend plus lentes et utilise davantage votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et utilise le plus de votre forfait. Une nouvelle Machine démarre en **Réflexion faible** : les résultats sont bons et votre forfait est beaucoup moins sollicité. Toute modification s’applique à partir du message suivant.

Pour le modifier dans un seul chat, touchez le modèle ou le niveau de réflexion sous sa zone de saisie. Choisissez à nouveau l’option Paramètres pour suivre les paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance gardent leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites de 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, la page indique la part utilisée et la date de chaque réinitialisation. Consulter ces informations ne sollicite pas votre forfait.

## De la marge pour vos propres chats

Le travail en arrière-plan laisse de la marge pour vos propres chats. Il se met en pause lorsque la limite de 5 heures atteint environ 65 %. La vérification des nouveaux messages se poursuit jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches utilisent environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, ne se met jamais en pause.

Le travail en arrière-plan n’utilise jamais GPT-6 Astra. Avec une connexion à ChatGPT et une version d’OpenClaw antérieure à 2026.11.10, il utilise GPT-6.1 Sol, même si votre modèle principal est GPT-6.2 Sol : dans ce cas, la version 6.2 ne réutilise pas ses instructions mises en cache et consomme davantage de votre forfait. À partir d’OpenClaw 2026.11.10, le travail en arrière-plan utilise à nouveau votre modèle principal. Vos chats conservent le modèle que vous avez choisi.

Avant une vérification, un petit modèle (GPT-6 Luna avec ChatGPT, Haiku avec Claude) met de côté les newsletters, les promotions et les notifications d’applications qui ne nécessitent clairement aucune action. Les vérifications utilisent ainsi moins de votre forfait. Ces éléments restent consultables. Les messages écrits par une personne, les factures, les alertes de sécurité et les codes de connexion sont toujours vérifiés.

## Avant d’atteindre une limite

Si votre forfait ChatGPT dispose de réinitialisations, Tâches affiche une courte ligne lorsque le travail en arrière-plan ralentit : vers 65 % de la limite de 5 heures ou 90 % de la limite hebdomadaire. Elle indique la part utilisée et le nombre de réinitialisations restantes. **Utiliser une réinitialisation** relance les limites après confirmation. × masque la ligne jusqu’à la réinitialisation de cette limite. Si vous n’avez pas de réinitialisations, rien de nouveau ne s’affiche.

Sur une Machine hébergée, votre Machine voit les réinitialisations et les utilise dès que Codex sur votre Machine est connecté au même compte ChatGPT. D’ici là, Tâches et Paramètres affichent **Activer les réinitialisations**. Cette option ouvre l’étape Codex de votre page de configuration, où vous vous connectez avec un code, comme pour votre connexion à ChatGPT.

## Quand une limite est atteinte

En haut du tableau de bord, vous voyez la limite atteinte et sa date de réinitialisation. Les tâches attendent, puis reprennent là où elles en étaient. Rien n’est perdu. Si votre forfait ChatGPT dispose de réinitialisations, **Utiliser une réinitialisation** relance les limites. Sur une Machine hébergée sans connexion à Codex, **Activer les réinitialisations** ouvre plutôt votre page de configuration. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine dispose d’un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, sans mettre de tâches en attente. En haut du tableau de bord, le message indique « Limite ChatGPT atteinte, utilisation de votre modèle de secours. » Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Changer le modèle principal

Le modèle principal est celui qu’utilise le reste de The Machine. Sur une Machine hébergée, vous pouvez le modifier sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
