---
title: Graph d’équipe
area: fleet
summary: Expérimental. Partagez le travail avec vos clients avec votre Fleet professionnelle, comme dans un CRM. Découvrez ce qui est partagé, ce qui ne l’est jamais et comment garder certains éléments privés.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
Dans une Fleet professionnelle, votre Machine peut partager le travail avec vos clients avec les Machines de vos collègues, comme dans un CRM partagé. Cette fonctionnalité est **Expérimental** et désactivée par défaut.

## L’activer

Un administrateur active **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**, puis confirme que l’entreprise peut partager ces e-mails et en a informé son personnel. Tout le monde peut voir si le partage est activé.

Le fait d’exiger l’adresse e-mail professionnelle ou l’agenda de tout le monde active aussi le partage. Chaque personne choisit ensuite ce qu’elle partage en plus dans **Vos connexions**. Le premier partage d’un nouveau collègue est différé d’une heure, pour lui laisser le temps de garder certains éléments privés.

## Vos connexions

Dans **Ce qui est partagé**, **Vos connexions** répertorie chaque connexion avec un interrupteur. Les connexions professionnelles dont le domaine correspond à celui de votre Fleet sont activées par défaut. Celles qui utilisent le domaine d’une autre entreprise sont désactivées par défaut et indiquent « Autre entreprise, non partagé ». Les connexions personnelles ne sont jamais partagées. Désactiver une connexion annule le partage de ce qu’elle a transmis.

L’agenda d’une autre personne, auquel vous accédez avec vos propres identifiants, apparaît sous son propre nom comme connexion personnelle.

Même lorsqu’une connexion est activée, chaque fil est classé séparément. Le Slack de votre entreprise ne concerne que les collègues. Seuls les chats Slack Connect avec une autre entreprise peuvent relever du travail avec des clients. Les fils personnels, réservés aux collègues, sensibles ou automatisés restent à l’écart, sauf si vous les partagez vous-même.

## Exigé par la Fleet

Dans **Exigé par la Fleet**, un administrateur peut exiger l’adresse **E-mail pro** et l’**Agenda pro** de tout le monde dans le domaine de la Fleet, après avoir confirmé que l’entreprise en a informé son personnel. Les e-mails professionnels appartiennent à l’entreprise, comme dans n’importe quel CRM. Les connexions exigées portent la mention « Exigé par » suivie du nom de votre Fleet et ne peuvent pas être désactivées. Les fils que vous gardez privés le restent.

## Ce qui est partagé avec l’équipe

