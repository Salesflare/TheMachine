---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: c54b334f5764bdf9
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, la dernière étape que vous avez confirmée, comme un formulaire envoyé ou un problème résolu, s’est déroulée pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum, et vous la recevez aussi sur votre téléphone.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par le plus urgent. Chaque tâche indique **Préparée** (le travail est terminé, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (elle nécessite d’abord votre décision ou votre réponse), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **En attente des autres** : les tâches dont la prochaine étape dépend de quelqu’un d’autre sont regroupées et repliées (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : vos promesses et celles des autres. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec l’heure de clôture, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». **Ouvrir** vous y conduit. La recherche permet de trouver une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou à échéance d’ici demain, puis les questions de votre Fleet, les suivis d’un tableau, puis le reste. Dans chaque groupe, les plus récentes s’affichent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, puis les autres de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et permet à votre Machine d’en tirer des enseignements. Ces tâches ne sont jamais marquées comme en retard. Au bout d’un jour, elles se clôturent automatiquement, avec la possibilité d’**Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, par exemple sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le nom affiché est celui associé à son adresse, jamais celui qu’a utilisé l’expéditeur. Votre Machine vérifie ce type de message auprès de la personne à l’adresse que vous avez déjà, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, pour une relecture ou une réponse par exemple, indique l’étape concernée sous **En attente de**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors la personne dont elle attend toujours une réponse.

Quand une tâche concerne un résultat qu’une autre personne doit fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement. Vous pouvez **Annuler** cette action. Si rien n’arrive au moment de relancer la personne, la tâche revient avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui permettra de considérer la tâche comme terminée.

Une tâche à laquelle personne n’a touché pendant une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec la possibilité d’**Annuler**. **Garder** la conserve, et elle ne posera plus la question. Sans réponse après une autre semaine, elle est déplacée dans Revient plus tard. Elle n’est alors plus comptabilisée sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet devenu inactif et sans tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et affiche une liste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique, avec **Vérifier maintenant** en dessous.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’un type. Le même filtre est appliqué sur votre téléphone et votre ordinateur. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à toutes les tâches. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le dernier récap du matin ou du soir et le nombre d’éléments qu’il comprend, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Touchez-la pour relire le récap, avec **Copier** pour le coller où vous voulez. Une fois ouvert ou fermé en touchant son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet** sous **Détails** permet de modifier le projet ou de retirer la tâche du projet. Consultez [les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** permet de déplacer une tâche vers votre autre domaine. Les sources qu’elle peut lire et les messages qu’elle peut envoyer sont déplacés avec elle. **Annuler** dans la note permet de la remettre à sa place.

Quand une tâche nécessite votre autre domaine et que tous les messages à l’origine de la tâche s’y trouvent, elle y est déplacée et continue automatiquement. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge avant que vous ne touchiez ce bouton. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que votre Machine trouve où elle doit aller. En attendant, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages qui en sont à l’origine. Quand elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez étiquetée Perso est considérée comme personnelle. Les e-mails concernant une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Une tâche professionnelle qui arrive sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte mail personnelle, est professionnelle dès le départ. Une tâche que vous avez déplacée ou associée à un domaine reste toujours là où vous l’avez mise. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, jamais l’adresse à laquelle elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle l’e-mail est arrivé. Elle n’apparaît jamais dans une Fleet Travail ni dans le Graph de l’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec chaque brouillon affiché en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le traitement. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est pas incluse : elle attend votre réponse, pas un appui sur un bouton.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès que 40 messages sont en attente ou qu’un message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Vérifications sous Connexions, le statut indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans un chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher son statut et **Détails**, qui ouvre Vérifications sous Connexions. S’il y a des tâches ouvertes, le bouton se trouve en haut de la liste sur un ordinateur. Une courte ligne s’affiche uniquement pendant une vérification ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans un chat.

LinkedIn, X et Salesflare gardent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qui a été trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Si une nouvelle tâche est mise de côté pour un meilleur moment, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise de côté jusqu’à demain 08:30 ».

Touchez la ligne pour afficher chaque fil d’e-mails, chat et notification avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle rien n’a été nécessaire, par exemple « Vous étiez seulement en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Si la vérification n’a fourni qu’une raison vague, le fil n’en indique aucune. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir la suite. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà affiché ne s’affiche qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que votre Machine vous envoie, comme le récap du matin ou un avis de correction, ne sont jamais lus ni affichés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : le bouton apparaît directement sur une tâche prête sans brouillon, sinon en haut de **…**, y compris pour une tâche qui nécessite votre décision. La tâche quitte aussitôt la liste, et une note propose **Annuler**. Balayez la note pour la faire disparaître ou faites-la glisser avec la souris pour la fermer plus rapidement. Le changement est conservé.

Pour que la tâche soit faite autrement, dites-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une relecture](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour le renommer, ou demandez-le dans le chat, par exemple « Renomme-la en … ». Votre titre est conservé.

**Rouvrir** réactive une tâche clôturée. Elle réapparaît aussi automatiquement lorsqu’un nouvel élément arrive, comme un nouveau message de cette personne, mais pas lorsque vous répondez vous-même. La tâche indique alors quand elle est réapparue et est triée comme une nouvelle tâche. La conversation dans son chat reprend là où elle s’était arrêtée, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les modalités de paiement mentionnées sur la facture. Les factures payées automatiquement, par prélèvement ou avec une carte enregistrée par exemple, ne deviennent pas des tâches. Quand un e-mail reçu plus tard confirme le paiement, par exemple l’expéditeur qui indique avoir reçu votre paiement, la tâche se clôture automatiquement. **Annuler** permet de la réactiver pendant un jour.

Une tâche qui n’était utile que jusqu’à une heure précise, comme une confirmation avant une réunion, se clôture automatiquement après cette heure. Elle est déplacée dans **Fait / écarté** avec le statut « N’est plus nécessaire ». **Annuler** permet de la réactiver pendant un jour.

Avant qu’un message ou un transfert pour une autre personne soit indiqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a accepté, la tâche se clôture automatiquement. **Annuler** permet de la réactiver pendant un jour.

Quand un nouveau message change les plans, par exemple si une fête est déplacée ou une réservation annulée, The Machine met à jour ses tâches automatiquement. Une tâche toujours utile suit les nouveaux plans. Une tâche qui n’a plus rien à faire est déplacée dans **Fait / écarté** avec le statut « Pas nécessaire ». Son chat indique « Mise à jour : » et la raison. **Annuler** permet de la réactiver pendant un jour.

Pour vos premières tâches, un court conseil présente les actions principales : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous ne touchiez **Envoyer**. Un conseil disparaît définitivement dès que vous utilisez son bouton ou touchez ×.

Le premier jour, un message d’accueil apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier, pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique qui est concerné, l’organisation s’il y en a une (pas uniquement parce que la personne y travaille), le projet, Travail ou Perso et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom ou une organisation s’affiche avec sa photo ou son logo si le Graph en a un, sinon avec ses initiales. Si un logo est illisible à cette taille, par exemple parce qu’il est blanc sur un fond transparent ou qu’il s’agit d’un long nom stylisé, l’initiale s’affiche aussi.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact par e-mail il y a 12 jours ; rien depuis ». Elle s’affiche lorsque le dernier échange avec cette personne date ou reste sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de deviner.

Quand un canal non connecté est mentionné, touchez Connexion à côté pour le connecter.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la raison de sa clôture en dessous, par exemple « Fait : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il est issu, avec le logo du service correspondant. Touchez-la pour lire le fil. Le brouillon affiche le logo du service auquel il sera envoyé, pour repérer tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de la contribution d’une personne ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « D’après Sam dans #ops ». Touchez-la pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) affiche une conversation complète, de la plus ancienne à la plus récente : les messages précédant celui dont traite la tâche et les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre directement. **Afficher les messages précédents** ajoute les messages plus anciens. Un e-mail affiche le reste de son fil, replié au-dessus et en dessous.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations qui ne figurent pas dans son en-tête, comme les adresses complètes en Cc, les destinataires en Cci ou une autre adresse de réponse. Si rien n’est à ajouter, aucune information n’apparaît.

Une réponse dans un fil Slack affiche aussi les messages envoyés avant le début du fil. Le lien d’une tâche vers le message qui lui est associé l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche son nom, son projet et son domaine (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste affichée brièvement ; le message à l’origine de la tâche se trouve sous **Détails**.

Une tâche « En attente de » renvoie au dernier message que vous avez envoyé à la personne concernée, celui dont vous attendez la réponse : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur un ordinateur, **+** sur un téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. La création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, la tâche est associée au domaine qui convient, selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « vendredi prochain », « 3 nov. », « 14 h » ou « dans 2 heures », y compris dans votre langue. L’icône de calendrier propose des options rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique son origine, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur un téléphone, l’icône d’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit quand elle s’en occupe. Les fichiers seuls suffisent : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en petit format. Touchez-la pour l’agrandir.
