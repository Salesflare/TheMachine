---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait déjà utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 249d2d7d6c368cfe
---
**Paramètres**, **Modèle** indique quel modèle d’IA effectue votre **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

Sur une Machine hébergée avec une connexion ChatGPT, le modèle principal est GPT-6.2 Sol. Il répond plus vite que GPT-6.1 Sol, au même prix.

Les forfaits personnels ChatGPT ou Claude peuvent utiliser vos chats pour l’entraînement par défaut. **Désactiver l’entraînement avec vos données** ouvre le réglage correspondant chez le fournisseur, et **Fait** masque cette ligne.

## Modèle et réflexion pour les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats liés aux tâches et pour l’Aide. Vous ne voyez que les modèles et les niveaux proposés par votre méthode de connexion.

Un niveau de réflexion plus élevé donne de meilleures réponses aux questions difficiles, mais prend plus de temps et consomme davantage votre forfait. **Réflexion ultra** fait appel à des renforts pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine démarre avec **Réflexion faible**, qui donne de bons résultats tout en consommant beaucoup moins votre forfait. Toute modification s’applique à partir du message suivant.

Pour modifier ce réglage dans un seul chat, touchez le modèle ou le niveau de réflexion sous sa zone de saisie. Sélectionnez de nouveau **Paramètres** pour appliquer les réglages définis dans Paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance gardent leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites sur 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, vous voyez la quantité utilisée et l’heure de réinitialisation de chaque limite. La consultation ne consomme rien de votre forfait.

## De la place pour vos propres chats

Le travail en arrière-plan laisse de la place pour vos propres chats. Il se met en pause quand la limite sur 5 heures atteint environ 65 %. La vérification des nouveaux messages continue jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches consomment environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme avec une clé API, n’entraîne jamais de pause.

Le travail en arrière-plan n’utilise jamais GPT-6 Astra. Il utilise plutôt GPT-6.2 Sol, ou GPT-6.1 Sol si la version 6.2 n’est pas configurée.

## Quand une limite est atteinte

En haut du tableau de bord, vous voyez quelle limite a été atteinte et quand elle sera réinitialisée. Le travail attend, puis reprend là où il en était. Rien n’est perdu. Si votre forfait ChatGPT permet des réinitialisations, **Utiliser une réinitialisation** réinitialise les limites. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine a un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, et le travail n’attend pas. En haut du tableau de bord, le message « Limite ChatGPT atteinte, utilisation du modèle de secours. » s’affiche. Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Modifier le modèle principal

Le modèle principal est utilisé par le reste de The Machine. Sur une Machine hébergée, modifiez-le sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
