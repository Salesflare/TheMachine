---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 16f31364b3da3827
---
The Machine lit tout ce qui est nouveau et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez validée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum, et votre téléphone en est également informé.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche porte la mention **Préparée** (le travail est terminé, et **Faire** ou **Envoyer** l’exécute), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un compte rendu, sans décision à prendre).
- **En attente des autres** : les tâches pour lesquelles la prochaine étape revient à quelqu’un d’autre sont repliées (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec leur date de fin, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après votre envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lundi. » **Ouvrir** permet d’y accéder. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou dont l’échéance est demain au plus tard, puis les questions de votre Fleet, les suivis d’un tableau et enfin le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou dont l’échéance est demain au plus tard apparaissent d’abord, puis le reste, des plus récentes aux plus anciennes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais signalées comme en retard. Au bout d’un jour, elles se clôturent automatiquement. Vous pouvez alors **Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le nom affiché est celui de l’adresse utilisée, jamais celui que l’expéditeur a choisi. Votre Machine vérifie ces messages auprès de la personne à l’adresse que vous connaissez déjà, jamais auprès de leur expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple pour une révision ou une réponse, indique l’étape **En attente de**. Elle reste dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors qui doit encore répondre.

Quand une tâche concerne un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement. Vous pouvez alors **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Si personne ne touche à une tâche pendant une semaine, elle demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture. Vous pouvez alors **Annuler**. **Garder** la conserve et elle ne pose plus la question. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et son nombre n’est plus comptabilisé sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet inactif qui n’a aucune tâche ouverte peut recevoir une tâche proposant une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique, avec **Vérifier maintenant** juste en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur appliquent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, par exemple un élément qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre option : dans **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire ce récap. L’option **Copier** permet de le coller où vous voulez. Une fois ouvert ou après avoir appuyé sur son **×**, il reste affiché sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso ou uniquement pour l’option sélectionnée.

Une tâche associée à un projet affiche le nom de ce projet sous son titre. Appuyez dessus pour ouvrir le projet. **Projet**, sous **Détails**, permet de modifier ou de supprimer cette association. Voir [les tâches d’un projet](projects.md#a-project-s-to-dos).

L’option **Domaine**, sous **Détails**, permet de déplacer une tâche vers votre autre domaine. Les éléments auxquels elle peut accéder pour lire et envoyer des messages changent aussi. **Annuler** dans la note permet de la remettre à son emplacement précédent.

Quand une tâche a besoin de votre autre domaine pour avancer et que tous les messages associés s’y trouvent, elle s’y déplace et continue automatiquement. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous n’appuyez pas dessus. Une tâche que vous avez créée sans choisir Travail ou Perso se déplace automatiquement dès que son domaine est identifié. En attendant, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages qui lui sont associés. Quand elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez désignée comme Perso est considérée comme Perso. Les e-mails concernant une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche liée à votre vie personnelle, comme un message de votre famille reçu sur votre adresse professionnelle, est considérée comme Perso dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un message d’un client sur WhatsApp ou une commande dans votre boîte mail personnelle, est considéré comme Travail dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche Perso de ce type répond tout de même depuis l’adresse professionnelle qui a reçu son e-mail et n’apparaît jamais dans une Fleet Travail ni dans le Graph de l’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec chaque brouillon complet et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est pas incluse dans ce parcours : elle attend votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le message le plus ancien d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis traités ensemble à 06:30, afin que vos tâches soient prêtes avant le récap du matin. La section Vérifications, sous Connexions, indique « Suspendues pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous absentiez pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour afficher son état et **Détails**, qui ouvre la section Vérifications, sous Connexions. Si des tâches sont ouvertes, cette option se trouve en haut de la page sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Quand une nouvelle tâche attend un moment plus approprié, par exemple le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Appuyez sur la ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a trouvé qu’une imprécise. Appuyez sur un élément pour le lire.

Les 10 premiers éléments s’affichent. Appuyez en dessous pour voir les suivants. Le nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos réponses sont lues pour comprendre le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou un avis de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche l’étape suivante, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser quoi changer : la manière de procéder ou, une fois un brouillon prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée. Cette option est visible sur une tâche prête sans brouillon, sinon en haut du menu **…**, y compris pour une tâche qui nécessite votre décision. Elle disparaît immédiatement de la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou faites-le glisser hors de l’écran avec la souris pour le fermer plus vite. La modification est conservée.

Pour que la tâche soit effectuée autrement, dites-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la vérifier](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom**, sous **Détails**, pour le modifier. Le titre que vous choisissez est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle réapparaît également automatiquement en cas de nouvel événement, comme un nouveau message de cette personne, mais pas si vous répondez vous-même. Elle indique alors la date de son retour et apparaît parmi les nouvelles tâches. Le chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche qui indique le montant, l’échéance et les modalités de paiement figurant sur la facture. Les factures payées automatiquement, par prélèvement ou avec une carte enregistrée par exemple, ne deviennent pas des tâches. Quand un e-mail ultérieur confirme le paiement, par exemple si l’expéditeur indique l’avoir reçu, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement une fois cette heure passée. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit marqué comme prêt, votre Machine vérifie les discussions récentes que vous avez eues avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si une personne a été sollicitée et a répondu oui, elle se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Quand un message plus récent modifie le plan, par exemple si une fête est déplacée ou une réservation annulée, The Machine met elle-même à jour ses tâches. Une tâche toujours utile s’adapte au nouveau plan. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » suivi de la raison, et **Annuler** permet de la rétablir pendant un jour.

Pour vos premières tâches, un court conseil présente les actions principales : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**. Le conseil disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est rédigée en premier, pour être prête dès votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique les personnes concernées, l’organisation s’il y en a une (pas uniquement parce qu’une personne y travaille), le projet, Travail ou Perso, et la date de création. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Les personnes et les organisations sont représentées par leur photo ou leur logo si le Graph en contient un, et par leurs initiales dans le cas contraire. Un logo illisible à cette taille, par exemple un logo blanc sur fond transparent ou un long nom stylisé, est également remplacé par une initiale.

Une ligne discrète indique parfois ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail, aucun échange depuis ». Elle apparaît quand le dernier échange est ancien ou sans réponse, et mentionne les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Quand un canal non connecté est mentionné, l’option Se connecter à côté ouvre la connexion correspondante.

Un titre décrit ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la façon dont elle s’est conclue en dessous, par exemple « Terminé : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique de quel message il provient, avec le logo du service concerné. Appuyez dessus pour lire le fil de discussion. Le brouillon affiche le logo du service auquel il sera envoyé. Vous voyez ainsi immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Quand le brouillon s’appuie sur une suggestion faite ailleurs, par exemple celle d’un collègue dans Slack, une ligne l’indique, par exemple « D’après Sam dans #ops ». Appuyez dessus pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, du plus ancien au plus récent : les messages précédant celui auquel la tâche se rapporte, puis les réponses. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute des messages plus anciens. Pour un e-mail, le reste du fil est replié au-dessus et au-dessous.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en copie, les adresses en copie cachée ou une autre adresse de réponse. Si rien n’est à ajouter, cette section est vide.

Une réponse dans un fil Slack affiche aussi les messages publiés avant le début du fil. Le lien d’une tâche vers le message d’origine l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste compacte : son message d’origine se trouve sous **Détails**.

Une tâche « En attente de » renvoie vers votre dernier message à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, elle est classée dans le domaine approprié selon les personnes concernées et le sujet. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : indiquez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue également. L’icône du calendrier propose des dates rapides et l’option **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : ajoutez le message concerné, qu’il s’agisse d’un e-mail, Slack, Teams, WhatsApp, Telegram ou de tout autre message auquel The Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo situé à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × permet d’en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit quand elle s’en occupe. Vous pouvez ajouter uniquement des fichiers : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo apparaît en petit format. Appuyez dessus pour l’afficher en taille réelle.
