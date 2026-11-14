---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: eee77413a4bdbf0b
---
Dans **Paramètres** > **Modèle**, vous pouvez voir quel modèle d’IA effectue le **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

## Modèle et réflexion pour les chats

Dans **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats de tâches et l’aide. Vous ne voyez que les modèles et les niveaux proposés par votre mode de connexion.

Un niveau de réflexion plus élevé permet de mieux répondre aux questions difficiles, mais prend plus de temps et consomme davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine utilise **Réflexion faible** par défaut : vous obtenez de bons résultats en consommant beaucoup moins de votre forfait. Tout changement s’applique à partir du message suivant.

Pour changer le modèle ou le niveau de réflexion d’un seul chat, appuyez sur le modèle ou le niveau de réflexion sous sa zone de message. Sélectionnez de nouveau **Paramètres** pour appliquer les réglages de Paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance conservent leur propre modèle.

## Limites

Si votre forfait impose des limites d’utilisation, comme les limites de 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, vous pouvez voir la part utilisée et l’heure de réinitialisation de chaque limite. Consulter ces informations ne consomme pas votre forfait.

## Garder de la marge pour vos propres chats

Le Travail en arrière-plan garde de la marge pour vos propres chats. Il se met en pause lorsque la limite de 5 heures est atteinte à environ 65 %. Les vérifications des nouveaux messages continuent jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches utilisent environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, ne se met jamais en pause.

Le Travail en arrière-plan ne fonctionne jamais avec GPT-6 Astra. Il utilise plutôt GPT-6.1 Sol.

## Lorsqu’une limite est atteinte

En haut du tableau de bord, vous pouvez voir quelle limite a été atteinte et quand elle sera réinitialisée. Le travail est mis en attente, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT permet des réinitialisations, **Utiliser une réinitialisation** réinitialise les limites. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine dispose d’un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, sans mettre le travail en attente. En haut du tableau de bord, le message « Limite ChatGPT atteinte, utilisation du modèle de secours. » s’affiche. Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Changer le modèle principal

Le modèle principal est utilisé par le reste de The Machine. Pour une Machine hébergée, vous pouvez le changer sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
