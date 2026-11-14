---
title: ChatGPT
area: connections
summary: Connectez-vous avec ChatGPT pour utiliser votre Machine avec votre forfait ChatGPT et importer vos compétences ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## À quoi ça sert

Connectez-vous avec ChatGPT : votre Machine lit et rédige avec lui, avec votre propre forfait ChatGPT. The Machine n’a pas d’IA propre : les requêtes sont envoyées directement à OpenAI, sous votre compte et selon leurs conditions.

## Se connecter

Sur une Machine hébergée, appuyez sur **Se connecter avec ChatGPT** sur votre page de configuration, puis saisissez le code affiché sur ChatGPT. Vous vous êtes déconnecté depuis ? Appuyez sur **Reconnecter ChatGPT**.

OpenAI refuse le code ? Ouvrez vos [paramètres de sécurité ChatGPT](https://chatgpt.com/settings/security), faites défiler jusqu’en bas et activez l’option **Activer la connexion par code d’appareil pour Codex, Excel, PowerPoint et Word**. Saisissez ensuite le code à nouveau.

Vous ne voyez pas cette option ? Si vous utilisez un compte professionnel (Business, Enterprise ou Edu), l’administrateur ChatGPT doit l’activer dans [Autorisations et rôles](https://chatgpt.com/admin/permissions), sous **Codex et travail local**.

Sur votre propre ordinateur, exécutez `openclaw models auth login` dans un terminal.

## Limites d’utilisation

Un forfait ChatGPT comporte une limite sur 5 heures et une limite hebdomadaire. **Paramètres**, **Modèle** indique la part utilisée pour chacune et la date de leur réinitialisation. Les tâches en arrière-plan s’interrompent bien avant d’atteindre une limite, pour vous laisser de la marge pour vos propres chats. Lorsqu’une limite est atteinte, le haut du tableau de bord indique quand elle est réinitialisée. Voir [Modèle](model.md).

## Importer vos compétences ChatGPT

Dans **Paramètres**, **Compétences**, appuyez sur **Importer**, choisissez **Depuis ChatGPT**, puis appuyez sur **Trouver mes compétences**. Seules leurs instructions sont importées. Voir [Compétences](skills.md).

## Le retirer

Choisissez un autre modèle sur votre page de configuration (ou, sur votre propre ordinateur, connectez-vous de la même manière à un autre fournisseur). Pour révoquer son accès auprès d’OpenAI, déconnectez-vous de la session dans vos paramètres de sécurité ChatGPT.
