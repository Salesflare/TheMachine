---
title: Tâches
area: cards
summary: Une tâche par sujet qui nécessite votre attention, prête à être validée. Découvrez les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: f77d6b07f6f94ce5
---
Votre Machine lit tous les nouveaux messages et ne crée une tâche que si quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum. Votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par ce qui arrive à échéance d’ici demain. Chaque tâche porte l’une de ces mentions : **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (une décision ou une réponse est nécessaire ; si le travail ne peut pas continuer ou être utilisé sans une information que vous seul avez, comme un prix, un fait ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches sans nouveauté depuis une semaine sont regroupées ici (voir ci-dessous).
- **En attente des autres** : les tâches dont la prochaine étape revient à quelqu’un d’autre sont regroupées ici (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, les messages qui [partiront plus tard](send-later.md) et celles restées sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche conservée. » **Ouvrir** vous y mène. La recherche permet de retrouver une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, suivies des questions de votre Fleet, des suivis d’un tableau, puis du reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant sa préparation et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, puis les autres de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais signalées en retard. Si un message en fait état, la tâche se clôture automatiquement au bout d’un jour, avec **Annuler**. Sinon, elle attend que vous appuyiez sur **Marquer comme fait**.

Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture elle aussi automatiquement. Une réponse qui indique qu’un fichier est joint alors qu’il ne l’est pas ne clôture pas la tâche.

Lorsqu’un message vient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example pour sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » L’expéditeur est présenté avec sa propre adresse, jamais avec le nom qu’il a utilisé. Votre Machine vérifie le message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son expéditeur.

Une tâche qui attend encore quelqu’un d’autre, par exemple une relecture ou une réponse, indique l’étape concernée sous **En attente de**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si elle est passée. Elle indique alors qui doit encore répondre.

Lorsqu’une tâche dépend d’un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** indique ce résultat sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les tâches récentes s’affichent en premier après quelques jours d’absence. Il n’y a pas de nouveauté s’il n’y a aucun nouveau message à son sujet ni aucune action de votre part, comme un message dans le chat, une modification ou une mise en attente. La consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme inutiles toutes les tâches de Plus anciennes après une seule confirmation, comme le fait **Pas nécessaire** pour chacune d’elles, avec **Annuler**. Une nouveauté sur l’une d’elles la fait revenir dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve et elle ne vous le demandera plus. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard. Le nombre sur l’icône de l’application et le récap du matin ne la comptent alors plus. Ouvrir la tâche, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique, avec **Vérifier maintenant** en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou un seul type. Votre téléphone et votre ordinateur utilisent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à toutes les tâches. Une alerte concernant votre Machine, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso. Elle s’affiche uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre choix : sous **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptabilisait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire le récap, puis sur **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou que vous appuyez sur son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche liée à un projet affiche le nom du projet sous son titre. Appuyez dessus pour ouvrir le projet. **Projet**, sous **Détails**, permet de modifier le projet ou de retirer la tâche du projet. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, sous **Détails**, déplace une tâche vers votre autre domaine. Les sources qu’elle peut lire et utiliser pour envoyer des messages sont déplacées avec elle. **Annuler**, dans la note, la remet à sa place.

Lorsqu’une tâche a besoin de votre autre domaine pour continuer et que tous les messages dont elle provient s’y trouvent, elle s’y déplace et continue automatiquement. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous n’appuyez pas dessus. Une tâche que vous avez ajoutée sans choisir Travail ou Perso se déplace automatiquement dès qu’elle trouve sa place. D’ici là, elle n’apparaît ni dans Travail ni dans Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Lorsqu’elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez désignée comme Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche liée à votre vie personnelle, comme un message d’un membre de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte mail personnelle ou une [promesse](promises.md) liée au travail, est professionnel dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où une tâche s’affiche et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` passe la tâche et Échap arrête le processus. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, le récapitulatif indique le nombre de tâches envoyées ou clôturées, ainsi que celles qui sont encore en préparation.

Une tâche qui vous pose une question n’est pas incluse : elle attend votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le plus ancien message d’une personne est en attente depuis 15 minutes. Les newsletters, notifications et reçus sont inclus lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont quand même lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant votre récapitulatif du matin. Dans Connexions, la section Vérifications indique « Suspendues pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous absentiez pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre Vérifications dans Connexions. S’il y a des tâches ouvertes, l’option se trouve en haut sur ordinateur. Une courte ligne s’affiche à cet endroit uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare gardent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle ne concerne que cette vérification : les tâches déjà dans votre liste restent telles quelles. Lorsqu’une nouvelle tâche attend un meilleur moment, comme votre récapitulatif du matin, la ligne indique jusqu’à quand : « 1 tâche reportée à demain, 08:30 ».

Appuyez sur la ligne pour afficher chaque fil d’e-mails, chat et notification, accompagné de l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, et la tâche créée ou la raison pour laquelle aucun suivi n’était nécessaire, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Si la vérification n’a donné qu’une raison vague, aucun motif n’est affiché pour un fil. Appuyez sur un élément pour le lire, ainsi que les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Appuyez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà dans la liste ne s’affiche qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que votre Machine vous envoie, comme votre récapitulatif du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qu’il faut changer : la façon de faire, ou, une fois le brouillon prêt, les modifications à y apporter. Si vous laissez votre texte inachevé, vous le retrouverez à votre retour. **Annuler** l’efface.

**Marquer comme fait** signifie que la tâche est traitée. L’option est visible pour une tâche prête sans brouillon ou une tâche qui vous pose une question ; sinon, elle se trouve en haut du menu **…**. La tâche quitte aussitôt la liste, et **Annuler** apparaît dans le message. Faites glisser le message pour le supprimer ou déplacez-le avec la souris pour le clôturer plus tôt. La modification est conservée.

Pour que la tâche soit faite autrement, indiquez-le dans son **Chat**. La réponse précise uniquement ce qui a changé, par exemple une mise en attente et sa durée. Si une modification n’a pas pu être effectuée, comme un changement d’échéance, la réponse vous l’indique.

Dans **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une relecture](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom**, sous **Détails**, pour le modifier. Vous pouvez aussi le demander dans le chat, par exemple : « Renomme-la en… ». Le titre que vous choisissez est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle réapparaît aussi automatiquement en cas de nouveauté, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La date de son retour s’affiche et elle est triée comme une nouvelle tâche. Le chat reprend là où il en était, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche qui indique le montant, l’échéance et les informations de paiement figurant sur la facture. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple une confirmation de réception de votre règlement envoyée par l’expéditeur, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à recevoir avant une réunion, se clôture automatiquement une fois cette heure passée. Elle est déplacée dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la fait réapparaître pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un apparaisse comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche a déjà été faite, par exemple si une personne a reçu une demande et a répondu oui, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message, avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête est déplacée dans un autre lieu ou si une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche toujours nécessaire suit le nouveau plan. Si elle n’a plus rien à faire, elle est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et la raison. **Annuler** la fait réapparaître pendant un jour.

Lors de vos premières tâches, un court conseil présente les actions principales : **Demander des modifications** et **Pas nécessaire**. Il rappelle aussi que rien n’est envoyé tant que vous n’avez pas appuyé sur **Envoyer**. Le conseil disparaît définitivement dès que vous utilisez le bouton correspondant ou que vous appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique depuis combien de temps une personne attend votre réponse. Cette réponse est rédigée en premier, pour qu’elle soit prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation lorsqu’il y en a une (pas seulement parce que la personne y travaille), le projet, Travail ou Perso, et la date de réception. Appuyez sur un nom pour ouvrir la page de cette personne dans le Graph.

Le nom d’une personne ou d’une organisation s’accompagne de sa photo ou de son logo si le Graph en a un, et de ses initiales dans le cas contraire. Si un logo est illisible en petit, par exemple s’il est blanc sur fond transparent ou s’il s’agit d’un long nom stylisé, l’initiale s’affiche aussi.

Une discrète ligne peut indiquer une information inconnue, par exemple « Dernier contact par e-mail il y a 12 jours, aucun échange depuis ». Elle s’affiche si le dernier échange avec cette personne est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est mentionné, appuyez sur Connecter à côté de son nom pour ouvrir sa connexion.

Le titre indique ce qu’il faut faire et ne change que si cette action change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Fait : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service concerné. Appuyez dessus pour lire le fil. Le brouillon affiche le logo du service auquel il sera envoyé : vous voyez ainsi tout de suite s’il s’agit d’une réponse dans Slack ou d’un e-mail.

Si le brouillon s’appuie sur l’intervention d’une personne ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « Selon Sam dans #ops ». Appuyez dessus pour lire le message. Cette ligne disparaît lorsqu’une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous la forme d’une seule conversation, de la plus ancienne à la plus récente : les messages précédant celui dont parle la tâche, puis les réponses qui ont suivi. Dans WhatsApp, Telegram ou Signal, vos messages sont affichés à droite, comme dans l’application. Le message lié à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification. Il porte la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si vous l’avez installée.

Les **Détails** d’un e-mail affichent uniquement les informations qui ne figurent pas dans son en-tête, comme les adresses complètes en Cc, les destinataires en Cci ou une autre adresse de réponse. S’il n’y a rien à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages échangés avant le début du fil. Le lien d’une tâche vers le message correspondant l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Appuyez sur le titre pour ouvrir le chat. Les tâches terminées restent compactes ; le message dont elles proviennent se trouve sous **Détails**.

Une tâche « En attente de » contient un lien vers votre dernier message à la personne, celui auquel vous attendez une réponse : « E-mail à Pat · mar. »

## Créer une tâche soi-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. La création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée là où elle doit être, selon les personnes et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

Si vous fermez la fenêtre avant d’ajouter la tâche, votre texte et vos choix seront conservés la prochaine fois, mais pas les fichiers. Appuyez sur **Supprimer** dans le message pour les effacer.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures ». Vous pouvez aussi le faire dans votre langue. L’icône de calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message auquel The Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Appuyez sur × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent à créer une tâche : les informations sont extraites d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Appuyez dessus pour l’agrandir.