- Les fils de clients : les e-mails professionnels échangés avec des personnes extérieures à votre entreprise, pièces jointes comprises.
- Les personnes, entreprises et projets professionnels, avec une courte chronologie. Dans la **Chronologie** d’une page, l’**Équipe** voit chaque événement une seule fois, dans la langue utilisée par la Machine du collègue qui l’a rédigé, avec la liste des personnes à l’origine de l’événement : « via Sam, Kim et Lee ».
- Une petite copie du logo d’une entreprise et de la photo professionnelle d’une personne, récupérée depuis une recherche, Slack, LinkedIn, X, Salesflare ou Microsoft. Jamais une photo de contacts Google, WhatsApp, Telegram ou Facebook, ni une photo que vous avez modifiée ou supprimée.
- Sur un tableau d’équipe, les réunions d’un projet, les notes Zoom, les conversations Intercom et les chats. Les éléments sensibles, comme les transactions, et les chats réservés aux collègues restent à l’écart.
- Le nombre et les dates des [briefs d’équipe](fleet.md#brief-requests) d’un collègue.
- Les réponses aux questions d’un collègue sur les personnes qui connaissent quelqu’un ou sur le contexte d’une réunion. Consultez [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- Les [apprentissages de l’équipe](fleet.md#team-learnings) : la façon dont l’équipe travaille, sans noms ni détails sur les clients.

## Ce qui n’est pas partagé automatiquement

- Les fils sensibles : achat ou vente d’une entreprise, investissements, négociations, RH et recrutement, questions juridiques, santé, argent et sécurité. Même leur existence n’est pas partagée.
- Les e-mails automatisés : reçus, factures, alertes, newsletters et factures de fournisseurs.
- Les fils réservés aux collègues, les e-mails personnels et tout ce qui provient d’un compte personnel. Les contenus personnels ne sont jamais partagés, même si vous appuyez sur Équipe.
- Tout ce que vous avez marqué **Garder privé**, ainsi que les tableaux et projets définis sur « Vous uniquement ».
- Les personnes que vous avez classées comme personnelles, comme votre famille ou vos amis, et leurs e-mails. Un projet auquel elles participent est tout de même partagé avec son tableau, mais sans elles.

Chaque fil est évalué selon son sujet, et le résultat peut être incorrect. Vérifiez ce qui serait partagé et choisissez Garder privé pour corriger le classement. Si vous partagez vous-même un fil avec l’équipe ou avec certaines personnes, cela remplace son classement comme sensible. Vérifiez donc qui y aura accès.

## Partager un tableau avec certaines personnes

Dans le menu **⋯** d’un tableau, appuyez sur **Partager le tableau…**, puis choisissez des collègues. Seuls ces collègues reçoivent les projets du tableau avec leur chronologie complète : e-mails, réunions et notes Zoom, conversations Intercom, chats, tâches et changements. Les éléments sensibles, comme les transactions, sont également partagés.

Les fils personnels et réservés aux collègues restent à l’écart, tout comme ceux de votre famille et de vos amis, les e-mails automatisés et les connexions que vous n’avez pas sélectionnées.

- Les projets ajoutés au tableau par la suite sont également partagés. Les projets déplacés hors du tableau ne le sont plus.
- Si vous retirez une personne ou ne sélectionnez personne, le contenu est retiré de sa Machine.
- Pour partager un seul fil avec certaines personnes, appuyez sur son libellé, puis sur **Partager avec…**. Cela peut inclure des e-mails professionnels sensibles ou automatisés, mais jamais des fils personnels ou réservés aux collègues.

## Vous hésitez ? Le partage attend

Quand votre Machine n’est pas sûre, elle ne partage rien. Les fils concernés attendent dans **Partager ceux-ci ?**, regroupés par catégorie (par exemple « Échanges avec des partenaires et annonces »), avec une suggestion pour chaque groupe :

- **Partager avec l’équipe** : tout le monde dans la Fleet.
- **Partager avec…** : uniquement les collègues que vous choisissez, par exemple un membre du tableau pour des discussions avec des investisseurs.
- **Garder privé** : le contenu reste accessible uniquement à vous.

Une seule action permet de décider pour tout un groupe. Ouvrez un groupe pour décocher les fils que vous souhaitez examiner un par un.

Les discussions sur l’achat, la vente ou l’investissement dans une entreprise, ainsi que les sujets liés au conseil d’administration, sont sensibles et n’attendent donc pas ici. Les échanges professionnels courants avec une entreprise partenaire relèvent du travail avec des clients.

## Avant le premier partage

Votre premier partage est envoyé automatiquement une heure après que votre Machine vous en a informé. Pendant ce délai, ouvrez **Fleet**, puis **Ce qui est partagé** pour consulter les fils de clients qui seraient partagés, classés par entreprise. Appuyez sur **Garder privé** pour ceux que vous ne souhaitez pas partager, ou sur **Partager maintenant** pour les envoyer sans attendre. Les administrateurs voient qui n’a pas encore partagé.

## Ce qui est partagé

**Fleet** › **Ce qui est partagé** récapitule tout : le nombre d’éléments par catégorie, chaque fil partagé et la raison du partage, ceux qui figurent dans **Partager ceux-ci ?**, ainsi que ce que vous gardez privé. Appuyez sur un objet pour lire le fil correspondant. **Paramètres** et le libellé de chaque fil renvoient également à cette page.

Un nouveau fil de client attend une heure avant d’être partagé, pour vous laisser le temps de changer d’avis.

## Annuler un partage

Appuyez sur le libellé **Équipe** d’un fil, puis sur **Ne plus partager**. La Machine de chaque collègue supprime le fil, ses pièces jointes et les entrées correspondantes dans la chronologie. Si elle est hors ligne, la suppression a lieu dès qu’elle se reconnecte. Quelqu’un a peut-être déjà lu le fil.

L’action **Garder privé** sur une personne, une entreprise ou un projet annule le partage de tous les éléments correspondants.

Si vous gardez privés deux fils avec la même entreprise, votre Machine vous demande une seule fois si vous souhaitez toujours garder cette entreprise privée.

## Qui peut voir ces éléments

Uniquement les Machines de vos collègues. Le chiffrement est de bout en bout. The Machine Network les transmet, mais ne peut pas les lire.

## Ajouter une personne et ses nouveaux appareils

Un administrateur autorise chaque personne une seule fois. La demande apparaît dans **Tâches** pour tous les administrateurs, et c’est la première réponse qui compte. Ensuite, le partage ne nécessite plus d’approbation.

En attendant, le Graph et la Fleet de la nouvelle personne indiquent les administrateurs dont l’approbation est nécessaire. **Les miens** et **Équipe** s’affichent quelques secondes après l’approbation, sans actualiser la page.

La nouvelle Machine d’une personne déjà membre reçoit le Graph de l’équipe au bout de 24 heures. Dans l’intervalle, les administrateurs peuvent appuyer sur **Pas à eux** pour empêcher le partage.

## Quand une personne quitte l’équipe

Elle ne reçoit plus rien à partir de ce moment. Les éléments qu’elle a partagés restent accessibles à l’équipe. Un administrateur peut aussi **Retirer** une personne, puis **Partager à nouveau** plus tard.

## Désactiver le partage pour tout le monde

Un administrateur désactive **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**. Plus rien n’est partagé à partir de ce moment.

**Désactiver** conserve les éléments que les collègues ont déjà reçus. **Désactiver et retirer les données partagées** les supprime de toutes les Machines. Si le partage est réactivé, chaque personne doit d’abord examiner à nouveau les éléments.

## Arrêter de partager votre travail

Désactivez vos connexions dans **Vos connexions**, sauf si la Fleet les exige. Les éléments qu’elles ont partagés sont retirés.

Consultez aussi [Fleets](fleet.md) et [Sécurité et confidentialité](security-and-privacy.md).
