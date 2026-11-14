---
title: Graph d’équipe
area: fleet
summary: Expérimental. Partagez le travail avec vos clients avec votre Fleet professionnel, comme dans un CRM. Découvrez ce qui est partagé, ce qui ne l’est jamais et comment garder certains éléments privés.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
Dans une Fleet professionnelle, votre Machine peut partager le travail avec vos clients avec les Machines de vos collègues, comme dans un CRM partagé. Cette fonctionnalité est **Expérimental** et désactivée par défaut.

## Activer le partage

Un admin active **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**, puis confirme que l’entreprise peut partager ces e-mails et en a informé ses employés. Tout le monde voit si le partage est activé.

Le partage s’active aussi si l’entreprise exige l’adresse e-mail professionnelle ou l’agenda professionnel de tout le monde. Chaque personne choisit ensuite ce qu’elle partage en plus dans **Vos connexions**. Le premier partage d’un nouvel équipier attend une heure, pour lui laisser le temps de garder certains éléments privés.

## Vos connexions

**Vos connexions** dans **Ce qui est partagé** affiche chaque connexion avec un bouton d’activation. Les connexions professionnelles du domaine de votre Fleet sont activées par défaut. Celles d’un domaine appartenant à une autre entreprise sont désactivées par défaut et indiquent « Autre entreprise, non partagé ». Les connexions personnelles ne sont jamais partagées. Désactiver une connexion annule le partage de ce qu’elle a transmis.

Le calendrier d’une autre personne auquel vous accédez avec votre propre compte apparaît sous son propre nom, comme calendrier personnel.

Dans une connexion activée, chaque fil est tout de même classé. Le Slack de votre entreprise ne compte que comme échanges entre collègues. Seuls les chats Slack Connect avec une autre entreprise peuvent concerner des clients. Les fils personnels, réservés aux collègues, sensibles et automatisés ne sont pas partagés, sauf si vous en partagez un vous-même.

## Connexions exigées par la Fleet

Un admin peut exiger l’adresse e-mail **E-mail pro** et l’**Agenda pro** de tout le monde sur le domaine de la Fleet, dans **Exigé par la Fleet**, après avoir confirmé que l’entreprise en a informé ses employés. Les e-mails professionnels appartiennent à l’entreprise, comme dans tout CRM. Les connexions exigées indiquent « Exigé par » votre Fleet et ne peuvent pas être désactivées. Les fils que vous gardez privés le restent.

## Ce qui est partagé avec l’équipe

