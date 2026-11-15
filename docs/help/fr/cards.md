---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Découvrez les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 81b65d513aa5941b
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement si quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme l’envoi d’un formulaire ou la résolution d’un problème, a été effectuée pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum, et votre téléphone en est également informé.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche indique **Préparée** (le travail est fait, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (elle nécessite d’abord votre décision ou une réponse), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **En attente des autres** : les tâches repliées dont la prochaine étape incombe à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». **Ouvrir** vous y conduit. La recherche permet de trouver une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou à échéance d’ici demain, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche conserve sa place pendant que votre Machine la prépare et quand elle est terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain apparaissent en premier, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore fermée. **Rouvrir** la remet dans votre liste et votre Machine en tire des enseignements. Ces tâches ne sont jamais indiquées comme en retard. Après un jour, elles se ferment automatiquement, avec **Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi automatiquement.

Lorsqu’un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne est affichée avec sa propre adresse, jamais avec le nom qu’elle a utilisé. Votre Machine vérifie le message auprès de la personne à l’adresse que vous connaissez déjà, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une relecture ou une réponse, indique l’étape concernée avec **En attente de**. Elle reste dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question en retour : la tâche revient le matin précédant son échéance, le jour de l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors toujours qui doit répondre.

Lorsqu’une tâche dépend d’un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne ferme pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se ferme automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Si personne ne s’occupe d’une tâche pendant une semaine, elle demande une seule fois : **Toujours utile ?** **Pas nécessaire** la ferme, avec **Annuler**. **Garder** la conserve, et elle ne posera plus la question. Si vous ne répondez pas pendant une semaine de plus, elle est repliée dans Revient plus tard et n’est plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. Ouvrez-la, envoyez un message dans le chat, modifiez-la, mettez-la en attente ou attendez un nouveau message pour la faire réapparaître.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique et affiche **Vérifier maintenant** en dessous.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur affichent le même filtre. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, par exemple un composant qui redémarre sans cesse, n’est ni Travail ni Perso et s’affiche uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et le nombre d’éléments qu’il contient, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Touchez-la pour relire ce récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou que vous touchez son **×**, il reste disponible sur tous vos appareils jusqu’au récap suivant.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste ouvert, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de le retirer. Voir [les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche dans votre autre domaine. Les messages qu’elle peut lire et envoyer changent avec elle. **Annuler** dans la note la remet à sa place.

Lorsqu’une tâche doit passer dans votre autre domaine et que tous les messages concernés s’y trouvent, elle s’y déplace automatiquement et continue. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge tant que vous ne l’avez pas touchée. Une tâche que vous avez créée sans choisir Travail ou Perso se déplace automatiquement dès qu’elle trouve sa place. En attendant, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un membre de votre famille qui écrit à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous arrive sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte de réception personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, jamais où elle répond : la réponse est toujours envoyée là où se trouve la conversation, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et n’apparaît jamais dans une Fleet professionnelle ni dans le Graph de l’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les parcourir une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est pas incluse : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le message le plus ancien d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités à la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont tout de même lus et conservés, puis vérifiés ensemble à 06:30, afin que vos tâches soient prêtes avant votre récap du matin. Dans Connexions, Vérifications indique « Suspendues pour la nuit, rattrapage à 06:30 ». Si vous ouvrez l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour l’afficher avec **Détails**, qui ouvre Vérifications sous Connexions. S’il y a des tâches ouvertes, l’option se trouve en haut de la liste sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Lorsqu’une nouvelle tâche est gardée pour un moment plus opportun, par exemple votre récap du matin, la ligne indique jusqu’à quand : « 1 tâche gardée jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle rien n’était nécessaire, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Aucun motif n’est affiché pour un fil si la vérification n’a donné qu’une raison vague. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez en dessous pour afficher le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié ne s’affiche qu’une seule fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour leur contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche la prochaine étape, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** indique ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, les éléments à modifier. **Marquer comme fait** signifie que la tâche est traitée : cette option est visible sur une tâche prête sans brouillon, sinon en haut de **…**, y compris pour une tâche qui nécessite votre décision. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Balayez le message pour le faire disparaître ou, avec une souris, faites-le glisser pour le fermer plus vite. La modification est conservée.

Pour procéder autrement, dites-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la relire](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une fréquence définie](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez éventuellement indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour renommer la tâche. Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche fermée. Elle réapparaît également automatiquement si quelque chose de nouveau se produit, par exemple si la personne vous envoie un nouveau message, mais pas si vous lui répondez.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, l’échéance et les modalités de paiement figurant sur la facture. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple si l’expéditeur confirme avoir reçu votre règlement, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’est utile que jusqu’à un moment donné, comme une confirmation à envoyer avant une réunion, se ferme automatiquement après ce moment. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos discussions récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Lorsqu’un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a accepté, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant un jour.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête change de lieu ou si une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche toujours utile suit le nouveau plan. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire », son chat indique « Mise à jour : » et la raison, et **Annuler** permet de la rétablir pendant un jour.

Lors de vos premières tâches, une courte astuce présente les actions clés : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. Une astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue en haut de Tâches indique le nom de la personne qui attend votre réponse depuis le plus longtemps. Le brouillon de cette réponse est préparé en premier pour être prêt à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation s’il y en a une (pas simplement parce que quelqu’un y travaille), le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom et une organisation affichent leur photo ou leur logo si le Graph en a un, et leurs initiales dans le cas contraire. Un logo difficile à lire à cette taille, par exemple blanc sur fond transparent ou sous la forme d’un long nom, est également remplacé par l’initiale.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis. » Elle s’affiche lorsque votre dernier échange avec la personne remonte à longtemps ou est resté sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de deviner.

Si la ligne mentionne un canal qui n’est pas connecté, l’option **Connecter** à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre et indique en dessous comment elle s’est terminée, par exemple « Terminé : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique le message d’origine, avec le logo du service concerné. Touchez-la pour lire le fil. Le brouillon affiche le logo du service auquel il est destiné, pour que vous voyiez tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte des informations d’une personne ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « Selon Sam dans #ops ». Touchez-la pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, de la plus ancienne à la plus récente : les messages précédant celui dont parle la tâche, puis les réponses qui l’ont suivi. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste d’un fil d’e-mails est replié au-dessus et en dessous du message concerné.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, en Cci ou une adresse de réponse différente. Si rien n’est à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche également les messages envoyés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre aussi ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche son nom, son projet et son domaine (touchez l’un de ces éléments pour le modifier), votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste concise : le message d’origine se trouve sous **Détails**.

Une tâche en attente de quelqu’un d’autre contient un lien vers votre dernier message envoyé à cette personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche vous-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, la tâche est classée selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue également. L’icône du calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient selon une fréquence définie. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message disponible dans The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’icône d’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour retirer un fichier.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Les fichiers seuls suffisent : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour la voir en taille réelle.
