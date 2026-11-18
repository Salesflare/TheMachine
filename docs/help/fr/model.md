---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: c7a96914e4deb3d4
---
Dans **Paramètres**, **Modèle** indique quel modèle d’IA effectue votre **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

Un forfait personnel ChatGPT ou Claude peut utiliser vos chats pour entraîner ses modèles par défaut. **Désactiver l’entraînement avec vos données** ouvre ce paramètre chez le fournisseur, et **Fait** masque cette ligne.

## Modèle et réflexion pour les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats de tâches et l’aide. Vous ne voyez que les modèles et les niveaux proposés par votre mode de connexion.

Un niveau de réflexion plus élevé améliore les réponses aux questions difficiles, mais les rend plus lentes et consomme davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine démarre avec **Réflexion faible** : de bons résultats pour une consommation bien moindre de votre forfait. Tout changement s’applique à partir du message suivant.

Pour le modifier dans un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Sélectionnez à nouveau **Paramètres** pour suivre les réglages de Paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance gardent leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites de 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, cette page indique la part utilisée et la date de chaque réinitialisation. La consultation ne consomme jamais votre forfait.

## De la marge pour vos propres chats

Le travail en arrière-plan laisse de la marge pour vos propres chats. Il se met en pause à environ 65 % de la limite de 5 heures. La vérification des nouveaux messages continue jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches utilisent environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, ne met jamais le travail en pause.

Le travail en arrière-plan n’utilise jamais GPT-6 Astra. Il utilise GPT-6.2 Sol à la place, ou GPT-6.1 Sol si GPT-6.2 n’est pas configuré.

## Quand une limite est atteinte

En haut du tableau de bord, un message indique quelle limite a été atteinte et quand elle est réinitialisée. Le travail attend, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT permet des réinitialisations, **Utiliser une réinitialisation** relance les limites. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine a un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, sans interrompre le travail. En haut du tableau de bord, le message indique « Limite ChatGPT atteinte, utilisation du modèle de secours. » Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Modifier le modèle principal

Le modèle principal est celui qu’utilise le reste de The Machine. Sur une Machine hébergée, modifiez-le sur votre page de configuration, sous **Votre IA**. Sur votre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
