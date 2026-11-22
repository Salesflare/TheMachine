---
title: Graph d’équipe
area: fleet
summary: Expérimental. Partagez le travail lié aux clients avec votre Fleet Travail, comme dans un CRM. Découvrez ce qui peut être partagé, ce qui ne l’est jamais et comment garder certains éléments privés.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: 9788be6d2d5e3fa6
---
Dans une Fleet Travail, votre Machine peut partager le travail lié aux clients avec les Machines de vos collègues, comme dans un CRM partagé. Cette fonctionnalité est **Expérimental** et désactivée par défaut.

## L’activer

Un administrateur active **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**, puis confirme que l’entreprise peut partager ces e-mails et en a informé ses employés. Tout le monde voit si le partage est activé.

Le fait d’exiger l’e-mail pro ou l’agenda de tout le monde active aussi le partage. Chacun choisit ensuite les autres éléments à partager dans **Vos connexions**. Le premier partage d’un nouveau collègue attend une heure, pour lui laisser le temps de garder certains éléments privés.

## Vos connexions

La section **Vos connexions** de **Ce qui est partagé** répertorie chaque connexion avec un bouton d’activation. Les connexions professionnelles du domaine de votre Fleet sont activées par défaut. Celles d’un autre domaine d’entreprise sont désactivées par défaut et portent la mention « Autre entreprise, non partagée ». Les connexions personnelles ne sont jamais partagées. Désactiver une connexion annule les partages qu’elle a permis.

L’agenda d’une autre personne que vous consultez avec votre propre compte apparaît sous son propre nom, comme un agenda personnel.

Même quand une connexion est activée, chaque fil est classé séparément. Le Slack de votre entreprise ne compte que comme un échange entre collègues. Seuls les chats Slack Connect avec une autre entreprise peuvent être considérés comme du travail lié aux clients. Les fils personnels, réservés aux collègues, sensibles ou automatisés ne sont pas partagés, sauf si vous les partagez vous-même.

## Exigé par la Fleet

Un administrateur peut exiger l’**E-mail pro** et l’**Agenda pro** de tout le monde sur le domaine de la Fleet, dans **Exigé par la Fleet**, après avoir confirmé que l’entreprise en a informé ses employés. Comme dans n’importe quel CRM, les e-mails professionnels appartiennent à l’entreprise. Les connexions exigées portent la mention « Exigé par » suivie du nom de votre Fleet et ne peuvent pas être désactivées. Les fils que vous gardez privés le restent.

## Ce qui est partagé avec l’équipe

