---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Découvrez ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 6cbbad37c4dfaf07
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, vous retrouvez une dernière étape que vous avez validée, comme un formulaire ou un ticket, et qui a été effectuée pendant votre absence. Elle reste là jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum, et votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par le plus urgent. Chaque tâche indique **Préparée** (le travail est fait, et **Faire** ou **Envoyer** permet de le terminer), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part), **En préparation…** (votre Machine est en train de s’en occuper) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **En attente des autres** : les tâches repliées dont la prochaine étape revient à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : vos promesses et celles des autres envers vous. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec leur date de fin, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées sont marquées **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». **Ouvrir** vous y conduit. La recherche retrouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou à échéance demain au plus tard, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque catégorie, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les autres de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et votre Machine en tire des enseignements. Ces tâches ne sont jamais indiquées comme étant en retard. Après un jour, elles se clôturent automatiquement, avec **Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Si un message vient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne est affichée sous sa propre adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son auteur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une vérification ou une réponse, indique l’étape **En attente de**. Elle reste dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si elle est déjà passée. Elle indique alors la personne dont la réponse est toujours attendue.

Quand une tâche concerne un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si vous n’avez rien reçu au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Si personne n’a touché à une tâche pendant une semaine, elle demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve, sans jamais reposer la question. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et elle n’est plus comptabilisée sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté sans activité et sans tâche ouverte peut générer une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et votre liste reste vide. Pendant ses vérifications, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, elle l’indique, avec **Vérifier maintenant** juste en dessous.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’une catégorie. Votre téléphone et votre ordinateur conservent le même choix. Quand Travail ou Perso est activé, **Tout afficher** permet de revenir à l’affichage complet. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : sous **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Appuyez dessus pour relire ce récap, ou sur **Copier** pour le coller où vous voulez. Une fois ouvert ou fermé avec son **×**, il reste affiché sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est toujours en cours, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche liée à un projet affiche le nom du projet sous son titre. Appuyez dessus pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de retirer la tâche du projet. Voir [les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les messages auxquels elle peut accéder pour les lire et y répondre sont déplacés avec elle. **Annuler** dans le message permet de la remettre à sa place.

Quand une tâche a besoin de votre autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et continue. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous n’avez pas appuyé dessus. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement une fois que son domaine est identifié. En attendant, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte professionnelle que vous avez étiquetée Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, par exemple un message d’un proche envoyé à votre adresse professionnelle, est considérée comme personnelle dès le départ.

Le travail qui arrive sur un compte personnel, par exemple un message d’un client sur WhatsApp ou une commande dans votre boîte personnelle, est considéré comme professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre option.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et elle n’apparaît jamais dans une Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les parcourir une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie le contenu affiché, `S` le met en attente, `→` passe à la tâche suivante et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est pas incluse : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le plus ancien message d’une personne est en attente depuis 15 minutes. Les newsletters, notifications et reçus sont pris en compte lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Sous Connexions, la section Vérifications affiche « En pause pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous soyez absenté pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour afficher son état et **Détails**, qui ouvre les vérifications sous Connexions. S’il y a des tâches ouvertes, cette option se trouve en haut sur ordinateur. Une courte ligne n’apparaît que pendant une vérification ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare gardent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Si une nouvelle tâche attend le bon moment, par exemple le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Appuyez sur cette ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : son auteur, son objet ou ses premiers mots, ainsi que la nouvelle tâche associée ou la raison pour laquelle aucune tâche n’était nécessaire, par exemple « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a trouvé qu’une de vague. Appuyez sur un élément pour le lire.

Les 10 premiers éléments s’affichent, et un appui en dessous permet d’afficher le reste. Le nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour leur contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou un avis de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche la prochaine étape, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** juste à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** précise ce qu’il faut changer : la manière de s’y prendre ou, une fois le brouillon prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : l’option est visible sur une tâche prête sans brouillon, sinon elle se trouve en haut du menu **…**, y compris pour les tâches qui attendent votre décision. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou faites-le glisser hors de l’écran avec la souris pour le fermer plus vite. Cette action est conservée.

Pour que la tâche soit faite autrement, dites-le dans son **Chat**.

Dans le menu **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la vérifier](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez aussi préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour renommer la tâche. Votre titre est conservé.

**Rouvrir** réactive une tâche clôturée. Elle peut aussi réapparaître automatiquement quand quelque chose de nouveau se produit, par exemple si la personne vous envoie un nouveau message, mais pas après votre propre réponse.

Une facture que vous devez encore régler vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les détails de paiement fournis sur la facture. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Quand un e-mail ultérieur confirme le paiement, par exemple lorsque l’expéditeur confirme avoir reçu votre règlement, la tâche se clôture automatiquement. **Annuler** la réactive pendant un jour.

Une tâche qui n’a d’utilité que jusqu’à une heure définie, par exemple une confirmation à envoyer avant une réunion, se clôture automatiquement après cette heure. Elle est déplacée dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la réactive pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lus. Si un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** la réactive pendant un jour.

Quand un message plus récent modifie le plan, par exemple si une fête a lieu dans un autre endroit ou si une réservation est annulée, The Machine met à jour ses tâches automatiquement. Une tâche qui reste utile tient compte du nouveau plan. Si rien ne reste à faire, elle est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire », son chat indique « Mis à jour : » et explique pourquoi. **Annuler** la réactive pendant un jour.

Lors de vos premières tâches, un bref conseil vous présente les actions principales : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. Un conseil disparaît définitivement dès que vous utilisez le bouton correspondant ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation si la tâche en concerne une (et non simplement parce que quelqu’un y travaille), le projet, Travail ou Perso, et la date de réception. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations sont accompagnés de leur photo ou de leur logo si le Graph en a un, sinon de leurs initiales. Si le logo est difficile à lire en petit, par exemple s’il est blanc sur un fond transparent ou s’il s’agit d’un mot-symbole horizontal, les initiales s’affichent aussi.

Une ligne discrète indique parfois ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail, rien depuis ». Elle apparaît si le dernier échange est ancien ou sans réponse, et indique les canaux non connectés, comme WhatsApp. Votre Machine précise ce qu’elle ne sait pas au lieu de faire des suppositions.

Si la ligne mentionne un canal qui n’est pas connecté, l’option Connecter juste à côté permet d’établir la connexion.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée garde son titre, avec la façon dont elle s’est terminée juste en dessous, par exemple « Terminé : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique de quel message il provient, avec le logo du service concerné. Appuyez dessus pour lire le fil. Le brouillon affiche le logo du service auquel il est destiné, pour voir tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de la contribution d’une personne ailleurs, par exemple d’une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « D’après Sam dans #ops ». Appuyez dessus pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une conversation, de la plus ancienne à la plus récente : les messages précédant celui dont traite la tâche, puis les réponses suivantes. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’application. Le message associé à la tâche est marqué « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste du fil d’un e-mail est replié au-dessus et en dessous du message concerné.

Les **Détails** d’un e-mail indiquent uniquement les informations absentes de son en-tête, comme les adresses complètes en copie, les destinataires en copie cachée ou une autre adresse de réponse. Si rien n’est à ajouter, cette section est absente.

Une réponse dans un fil Slack affiche aussi les messages envoyés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste compacte, et le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » comporte un lien vers votre dernier message à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quoi. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il date de longtemps.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue. L’icône du calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son auteur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo juste à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Appuyez sur × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit quand elle s’en occupe. Vous pouvez ajouter uniquement des fichiers : The Machine crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en miniature. Appuyez dessus pour la voir en taille réelle.
