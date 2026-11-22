---
title: Partager les apprentissages avec l’équipe
area: security
summary: Au plus une fois par jour, votre Machine propose à l’équipe The Machine quelques apprentissages généraux et vote sur ceux d’autres Machines. Aucune information personnelle.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
translated: 8a7418cb4cb27e7b
---
## Ce que c’est

Au plus une fois par jour, quand il y a du nouveau, votre Machine transforme ce qu’elle a appris de vous en quelques apprentissages généraux qui pourraient améliorer The Machine pour tout le monde. Par exemple : « Les brouillons destinés à des personnes qui ne connaissent pas encore le contexte devraient le présenter d’abord. » Elle ne propose jamais deux fois le même apprentissage.

Chaque apprentissage comprend de 1 à 3 cas d’usage : une situation, ce que vous faites et ce qui devrait se passer. Par exemple : une première réponse à un client qui ne vous connaît pas encore ; vous ouvrez le brouillon ; il explique qui vous êtes avant de formuler la demande. L’équipe s’en sert pour développer The Machine.

## Ce qui est partagé et ce qui ne l’est jamais

- Seul le principe général est partagé, avec un court exemple fictif si cela peut aider.
- Les noms, adresses e-mail, liens, numéros de téléphone, dates et montants sont retirés avant que vous le voyiez. Chaque apprentissage indique ce qui a été retiré.
- Les cas d’usage sont vérifiés plus strictement : ils ne contiennent ni citations ni noms. Tout cas qui ne respecte pas ces règles est exclu, même après vos modifications.
- Le filtrage peut laisser passer des détails. Lisez donc le texte exact avant de sélectionner **Envoyer**.
- Un journal d’erreurs n’est envoyé que si vous cochez **Joindre le journal d’erreurs**. Lisez aussi cet extrait.

## Quand le système vous le demande

Les apprentissages sont envoyés automatiquement, sauf si vous avez désactivé cette option (voir ci-dessous). Quand le système vous le demande, une note sous **Apprentissage**, **Partagé** indique : « Partager 3 apprentissages avec l’équipe The Machine ? » Sélectionnez **Vérifier** pour voir exactement ce qui serait envoyé. Modifiez ou supprimez chaque apprentissage ou cas d’usage (chaque apprentissage doit en garder au moins un), puis sélectionnez **Envoyer**. Vous pouvez aussi choisir **Pas maintenant** ou **Ne plus demander**. Une nouvelle proposition remplace celle à laquelle vous n’avez pas encore répondu.

Le contenu est scellé pour l’équipe et envoyé sous un nom fictif, sauf si vous cochez **Ajouter mon e-mail pour que l’équipe puisse répondre**.

D’autres Machines peuvent voter sur un apprentissage que vous avez partagé, sans savoir qui l’a envoyé.

## Envoi automatique

L’option **Envoyer les apprentissages automatiquement**, dans Paramètres, Sécurité, est activée par défaut. Les nouveaux apprentissages sont envoyés sans vous demander votre avis, après les mêmes vérifications. Désactivez-la pour que le système vous le demande à chaque fois. Si vous l’aviez déjà désactivée, elle le reste.

Les apprentissages tirés de vos tâches personnelles nécessitent toujours votre accord. Si vous aviez activé vous-même l’envoi automatique auparavant, ils sont aussi envoyés automatiquement, comme vous l’aviez choisi.

Chaque apprentissage envoyé figure tel qu’il a été transmis dans Paramètres, **Activité**, et dans Fleet, **Activité**. Sélectionnez **Retirer** pour qu’il ne soit plus visible par l’équipe.

Votre adresse e-mail et les journaux d’erreurs ne sont jamais envoyés automatiquement. Une Fleet de travail en mode **Prudent**, ou la désactivation de **Proposer de partager des apprentissages**, bloque l’envoi automatique. Si vous réactivez cette option, le système vous le demande à chaque fois.

## Désactiver le partage

Désactivez **Proposer de partager des apprentissages** dans Paramètres, Sécurité. Consultez [Niveaux de sécurité](security-levels.md). Le partage nécessite [The Machine Network](/network).

Le même réglage désactive les [apprentissages de l’équipe](fleet.md#team-learnings) pour votre Fleet de travail et retire ceux que votre Machine a partagés.

## Votes

Les apprentissages d’autres Machines vous sont aussi proposés. Une fois par jour, une courte vérification vous demande si cela aurait changé quelque chose sur votre Machine au cours de la semaine passée. Seul le vote est transmis. Vos propres apprentissages ne vous sont jamais proposés.

Pour voter « utile » ou « sans intérêt », il faut un cas concret de la semaine passée : une tâche ou quelque chose que vous avez demandé dans le chat de cet apprentissage, formulé de manière générale et vérifié comme un cas d’usage. Sans exemple, votre Machine s’abstient et le vote n’est pas comptabilisé. Une semaine sans activité signifie qu’aucun vote n’est envoyé.

L’équipe classe les apprentissages selon le nombre de votes utiles et choisit ceux qui seront intégrés à The Machine pour tout le monde. Rien ne change automatiquement.

**Voter sur les apprentissages d’autres Machines** dans Paramètres, Sécurité propose trois options :

- **Activé**, l’option par défaut : les votes sont envoyés automatiquement.
- **Demander d’abord** : les votes attendent votre réponse sous **Apprentissage**, **Partagé**, chacun avec l’apprentissage et le vote. Envoyez-les ou ignorez-les un par un ou tous à la fois. Aucune tâche ni notification. Les votes auxquels vous ne répondez pas expirent après 14 jours.
- **Désactivée** : aucun vote n’est envoyé et les votes en attente sont supprimés.
