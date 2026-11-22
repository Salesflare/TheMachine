---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait déjà utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: a6db52984a6fddeb
---
Dans **Paramètres**, **Modèle** indique quel modèle d’IA effectue le **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

Sur une Machine hébergée avec une connexion ChatGPT, le modèle principal est GPT-6.2 Sol : il répond plus vite que GPT-6.1 Sol, au même prix.

Avec un forfait personnel ChatGPT ou Claude, vos chats peuvent être utilisés par défaut pour entraîner les modèles. **Désactiver l’entraînement avec vos données** ouvre le réglage correspondant chez le fournisseur, et **Fait** masque la ligne.

## Modèle et réflexion dans les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats liés aux tâches et à l’aide. Vous ne voyez que les modèles et les niveaux proposés par votre connexion.

Un niveau de réflexion plus élevé donne de meilleures réponses aux questions difficiles, mais ralentit les réponses et consomme davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine utilise **Réflexion faible** par défaut : les résultats sont bons et votre forfait est beaucoup moins sollicité. Toute modification prend effet à partir du message suivant.

Pour modifier ces réglages dans un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Sélectionnez de nouveau **Paramètres** pour suivre les réglages définis dans Paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance gardent leur propre modèle.

## Limites

Si votre forfait a des limites d’utilisation, comme les limites sur 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, la part utilisée et la date de chaque réinitialisation s’affichent. La consultation ne consomme rien de votre forfait.

## De la place pour vos chats

Le travail en arrière-plan laisse de la place pour vos propres chats. Il s’interrompt lorsque la limite sur 5 heures atteint environ 65 %. Les vérifications des nouveaux messages continuent jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches consomment environ un septième de votre limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, ne s’interrompt jamais.

Le travail en arrière-plan n’utilise jamais GPT-6 Astra. Pour l’instant, avec une connexion ChatGPT, il utilise GPT-6.1 Sol, même si votre modèle principal est GPT-6.2 Sol. Avec cette connexion, GPT-6.2 ne réutilise pas encore ses instructions mises en cache et consomme donc davantage de votre forfait. Vos chats conservent le modèle que vous avez choisi.

## Lorsqu’une limite est atteinte

En haut du tableau de bord, vous voyez quelle limite a été atteinte et quand elle sera réinitialisée. Le travail attend, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT propose des réinitialisations, **Utiliser une réinitialisation** relance les limites. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine a un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte et aucun travail n’attend. En haut du tableau de bord, le message « Limite ChatGPT atteinte, utilisation du modèle de secours. » s’affiche. Si le modèle de secours cesse de fonctionner, les interruptions reprennent.

## Modifier le modèle principal

Le modèle principal est celui qu’utilise le reste de The Machine. Sur une Machine hébergée, modifiez-le sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez les guides [ChatGPT](chatgpt.md), [Mistral](mistral.md) et [des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
