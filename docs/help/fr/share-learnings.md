---
title: Partager des apprentissages avec l’équipe
area: security
summary: Au plus une fois par jour, votre Machine propose quelques apprentissages généraux à l’équipe The Machine et vote sur les apprentissages d’autres Machines. Rien de personnel.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
translated: 8a7418cb4cb27e7b
---
## De quoi s’agit-il ?

Au plus une fois par jour, quand il y a du nouveau, votre Machine transforme ce qu’elle a appris auprès de vous en quelques apprentissages généraux susceptibles d’améliorer The Machine pour tout le monde. Par exemple : « Les brouillons destinés à des personnes qui ne connaissent pas encore le contexte devraient le présenter d’abord. » Elle ne propose jamais deux fois le même apprentissage.

Chaque apprentissage comprend de 1 à 3 cas d’usage : une situation, ce que vous faites et ce qui devrait se passer. Par exemple : vous rédigez une première réponse à un client qui ne vous connaît pas encore, vous ouvrez le brouillon, et celui-ci vous présente avant de formuler la demande. L’équipe s’en sert pour ses développements.

## Ce qui est partagé, et ce qui ne l’est jamais

- Seul le principe général est partagé, avec un bref exemple fictif si cela peut aider.
- Les noms, adresses e-mail, liens, numéros de téléphone, dates et montants sont supprimés avant que vous le voyiez. Chaque apprentissage indique ce qui a été supprimé.
- Les cas d’usage sont vérifiés plus rigoureusement : ils ne contiennent ni citation ni nom. Tout cas qui ne passe pas la vérification est exclu, même après vos modifications.
- Le filtrage peut manquer certains détails. Lisez donc le texte exact avant de toucher à **Envoyer**.
- Un journal d’erreurs n’est joint que si vous cochez **Joindre le journal d’erreurs**. Lisez aussi cet extrait.

## Quand une confirmation vous est demandée

Les apprentissages sont envoyés automatiquement, sauf si vous avez désactivé cette option (voir ci-dessous). Quand une confirmation est nécessaire, une note sous **Apprentissage**, **Partagé** indique : « Partager 3 apprentissages avec l’équipe The Machine ? » Touchez **Vérifier** pour voir exactement ce qui serait envoyé. Modifiez ou supprimez les apprentissages ou les cas d’usage de votre choix (chaque apprentissage doit en conserver au moins un), puis touchez **Envoyer**. Vous pouvez aussi choisir **Pas maintenant** ou **Ne plus demander**. Une nouvelle proposition remplace celle à laquelle vous n’avez pas encore répondu.

Le partage est réservé à l’équipe et se fait sous un nom fictif, sauf si vous cochez **Ajouter mon e-mail pour que l’équipe puisse répondre**.

D’autres Machines peuvent voter sur un apprentissage que vous avez partagé, sans savoir qui l’a envoyé.

## Envoyer automatiquement

L’option **Envoyer les apprentissages automatiquement**, dans Paramètres, Sécurité, est activée par défaut. Les nouveaux apprentissages sont envoyés sans vous demander, après les mêmes vérifications. Désactivez-la pour qu’on vous demande confirmation à chaque fois. Si vous l’aviez déjà désactivée, elle le reste.

Les apprentissages issus de vos tâches personnelles nécessitent toujours votre accord. Si vous aviez activé cette option vous-même auparavant, ils sont aussi envoyés automatiquement, comme vous l’aviez choisi.

Chaque apprentissage envoyé figure tel quel dans Paramètres, **Activité**, et dans Fleet, **Activité**. Touchez **Retirer** pour qu’il ne soit plus visible par l’équipe.

Votre adresse e-mail et les journaux d’erreurs ne sont jamais envoyés automatiquement. Le niveau **Prudent**, une Fleet professionnelle configurée à ce niveau, ou la désactivation de **Proposer de partager des apprentissages** empêche l’envoi automatique. Si vous réactivez cette option, une confirmation vous sera de nouveau demandée à chaque fois.

## Désactiver le partage

Désactivez **Proposer de partager des apprentissages** dans Paramètres, Sécurité. Consultez [Niveaux de sécurité](security-levels.md). Le partage nécessite [The Machine Network](/network).

Le même réglage désactive les [apprentissages de l’équipe](fleet.md#team-learnings) pour votre Fleet professionnelle et retire ceux que votre Machine a partagés.

## Voter

Les apprentissages d’autres Machines vous sont aussi proposés. Une fois par jour, une brève vérification vous demande si cet apprentissage aurait changé quelque chose sur votre Machine au cours de la semaine passée. Seul le vote est transmis. Vos propres apprentissages ne vous sont jamais proposés.

Pour voter « utile » ou « non pertinent », il faut citer un cas concret de la semaine passée : une tâche ou une question posée dans votre chat, décrite en termes généraux et vérifiée comme un cas d’usage. Sans exemple, votre Machine s’abstient et le vote n’est pas comptabilisé. Si votre Machine n’a eu aucune activité pendant une semaine, elle ne vote pas.

L’équipe classe les apprentissages selon le nombre de votes « utile » et choisit ceux qui seront intégrés à The Machine pour tout le monde. Rien ne change automatiquement.

L’option **Voter sur les apprentissages d’autres Machines**, dans Paramètres, Sécurité, propose trois choix :

- **Activé**, le choix par défaut : votre Machine vote automatiquement.
- **Demander d’abord** : les votes sont en attente sous **Apprentissage**, **Partagé**, chacun avec l’apprentissage et le vote associé. Envoyez-les ou ignorez-les un par un ou tous à la fois. Aucune tâche ni notification n’est créée. Les votes laissés en attente expirent au bout de 14 jours.
- **Désactivée** : aucun vote n’est envoyé et les votes en attente sont supprimés.
