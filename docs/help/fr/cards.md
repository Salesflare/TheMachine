---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à recevoir votre validation. Découvrez la signification des différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Votre Machine lit toutes les nouveautés et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe ainsi :

- **Pour vous** : tout ce qui attend votre réponse, en commençant par le plus urgent. Chaque tâche indique **Préparée** (le travail est terminé, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (une décision ou une réponse de votre part est d’abord nécessaire) ou **En préparation…** (votre Machine s’en occupe).
- **Tout juste fait** : une dernière étape que vous avez confirmée, comme un formulaire ou un ticket, a été effectuée pendant votre absence. Elle reste affichée jusqu’à ce que vous appuyiez sur **Compris**, pendant une journée au maximum, et vous recevez aussi une notification sur votre téléphone.
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec leur date de fin, comme « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après l’envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lundi. » **Ouvrir** vous y conduit. La recherche permet de trouver une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les questions de votre Fleet, puis le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les autres de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, comme « PR #3451 fusionnée », mais qu’elle n’est pas encore close. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais considérées comme en retard. Au bout d’une journée, elles se ferment automatiquement, avec **Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi automatiquement.

Lorsqu’un message provient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Cette personne n’est pas Sam Lee. » Elle affiche cette personne sous sa véritable adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie le message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son expéditeur.

Une tâche qui attend encore quelqu’un d’autre, comme une relecture ou une réponse, indique l’étape **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si elle est déjà passée. Elle indique alors la personne dont elle attend toujours une réponse.

Lorsqu’une tâche porte sur un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se ferme automatiquement, avec **Annuler**. Si vous n’avez toujours pas reçu de réponse au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche à laquelle personne n’a touché pendant une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôt, avec **Annuler**. **Garder** la conserve, et elle ne vous le demandera plus. Sans réponse pendant une semaine supplémentaire, elle se replie dans Revient plus tard, et elle n’est plus comptabilisée sur l’icône de l’application ni dans le récap du matin. Si vous l’ouvrez, lui envoyez un message dans le chat, la modifiez, la mettez en attente ou recevez un nouveau message, elle réapparaît.

Une fois par semaine, un projet qui n’a plus donné de nouvelles et ne comporte aucune tâche ouverte peut générer une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et laisse la liste vide. Pendant une vérification, elle se réveille et vous l’indique. Si une vérification a échoué ou a pris du retard, la ligne vous le signale, avec **Vérifier maintenant** juste en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’un type donné. Votre téléphone et votre ordinateur utilisent le même filtre. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, par exemple un composant qui ne cesse de redémarrer, n’est ni Travail ni Perso : elle apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : **Perso uniquement · Travail · Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et le nombre d’éléments comptabilisés, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Appuyez dessus pour relire ce récap, puis sur **Copier** pour le coller où vous voulez. Une fois ouvert ou après avoir appuyé sur son **×**, il reste affiché sur tous vos appareils jusqu’au prochain récap.

Si aucun récap récent n’est disponible, la ligne indique **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche liée à un projet affiche le nom de celui-ci sous son titre. Appuyez dessus pour ouvrir le projet. **Projet** sous **Détails** permet de modifier le projet ou de retirer la tâche du projet. Voir [les tâches d’un projet](projects.md#a-projects-to-dos).

**Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les sources que la tâche peut lire et utiliser pour envoyer des messages la suivent. **Annuler** dans la notification la remet à son emplacement précédent.

Lorsqu’une tâche a besoin de votre autre domaine pour avancer et que les messages dont elle provient s’y trouvent tous, elle s’y déplace et continue automatiquement. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous n’appuyez pas dessus. Une tâche que vous avez ajoutée sans choisir Travail ou Perso se déplace automatiquement une fois son domaine déterminé. En attendant, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez définie comme Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est considérée comme personnelle dès le départ.

Le travail qui vous arrive sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte mail personnelle, est considéré comme professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée là où se trouve la conversation, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et n’apparaît jamais dans un Fleet professionnel ni dans le Graph de l’équipe.

Quand plusieurs tâches sont en attente, **Passer en revue** dans l’en-tête de Pour vous vous les présente une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question est exclue de ce parcours : elle attend votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès que 40 messages sont en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont en pause : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant votre récap du matin. Dans Connexions, la ligne des vérifications indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous ouvrez l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre la page Vérifications sous Connexions. Si des tâches sont ouvertes, cette option se trouve en haut de la page sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou a pris du retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Si une nouvelle tâche attend un moment plus opportun, comme votre récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Appuyez sur la ligne pour voir chaque fil d’e-mail, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, puis la nouvelle tâche ou la raison pour laquelle le message n’en a pas nécessité, par exemple « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une de vague. Appuyez sur un élément pour le lire.

Les 10 premiers éléments s’affichent. Appuyez sous la liste pour afficher le reste. Le nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour tenir compte du contexte et des promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails envoyés par The Machine, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre essai ou une invitation sont lus normalement.

## Les boutons

Une tâche indique l’étape suivante, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser quoi changer : la façon de procéder ou, lorsqu’un brouillon est prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : l’option est visible sur une tâche prête sans brouillon, sinon elle se trouve en haut du menu **…**, y compris pour une tâche qui attend votre décision. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Faites disparaître le message d’un balayage ou faites-le glisser hors de l’écran avec la souris pour le fermer plus vite. La modification est conservée.

Pour que la tâche soit effectuée autrement, indiquez-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la relire](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez aussi indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour renommer la tâche. Le titre que vous choisissez est conservé.

**Rouvrir** réaffiche une tâche close. Elle réapparaît aussi automatiquement lorsqu’un nouvel événement se produit, par exemple un nouveau message de la personne, mais pas lorsque vous lui répondez.

Une facture que vous devez régler vous-même, quel que soit le pays, devient une tâche qui indique le montant, la date d’échéance et les informations de paiement fournies. Les factures réglées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur indique que la facture est payée, par exemple si l’expéditeur confirme avoir reçu votre paiement, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant une journée.

Une tâche qui n’est utile que jusqu’à un moment précis, comme une confirmation à obtenir avant une réunion, se ferme automatiquement après ce moment. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant une journée.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos échanges récents avec les personnes concernées, y compris dans les discussions de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la demande a été faite et acceptée, elle se ferme automatiquement. **Annuler** permet de la rétablir pendant une journée.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête est déplacée dans un autre lieu ou si une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche qui reste pertinente suit le nouveau plan. Si plus rien n’est à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire », son chat indique « Mis à jour : » suivi de la raison, et **Annuler** permet de la rétablir pendant une journée.

Lors de vos premières tâches, une courte astuce vous présente les actions essentielles : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**. Une astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier, pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique qui est concerné, l’organisation si la tâche porte sur une organisation (et non simplement parce que la personne y travaille), le projet, Travail ou Perso, ainsi que la date d’arrivée. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en possède un, et leurs initiales dans le cas contraire. Si un logo est illisible à cette taille, par exemple un logo blanc sur fond transparent ou un nom de marque très large, les initiales s’affichent aussi.

Une ligne discrète indique parfois ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail ; aucun échange depuis ». Elle s’affiche si le dernier échange avec la personne est ancien ou sans réponse, et mentionne les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est mentionné, **Connecter** à côté permet d’établir la connexion.

Le titre indique ce qu’il faut faire et ne change que si cela change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Fait : Sam l’a signé mardi ».

Une ligne en gris clair au-dessus du brouillon indique le message dont il provient, avec le logo du service correspondant. Appuyez dessus pour lire le fil. Le brouillon affiche le logo de sa destination, pour voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon reprend une suggestion reçue ailleurs, par exemple celle d’un collègue dans Slack, une ligne l’indique, comme « Basé sur le message de Sam dans #ops ». Appuyez dessus pour lire le message.

Une conversation de chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche d’un seul tenant, de la plus ancienne à la plus récente : les messages précédant celui auquel la tâche se rapporte, puis les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Les autres messages d’un fil d’e-mail sont repliés au-dessus et en dessous du message concerné.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en copie, les destinataires en copie cachée ou une autre adresse de réponse. Si aucune information ne manque, la section ne s’affiche pas.

Une réponse dans un fil Slack affiche aussi les messages qui précèdent le début du fil. Le lien d’une tâche vers son propre message l’ouvre aussi ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom de la tâche, son projet et son domaine (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. **Chat ›** ouvre le chat. Une tâche terminée reste concise : son message d’origine se trouve sous **Détails**.

Une tâche indiquant « En attente de » contient un lien vers votre dernier message envoyé à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur) permet d’ajouter une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne choisissez ni Travail ni Perso, la tâche est classée au bon endroit selon la personne et le sujet. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez une date ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue. L’icône du calendrier propose des dates rapides et l’option **Choisir une date**.
- **Message** : joignez le message concerné : un e-mail, un message Slack, Teams, WhatsApp, Telegram ou tout autre message auquel The Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Appuyez sur × pour en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Les fichiers seuls suffisent : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en miniature : appuyez dessus pour la voir en taille réelle.
