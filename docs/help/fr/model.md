---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
**Paramètres**, **Modèle** indique quel modèle d’IA effectue votre **Travail en arrière-plan** et comment vous êtes connecté, par exemple avec ChatGPT.

Sur une Machine hébergée avec une connexion ChatGPT, le modèle principal est GPT-6.2 Sol : il répond plus vite que GPT-6.1 Sol, au même prix.

Un forfait personnel ChatGPT ou Claude peut entraîner ses modèles sur vos chats par défaut. **Désactiver l’entraînement avec vos données** ouvre ce paramètre chez le fournisseur, et **Fait** masque la ligne.

## Modèle et réflexion pour les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats consacrés aux tâches et pour l’Aide. Vous ne voyez que les modèles et les niveaux proposés par votre mode de connexion.

Un niveau de réflexion plus élevé permet de mieux répondre aux questions difficiles, mais les réponses sont plus lentes et consomment davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus. Une nouvelle Machine démarre avec **Réflexion faible** : de bons résultats pour une consommation bien moindre de votre forfait. Toute modification s’applique à partir du message suivant.

Pour le modifier dans un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Choisissez de nouveau l’option Paramètres pour suivre les paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance utilisent leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites de 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, la page indique la part utilisée et l’heure de réinitialisation de chaque limite. Consulter cette page ne consomme rien de votre forfait.

## Garder de la marge pour vos chats

Le travail en arrière-plan laisse de la marge pour vos propres chats. Il se met en pause lorsque la limite de 5 heures est atteinte à environ 65 %. Les vérifications des nouveaux messages continuent jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches utilisent environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, n’entraîne jamais de pause.

Le travail en arrière-plan n’utilise jamais GPT-6 Astra. Pour le moment, avec une connexion ChatGPT, il utilise GPT-6.1 Sol, même si votre modèle principal est GPT-6.2 Sol : avec cette connexion, GPT-6.2 ne réutilise pas encore ses instructions mises en cache, et consomme donc davantage de votre forfait. Vos chats conservent le modèle que vous avez choisi.

Avant une vérification, un petit modèle (GPT-6 Luna avec ChatGPT, Haiku avec Claude) met de côté les newsletters, promotions et notifications d’applications qui ne nécessitent clairement aucune action, pour que les vérifications consomment moins de votre forfait. Ces messages restent consultables. Les messages écrits par une personne, les factures, les alertes de sécurité et les codes de connexion sont toujours vérifiés.

## Avant d’atteindre une limite

S’il reste des réinitialisations sur votre forfait ChatGPT, Tâches affiche un court message lorsque le travail en arrière-plan ralentit : vers 65 % de la limite de 5 heures ou 90 % de la limite hebdomadaire. Il indique la part utilisée et le nombre de réinitialisations restantes. **Utiliser une réinitialisation** réinitialise les limites après votre confirmation. × masque le message jusqu’à la réinitialisation de la limite concernée. Si aucune réinitialisation ne reste, aucun nouveau message ne s’affiche.

Sur une Machine hébergée, votre Machine détecte et utilise les réinitialisations dès que Codex sur votre Machine est connecté au même compte ChatGPT. D’ici là, Tâches et Paramètres affichent **Activer les réinitialisations**. Ce bouton ouvre l’étape Codex de votre page de configuration, où vous vous connectez avec un code, comme pour votre connexion ChatGPT.

## Quand une limite est atteinte

En haut du tableau de bord, vous voyez quelle limite a été atteinte et quand elle sera réinitialisée. Le travail attend, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT comprend des réinitialisations, **Utiliser une réinitialisation** réinitialise les limites. Sur une Machine hébergée sans connexion à Codex, **Activer les réinitialisations** ouvre plutôt votre page de configuration. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page ChatGPT correspondante.

## Avec un modèle de secours

Si votre Machine dispose d’un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte, et le travail ne se met pas en attente. En haut du tableau de bord, le message indique « Limite ChatGPT atteinte, utilisation du modèle de secours ». Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Modifier le modèle principal

Le modèle principal est utilisé par le reste de The Machine. Sur une Machine hébergée, modifiez-le sur votre page de configuration, dans la section Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
