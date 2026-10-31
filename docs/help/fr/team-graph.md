---
title: Graph d’équipe
area: fleet
summary: Expérimental. Partagez votre travail client avec votre Fleet Travail, comme un CRM. Ce qui part, ce qui ne part jamais, et comment garder quelque chose privé.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
---
Dans une Fleet Travail, votre Machine peut partager votre travail client avec les Machines de vos collègues, comme un CRM partagé. C’est **Expérimental** : c’est nouveau et ça évolue encore, donc c’est désactivé au départ.

## L’activer

Un admin active **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**, et confirme que l’entreprise peut partager ces e-mails et qu’elle a prévenu ses équipes. Tout le monde voit si c’est activé. Une Fleet qui partageait déjà reste activée. Ensuite, chaque personne regarde ce qui partirait et appuie sur **Commencer**. Rien ne part avant.

## Vos connexions

**Vos connexions**, dans **Ce qui est partagé**, liste chaque connexion avec un interrupteur. Celles de travail sur le domaine de votre Fleet sont activées au départ. Une connexion sur le domaine d’une autre entreprise est désactivée au départ, même si c’est un compte de travail : elle indique « Autre entreprise, non partagé ». Vous pouvez l’activer. Les connexions perso ne partent jamais. En désactiver une reprend ce qu’elle a partagé.

L’agenda d’une autre personne que vous lisez avec votre propre connexion apparaît sous son nom, comme une connexion perso.

Dans une connexion activée, chaque fil est quand même trié. Le Slack de votre propre entreprise compte comme entre collègues uniquement, messages directs compris : seule une conversation Slack Connect avec une autre entreprise peut être un fil client. Les fils perso et ceux entre collègues uniquement restent exclus. Les e-mails sensibles et automatiques restent hors du partage automatique ; vos choix de partage explicites peuvent passer outre ces classements.

## Exigé par la Fleet

Un admin peut exiger l’**E-mail pro** et l’**Agenda pro** de chacun sur le domaine de la Fleet, sous **Exigé par la Fleet**, après avoir confirmé que l’entreprise a prévenu ses équipes. Les e-mails de travail appartiennent à l’entreprise, comme dans tout CRM. Ces connexions indiquent alors « Exigé par » votre Fleet et ne peuvent pas être désactivées. Les fils que vous gardez privés restent privés.

## Ce qui part vers l’équipe

- Les fils clients : les e-mails de travail avec des personnes extérieures à votre entreprise, avec leurs pièces jointes.
- Les personnes, organisations et projets de travail, avec une courte chronologie.
- Sur un tableau d’équipe, les réunions d’un projet, les notes Zoom, les conversations Intercom et les chats aussi, parce qu’ils sont sur le tableau. Les éléments sensibles, comme les deals, restent exclus.

## Exclu du partage automatique

- Les fils sensibles : achat ou vente d’une entreprise, investissements, valorisations, négociations, RH, embauche et recruteurs, juridique, santé, argent, sécurité. Pas même le fait qu’ils existent.
- Les e-mails automatiques : reçus, factures, alertes, newsletters, et les factures de votre entreprise avec ses fournisseurs.
- Les fils internes (entre collègues uniquement), les e-mails perso et tout ce qui vient d’un compte perso. Le perso ne part jamais, même si vous appuyez sur Équipe.
- Tout ce que vous avez marqué **Garder privé**, ainsi que les tableaux et projets réglés sur Vous seul.

Chaque fil est jugé séparément, selon son sujet. Le classement peut se tromper ; vérifiez ce qui partirait et utilisez Garder privé pour corriger. Votre choix explicite Équipe ou un partage avec des collègues nommés peut passer outre un classement sensible ; vérifiez les destinataires avant de partager.

## Partager un tableau avec des personnes choisies

Dans le menu **⋯** d’un tableau, appuyez sur **Partager le tableau…** et choisissez des collègues. Seules ces personnes reçoivent ses projets avec leur chronologie complète : fils d’e-mails, réunions et leurs notes Zoom, conversations Intercom, chats, tâches et déplacements. Les éléments sensibles partent aussi, comme les deals.

Les fils perso et ceux entre collègues uniquement restent exclus, de même que les personnes de votre Famille ou de vos Amis et les e-mails automatiques quand seul leur tableau est partagé. Les connexions que vous n’avez pas sélectionnées restent exclues aussi.