- Les fils avec des clients : les e-mails professionnels échangés avec des personnes hors de votre entreprise, pièces jointes comprises.
- Les personnes, les organisations et les projets professionnels, avec une chronologie succincte. Sur la page d’un élément, **Chronologie** affiche chaque événement une seule fois dans la langue de votre collègue si sa Machine l’a rédigé dans cette langue, avec les personnes à l’origine de l’événement : « via Sam, Kim, et Lee ».
- Une petite copie du logo d’une organisation et de la photo professionnelle d’une personne : récupérée par recherche, depuis Slack, LinkedIn, X, Salesflare ou Microsoft. Jamais une image issue de Google Contacts, WhatsApp, Telegram ou Facebook, ni une image que vous avez modifiée ou supprimée.
- Sur un tableau d’équipe, les réunions d’un projet, les notes Zoom, les conversations Intercom et les chats. Les échanges sensibles, comme les négociations, et ceux réservés aux collègues ne sont pas partagés.
- Le nombre et les dates des éléments du [brief d’équipe](fleet.md#brief-requests) d’un collègue.
- Les réponses aux questions d’un collègue sur les personnes qui connaissent quelqu’un ou sur le contexte d’une réunion. Consultez [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- Les [apprentissages de l’équipe](fleet.md#team-learnings) : la façon dont l’équipe travaille, sans noms ni informations sur les clients.

## Éléments exclus du partage automatique

- Les fils sensibles : achat ou vente d’une entreprise, investissements, négociations, RH et recrutement, questions juridiques, santé, argent, sécurité. Même leur existence n’est pas révélée.
- Les e-mails automatisés : reçus, factures, alertes, newsletters et factures de fournisseurs.
- Les fils réservés aux collègues, les e-mails personnels et tout ce qui provient d’un compte personnel. Les éléments personnels ne sont jamais partagés, même si vous touchez **Équipe**.
- Tout élément marqué **Garder privé**, ainsi que les tableaux et projets réservés à vous seul.
- Les personnes que vous avez classées comme personnelles, comme votre famille ou vos amis, et leurs e-mails. Un projet auquel elles participent est tout de même partagé avec son tableau, mais sans elles.

Chaque fil est classé selon son contenu, mais le classement peut être incorrect. Vérifiez ce qui serait partagé et utilisez **Garder privé** pour corriger le tir. Si vous partagez vous-même un fil avec l’équipe ou des personnes précises, cette action remplace l’étiquette « sensible ». Vérifiez donc qui y aura accès.

## Partager un tableau avec certaines personnes

Dans le menu **⋯** d’un tableau, touchez **Partager le tableau…**, puis choisissez les collègues concernés. Eux seuls reçoivent les projets du tableau avec leur chronologie complète : e-mails, réunions et notes Zoom, conversations Intercom, chats, tâches et changements. Les échanges sensibles, comme les négociations, sont également partagés.

Les fils personnels et ceux réservés aux collègues ne sont pas partagés, pas plus que ceux de votre famille et de vos amis, les e-mails automatisés et les connexions que vous n’avez pas sélectionnées.

- Les projets ajoutés au tableau par la suite sont également partagés. Ceux qui en sont retirés ne le sont plus.
- Si vous retirez une personne ou ne choisissez personne, le partage est annulé sur sa Machine.
- Pour partager un seul fil avec certaines personnes, touchez son étiquette, puis **Partager avec…**. Vous pouvez ainsi partager des e-mails professionnels sensibles ou automatisés, mais jamais des fils personnels ou réservés aux collègues.

## En cas de doute, le partage attend

Si votre Machine hésite, elle ne partage rien. Les fils concernés apparaissent dans **Partager ceux-ci ?**, regroupés par type, par exemple « Échanges avec des partenaires et annonces », avec une suggestion pour chacun :

- **Partager avec l’équipe** : tout le monde dans la Fleet.
- **Partager avec…** : uniquement les collègues que vous choisissez, par exemple un membre du tableau pour des négociations avec des investisseurs.
- **Garder privé** : le contenu reste visible par vous seul.

Une seule action permet de choisir pour tout un groupe. Ouvrez un groupe pour décocher les fils que vous souhaitez examiner un par un.

Les discussions sur l’achat, la vente ou l’investissement dans une entreprise, ainsi que les sujets du conseil d’administration, sont sensibles. Elles n’apparaissent donc pas ici. Les échanges courants avec une entreprise partenaire concernent des clients.

## Avant le premier partage

Votre premier partage est envoyé automatiquement une heure après que votre Machine vous en a informé. Pendant ce délai, ouvrez **Fleet**, puis **Ce qui est partagé** pour consulter, par organisation, les fils concernant des clients qui seraient partagés. Touchez **Garder privé** pour en exclure un, ou **Partager maintenant** pour l’envoyer tout de suite. Les admins voient qui n’a pas encore partagé.

## Ce qui est partagé

**Fleet** › **Ce qui est partagé** affiche tout : le nombre d’éléments par type, chaque fil partagé et la raison du partage, ceux qui figurent dans **Partager ceux-ci ?**, ainsi que les éléments que vous gardez privés. Touchez un sujet pour le lire. **Paramètres** et l’étiquette de chaque fil renvoient également ici.

Un nouveau fil concernant un client attend une heure avant d’être partagé, pour vous laisser le temps de changer d’avis.

## Annuler le partage

Touchez l’étiquette **Équipe** d’un fil, puis **Ne plus partager**. La Machine de chaque collègue supprime le fil, ses pièces jointes et les entrées correspondantes dans la chronologie, ou le fait dès qu’elle se reconnecte. Quelqu’un a peut-être déjà lu le contenu.

En touchant **Garder privé** sur une personne, une organisation ou un projet, vous annulez le partage de tout son contenu.

Si vous gardez privés deux fils concernant la même entreprise, votre Machine vous demande une fois si vous souhaitez toujours garder cette entreprise privée.

## Qui peut voir le contenu

Seules les Machines de vos collègues. Le contenu est chiffré de bout en bout. The Machine Network le transmet, mais ne peut pas le lire.

## Nouveaux membres et appareils

Un admin autorise chaque personne une seule fois. La demande apparaît dans **Tâches** pour tous les admins, et seule la première réponse est prise en compte. Ensuite, le partage ne nécessite aucune autre autorisation.

En attendant, le Graph et la Fleet de la nouvelle personne indiquent quels admins doivent encore l’autoriser. **Les miens** et **Équipe** apparaissent quelques secondes après l’autorisation, sans actualiser la page.

Une nouvelle Machine appartenant à une personne déjà membre reçoit le Graph de l’équipe après 24 heures. Pendant ce délai, les admins peuvent toucher **Pas à eux** pour empêcher le partage.

## Départ d’un membre

À partir de ce moment, la personne ne reçoit plus rien de nouveau. Le contenu qu’elle a partagé reste accessible à l’équipe. Un admin peut aussi **Retirer** une personne, puis **Partager à nouveau** plus tard.

## Désactiver le partage pour tout le monde

Un admin désactive **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**. Plus rien n’est partagé.

**Désactiver** conserve les éléments déjà reçus par les collègues. **Désactiver et retirer les données partagées** les supprime de toutes les Machines. Lorsque le partage est réactivé, chaque personne doit d’abord examiner à nouveau les éléments.

## Arrêter de partager votre travail

Désactivez vos connexions dans **Vos connexions**, sauf si la Fleet les exige. Le contenu qu’elles ont partagé est retiré.

Consultez aussi [Fleets](fleet.md) et [Sécurité et confidentialité](security-and-privacy.md).
