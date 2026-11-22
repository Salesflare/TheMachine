---
title: Tâches
area: cards
summary: Une tâche par chose qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 84b8879d98f26aa2
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement si quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum. Votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche indique **Préparée** (le travail est fait, et **Faire** ou **Envoyer** permet de le terminer), **Vous attend** (elle nécessite d’abord votre décision ou une réponse), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un bref résumé, sans décision à prendre).
- **Plus ancien** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir plus bas).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir plus bas).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir plus bas).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé vers Fait. » ou « Envoyé. Déplacé vers Plus tard jusqu’à lundi. » Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », ne clôt pas la tâche : « Envoyé. Tâche laissée ouverte. » **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, suivies des questions de votre Fleet, des relances d’un tableau, puis du reste. Dans chaque groupe, les plus récentes s’affichent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, puis les autres de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais indiquées comme en retard. Au bout d’un jour, elles se clôturent automatiquement. Vous pouvez alors appuyer sur **Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture également automatiquement.

Lorsqu’un message vient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche le signale clairement : « Ce n’est pas Sam Lee. » L’expéditeur est identifié par sa propre adresse, jamais par le nom qu’il a indiqué. Votre Machine vérifie le message auprès de la personne qui utilise l’adresse que vous connaissez déjà, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, comme une relecture ou une réponse, indique l’étape concernée avec **En attente de**. Elle apparaît dans **En attente des autres**, dans une section repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci est plus tard dans la journée, ou le lendemain matin si elle est déjà passée. Elle indique alors toujours la personne dont elle attend la réponse.

