---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait déjà consommée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: d63ec55d8d0339e6
---
**Paramètres**, **Modèle** indique quel modèle d’IA effectue votre **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

Sur une Machine hébergée avec une connexion à ChatGPT, le modèle principal est GPT-6.2 Sol : il répond plus vite que GPT-6.1 Sol, au même prix.

Un forfait personnel ChatGPT ou Claude peut utiliser vos chats pour l’entraînement par défaut. **Désactiver l’entraînement avec vos données** ouvre ce paramètre chez le fournisseur, et **Fait** masque la ligne.

## Modèle et réflexion dans les chats

Dans **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats de tâches et l’aide. Vous ne voyez que les modèles et les niveaux proposés avec votre connexion.

Un niveau de réflexion plus élevé améliore les réponses aux questions difficiles, mais il est plus lent et consomme davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine utilise par défaut **Réflexion faible** : les résultats sont bons et votre forfait est beaucoup moins sollicité. Toute modification s’applique à partir du message suivant.

Pour le modifier dans un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Sélectionnez de nouveau l’option **Paramètres** pour suivre les réglages de **Paramètres**.

Les vérifications, votre profil et les brouillons préparés à l’avance conservent leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites sur 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, vous voyez la quantité utilisée et la date de chaque réinitialisation. Consulter ces informations ne consomme jamais votre forfait.

## De la marge pour vos propres chats

Le **Travail en arrière-plan** laisse de la marge pour vos propres chats. Il ralentit lorsque la limite sur 5 heures atteint environ 65 %. Les vérifications des nouveaux messages continuent jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches utilisent environ un septième de cette limite par jour. Une connexion sans limites, comme une clé API, ne met jamais le travail en pause.

Le **Travail en arrière-plan** ne fonctionne jamais avec GPT-6 Astra. Avec une connexion à ChatGPT, il utilise GPT-6.1 Sol pour le moment, même si votre modèle principal est GPT-6.2 Sol. Avec cette connexion, la version 6.2 ne réutilise pas encore ses instructions mises en cache, et consomme donc davantage de votre forfait. Vos chats conservent le modèle que vous avez choisi.

## Avant d’atteindre une limite

Si votre forfait ChatGPT dispose de réinitialisations restantes, Tâches affiche une courte ligne lorsque le travail en arrière-plan ralentit : vers 65 % de la limite sur 5 heures ou 90 % de la limite hebdomadaire. Elle indique la quantité utilisée et le nombre de réinitialisations restantes. **Utiliser une réinitialisation** relance les limites après confirmation. × masque la ligne jusqu’à la réinitialisation de cette limite. S’il ne vous reste aucune réinitialisation, rien de nouveau ne s’affiche.

## Quand une limite est atteinte

En haut du tableau de bord, vous voyez quelle limite a été atteinte et quand elle sera réinitialisée. Le travail attend, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT dispose de réinitialisations, **Utiliser une réinitialisation** relance les limites. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine dispose d’un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, sans interrompre le travail. En haut du tableau de bord, le message indique : « Limite ChatGPT atteinte, utilisation du modèle de secours. » Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Changer le modèle principal

Le modèle principal est utilisé par le reste de The Machine. Sur une Machine hébergée, changez-le sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
