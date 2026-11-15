---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 744a27a77ab747ac
---
Dans **Paramètres**, **Modèle** indique quel modèle d’IA The Machine utilise pour le **Travail en arrière-plan** et avec quel compte vous êtes connecté, par exemple ChatGPT.

Un forfait personnel ChatGPT ou Claude peut utiliser vos chats pour entraîner ses modèles par défaut. **Désactiver l’entraînement avec vos données** ouvre ce réglage chez le fournisseur, et **Fait** masque cette ligne.

## Modèle et réflexion pour les chats

Dans **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats liés aux tâches et pour l’Aide. Vous ne voyez que les modèles et les niveaux proposés par le compte avec lequel vous êtes connecté.

Un niveau de réflexion plus élevé permet de mieux répondre aux questions difficiles, mais ralentit les réponses et consomme davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine commence avec **Réflexion faible** : de bons résultats pour une part bien moindre de votre forfait. Le changement s’applique à partir du prochain message.

Pour le modifier dans un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Sélectionnez à nouveau **Paramètres** pour suivre les réglages de Paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance utilisent chacun leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites sur 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, vous voyez quelle part a été utilisée et quand chaque limite est réinitialisée. Consulter ces informations ne consomme rien de votre forfait.

## De la marge pour vos propres chats

Le travail en arrière-plan vous laisse de la marge pour vos propres chats. Il se met en pause lorsque vous atteignez environ 65 % de la limite sur 5 heures. La vérification des nouveaux messages continue jusqu’à environ 90 % de la limite hebdomadaire ; les autres tâches utilisent environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme avec une clé API, ne se met jamais en pause.

Le travail en arrière-plan ne fonctionne jamais avec GPT-6 Astra. Il utilise plutôt GPT-6.1 Sol.

## Quand une limite est atteinte

En haut du tableau de bord, vous voyez quelle limite a été atteinte et quand elle sera réinitialisée. Le travail se met en attente, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT permet des réinitialisations, **Utiliser une réinitialisation** relance les limites à zéro. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine dispose d’un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, sans mettre le travail en attente. En haut du tableau de bord, le message indique : « Limite ChatGPT atteinte, utilisation de votre modèle de secours. » Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Modifier le modèle principal

Le modèle principal est celui qu’utilise le reste de The Machine. Sur une Machine hébergée, modifiez-le sur votre page de configuration, dans la section Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