Lorsqu’une tâche porte sur un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement. Vous pouvez alors appuyer sur **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche qui n’a rien de nouveau depuis une semaine passe de Pour vous à **Plus ancien**, pour que les tâches récentes s’affichent en premier après quelques jours d’absence. Rien de nouveau signifie qu’il n’y a eu ni nouveau message, ni action de votre part, comme un message dans le chat, une modification ou une mise en attente. Le simple fait de consulter la tâche ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires toutes les tâches de Plus ancien après une seule confirmation, comme le fait **Pas nécessaire** pour une tâche à la fois. Vous pouvez alors appuyer sur **Annuler**. Si une tâche reçoit du nouveau, elle revient dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture. Vous pouvez alors appuyer sur **Annuler**. **Garder** la conserve, et la question ne s’affichera plus. Si vous ne répondez pas pendant une autre semaine, elle est repliée dans Revient plus tard. Elle n’est alors plus comptabilisée sur l’icône de l’app ni dans le récap du matin. Le fait de l’ouvrir, d’envoyer un message dans le chat, de la modifier, de la mettre en attente ou de recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet qui n’a pas avancé et ne contient aucune tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique et propose **Vérifier maintenant**.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou celles d’un seul type. Votre téléphone et votre ordinateur partagent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’affichage complet. Une alerte concernant votre Machine elle-même, par exemple un composant qui redémarre sans cesse, n’est ni Travail ni Perso et n’apparaît que dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre affichage : sous **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire le récap, puis sur **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou que vous appuyez sur son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom du projet sous son titre. Appuyez dessus pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de le retirer. Consultez [les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les sources qu’elle peut lire et les messages qu’elle peut envoyer sont déplacés avec elle. **Annuler** dans la note permet de la remettre à sa place.

Lorsqu’une tâche doit passer dans votre autre domaine pour avancer et que tous les messages à son origine s’y trouvent, elle y est déplacée automatiquement et le travail se poursuit. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge avant que vous appuyiez dessus. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès que votre Machine trouve où elle doit aller. En attendant, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages dont elle est issue. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les e-mails concernant une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message d’un membre de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où une tâche s’affiche et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée là où se trouve la conversation, même après un déplacement, sauf si vous choisissez une autre option.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé. Elle n’apparaît jamais dans une Fleet professionnelle ni dans le Graph de l’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec chaque brouillon affiché en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, la touche Entrée envoie le contenu affiché, `S` met la tâche en attente, `→` l’ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question est exclue des deux groupes : elle attend votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont inclus à la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont en pause : les nouveaux messages sont quand même lus et conservés, puis vérifiés ensemble à 06:30. Vos tâches sont ainsi prêtes avant le récap du matin. Dans Connexions, la ligne Vérifications indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’app, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiatement.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour afficher son état et **Détails**, qui ouvre Vérifications sous Connexions. Si des tâches sont ouvertes, l’option se trouve en haut de la liste sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification ayant lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Lorsqu’une nouvelle tâche est mise de côté jusqu’à un moment plus approprié, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise de côté jusqu’à demain 08:30 ».

Appuyez sur la ligne pour afficher chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche créée ou la raison pour laquelle le message n’en nécessitait pas, par exemple « Vous étiez seulement en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Appuyez sur un élément pour le lire.

Les 10 premiers éléments s’affichent. Appuyez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà affiché n’apparaît qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour comprendre le contexte et repérer les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou un avis de correction, ne sont jamais lus ni affichés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qu’il faut modifier : la façon de procéder ou, une fois le brouillon prêt, son contenu. **Marquer comme fait** indique que la tâche est traitée : cette option est visible sur une tâche prête sans brouillon, et sinon en haut de **…**, y compris pour une tâche qui nécessite votre décision. La tâche disparaît immédiatement de la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou faites-le glisser hors de l’écran avec la souris. La modification est conservée.

Pour que la tâche soit réalisée autrement, dites-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la relire](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez éventuellement indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat de la tâche, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle revient aussi automatiquement lorsqu’un nouvel événement survient, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La tâche indique alors la date de son retour et est classée comme nouvelle. Le chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche avec le montant, la date d’échéance et les modalités de paiement indiqués sur la facture. Ce n’est pas le cas des factures réglées automatiquement, comme un prélèvement automatique ou une carte enregistrée. Si un e-mail ultérieur indique que le paiement a été effectué, par exemple si l’expéditeur confirme l’avoir reçu, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement après cette heure. Elle passe dans **Fait / écarté** avec la mention « Plus nécessaire ». **Annuler** la fait réapparaître pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les conversations de groupe, et attend que Slack les ait lues. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête change de lieu ou si une réservation est annulée, The Machine met à jour ses tâches automatiquement. Une tâche qui reste pertinente suit le nouveau plan. Si elle n’a plus rien à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et précise pourquoi. **Annuler** la fait réapparaître pendant un jour.

Lors de vos premières tâches, une courte astuce vous présente les actions clés : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant d’appuyer sur **Envoyer**. L’astuce disparaît définitivement lorsque vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches. Il indique qui attend depuis le plus longtemps votre réponse. Le brouillon de cette réponse est préparé en premier pour être prêt à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, son organisation s’il y en a une (pas uniquement parce qu’elle y travaille), le projet, Travail ou Perso, et la date d’arrivée du message. Appuyez sur un nom pour ouvrir la page de cette personne dans le Graph.

Un nom ou une organisation s’affiche avec sa photo ou son logo si le Graph en a un, sinon avec ses initiales. Si un logo est illisible à cette taille, par exemple s’il est blanc sur fond transparent ou s’il s’agit d’un long nom stylisé, les initiales s’affichent également.

Une ligne discrète indique parfois les informations manquantes, par exemple « Dernier contact il y a 12 jours par e-mail, rien depuis. » Elle s’affiche lorsque votre dernier échange avec cette personne date d’un moment ou est resté sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine vous signale ce qu’elle ne sait pas au lieu de deviner.

Lorsqu’un canal non connecté est indiqué, appuyez sur Connecter à côté pour ouvrir la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec le résultat en dessous, par exemple « Terminé : Sam l’a signé mardi ».

Au-dessus du brouillon, une ligne discrète indique le message dont il provient, avec le logo du service concerné. Appuyez dessus pour lire le fil. Le brouillon affiche le logo de sa destination, pour voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon s’appuie sur une contribution envoyée ailleurs, comme une suggestion d’un collègue dans Slack, une ligne le précise, par exemple « Basé sur le message de Sam dans #ops ». Appuyez dessus pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, dans l’ordre chronologique : les messages précédant celui qui concerne la tâche, puis les réponses qui ont suivi. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’app. Le message lié à la tâche porte la mention « Cette tâche » et s’affiche dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste d’un fil d’e-mails est replié au-dessus et en dessous du message concerné.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’app Gmail si elle est installée.

Les **Détails** d’un e-mail indiquent uniquement les informations absentes de son en-tête, comme les adresses Cc complètes, les destinataires en Cci ou une autre adresse de réponse. S’il n’y a rien à ajouter, aucun détail ne s’affiche.

Une réponse dans un fil Slack affiche aussi les messages échangés avant le début du fil. Le lien d’une tâche vers le message d’origine l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste concise : le message d’origine se trouve sous **Détails**.

Une tâche en attente de quelqu’un d’autre contient un lien vers votre dernier message à cette personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet d’ajouter une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, la tâche est classée là où elle doit être, selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il date de longtemps.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », y compris dans votre langue. L’icône de calendrier propose des dates rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, de Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’icône d’appareil photo permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Appuyez sur × pour retirer un fichier.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent à créer une tâche : elle en extrait les informations d’un PDF ou d’un fichier texte. Une photo s’affiche en miniature. Appuyez dessus pour la voir en taille réelle.
