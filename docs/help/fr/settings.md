---
title: Paramètres
area: settings
summary: Où trouver chaque paramètre, du mode clair à la sécurité et à votre compte.
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
Ouvrez les **Paramètres** avec la roue dentée en haut. Voici les onglets :

- **Compte** : **Vos adresses** (celles qui sont considérées comme les vôtres) et **Se déconnecter**, en haut. Sur une Machine hébergée, vous trouverez aussi votre forfait, vos factures, Fleet, vos amis, la connexion et les données, avec **Résilier le forfait** et **Supprimer le compte** tout en bas. Sur une Machine installée sur votre ordinateur et associée au Network : votre Fleet, votre nom d’utilisateur, vos amis et la connexion, chacun avec un lien vers la partie correspondante de votre compte (connectez-vous à cet endroit), et **Supprimer le compte** tout en bas. Si elle n’est pas encore associée : **Rejoindre le Network**, en haut. Consultez [Forfaits et facturation](plans-and-billing.md).
- **Général** : la langue et la région, cet appareil, la saisie vocale, le navigateur de votre Machine, votre Fleet, l’exportation et l’importation, ainsi que la version utilisée. S’il n’y a pas d’onglet Compte, **Rejoindre le Network** se trouve à la fin.
- **Sécurité** : Standard ou Prudente. Consultez [Niveaux de sécurité](security-levels.md). Vous trouverez aussi **Accès du support** lorsqu’il est activé : consultez [Contacter le support](get-support.md#support-access).
- **Activité** : tout ce que The Machine a fait pour vous, du plus récent au plus ancien. Consultez [Activité](activity.md).
- **Notifications** : où vous recevez les notifications, et vos heures de travail. Consultez [Notifications](notifications.md) et [Heures de travail](work-hours.md).
- **Rédaction** : vos signatures et votre façon d’écrire. Consultez [Rédaction](writing.md).
- **Compétences** : les guides que suit votre Machine. Consultez [Compétences](skills.md).
- **Applis** : les applis de The Machine pour votre téléphone et votre ordinateur, puis Claude, ChatGPT et les autres IA que vous avez connectées, ainsi que ce que chacune peut faire. Sur un ordinateur, la liste comprend l’appli de bureau pour Windows, Mac et Linux, avec **Télécharger** pour chacune, et indique celle pour **Cet ordinateur**. Consultez [L’application mobile](mobile-app.md), [L’application de bureau](desktop-app.md) et [Connecter d’autres IA](ai-connections.md).
- **Modèle** : l’IA qui lit et rédige pour vous, et ses limites. Consultez [Modèle](model.md). Vous trouverez aussi **Codex et Claude Code** : consultez [Transférer à Claude Code ou Codex](hand-to-agent.md). Et **Recherche par le sens**, plus bas.

Un onglet sans contenu est masqué.

## Général

- **Langue et région** : votre **Région** détermine le format des dates, des heures et des nombres (24 oct. ou 24 octobre). **Format de l’heure** permet de choisir entre le format sur 12 heures (2:05 PM) et celui sur 24 heures (14:05). Les tâches, Telegram, le récap et les messages Fleet suivent ces deux paramètres. Une Machine hébergée utilise le fuseau horaire que vous avez choisi lors de l’inscription.
- **Langue** : English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. La langue de votre navigateur est sélectionnée par défaut. Le tableau de bord, l’aide, les notifications, Telegram, le récap hebdo et les tâches rédigées par votre Machine changent dès que vous choisissez une langue. Les anciens textes restent tels quels. Vos collègues reçoivent les questions Fleet et Fleet Famille dans leur propre langue. Les brouillons destinés à d’autres personnes restent dans la langue de leur conversation.
- **Cet appareil** : **Installer l’app**, **Notifications** avec **Envoyer un test**, et **Mode clair**, pour ce navigateur ou ce téléphone uniquement. Consultez [Installer l’app et activer les notifications](phone-app.md). Sur [Omarchy](omarchy.md), vous trouverez aussi **Thème Omarchy**.
- **Saisie vocale** : comment vos paroles sont converties en texte et quelle voix est utilisée pour Talk en direct. Consultez [Saisie vocale](voice-input.md) et [Parler en direct](talk-live.md).
- **Ouvrir le navigateur de la Machine ↗** : le navigateur que votre Machine utilise pour des sites comme LinkedIn.
- **Règles Fleet** : consultez [Règles de partage](sharing-rules.md).
- **Exporter** :
  - **Tout** : tout ce que votre Machine sait, dans un seul fichier chiffré, à transférer ou à conserver, et **Importer** pour en importer un. Consultez [Passer sur un autre ordinateur](moving.md).
  - **Connaissances pour une autre IA** : ce que votre Machine a appris, dans des fichiers lisibles par n’importe quelle IA. Consultez [Connaissances pour une autre IA](knowledge-export.md).

## Version

La version utilisée par votre Machine. Les mises à jour s’installent automatiquement. Lorsqu’une nouvelle version est prête sur une Machine hébergée, **Mettre à jour** l’installe immédiatement. L’opération prend quelques minutes et vos données sont conservées.

Sur votre propre ordinateur, un minuteur quotidien installe chaque nouvelle version signée sur Linux. Consultez [Lancer The Machine sur votre propre ordinateur](self-hosted-setup.md).

## Recherche par le sens

Dans **Paramètres**, ouvrez **Modèle**. Cette fonction trouve des e-mails, des messages et des notes selon leur sujet, pas seulement selon les mots qu’ils contiennent. Sur une Machine hébergée, une petite IA installée directement sur la Machine s’en charge, sans envoyer quoi que ce soit ailleurs. La fonction est activée à partir de 8 Go de mémoire. Avec 4 Go, activez-la à l’aide de son interrupteur. Elle utilise environ un demi-gigaoctet, ce qui peut ralentir une Machine très sollicitée. Lorsqu’elle est désactivée, la préparation d’une tâche recherche toujours les messages pertinents, à partir des mots utilisés.

Sur votre propre ordinateur, il s’agit du bloc `embeddings` dans `config.json`. Redémarrez la Machine après toute modification.

## Sur cette Machine

Lorsque votre Machine fonctionne sur votre propre ordinateur, certaines opérations sont effectuées sur place, dans un terminal :

- Le fichier de paramètres, `config.json` : tous les paramètres au même endroit. Redémarrez la Machine après toute modification.
- `assistant connect` : ajouter une source, comme `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off` : les messages sur Telegram. Consultez [Telegram](telegram.md).
- `assistant doctor` : vérifie tout et affiche une solution pour chaque problème.

## Vos adresses

Toutes les adresses vous appartenant que la Machine a trouvées : vos comptes, vos alias Gmail ou Outlook, votre agenda, vos profils Slack et Intercom. Les e-mails et les réunions provenant de ces adresses sont considérés comme les vôtres. **Retirer** celles qui ne vous appartiennent pas.

Une adresse partagée, comme info@ ou un groupe Google, n’est jamais considérée comme la vôtre par défaut. Les adresses dont la Machine n’est pas sûre apparaissent sous **Peut-être à vous**. Choisissez une option :

- **À moi : personne d’autre n’y répond** : l’adresse est considérée comme la vôtre. Les e-mails qui y sont envoyés peuvent devenir vos tâches.
- **À l’équipe : d’autres y répondent aussi** : l’adresse n’est pas considérée comme la vôtre. Les e-mails envoyés uniquement à cette adresse ne créent aucune tâche ni aucun brouillon pour vous. Ils alimentent tout de même le Graph.
- **Pas à moi** : l’adresse ne sera pas considérée comme la vôtre.

Choisissez en fonction des personnes qui répondent à l’adresse aujourd’hui. Une boîte d’équipe comme support@ appartient à l’équipe. Une adresse comme partnerships@ à laquelle vous seule répondez vous appartient. Modifiez le choix lorsque d’autres personnes commencent aussi à y répondre.

**Modifier**, sur la ligne correspondante, permet de changer votre choix plus tard. Votre propre adresse de connexion vous appartient toujours.

### Domaines de votre entreprise

Les domaines de vos propres adresses sont considérés comme ceux de votre entreprise. Vous en utilisez un autre aussi, comme acme.co en plus de acme.com ? Saisissez-le sous **Les domaines de votre entreprise**, puis cliquez sur **Ajouter**.

Les personnes qui utilisent ces domaines sont alors considérées comme des collègues, jamais comme des clients : leurs échanges n’apparaissent pas dans le Graph d’équipe et aucune organisation n’est créée pour elles. **Retirer** permet de supprimer un domaine. Les domaines de messagerie gratuits comme gmail.com ne peuvent pas être ajoutés.

Un alias Gmail qui vous appartient peut aussi être utilisé dans le champ **De** d’un brouillon, si Gmail confirme que vous pouvez envoyer des messages depuis cette adresse. Consultez [Gmail](gmail.md#what-it-can-send).