- Un projet ajouté au tableau plus tard part aussi. Un projet retiré du tableau est repris.
- Retirez quelqu’un, ou ne choisissez personne, et c’est repris de sa Machine.
- Un fil peut aussi partir vers des personnes choisies : appuyez sur son étiquette, puis sur **Partager avec…**. Ce choix explicite peut inclure des e-mails de travail sensibles ou automatiques. Les fils perso et ceux entre collègues uniquement ne peuvent pas être partagés.

## Pas sûr ? Ça attend

Quand votre Machine n’est pas sûre, elle ne partage pas. Ces fils attendent sous **Partager ceux-ci ?**, groupés selon ce qu’ils sont (comme « Échanges de partenaires et de listings »), chaque groupe avec un choix suggéré :

- **Partager avec l’équipe** envoie à toute la Fleet.
- **Partager avec…** envoie seulement aux coéquipiers que vous choisissez, par exemple un membre du conseil pour des discussions avec des investisseurs. Le reste de l’équipe ne le reçoit pas.
- **Garder privé** le garde chez vous.

Un seul appui décide pour tout un groupe. Ouvrez un groupe pour voir ses fils et décochez ceux que vous voulez décider à part.

Les discussions sur l’achat, la vente ou l’investissement dans une entreprise, et les sujets du conseil, comptent comme sensibles : elles n’attendent donc pas ici. Les listings, les intégrations et le reste du travail courant avec une entreprise partenaire sont du travail client.

## Avant le premier partage

Ouvrez **Fleet**, puis **Ce qui est partagé**. La liste montre les fils clients qui partiraient, par organisation. Appuyez sur **Garder privé** pour ceux que vous voulez, puis sur **Commencer**.

Tant que vous n’avez pas commencé, votre Machine vous le rappelle tous les quelques jours, pendant vos heures de travail. Les admins voient qui n’a pas encore commencé.

## Ce qui est partagé

**Fleet** › **Ce qui est partagé** montre tout au même endroit : le nombre par type, chaque fil partagé avec la raison de son envoi, ceux qui attendent sous **Partager ceux-ci ?**, et ce que vous gardez privé. **Paramètres** a un raccourci, tout comme l’étiquette de chaque fil. Touchez l’objet d’un fil pour le lire.

Un nouveau fil client attend une heure avant de partir, pour vous laisser le temps de changer d’avis.

## Arrêter de partager un fil

Appuyez sur l’étiquette **Équipe** d’un fil, puis sur **Ne plus partager**. Votre Machine prévient la Machine de chaque collègue, et chacune supprime le fil, ses pièces jointes et ses lignes dans la chronologie. Une Machine éteinte le fait à son retour. Quelqu’un l’a peut-être déjà lu.

**Garder privé** sur une personne, une organisation ou un projet retire tout le partage de la même façon.

Gardez privés deux fils avec la même entreprise et votre Machine vous demande une fois : toujours garder privés les fils de cette entreprise ?

## Qui le voit

Uniquement les Machines de vos collègues. Tout est chiffré de bout en bout, scellé pour la Machine de chaque collègue. The Machine Network ne fait que transmettre et ne peut pas lire.

## Arrivées et nouveaux appareils

Un admin fait entrer chaque personne dans la Fleet une fois. Ensuite, partager avec elle ne demande plus d’accord. La demande s’affiche dans **Suggestions** pour chaque admin, et la première réponse vaut pour toute l’équipe. Les membres ne la reçoivent jamais.

Une nouvelle Machine d’une personne déjà membre reçoit le Graph de l’équipe après 24 heures. Les admins la voient en attendant et peuvent appuyer sur **Pas la sienne** pour l’exclure.

## Quand quelqu’un part

La personne ne reçoit plus rien de nouveau à partir de ce moment. Ce qu’elle a partagé reste dans l’équipe. Un admin peut aussi **Retirer** quelqu’un, puis **Partager à nouveau** plus tard.

## Le désactiver pour tout le monde

Un admin peut désactiver **Partager le Graph dans cette Fleet** dans **Ce qui est partagé**. Tout le monde voit si c’est activé. Quand c’est désactivé, plus rien de nouveau ne part.

**Désactiver** garde ce qui est déjà sur les Machines des collègues. **Désactiver et supprimer les données partagées** fait supprimer à chaque Machine ce qu’elle a reçu. Quand le partage revient, chaque personne vérifie d’abord à nouveau.

## Arrêter de partager votre propre travail

Désactivez vos connexions sous **Vos connexions**, sauf si la Fleet les exige. Ce qu’elles ont partagé est repris.

Voir aussi [Fleets](fleet.md) et [Sécurité et confidentialité](security-and-privacy.md).
