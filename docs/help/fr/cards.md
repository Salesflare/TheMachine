---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Découvrez ce que signifie chaque partie d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 4209ed807e753101
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver vos tâches

La page **Tâches** les regroupe ainsi :

- **Tout juste fait** : tout en haut, la dernière étape que vous avez validée, comme un formulaire envoyé ou un problème résolu pendant votre absence. Elle reste là jusqu’à ce que vous touchiez **Compris**, pendant un jour au maximum. Votre téléphone la signale aussi.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (elle nécessite d’abord votre décision ou votre réponse ; si le travail est bloqué par un élément que vous seul pouvez fournir, comme une information, une connexion ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape revient à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. La tâche reste ouverte. » **Ouvrir** permet d’y accéder. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque groupe, les plus récentes s’affichent en premier. Une tâche garde sa place pendant que votre Machine la prépare et lorsqu’elle est terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les autres par ordre de nouveauté. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et permet à votre Machine d’en tirer des enseignements. Ces tâches ne sont jamais considérées comme en retard. Si un message indique qu’elle est terminée, elle se clôture automatiquement au bout d’un jour, avec **Annuler**. Sinon, elle attend que vous touchiez **Marquer comme fait**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture elle aussi automatiquement.

Si un message vient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne est présentée par sa propre adresse, jamais par le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne associée à l’adresse que vous avez déjà, jamais auprès de son auteur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une vérification ou une réponse, indique **En attente de :** suivi de l’étape concernée. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. Il en va de même après une question de votre part : la tâche revient le matin avant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si elle est déjà passée. Elle indique alors qui doit encore répondre.

Quand une tâche dépend d’un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche revient avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier cela.

Une tâche qui n’a rien de nouveau depuis une semaine passe de Pour vous à **Plus anciennes**. Ainsi, après quelques jours d’absence, les tâches récentes apparaissent en premier. Rien de nouveau signifie qu’aucun nouveau message n’a été reçu et que vous n’avez rien fait sur la tâche, comme écrire dans le chat, la modifier ou la mettre en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme inutiles toutes les tâches de Plus anciennes après une seule confirmation, comme **Pas nécessaire** le fait une par une, avec **Annuler**. Tout nouvel élément les fait revenir dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine pose une seule fois la question **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve et la question ne s’affiche plus. Sans réponse pendant une semaine de plus, elle est repliée dans Revient plus tard, et elle n’est plus comptabilisée dans le nombre affiché sur l’icône de l’app ni dans le récap du matin. La consulter, écrire dans son chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté inactif sans tâche ouverte peut recevoir une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant ses vérifications, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique et affiche **Vérifier maintenant**.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur utilisent le même choix. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, par exemple un élément qui redémarre sans cesse, n’est ni Travail ni Perso et s’affiche uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire le récap, avec **Copier** pour le coller où vous voulez. Une fois ouvert ou après avoir touché son **×**, il reste affiché sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso, ou uniquement pour la vue sélectionnée.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet**, sous **Détails**, permet de modifier le projet ou de le retirer. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, sous **Détails**, permet de déplacer une tâche dans votre autre domaine. Les messages auxquels elle peut accéder et auxquels elle peut répondre la suivent. **Annuler**, dans la note, permet de la déplacer à nouveau.

Quand une tâche a besoin de votre autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et se poursuit. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que son domaine est déterminé. D’ici là, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez classée comme Perso compte comme personnelle. Les e-mails d’une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, par exemple un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous parvient sur un compte personnel, par exemple un client sur WhatsApp, une commande dans votre boîte mail personnelle ou une [promesse](promises.md) concernant le travail, est associé à Travail dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où la tâche s’affiche et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation concernée, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle l’e-mail a été envoyé. Elle n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` passe à la suite et Échap arrête le parcours. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, le récap indique ce qui a été envoyé ou clôturé et ce qui est encore en préparation.

Les tâches qui vous posent une question sont exclues des deux groupes : elles attendent votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont quand même lus et conservés, puis traités ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « En pause pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’app, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiatement.

**Vérifier maintenant** lance immédiatement la vérification de toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher **Détails**, qui ouvre Vérifications dans Connexions. S’il y a des tâches ouvertes, l’option se trouve en haut de la page sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle concerne uniquement cette vérification : les tâches déjà dans votre liste restent telles quelles. Si une nouvelle tâche attend un moment plus approprié, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Touchez cette ligne pour afficher chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’auteur, l’objet ou les premiers mots du message, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’en nécessitait pas, comme « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a fourni qu’une vague. Touchez un élément pour le lire avec les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Touchez sous ceux-ci pour voir la suite. Le nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà affiché ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou une notification de correction, ne sont jamais lus ni affichés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche indique la prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer quoi changer : la façon de faire, ou, une fois le brouillon prêt, ce qu’il faut modifier. **Marquer comme fait** indique que la tâche est traitée : l’option est visible sur une tâche prête sans brouillon ou une tâche qui vous pose une question. Sinon, elle se trouve en haut de **…**. La tâche disparaît aussitôt de la liste, avec **Annuler** dans le message. Balayez le message ou faites-le glisser hors de l’écran avec la souris pour le fermer plus tôt. La modification est conservée.

Pour que la tâche soit faite autrement, indiquez-le dans son **Chat**. La réponse mentionne uniquement les changements effectués, par exemple la mise en attente et sa durée. Si un élément n’a pas pu être modifié, comme une échéance, elle vous le signale.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une vérification](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour le renommer, ou demandez-le dans le chat, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** réactive une tâche clôturée. Elle peut aussi réapparaître automatiquement si un nouvel événement survient, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La tâche indique alors quand elle est revenue et se classe comme une nouvelle tâche. Son chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche avec le montant, l’échéance et les coordonnées de paiement indiqués sur la facture. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Si un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur indiquant qu’il l’a reçu, la tâche se clôture automatiquement. **Annuler** la rétablit pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure définie, comme une confirmation à envoyer avant une réunion, se clôture automatiquement après cette heure. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la rétablit pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, elle se clôture automatiquement. **Annuler** la rétablit pendant un jour.

Si quelqu’un a écrit dans la même conversation après la création de votre brouillon, **Envoyer** est bloqué : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez à nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent change le plan, par exemple si une fête a lieu dans un autre endroit ou si une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche toujours nécessaire suit le nouveau plan. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mise à jour : » et la raison, et **Annuler** la rétablit pendant un jour.

Un bref conseil s’affiche avec vos premières tâches pour présenter les actions principales : **Demander des modifications** et **Pas nécessaire**, et préciser que rien n’est envoyé avant que vous touchiez **Envoyer**. Le conseil disparaît définitivement dès que vous utilisez son bouton ou touchez ×.

Le premier jour, le haut de la page Tâches vous souhaite la bienvenue et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier, pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique qui est concerné, l’organisation s’il y en a une (jamais uniquement parce que la personne y travaille), le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans Graph.

Les noms et les organisations affichent leur photo ou leur logo si Graph en a un, et leurs initiales dans le cas contraire. Si un logo est difficile à lire en petit, par exemple s’il est blanc sur fond transparent ou s’il s’agit d’un long nom, les initiales s’affichent aussi.

Une ligne discrète indique parfois ce qui est inconnu, par exemple « Dernier contact par e-mail il y a 12 jours, aucun échange depuis ». Elle s’affiche lorsque le dernier échange est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Quand un canal non connecté est mentionné, l’option Connecter à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Fait : Sam l’a signée mardi ».

Au-dessus du brouillon, une ligne discrète indique le message dont il provient, avec le logo du service concerné. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, pour voir tout de suite s’il s’agit d’une réponse dans Slack ou d’un e-mail.

Si le brouillon tient compte d’une suggestion formulée ailleurs, par exemple par un collègue dans Slack, une ligne l’indique, comme « D’après Sam dans #ops ». Touchez-la pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, du plus ancien au plus récent : les messages précédant celui auquel la tâche se rapporte, puis les réponses suivantes. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’app. Le message lié à la tâche porte la mention « Cette tâche » et s’affiche ouvert. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous.

Un message s’ouvre de la même manière depuis la recherche, Graph, les réponses d’Ask ou la dernière vérification, avec la mention « Ce message » (ou « Nouveaux messages »).

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’app Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, en Cci ou une adresse de réponse différente. S’il n’y a rien à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages envoyés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste concise : le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » renvoie à votre dernier message à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche vous-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quel besoin. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée dans le domaine qui convient, selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il date.

- **Échéance** : saisissez un jour ou une heure, comme « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue. L’icône de calendrier donne accès à des choix rapides et à **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, de Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son auteur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur téléphone, l’icône d’appareil photo permet de prendre une photo. Jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent : elle remplit la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en petit : touchez-la pour l’agrandir.
