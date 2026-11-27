---
title: Modèle
area: settings
summary: Quel modèle d’IA vous répond, son niveau de réflexion et la part des limites de votre forfait qu’il a utilisée.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: b76f4f927bfd7be1
---
**Paramètres**, **Modèle** indique quel modèle d’IA s’occupe de votre **Travail en arrière-plan** et comment vous êtes connecté, par exemple à ChatGPT.

Sur une Machine hébergée avec une connexion à ChatGPT, le modèle principal est GPT-6.2 Sol : ses réponses sont plus rapides que celles de GPT-6.1 Sol, au même prix.

Sur une Machine hébergée, une connexion à Claude reste valide environ un an. Avec `claude auth login`, elle expire environ quatre semaines après votre connexion. Trois jours avant, **Vous attend** vous en informe et vous recevez un e-mail. Une fois la connexion expirée, vous recevez une notification et, si ce n’est pas déjà fait, cet e-mail. **Se reconnecter** règle le problème en une étape.

Un forfait ChatGPT ou Claude personnel peut utiliser vos chats pour entraîner ses modèles par défaut : **Désactiver l’entraînement avec vos données** ouvre ce paramètre chez le fournisseur, et **Fait** masque la ligne.

## Modèle et réflexion dans les chats

Dans **Chats**, choisissez le modèle et le niveau de réflexion pour vos chats de tâches et l’Aide. Vous ne voyez que les modèles et les niveaux proposés par votre mode de connexion.

Un niveau de réflexion plus élevé donne de meilleures réponses aux questions difficiles, mais il est plus lent et utilise davantage votre forfait. **Réflexion ultra** fait appel à des assistants pour les questions les plus difficiles et utilise le plus de ressources. Une nouvelle Machine commence avec **Réflexion faible** : les résultats sont bons et votre forfait est beaucoup moins sollicité. Tout changement s’applique à partir du message suivant.

Pour le modifier dans un seul chat, touchez le modèle ou le niveau de réflexion sous la zone de saisie. Choisissez de nouveau l’option Paramètres pour suivre les paramètres.

Les vérifications, votre profil et les brouillons préparés à l’avance utilisent leur propre modèle.

## Limites

Si votre forfait comporte des limites d’utilisation, comme les limites de 5 heures et hebdomadaires d’un forfait ChatGPT ou Claude, cette page indique la part utilisée et la date de réinitialisation de chaque limite. La consultation n’utilise jamais votre forfait.

## De la marge pour vos propres chats

Le travail en arrière-plan laisse de la marge pour vos propres chats. Il s’interrompt lorsque la limite de 5 heures est atteinte à environ 65 %. La vérification des nouveaux messages continue jusqu’à environ 90 % de la limite hebdomadaire. Les autres tâches consomment environ un septième de la limite hebdomadaire par jour. Une connexion sans limites, comme une clé API, ne s’interrompt jamais.

Le travail en arrière-plan ne fonctionne jamais avec GPT-6 Astra. Avec une connexion à ChatGPT et une version d’OpenClaw antérieure à 2026.11.10, il utilise GPT-6.1 Sol, même si votre modèle principal est GPT-6.2 Sol : dans ce cas, la version 6.2 ne réutilise pas ses instructions mises en cache et sollicite davantage votre forfait. À partir d’OpenClaw 2026.11.10, le travail en arrière-plan utilise de nouveau votre modèle principal. Vos chats conservent le modèle que vous avez choisi.

Avant une vérification, un petit modèle (GPT-6 Luna avec ChatGPT, Haiku avec Claude) écarte les newsletters, les promotions et les notifications d’applications qui ne nécessitent clairement aucune action. Les vérifications sollicitent ainsi moins votre forfait. Ces messages restent accessibles dans les résultats de recherche. Les messages écrits par une personne, les factures, les alertes de sécurité et les codes de connexion sont toujours vérifiés.

## Avant d’atteindre une limite

Si votre forfait ChatGPT dispose de réinitialisations restantes, Tâches affiche un court message lorsque le travail en arrière-plan ralentit : quand la limite de 5 heures est atteinte à environ 65 %, ou la limite hebdomadaire à environ 90 %. Le message indique la part utilisée et le nombre de réinitialisations restantes. **Utiliser une réinitialisation** réinitialise les limites après confirmation. × masque le message jusqu’à la réinitialisation de cette limite. Si aucune réinitialisation ne vous reste, aucun nouveau message ne s’affiche.

Sur une Machine hébergée, votre Machine voit et utilise les réinitialisations dès que Codex sur votre Machine est connecté au même compte ChatGPT. En attendant, Tâches et Paramètres affichent **Activer les réinitialisations**. Cette option ouvre l’étape Codex de votre page de configuration, où vous vous connectez avec un code, comme pour votre connexion à ChatGPT.

## Quand une limite est atteinte

En haut du tableau de bord, un message indique la limite atteinte et sa date de réinitialisation. Le travail est mis en attente, puis reprend là où il s’était arrêté. Rien n’est perdu. Si votre forfait ChatGPT dispose de réinitialisations, **Utiliser une réinitialisation** réinitialise les limites. Sur une Machine hébergée sans connexion à Codex, **Activer les réinitialisations** ouvre plutôt votre page de configuration. Sinon, **Voir les réinitialisations dans ChatGPT** ouvre la page de ChatGPT.

## Avec un modèle de secours

Si votre Machine a un modèle de secours associé à un autre forfait ou fournisseur, il prend le relais lorsqu’une limite est atteinte et rien n’est mis en attente. En haut du tableau de bord, un message indique « Limite ChatGPT atteinte, utilisation du modèle de secours ». Si le modèle de secours cesse de fonctionner, les interruptions reprennent.

## Changer le modèle principal

Le modèle principal est celui qu’utilise le reste de The Machine. Sur une Machine hébergée, changez-le sur votre page de configuration, sous Votre IA. Sur votre propre ordinateur, consultez [ChatGPT](chatgpt.md), [Mistral](mistral.md) et le [guide des modèles](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
