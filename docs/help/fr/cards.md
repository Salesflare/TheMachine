---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e4ad156150993936
---
Votre Machine lit toutes les nouveautés et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver vos tâches

La page **Tâches** les regroupe :

- **Pour vous** : tout ce qui attend votre intervention, en commençant par le plus urgent. Chaque tâche indique **Préparée** (le travail est fait, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part) ou **En préparation…** (votre Machine s’en occupe).
- **Tout juste fait** : une dernière étape que vous avez confirmée, comme un formulaire ou un ticket, a été effectuée pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum, et votre téléphone vous en informe aussi.
- **Revient plus tard** : les tâches mises en attente et celles pour lesquelles vous n’avez pas répondu à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec l’heure de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après l’envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». **Ouvrir** vous y conduit. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance d’ici demain apparaissent d’abord, puis les questions de votre Fleet, puis le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain apparaissent d’abord, puis le reste, de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et votre Machine en tient compte. Ces tâches ne sont jamais considérées comme en retard. Après un jour, elles se clôturent automatiquement, avec **Annuler** pour revenir en arrière. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Une tâche qui attend encore quelqu’un d’autre, par exemple une vérification ou une réponse, indique **En attente de** cette étape. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la réactive. C’est aussi le cas après que vous avez renvoyé une question : elle revient le matin précédant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si elle est déjà passée. Elle indique alors qui doit encore répondre.

Quand une tâche concerne un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** l’indique dans **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler** pour revenir en arrière. Si vous n’avez rien reçu au moment de relancer la personne, la tâche revient avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche à laquelle personne n’a touché pendant une semaine vous demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler** pour revenir en arrière. **Garder** la conserve et la question ne s’affiche plus. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et elle n’est plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la réactive.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et la liste reste vide. Pendant une vérification, elle se réactive et vous le signale. Si une vérification a échoué ou est en retard, son statut l’indique, avec **Vérifier maintenant** en dessous.

Les vues **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’un type. Le même choix s’applique sur votre téléphone et votre ordinateur. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à toutes les tâches. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans arrêt, n’est ni Travail ni Perso et apparaît uniquement dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : **Perso uniquement · Travail · Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire ce récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou touchez son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso ou uniquement pour la vue sélectionnée.

