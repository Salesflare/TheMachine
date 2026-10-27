---
title: Modèle
area: settings
summary: Quel modèle d’IA répond pour vous, à quel point il réfléchit, et quelle part des limites de votre forfait il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
Dans **Paramètres**, **Modèle** montre le modèle utilisé pour le travail en arrière-plan (marqué **Travail en arrière-plan**) et votre mode de connexion, par exemple avec ChatGPT.

## Modèle et réflexion pour les chats

Sous **Chats**, choisissez le modèle et le niveau de réflexion qu’utilisent vos chats de tâche et l’Aide. La liste n’a que les modèles proposés par votre connexion, comme ceux de ChatGPT si vous vous êtes connecté avec ChatGPT, et chaque modèle seulement les niveaux qu’il a.

Plus de réflexion répond mieux aux questions difficiles, mais c’est plus lent et cela utilise davantage votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles : c’est le plus lent, et c’est ce qui utilise le plus. Un changement s’applique dès le message suivant.

Un chat peut utiliser autre chose : sous sa zone de message, appuyez sur le modèle ou le niveau de réflexion. Ce choix vaut pour ce chat seulement. Choisissez à nouveau la même chose que dans Paramètres pour suivre les Paramètres.

Les revues, votre profil et les brouillons préparés à l’avance gardent leur propre modèle.

## Limites

Si votre forfait a des limites d’utilisation, il montre la part utilisée de chacune et quand elle se réinitialise, par exemple la limite de 5 heures et la limite hebdomadaire d’un forfait ChatGPT ou Claude. Consulter ces chiffres n’utilise jamais votre forfait.

## De la place pour vos propres chats

Le travail en arrière-plan (vérifications, votre profil, brouillons préparés à l’avance) laisse de la place pour vos propres chats. Il se met en pause vers 65 % de la limite de 5 heures, et répartit la limite hebdomadaire à environ un septième par jour. Une connexion sans limite d’utilisation, comme une clé API, n’est jamais mise en pause.

Le travail en arrière-plan ne tourne jamais sur GPT-6 Astra. Il utilise GPT-6.1 Sol à la place.

## Quand une limite est atteinte

Le haut du tableau de bord indique quelle limite est atteinte et quand elle se réinitialise. Le travail attend, puis reprend là où il s’était arrêté. Rien n’est perdu. Certains forfaits ChatGPT incluent des réinitialisations : **Utiliser une réinitialisation** remet les limites à zéro, après confirmation. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Changer le modèle principal

Le modèle principal est celui qu’utilise le reste de The Machine. Sur une Machine hébergée, choisissez-en un autre sur votre page de configuration, sous Votre modèle. Sur votre propre ordinateur, changez-le dans OpenClaw. Voir [ChatGPT](chatgpt.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
