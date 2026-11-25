---
title: Sécurité et confidentialité
area: security
summary: Votre Machine privée, vos e-mails stockés sous forme chiffrée et rien n’est envoyé sans votre accord. Voici l’essentiel et quelques liens utiles.
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 27c910c92b215ad3
---
## En bref

- Votre Machine, rien qu’à vous : si elle est hébergée, elle se trouve dans le cloud de l’UE et vous est réservée. Vous pouvez aussi l’exécuter sur votre propre ordinateur.
- Nous ne lisons pas vos e-mails : les messages sont stockés sous forme chiffrée et nos outils d’assistance ne peuvent pas les ouvrir.
- Rien n’est envoyé sans votre accord : elle lit et rédige des brouillons, et c’est vous qui décidez de ce qui est envoyé. Voir [Faire](do-it.md).
- Aucune utilisation pour entraîner l’IA : nous n’avons pas notre propre IA. Votre fournisseur intervient avec votre compte et selon ses conditions.
- Apprentissages partagés avec l’équipe, sauf si vous les désactivez : de temps en temps, quelques conseils généraux, rien de personnel, vérifiés avant leur envoi. Voir [Partager les apprentissages](share-learnings.md).
- Rapports d’erreur, sauf si vous les désactivez : en cas de problème, le type d’erreur et l’endroit concerné dans le code. Jamais vos messages, vos noms ou vos adresses. Voir [Rapports d’erreur](error-reports.md).
- Statistiques d’utilisation sur une Machine hébergée : le nombre quotidien d’actions effectuées (par exemple, les tâches ouvertes ou les e-mails envoyés), jamais leur contenu, ainsi que le temps de chargement de votre tableau de bord (uniquement le temps de chargement, sur téléphone ou ordinateur, dans l’app ou le navigateur).
- Emportez vos données ou supprimez-les : exportez tout depuis **Paramètres** › **Général**, ou supprimez votre Machine et ses sauvegardes en un seul clic. Voir [Résilier ou supprimer](cancel-and-delete.md).
- Nos accès sont consignés : chaque fois que notre équipe consulte le rapport de votre Machine hébergée ou ses journaux. Les propriétaires et les administrateurs de Fleet peuvent voir ces accès sous **Activité**. Voir [Fleets](fleet.md).

## Sauvegardes

Une Machine hébergée sauvegarde vos données chaque nuit. La sauvegarde est chiffrée sur votre Machine avant d’en sortir, puis stockée dans Microsoft Azure, aux Pays-Bas (UE). Les 7 dernières sauvegardes quotidiennes, les 4 dernières hebdomadaires et les 3 dernières mensuelles sont conservées, soit environ 3 mois. Elles sont supprimées avec votre Machine.

Pouvons-nous les ouvrir ? Oui, pour restaurer une Machine qui ne fonctionne plus : nous détenons la clé séparément des sauvegardes. Les messages contenus dans une sauvegarde sont chiffrés une seconde fois avec une deuxième clé que nous détenons également. Cette clé est conservée sous scellés et ne figure jamais dans la sauvegarde.

Ces sauvegardes sont une protection. Gardez donc une copie de ce que vous ne pouvez pas perdre : **Tout**, dans **Paramètres** › **Général** › **Exporter**. Voir [Passer sur un autre ordinateur](moving.md).

Sur votre propre ordinateur, aucune sauvegarde n’est faite automatiquement et nous n’en avons aucune copie. Une sauvegarde chiffrée chaque nuit de votre dossier personnel suffit : voir [Bien démarrer](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md#later).

## Niveaux de sécurité

**Standard** conserve les paramètres par défaut actuels. **Prudent** n’affiche aucun texte dans les notifications, ne mémorise pas les connexions et conserve moins de données. L’administrateur d’un Fleet Travail peut régler le Fleet sur le niveau Prudent. Voir [Niveaux de sécurité](security-levels.md).

## Connexion

Pour accéder au tableau de bord hébergé, vous avez besoin d’une clé d’accès, ou de vous connecter avec Google ou Microsoft et de saisir un code d’authentification.

## Connexions

L’article de chaque connexion indique ce qu’elle lit et ce qu’elle peut envoyer. Vous pouvez déconnecter n’importe laquelle à tout moment : voir [Connexions](connections.md).

## Assistance

L’assistance fonctionne sur votre Machine et ne peut pas consulter vos données. Seul le sujet de chaque question est transmis à l’équipe The Machine, jamais vos mots. Voir [Demander de l’aide](help-chat.md#what-the-team-sees).

## En savoir plus

- [Sécurité](/security) : comment elle est conçue, ce que notre équipe peut ou ne peut pas voir, et comment nous recherchons les problèmes.
- [Avis de confidentialité](/privacy) et [conditions de traitement des données](/dpa).
- Vous avez trouvé un problème de sécurité ? Consultez la [politique de sécurité](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md).