Une tâche liée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet**, dans **Détails**, permet de le modifier ou de le retirer. Consultez [les tâches d’un projet](projects.md#a-projects-to-dos).

**Domaine**, dans **Détails**, permet de déplacer une tâche vers votre autre domaine. Les sources qu’elle peut lire et depuis lesquelles elle peut envoyer des messages sont déplacées avec elle. **Annuler** dans la note permet de la remettre à son emplacement précédent.

Quand une tâche doit passer dans votre autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et continue. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès que son domaine est déterminé. En attendant, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Lorsqu’elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte mail personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’emplacement choisi. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation concernée, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé. Elle n’apparaît jamais dans un Fleet professionnel ni dans le Graph de l’équipe.

Lorsque deux tâches ou plus vous attendent, **Passer en revue**, dans l’en-tête de Pour vous, les parcourt une par une dans l’ordre de la liste, avec le brouillon complet et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi la durée nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est incluse dans aucun des deux cas : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont inclus à la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont en pause : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30 pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous ouvrez l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher son statut et **Détails**, qui ouvre la section Vérifications dans Connexions. S’il y a des tâches ouvertes, cette option se trouve en haut sur un ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare ont leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Si une nouvelle tâche est mise de côté jusqu’à un moment plus opportun, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise de côté jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : son auteur, son sujet ou ses premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Si la vérification n’a fourni qu’une raison vague, le fil n’en indique aucune. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification de téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails de The Machine qui vous sont adressés, comme votre récap du matin ou une notification de correctif, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus comme d’habitude.

## Les boutons

Une tâche affiche l’étape suivante, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qu’il faut modifier : la façon de procéder ou, une fois le brouillon prêt, les changements à y apporter. **Marquer comme fait** indique que la tâche est traitée : l’option apparaît directement sur une tâche prête sans brouillon, sinon en haut de **…**, y compris pour une tâche qui nécessite votre décision. La tâche quitte aussitôt la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou faites-le glisser hors de la liste avec la souris pour le fermer plus tôt. La modification est conservée.

Pour procéder autrement, indiquez-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de faire une vérification](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tient compte.

Touchez le titre ou **Nom**, dans **Détails**, pour renommer la tâche. Votre titre est conservé.

**Rouvrir** réactive une tâche clôturée. Elle revient aussi automatiquement lorsqu’un nouvel événement survient, comme un nouveau message de la personne, mais pas après votre propre réponse.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les modalités de paiement mentionnées sur la facture. Ce n’est pas le cas des factures payées automatiquement, comme un prélèvement automatique ou une carte enregistrée. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple si l’expéditeur confirme l’avoir reçu, la tâche se clôture automatiquement. **Annuler** permet de la réactiver pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à recevoir avant une réunion, se clôture automatiquement après cette heure. Elle est déplacée dans **Fait / écarté** avec la mention « Plus nécessaire ». **Annuler** permet de la réactiver pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que c’est déjà fait, par exemple si la personne a été sollicitée et a accepté, la tâche se clôture automatiquement. **Annuler** permet de la réactiver pendant un jour.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête est déplacée ou une réservation annulée, The Machine met elle-même ses tâches à jour. Une tâche toujours utile suit le nouveau plan. Si elle n’a plus rien à faire, elle est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mise à jour : » et la raison. **Annuler** permet de la réactiver pendant un jour.

Pour vos premières tâches, une courte astuce présente les actions principales : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. L’astuce disparaît définitivement lorsque vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Le brouillon de cette réponse est préparé en premier, afin qu’il soit prêt à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique les personnes concernées, l’organisation s’il y en a une (jamais uniquement parce qu’une personne y travaille), le projet, Travail ou Perso et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom ou une organisation s’affiche avec sa photo ou son logo si le Graph en possède un, et avec ses initiales sinon. Si un logo est illisible en petit, par exemple blanc sur fond transparent ou sous forme de long nom stylisé, l’initiale s’affiche à la place.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact par e-mail il y a 12 jours, rien depuis ». Elle s’affiche lorsque le dernier échange avec cette personne date ou est resté sans réponse. Elle indique aussi les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine précise ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est mentionné, l’option Connecter à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si cela change. Une tâche terminée conserve son titre, avec la façon dont elle s’est conclue en dessous, par exemple « Fait : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique de quel message il provient, avec le logo du service. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination pour que vous voyiez tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon s’appuie sur les propos de quelqu’un ailleurs, comme la suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Touchez-la pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous forme d’une seule conversation, du plus ancien message au plus récent : les messages précédant celui auquel la tâche se rapporte, puis les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages sont à droite, comme dans l’application. Le message concerné par la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous.

Les **Détails** d’un e-mail n’affichent que les informations absentes de son en-tête, comme les adresses complètes en Cc, en Cci ou une autre adresse de réponse. S’il n’y a rien à ajouter, aucun détail ne s’affiche.

Une réponse dans un fil Slack affiche aussi les messages envoyés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre aussi ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. **Chat ›** ouvre le chat. Une tâche terminée reste concise : le message dont elle provient se trouve sous **Détails**.

Une tâche indiquant « En attente de » renvoie au dernier message que vous lui avez envoyé, celui dont vous attendez une réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur un ordinateur) permet de créer une tâche pour n’importe quoi. La création n’envoie rien. Si vous ne choisissez ni Travail ni Perso, la tâche est classée dans le bon domaine selon les personnes et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il date.

- **Échéance** : saisissez un jour ou une heure, comme « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », aussi dans votre propre langue. L’icône de calendrier propose des choix rapides et **Choisir une date**.
- **Message** : joignez le message concerné : un e-mail, un message Slack, Teams, WhatsApp, Telegram ou tout autre message auquel The Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son auteur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur un téléphone, l’icône d’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour retirer un fichier.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Les fichiers seuls suffisent : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en miniature. Touchez-la pour l’agrandir.
