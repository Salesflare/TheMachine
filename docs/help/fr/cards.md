---
title: Tâches
area: cards
summary: Une tâche par chose qui a besoin de vous, prête pour votre accord. Ce que veulent dire les parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Votre Machine lit tout ce qui est nouveau et ne crée une tâche que si quelque chose a besoin de vous. Une tâche par sujet, peu importe le nombre de messages.

## Où sont les tâches

La page **Tâches** les regroupe :

- **Pour vous** : tout ce qui vous attend, le plus urgent d’abord. Chaque tâche indique **Préparée** (le travail est fait, et **Faire** ou **Envoyer** s’en charge) **Vous attend** (il faut d’abord votre décision ou une réponse) ou **En préparation…** (votre Machine y travaille).
- **Tout juste fait** : une dernière étape que tu as confirmée, comme envoyer un formulaire ou créer un ticket, a réussi pendant ton absence. Elle montre ce qui s'est passé jusqu'à ce que tu touches **Compris**, un jour au plus, et ton téléphone l'apprend aussi. Ensuite, elle n'est plus que dans Fait.
- **Revient plus tard** : mise en attente, et les tâches sans réponse à **Toujours utile ?** (plus bas).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, selon le moment où elles l’ont été, les plus récentes d’abord, 30 à la fois quand vous faites défiler. Une tâche que vous venez d’envoyer est en haut, et chacune dit quand, comme « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées s’y placent selon le moment où elles ont commencé à le sembler, avec l’étiquette **Semble fait**.

Après un envoi, une courte note dit où se trouve la tâche, comme « Envoyé. Déplacé dans Fait. » ou, si elle attend une réponse, « Envoyé. Déplacé dans Plus tard jusqu’à lun. » **Ouvrir** vous y mène. Le fil qui quitte votre boîte de réception quelques jours ne concerne que votre messagerie. La recherche trouve une tâche par son titre ou son destinataire, aussi dans Plus tard et Fait.

**Pour vous** met d’abord ce qui est en retard ou dû d’ici demain, puis les questions de votre Fleet, puis le reste. Dans chaque partie, les plus récentes d’abord. Une tâche garde sa place pendant que votre Machine la prépare et quand elle a fini : seule sa marque change. Les autres groupes ouverts mettent d’abord ce qui est en retard ou dû d’ici demain, le reste du plus récent au plus ancien. La barre latérale garde le même ordre.

Une tâche marquée **Semble fait** s’affiche comme une tâche faite, avec ce qui montre qu’elle est faite, comme « PR #3451 fusionnée ». Elle n’est pas encore fermée : **Rouvrir** la remet dans votre liste, et votre Machine en tient compte. Elles ne sont jamais en retard et ne comptent pas comme en attente de vous. Au bout d’un jour, elle se ferme d’elle-même, avec **Annuler**. Une tâche que vous avez déjà réglée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi d’elle-même.

Une tâche dont la dernière étape reste ouverte chez quelqu’un d’autre, comme une relecture, une fusion ou une réponse, affiche **En attente de :** cette étape et reste ouverte. Elle attend dans **En attente des autres**, repliée au-dessus de Revient plus tard, et ne compte pas comme prête pour vous. Un nouveau message à son sujet la ramène. De même si vous avez répondu par une question : elle revient le matin avant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin une fois passée, et dit qui elle attend encore.

Quand une tâche vise un résultat qu’une autre personne doit fournir, comme un contrat signé ou un paiement, ses **Détails** affichent ce résultat comme **Terminé quand**. Envoyer votre part ne la ferme pas : elle attend dans **En attente des autres** jusqu’à ce qu’un message montre le résultat, puis se ferme toute seule, avec **Annuler**. Si rien n’arrive au moment de relancer, elle revient avec **Écris une courte relance** dans son chat. Pour changer ce qui compte comme terminé, dites-le dans le chat.

Une tâche que personne n’a touchée depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la ferme, avec **Annuler**. **Garder** la garde, et elle ne redemande jamais. L’ouvrir, un message dans le chat, une modification, la mettre en attente ou un nouveau message à son sujet comptent comme une action. Sans réponse une semaine de plus, elle se range dans Revient plus tard, sous Toujours utile ?, au lieu de disparaître. Le nombre sur l’icône de l’app et le récap du matin cessent alors de la compter. Une action la ramène.

Quand rien n’a besoin de vous, votre Machine fait la sieste sur la liste vide. Pendant qu’elle vérifie, elle se réveille et le dit. Si une vérification a échoué ou est en retard, sa ligne le dit, avec **Vérifier maintenant** en dessous.

