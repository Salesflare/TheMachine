---
title: ChatGPT
area: connections
summary: Connectez-vous avec ChatGPT pour faire tourner votre Machine sur votre abonnement ChatGPT, et importez vos compétences ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## À quoi ça sert

ChatGPT est le modèle qui lit et rédige pour vous, sur votre propre abonnement ChatGPT. The Machine n’a pas d’IA à elle. Les requêtes de votre Machine vont directement de votre serveur à OpenAI, sous votre compte et selon ses conditions.

## Se connecter

Sur une Machine hébergée, sur votre page de configuration, appuyez sur **Se connecter avec ChatGPT** et saisissez chez ChatGPT le code affiché. Déconnecté plus tard ? Appuyez sur **Reconnecter ChatGPT**.

OpenAI refuse le code ? Ouvrez vos [paramètres de sécurité ChatGPT](https://chatgpt.com/settings/security), descendez tout en bas et activez l’option "Enable device code sign-in for Codex, Excel, PowerPoint, and Word". Puis saisissez à nouveau le code.

Elle n’y est pas ? Sur un compte professionnel (Business, Enterprise ou Edu), un administrateur de l’espace de travail l’active dans [Permissions & roles](https://chatgpt.com/admin/permissions), sous « Codex and Work Local ». Une seule option vaut pour les deux codes : si le code de votre modèle a fonctionné, celui de Codex fonctionne aussi.

Sur votre propre ordinateur, connectez OpenClaw à ChatGPT avec `openclaw models auth login`.

## Limites d’utilisation

Un abonnement ChatGPT a une limite sur 5 heures et une limite hebdomadaire. **Paramètres**, puis **Modèle**, montre la part utilisée de chacune et quand elle se réinitialise. Le travail en arrière-plan s’arrête bien avant une limite, pour garder de la place pour vos propres chats. Quand une limite est atteinte, le haut du tableau de bord indique laquelle et quand elle se réinitialise, puis le travail reprend. Voir [Modèle](model.md).

## Importer vos compétences ChatGPT

Dans **Paramètres**, **Compétences**, appuyez sur **Importer**, choisissez **Depuis ChatGPT** et appuyez sur **Trouver mes compétences**. Elle lit les compétences que vous avez créées, dans le navigateur de votre Machine. Seules les instructions sont importées. Voir [Compétences](skills.md).

## La retirer

Choisissez un autre modèle sur votre page de configuration, ou connectez OpenClaw à un autre fournisseur. Pour couper son accès côté OpenAI, déconnectez la session dans vos paramètres de sécurité ChatGPT.
