---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre intervention, prête à recevoir votre accord. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: baa6b797e040a271
---
The Machine lit tout ce qui est nouveau et crée une tâche uniquement si quelque chose nécessite votre intervention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, vous trouverez une dernière étape que vous avez confirmée, comme un formulaire ou un problème, et qui a abouti pendant votre absence. Elle reste là jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum, et votre téléphone en est également informé.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par le plus urgent. Chaque tâche porte l’un de ces statuts : **Préparée** (le travail est fait, et **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (il faut d’abord prendre une décision ou répondre), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **En attente des autres** : les tâches dont la prochaine étape dépend de quelqu’un d’autre sont repliées (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec l’heure de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche est passée, par exemple « Envoyé. Déplacé vers Fait. » ou « Envoyé. Déplacé vers Plus tard jusqu’à lun. ». **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou arrivant à échéance demain ou avant apparaissent d’abord, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et lorsqu’elle est terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou arrivant à échéance demain ou avant apparaissent d’abord, suivies des plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et permet à votre Machine d’en tirer des enseignements. Ces tâches ne sont jamais indiquées comme en retard. Après un jour, elles se clôturent automatiquement, avec **Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture également automatiquement.

Lorsqu’un message provient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne apparaît sous sa propre adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, comme une révision ou une réponse, indique l’étape **En attente de** cette personne. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est également le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors la personne dont elle attend toujours la réponse.

Quand une tâche concerne un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Si personne ne touche à une tâche pendant une semaine, elle demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve, et elle ne vous le demande plus. Si vous ne répondez pas pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et elle n’est plus comptabilisée dans le nombre affiché sur l’icône de l’app ni dans le récap du matin. Ouvrir la tâche, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté sans activité et sans tâche ouverte peut recevoir une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre intervention, votre Machine se met en veille et votre liste reste vide. Pendant une vérification, elle se réveille et vous en informe. Si une vérification a échoué ou est en retard, la ligne l’indique et affiche **Vérifier maintenant** en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur utilisent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’affichage général. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni professionnelle ni personnelle. Elle apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et le nombre d’éléments qu’il contient, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Touchez-la pour relire ce récap, puis **Copier** pour le coller où vous voulez. Une fois ouvert ou fermé en touchant son **×**, il reste accessible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est toujours en cours, pour Travail et Perso, ou uniquement pour le type de tâches que vous avez sélectionné.

Une tâche liée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. L’option **Projet** sous **Détails** permet de le modifier ou de retirer la tâche du projet. Voir [les tâches d’un projet](projects.md#a-project-s-to-dos).

L’option **Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les éléments qu’elle peut lire et envoyer sont déplacés avec elle. **Annuler** dans la note la remet à sa place.

Lorsqu’une tâche a besoin de votre autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée et poursuit son chemin automatiquement. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès qu’elle trouve le domaine approprié. D’ici là, elle n’est associée ni à Travail ni à Perso, et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Lorsqu’elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez classée comme personnelle est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises vont dans les tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte de réception personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail et Perso déterminent où une tâche apparaît et avec qui elle est partagée, mais pas où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche personnelle de ce type répond quand même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et n’apparaît jamais dans une Fleet professionnelle ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, l’option **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, avec chaque brouillon affiché en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique également le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’apparaît dans aucun des deux groupes : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages lorsque 40 messages sont en attente ou que le plus ancien message d’une personne est en attente depuis 15 minutes. Les newsletters, notifications et reçus sont vérifiés lors du contrôle suivant, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, afin que vos tâches soient prêtes avant le récap du matin. La section Vérifications sous Connexions indique « Suspendues pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’app, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher son état, avec **Détails**, qui ouvre Vérifications sous Connexions. Si des tâches sont ouvertes, cette option se trouve en haut sur un ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre intervention » ou « · 2 nouvelles tâches ». Lorsqu’une nouvelle tâche attend le bon moment, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise de côté jusqu’à demain 08:30 ».

Touchez la ligne pour afficher chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle rien ne nécessitait d’action, comme « Seulement en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Aucun motif ne s’affiche si la vérification n’a donné qu’une raison vague. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez l’option en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification téléphonique concernant un message déjà dans la liste ne s’affiche qu’une seule fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** vous indique ce qu’il faut modifier : la façon de procéder ou, une fois le brouillon prêt, les éléments à changer. **Marquer comme fait** signifie que la tâche est traitée : l’option est visible sur une tâche prête sans brouillon, sinon elle se trouve en haut du menu **…**, y compris pour une tâche qui nécessite votre décision. La tâche quitte immédiatement la liste, et la notification propose **Annuler**. Balayez la notification ou faites-la glisser hors de l’écran avec la souris pour la fermer plus tôt. La modification est conservée.

Pour procéder autrement, dites-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confier la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demander à quelqu’un de la réviser](ask-to-review.md).
- **Répéter…** : elle [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : elle disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour le modifier. Votre titre reste inchangé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle réapparaît également automatiquement lorsqu’un nouvel événement survient, comme un nouveau message de cette personne, mais pas après votre propre réponse.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche avec le montant, la date d’échéance et les informations de paiement figurant sur la facture. Les factures payées automatiquement, comme un prélèvement automatique ou un paiement par carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple si l’expéditeur confirme avoir reçu votre paiement, la tâche se clôture automatiquement. **Annuler** la rétablit pendant un jour.

Une tâche qui n’a d’intérêt que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement à ce moment-là. Elle passe dans **Fait / écarté** avec la mention « Plus nécessaire ». **Annuler** la rétablit pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** la rétablit pendant un jour.

Lorsqu’un message plus récent modifie le programme, par exemple si une fête change de lieu ou si une réservation est annulée, The Machine met ses tâches à jour automatiquement. Une tâche qui reste pertinente suit le nouveau programme. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et la raison, et **Annuler** la rétablit pendant un jour.

Lors de vos premières tâches, une courte astuce présente les actions principales : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé tant que vous n’avez pas appuyé sur **Envoyer**. Une astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Lors de votre première journée, un message de bienvenue apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est rédigée en premier pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique qui est concerné, l’organisation s’il y en a une (et non simplement parce que quelqu’un y travaille), le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom ou une organisation s’affiche avec sa photo ou son logo si le Graph en a un, sinon avec ses initiales. Si un logo est difficile à lire en petit, par exemple du texte blanc sur fond transparent ou un long nom stylisé, les initiales s’affichent à la place.

Parfois, une ligne discrète indique ce qui est inconnu, comme « Dernier contact il y a 12 jours par e-mail, aucun échange depuis ». Elle s’affiche si le dernier échange avec cette personne est ancien ou sans réponse, et indique les canaux non connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est mentionné, l’option Connecter à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire, et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la manière dont elle s’est conclue en dessous, par exemple « Terminée : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service correspondant. Touchez-la pour lire le fil. Le brouillon affiche le logo du service auquel il sera envoyé, pour vous permettre de voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de la contribution de quelqu’un ailleurs, comme une suggestion d’un collègue dans Slack, une ligne le précise, par exemple « Selon Sam dans #ops ». Touchez-la pour lire ce message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous forme d’une conversation unique, du plus ancien au plus récent : les messages précédant celui auquel la tâche se rapporte, puis les réponses suivantes. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’app. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre dans la vue. **Afficher les messages précédents** ajoute les messages plus anciens. Les autres messages d’un fil d’e-mail sont repliés au-dessus et en dessous.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, l’e-mail s’ouvre dans l’app Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les éléments qui ne figurent pas dans son en-tête, comme les adresses complètes en Cc, les destinataires en Cci ou une autre adresse de réponse. S’il n’y a rien à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche également les messages échangés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste concise : le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » renvoie au dernier message que vous avez envoyé à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. ».

## Créer une tâche vous-même

**Nouvelle tâche** (sous **Rechercher** sur un ordinateur, sous **+** sur un téléphone ou avec `N`) permet d’ajouter une tâche pour n’importe quel sujet. La création d’une tâche n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, elle est classée dans le domaine approprié selon les personnes et le sujet concernés. Elle retrouve également l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, comme « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue également. L’icône de calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur un téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × permet d’en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez joindre uniquement des fichiers : elle remplit la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en petit : touchez-la pour l’agrandir.
