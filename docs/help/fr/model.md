---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 9a0777c555ab5637
---
**Paramètres**, **Modèle** indique quel modèle d’IA effectue votre **Travail en arrière-plan** et avec quel compte vous êtes connecté, par exemple ChatGPT.

Sur une Machine hébergée avec un compte ChatGPT connecté, le modèle principal est GPT-6.2 Sol : il répond plus vite que GPT-6.1 Sol, au même prix.

Une connexion à Claude expire environ quatre semaines après que vous vous êtes connecté. **Vous attend** vous en avertit trois jours avant. Une fois la connexion expirée, vous recevez une notification. **Se reconnecter** règle le problème en une étape.

Par défaut, un forfait personnel ChatGPT ou Claude peut utiliser vos chats pour entraîner ses modèles. **Désactiver l’entraînement avec vos données** ouvre le paramètre correspondant chez le fournisseur, et **Fait** masque la ligne.

## Modèle et réflexion pour les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats liés aux tâches et à l’aide. Seuls les modèles et les niveaux proposés par votre compte s’affichent.

Un niveau de réflexion plus élevé améliore les réponses aux questions difficiles, mais ralentit les réponses et consomme davantage de votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et consomme le plus de votre forfait. Une nouvelle Machine utilise **Réflexion faible** par défaut : les résultats sont bons et votre forfait est beaucoup moins sollicité. Toute modification s’applique à partir du message suivant.

Pour modifier ces options pour un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Sélectionnez de nouveau l’option Paramètres pour suivre les choix définis dans Paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance utilisent leur propre modèle.

## Limites

Si votre forfait impose des limites d’utilisation, comme les limites sur 5 h et hebdomadaires d’un forfait ChatGPT ou Claude, cette page indique la part utilisée et la date de chaque réinitialisation. La consultation de ces informations n’utilise pas votre forfait.

## De la marge pour vos propres chats

Le travail en arrière-plan laisse de la marge pour vos propres chats. Il se met en pause lorsque vous atteignez environ 65 % de la limite sur 5 h. Les vérifications des nouveaux messages continuent jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches utilisent environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, ne se met jamais en pause.

Le travail en arrière-plan n’utilise jamais GPT-6 Astra. Avec un compte ChatGPT connecté et une version d’OpenClaw antérieure à 2026.11.10, il utilise GPT-6.1 Sol, même si votre modèle principal est GPT-6.2 Sol : GPT-6.2 ne réutilise pas les instructions mises en cache dans ce cas, et consomme donc davantage de votre forfait. À partir d’OpenClaw 2026.11.10, le travail en arrière-plan utilise de nouveau votre modèle principal. Vos chats conservent le modèle que vous avez choisi.

Avant une vérification, un petit modèle (GPT-6 Luna avec ChatGPT, Haiku avec Claude) met de côté les newsletters, les promotions et les notifications d’applications qui ne nécessitent clairement aucune intervention, pour réduire la consommation de votre forfait. Vous pouvez toujours les retrouver avec la recherche. Les messages écrits par une personne, les factures, les alertes de sécurité et les codes de connexion sont toujours vérifiés.

## Avant d’atteindre une limite

Si votre forfait ChatGPT comprend des réinitialisations restantes, Tâches affiche un court message lorsque le travail en arrière-plan ralentit : à environ 65 % de la limite sur 5 h ou 90 % de la limite hebdomadaire. Il indique la part utilisée et le nombre de réinitialisations restantes. **Utiliser une réinitialisation** réinitialise les limites après confirmation. × masque le message jusqu’à la prochaine réinitialisation de cette limite. Si vous n’avez plus de réinitialisations, aucun nouveau message ne s’affiche.

Sur une Machine hébergée, votre Machine détecte et utilise les réinitialisations dès que Codex sur votre Machine est connecté au même compte ChatGPT. En attendant, Tâches et Paramètres affichent **Activer les réinitialisations**. Ce bouton ouvre l’étape Codex de votre page de configuration. Vous vous connectez avec un code, comme pour votre compte ChatGPT.

## Quand une limite est atteinte

Le haut du tableau de bord indique la limite atteinte et la date de sa réinitialisation. Le travail est mis en attente, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT comprend des réinitialisations, **Utiliser une réinitialisation** réinitialise les limites. Sur une Machine hébergée où Codex n’est pas connecté, **Activer les réinitialisations** ouvre plutôt votre page de configuration. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine dispose d’un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte et le travail n’est pas mis en attente. Le haut du tableau de bord affiche « Limite ChatGPT atteinte, utilisation du modèle de secours. » Si le modèle de secours cesse de fonctionner, les pauses reprennent.

## Modifier le modèle principal

Le modèle principal est utilisé par le reste de The Machine. Sur une Machine hébergée, modifiez-le sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