**Tout**, **Travail** et **Perso** au-dessus de la liste dans la barre latérale affichent toutes les tâches ou un seul type. Votre Machine garde ce choix, pour que votre téléphone et votre ordinateur affichent la même liste. Quand Travail ou Perso est actif, le haut de la liste l’indique, avec **Tout afficher** pour revenir. Une alerte sur votre Machine elle-même, comme une partie qui redémarre sans cesse, n’est ni Travail ni Perso et n’apparaît que sous Tout.

La ligne en haut de la liste passe aussi directement à l’autre : **Perso uniquement · Travail · Tout afficher**.

**Récap** en haut de la liste montre ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso, ou seulement celui que vous filtrez. **Copier** le met dans votre presse-papiers, en texte simple à coller partout. Il n’apparaît que s’il y a quelque chose à lister. Son **×** le masque sur tous vos appareils jusqu’au prochain récap du matin ou du soir, ou jusqu’au lendemain.

Une tâche liée à un projet affiche le nom du projet sur la ligne sous son titre ; il ouvre le projet. **Projet** sous **Détails** le change ou le retire. Voir [les tâches d’un projet](projects.md#a-projects-to-dos).

**Domaine** sous **Détails** déplace la tâche vers votre autre espace. Ce qu’elle peut lire et d’où elle peut envoyer suit le déplacement ; les messages d’où elle vient restent où ils sont. **Annuler** dans le message qui suit la remet en place.

Quand une tâche a besoin d’un autre espace pour avancer et que tous les messages dont elle vient s’y trouvent, elle s’y déplace toute seule et continue. Sinon, elle le demande avec un bouton **Déplacer vers Travail**. Rien ne bouge avant que vous appuyiez ; ensuite, elle continue toute seule. Une tâche ajoutée sans choisir Travail ou Perso se déplace toute seule dès qu’elle sait où elle va. D’ici là, elle n’indique ni Travail ni Perso et reste privée.

Quand vous lancez une tâche, elle peut toujours lire les messages d’où elle vient, même dans la boîte d’une autre entreprise. Si elle a besoin d’autres messages d’un autre espace, elle le demande avec **Utiliser cet e-mail pour cette tâche** ; un appui les ajoute et elle continue. Le courrier pour une autre de vos entreprises va dès le départ dans les tâches de cette entreprise. Une tâche de votre vie privée, comme votre famille qui écrit à votre adresse pro, est Perso dès le départ.

Le travail qui vous arrive sur un compte perso, comme un client sur WhatsApp ou une commande dans votre boîte perso, est Travail dès le départ. Une tâche que vous avez déplacée ou placée vous-même reste toujours où vous l’avez mise. Travail ou Perso décide où une tâche apparaît et avec qui elle est partagée, jamais par où elle répond : une réponse va toujours là où est la conversation, même après un déplacement, sauf si vous choisissez un autre moyen.

Sa réponse part quand même de l’adresse pro où elle est arrivée, et elle n’apparaît jamais dans une Work Fleet ni dans le Graph d’équipe.

À partir de deux en attente, **Passer en revue** dans l’en-tête de Pour vous les passe une par une, dans l’ordre de la liste, chaque brouillon en entier, avec **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie ce qui est à l’écran, `S` met en attente, `→` ignore et Échap arrête. Sous le titre, l’en-tête dit aussi combien de temps elles prennent à votre rythme, comme "environ 2 min".

Une tâche qui vous pose une question reste en dehors des deux : il lui faut votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit, et vérifie ce qui est arrivé pour en tirer des tâches dès que 40 messages attendent ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus rejoignent la vérification suivante, dans l’heure.

**Vérifier maintenant** lit tout de suite chaque source. Quand rien n’est ouvert, touchez la ligne de votre Machine pour le voir, avec **Détails**, qui ouvre Vérifications dans Connexions. Quand des tâches sont ouvertes, il est en haut sur un ordinateur. Une courte ligne n’y apparaît que pendant une vérification, ou quand une a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare gardent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches dit ce qu’elle a trouvé dans toutes les sources, comme « 13 messages vérifiés à 16:11 · rien ne vous attend » ou « · 2 nouvelles tâches ». Quand une nouvelle tâche attend un meilleur moment, comme votre résumé du matin, elle dit jusqu’à quand : « 1 tâche en attente jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque conversation, chat et notification, avec l’icône de sa source : qui a écrit, l’objet ou les premiers mots, et sa nouvelle tâche ou pourquoi rien n’était nécessaire, comme « Seulement en copie, un collègue répond » ou « Rendez-vous déjà fixé jeudi ». Une conversation n’affiche aucune raison quand la vérification n’en a donné qu’une vague. Touchez-en un pour le lire.

Les 10 premiers s’affichent, et une touche en dessous montre le reste. Un nombre après un nom, comme (3), indique combien de nouveaux messages compte ce chat. Une notification du téléphone sur un message déjà listé n’apparaît qu’une fois. La ligne reste 12 heures après la vérification.

Elle ne compte que les e-mails qui vous sont adressés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas de nouveaux e-mails. Les e-mails que votre Machine vous envoie, comme votre résumé du matin ou un avis de correction, ne sont jamais lus ni listés. Les e-mails sur la facturation, votre essai ou une invitation sont lus comme d’habitude.

## Les boutons

Une tâche affiche son étape suivante, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** dit ce qu’il faut changer : comment faire, ou, une fois le brouillon prêt, ce qu’il faut y changer. Quand la rangée est pleine sur un téléphone, **Mettre en attente** passe dans **…**. **Marquer comme fait** (c’est réglé) est là aussi : visible sur une tâche prête sans brouillon, sinon en haut de **…**, aussi sur une qui attend votre décision. Elle quitte la liste tout de suite, avec **Annuler** dans le message. Balayez le message ou faites-le glisser avec la souris pour le fermer plus tôt. Le changement reste.

Pour la faire autrement, dites-le dans son **Chat**.

Sous **…** (sur un téléphone, ce menu s’ouvre depuis le bas de l’écran) :

- **Transférer…** : la confier à un coéquipier, à [Claude Code ou Codex](hand-to-agent.md) (ceux que vous avez configurés) ou [demander une relecture à quelqu’un](ask-to-review.md).
- **Répéter…** : elle [revient à un rythme régulier](recurring.md).
- **Pas nécessaire** : elle disparaît. Choisissez pourquoi, si vous voulez : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des leçons.

Appuyez sur le titre, ou sur **Nom** sous **Détails**, pour la renommer. Votre titre reste, même quand la tâche change.

Une tâche fermée peut revenir avec **Rouvrir**. Elle revient aussi d’elle-même quand il se passe quelque chose de nouveau, comme un nouveau message de la personne. Votre propre réponse ne la fait pas revenir.

Une facture que tu dois encore payer toi-même, de n’importe quel pays, devient une tâche avec le montant, l’échéance et les coordonnées de paiement de la facture. Celles payées automatiquement, comme un prélèvement ou une carte enregistrée, non. Si un e-mail plus récent montre qu’elle est payée, par exemple l’expéditeur confirme avoir reçu ton paiement, la tâche se ferme d’elle-même. **Annuler** la fait revenir pendant un jour.

Une tâche qui ne comptait que jusqu’à un moment précis, comme une confirmation avant une réunion, se ferme d’elle-même une fois ce moment passé. Elle passe dans les tâches terminées avec « Plus nécessaire » et la date. **Annuler** la fait revenir pendant un jour.

Avant qu’un message ou une passation pour quelqu’un apparaisse comme prêt, ta Machine vérifie tes discussions récentes avec les personnes concernées, en groupe aussi, et attend que Slack les ait lues. Si un message plus récent montre que c’est déjà fait, par exemple la personne a été sollicitée et a dit oui, la tâche se ferme d’elle-même. **Annuler** la fait revenir pendant un jour.

Quand un message plus récent change le plan, comme une fête déplacée ailleurs ou une réservation annulée, The Machine met ses tâches à jour elle-même. Une tâche qui compte encore suit le nouveau plan. Une tâche où il ne reste rien à faire passe dans les tâches terminées comme « Pas nécessaire », son chat dit « Mis à jour : » et pourquoi, et **Annuler** la ramène pendant un jour.

Sur vos premières tâches, une courte ligne sous les boutons montre l’essentiel : **Demander des modifications** et **Pas nécessaire** quand une tâche ne convient pas tout à fait, et sur votre premier brouillon prêt, que rien ne part avant que vous appuyiez sur **Envoyer**. Une astuce disparaît pour de bon dès que vous utilisez son bouton ou appuyez sur ×, sur tous vos appareils.

Le premier jour, le haut des Tâches vous salue par votre prénom et indique qui attend votre réponse depuis le plus longtemps. The Machine rédige cette réponse en premier, pour qu’elle soit prête à votre arrivée. Rien ne part avant que vous l’envoyiez. La ligne disparaît après votre premier jour ou votre première tâche décidée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation quand elle en concerne une (jamais seulement parce que quelqu’un y travaille), le projet, Travail ou Perso (sous **Tout**) et quand elle est arrivée, ainsi que son état quand son groupe ne le dit pas déjà. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Un nom et une organisation affichent leur photo ou leur logo quand le Graph en a un. Sinon, ils affichent leurs initiales. Un logo illisible à cette taille, comme du blanc sur fond transparent ou un logotype très large, affiche aussi l’initiale.

Parfois, une ligne discrète sous le texte dit ce qui n'est pas connu, comme « Dernier contact il y a 12 jours par e-mail ; rien depuis. » Elle n'apparaît que si le dernier échange est ancien ou toujours sans réponse, et nomme les canaux non connectés où une réponse a pu arriver, comme WhatsApp. Votre Machine prépare avec les mêmes faits : elle dit ce qu'elle ne sait pas au lieu de deviner.

Quand elle nomme un canal non connecté, Connecter à côté ouvre cette connexion.

Un titre dit ce qu'il faut faire. Il ne change que quand cela change, par exemple pour une nouvelle demande. Une tâche faite garde son titre, avec en dessous comment elle s'est terminée, par exemple ce qui est parti ou "Fait : Sam a signé mardi".

Au-dessus du brouillon, une ligne discrète nomme le message d’origine, avec le logo du service (Gmail, Slack, WhatsApp…). Appuyez dessus pour lire le fil. Le brouillon commence par le logo de sa destination : vous voyez si c’est une réponse Slack ou un e-mail avant de lire. Une étape sans brouillon, comme un transfert, montre le logo sur son bouton.

Quand le brouillon suit l’avis de quelqu’un d’autre dans un autre message, comme la suggestion d’un collègue dans Slack, une ligne sous la tâche l’indique, comme « D’après Sam dans #ops ». Appuyez dessus pour lire ce message ici, avec Ouvrir dans Slack ou Gmail à l’intérieur. Quand ce message est la source même de la tâche, la ligne de source l’affiche déjà, donc pas de deuxième ligne.

Un chat (Slack, WhatsApp, Telegram, Intercom…) se lit comme une seule conversation, du plus ancien au plus récent, chaque message une fois ; celui dont parle la tâche est marqué « Cette tâche ». Dans WhatsApp, Telegram ou Signal, vos propres messages sont à droite, comme dans l’app.

Pour un e-mail, **Détails** n’affiche que ce que l’en-tête ne dit pas, comme les adresses Cc complètes, Cci ou une autre adresse de réponse ; s’il n’y a rien à ajouter, il n’apparaît pas.

Une réponse dans un fil Slack montre aussi ce qui a été dit avant le fil. Un lien de la tâche vers son propre message l'ouvre aussi ici, avec **Ouvrir dans Slack** en bas.

**Détails** montre son nom, son projet et son espace (appuyez sur l’un d’eux pour le changer), votre dernière note et le résultat d’un agent de code. **Chat ›** au bout de cette ligne ouvre le chat. Une tâche terminée reste courte : son titre, une ligne et ce qui est parti ; le message d’origine est dans ses **Détails**.

Une tâche « En attente de » (quelqu’un vous a promis quelque chose) renvoie vers votre dernier message à cette personne, celui auquel vous attendez une réponse : « E-mail à Pat · mar. ».

## En créer une vous-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur) ajoute une tâche pour n’importe quoi. La créer n’envoie rien. Sans Travail ni Perso choisi, elle va là où elle doit aller : selon les personnes et le sujet, une entreprise ou une boîte qu’elle nomme, ou l’e-mail qu’elle relance. Si rien ne l’indique, elle commence là où sont la plupart de vos tâches. The Machine cherche cet e-mail dans votre boîte, y compris les plus anciens pas encore récupérés.

- **Échéance** : tapez un jour ou une heure, comme « demain », « ven. prochain », « 3 nov. », « 15:00 », « dans 2 heures » ou « demain 14h ». L’anglais marche aussi (« in 2 hours », « tomorrow 9 »). L’icône du calendrier propose des choix rapides, comme pour la mise en attente, et **Choisir une date**.
- **Message** : joignez le message concerné : un e-mail, Slack, Teams, WhatsApp, Telegram ou tout autre message que The Machine a reçu. La recherche porte sur le texte ou l’expéditeur. Chaque résultat indique sa provenance, son expéditeur et sa date.
- **Fichiers** : touchez le trombone dans le champ, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur un téléphone, l’appareil photo à côté prend une photo. Jusqu’à 5 fichiers, des mêmes types et tailles que dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × en retire un.

Les fichiers restent avec la tâche : ils s’affichent sur la tâche et dans son chat, et The Machine les lit en travaillant dessus. Des fichiers seuls suffisent : The Machine lit le texte d’un PDF ou d’un fichier texte et remplit la tâche à partir de lui. Une photo s’affiche en petite image : touchez-la pour la voir en grand.