- Les fils de clients : les e-mails professionnels échangés avec des personnes extérieures à votre entreprise, pièces jointes comprises.
- Les contacts professionnels, les organisations et les projets, avec une brève chronologie. Dans la **Chronologie** d’une page, **Équipe** affiche chaque événement une seule fois, dans la langue utilisée par la Machine du collègue qui l’a rédigé, avec la liste des personnes à l’origine de l’événement : « par Sam, Kim et Lee ».
- Une petite copie du logo d’une organisation et de la photo professionnelle d’une personne, provenant d’une recherche, de Slack, LinkedIn, X, Salesflare ou Microsoft. Jamais une photo des contacts Google, WhatsApp, Telegram ou Facebook, ni une photo que vous avez modifiée ou supprimée.
- Sur un tableau d’équipe, les réunions d’un projet, les notes Zoom, les conversations Intercom et les chats. Les éléments sensibles, comme les transactions, et les chats réservés aux collègues ne sont pas partagés.
- Le nombre d’éléments et les dates du [brief d’équipe](fleet.md#brief-requests) d’un collègue.
- Les réponses aux questions d’un collègue sur les personnes qui connaissent quelqu’un ou sur le contexte d’une réunion. Consultez [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- Les [apprentissages d’équipe](fleet.md#team-learnings) : le fonctionnement de l’équipe, sans noms ni détails sur les clients.

## Ce qui n’est pas partagé automatiquement

- Les fils sensibles : achat ou vente d’une entreprise, investissements, négociations de transactions, RH et recrutement, questions juridiques, Santé, argent et sécurité. Même pas le fait qu’ils existent.
- Les e-mails automatisés : reçus, factures, alertes, newsletters et factures de fournisseurs.
- Les fils réservés aux collègues, les e-mails personnels et tout ce qui provient d’un compte personnel. Les éléments personnels ne sont jamais partagés, même si vous appuyez sur **Équipe**.
- Tout ce que vous avez marqué **Garder privé**, ainsi que les tableaux et projets réglés sur Vous uniquement.
- Les personnes que vous avez classées comme personnelles, comme votre famille ou vos amis, et leurs e-mails. Un projet auquel elles participent est tout de même partagé avec son tableau, mais sans elles.

Chaque fil est évalué en fonction de son contenu, et l’évaluation peut être incorrecte. Vérifiez ce qui serait partagé et utilisez **Garder privé** pour corriger le classement. Si vous partagez vous-même un fil avec l’équipe ou des personnes précises, ce choix l’emporte sur un classement comme sensible. Vérifiez donc avec qui vous le partagez.

## Partager un tableau avec certaines personnes

Dans le menu **⋯** d’un tableau, appuyez sur **Partager le tableau…**, puis choisissez des collègues. Eux seuls recevront les projets du tableau et leur chronologie complète : e-mails, réunions et notes Zoom, conversations Intercom, chats, tâches et changements. Les éléments sensibles, comme les transactions, seront également partagés.

Les fils personnels et réservés aux collègues ne sont pas partagés, pas plus que ceux de votre famille et de vos amis, les e-mails automatisés et les connexions que vous n’avez pas sélectionnées.

- Les projets ajoutés au tableau par la suite seront aussi partagés. Si un projet est retiré du tableau, son partage est annulé.
- Si vous retirez une personne ou ne sélectionnez personne, le partage est annulé sur sa Machine.
- Pour partager un seul fil avec certaines personnes, appuyez sur son libellé, puis sur **Partager avec…**. Vous pouvez ainsi partager des e-mails professionnels sensibles ou automatisés, mais jamais des fils personnels ou réservés aux collègues.

## En cas de doute, le partage attend

Quand votre Machine n’est pas sûre, elle ne partage rien. Les fils concernés attendent dans **Partager ceux-ci ?**, regroupés par type, par exemple « Échanges avec des partenaires et des plateformes d’annonces ». Un partage vous est suggéré pour chaque groupe :

- **Partager avec l’équipe** : tout le monde dans la Fleet.
- **Partager avec…** : uniquement les collègues que vous choisissez, par exemple un membre du tableau pour les discussions avec des investisseurs.
- **Garder privé** : le contenu reste visible uniquement par vous.

Une seule action suffit pour décider du sort d’un groupe entier. Ouvrez un groupe pour décocher les fils que vous préférez traiter un par un.

Les discussions sur l’achat, la vente ou l’investissement dans une entreprise, ainsi que les sujets liés au conseil d’administration, sont sensibles. Elles ne sont donc pas proposées ici. Les échanges courants avec une entreprise partenaire relèvent du travail lié aux clients.

## Avant le premier partage

Votre premier partage est envoyé automatiquement une heure après que votre Machine vous en a informé. Pendant ce délai, ouvrez **Fleet**, puis **Ce qui est partagé** pour voir, par organisation, les fils de clients qui seraient partagés. Appuyez sur **Garder privé** pour en exclure certains, ou sur **Partager maintenant** pour les envoyer immédiatement. Les administrateurs voient qui n’a pas encore partagé.

## Ce qui est partagé

**Fleet** › **Ce qui est partagé** récapitule tout : le nombre d’éléments par type, chaque fil partagé et la raison de son partage, ceux proposés dans **Partager ceux-ci ?**, ainsi que les éléments que vous gardez privés. Appuyez sur un objet pour lire le fil correspondant. **Paramètres** et le libellé de chaque fil renvoient également à cette page.

Un nouveau fil de client attend une heure avant d’être partagé, pour vous laisser le temps de changer d’avis. Il est ensuite partagé dans la demi-heure. L’annulation d’un partage et l’action **Garder privé** sont répercutées auprès de votre équipe dans les 5 minutes.

## Annuler un partage

Appuyez sur le libellé **Équipe** d’un fil, puis sur **Ne plus partager**. La Machine de chaque collègue supprime le fil, ses pièces jointes et les entrées correspondantes dans la chronologie, ou le fait dès qu’elle est de nouveau en ligne. Quelqu’un a peut-être déjà lu le contenu.

L’action **Garder privé** sur une personne, une organisation ou un projet annule le partage de tous ses éléments.

Si vous gardez privés deux fils concernant la même entreprise, votre Machine vous demande si vous souhaitez toujours garder cette entreprise privée.

## Qui peut voir le contenu

Uniquement les Machines de vos collègues. Le contenu est chiffré de bout en bout. The Machine Network le transmet, mais ne peut pas le lire.

## Ajouter des personnes et de nouveaux appareils

Un administrateur autorise chaque personne une seule fois. La demande apparaît dans **Tâches** pour tous les administrateurs, et la première réponse l’emporte. Par la suite, le partage ne demande plus d’approbation.

En attendant, le Graph et la Fleet de la nouvelle personne indiquent les administrateurs dont l’accord est attendu. **Les miens** et **Équipe** s’affichent quelques secondes après l’approbation, sans actualiser la page.

Une nouvelle Machine d’une personne déjà membre reçoit le Graph de l’équipe après 24 heures. Dans l’intervalle, les administrateurs peuvent appuyer sur **Pas à eux** pour empêcher son ajout.

## Lorsqu’une personne quitte l’équipe

Elle ne reçoit plus rien à partir de ce moment-là. Ce qu’elle a partagé reste accessible à l’équipe. Un administrateur peut aussi **Retirer** une personne, puis **Partager à nouveau** plus tard.

## Désactiver le partage pour tout le monde

Un administrateur désactive **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**. Aucun nouvel élément ne sera partagé.

**Désactiver** conserve ce que les collègues ont déjà reçu. **Désactiver et retirer les données partagées** demande à chaque Machine de supprimer ces données. Si le partage est réactivé, chaque personne doit d’abord les examiner à nouveau.

## Arrêter de partager votre travail

Désactivez vos connexions dans **Vos connexions**, sauf si la Fleet les exige. Les éléments partagés par leur intermédiaire sont retirés.

Consultez aussi [Fleets](fleet.md) et [Sécurité et confidentialité](security-and-privacy.md).
