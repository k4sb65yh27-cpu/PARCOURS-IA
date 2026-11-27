# Parcours IA : installation sur un serveur SATT

Version 2, 27/11/2026. Nouveautés par rapport à la version 1 : classement facultatif (désactivé par défaut), deux tables de plus dans la base, quatre commandes d'administration.

## Ce que c'est

Le Parcours IA est une application web de formation à l'usage des assistants d'IA (Claude, ChatGPT, Copilot, Le Chat). Elle se compose de fichiers statiques (HTML, JavaScript, CSS, images) et d'un script PHP de synchronisation.

- Sur PC, elle s'ouvre dans le navigateur. Edge et Chrome proposent aussi « Installer l'application ».
- Sur téléphone, on l'ajoute à l'écran d'accueil : Safari, Partager, puis « Sur l'écran d'accueil » sur iPhone ; Chrome, puis « Installer » sur Android.
- Elle fonctionne hors connexion une fois chargée.
- Avec un compte, la progression suit l'utilisateur d'un appareil à l'autre. Sans le script PHP, l'application marche quand même, mais la progression reste dans le navigateur.

Aucune ressource externe n'est chargée. L'application n'envoie aucune donnée ailleurs qu'au script de synchronisation du même serveur, et n'appelle aucun service d'IA.

## Prérequis

- Un serveur web en HTTPS. HTTPS est obligatoire pour l'installation sur téléphone et le fonctionnement hors ligne.
- PHP 8.1 ou plus, avec l'extension `pdo_sqlite`.
- Environ 3 Mo de disque pour l'application, plus quelques ko par utilisateur.

## Installation

1. Copier le dossier `parcours/` sous la racine web, par exemple pour obtenir `https://outils.sattse.com/parcours/`.
2. Vérifier que `parcours/config.json` contient `{"syncUrl": "api/sync.php"}`.
3. Ouvrir `parcours/api/config.php` et régler :
   - `data_dir` : le dossier de la base SQLite. Le placer de préférence hors de la racine web, par exemple `/var/lib/parcours-ia`. Le serveur web doit pouvoir y écrire.
   - `auth_mode` : `local` (comptes créés dans l'application) ou `remote_user` (identité fournie par le serveur, voir plus bas).
   - `allowed_domains` : les domaines autorisés à créer un compte, `sattse.com` par défaut.
   - `open_registration` : `false` pour réserver la création de comptes à l'administrateur.
   - `leaderboard` : laisser `false` à l'installation (voir la section « Classement »).
4. Tester : `php parcours/api/sync.php selftest` doit afficher `selftest OK` (il vérifie aussi le classement, dans une base temporaire).
5. Ouvrir l'adresse dans un navigateur, aller dans Profil : le bloc « Compte » apparaît.

### Apache

Les fichiers `.htaccess` fournis font deux choses : ils transmettent l'en-tête `Authorization` à PHP et ils interdisent l'accès web à `config.php` et au dossier `data/`. Il faut que `AllowOverride` les autorise. Sinon, reporter ces règles dans la configuration du site.

### Nginx

```nginx
location ~ ^/parcours/api/(data/|config\.php) { deny all; }
location ~ ^/parcours/api/sync\.php$ {
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param HTTP_AUTHORIZATION $http_authorization;
    fastcgi_pass unix:/run/php/php-fpm.sock;
}
```

## Deux modes de compte

**Mode `local` (par défaut).** L'utilisateur crée son compte dans l'application avec son courriel professionnel et un mot de passe de 10 caractères minimum.
- Les mots de passe sont hachés avec `password_hash`.
- Les jetons de connexion (180 jours par défaut) sont stockés hachés.
- Un compte est verrouillé 15 minutes après 10 essais erronés.

**Mode `remote_user`.** Ce mode réutilise l'authentification existante (SSO, LDAP ou Active Directory, authentification HTTP).
- Le serveur web protège `parcours/api/sync.php` et transmet l'identifiant dans `REMOTE_USER`.
- L'application n'affiche alors aucun formulaire et ne gère aucun mot de passe.
- Le reste de `parcours/` peut rester public : le contenu est générique.

## Administration

```
php parcours/api/sync.php list                      # comptes et dernière synchronisation
php parcours/api/sync.php add <courriel> <mdp>      # créer un compte
php parcours/api/sync.php passwd <courriel> <mdp>   # nouveau mot de passe (déconnecte les appareils)
php parcours/api/sync.php delete <courriel>         # supprimer compte et progression
```

## Classement (facultatif)

Le classement affiche, pour les seuls salariés qui l'ont choisi, les points d'XP de la semaine, du mois et depuis le début, ainsi qu'un score collectif et un score par métier. Il est désactivé par défaut et l'onglet « Classement » n'apparaît pas dans l'application tant qu'il l'est.

**Ne l'activez qu'après accord écrit du référent IA**, qui confirme que les démarches préalables sont faites : information des salariés, consultation du CSE le cas échéant, inscription au registre des traitements.

Activation : dans `api/config.php`, passer `leaderboard` à `true`. Réglages associés :
- `max_xp_per_day` (800) : hausse d'XP maximale prise en compte par jour et par participant. Au-delà, la hausse compte pour la progression personnelle mais pas pour le classement, et une ligne est écrite dans le journal d'erreurs PHP.
- `board_goal_week` (1000) : objectif collectif de la semaine, affiché aux participants.
- `board_min_group` (3) : un score par métier n'apparaît qu'à partir de ce nombre de participants du métier.
- `board_snap_months` (13) : durée de conservation des instantanés de début de semaine et de mois.

Fonctionnement :
- Participer se fait dans l'onglet, sous un nom affiché choisi (2 à 24 caractères, unique). Le courriel n'est jamais affiché.
- Seuls les dix premiers sont listés, avec la position de l'utilisateur ; les derniers rangs ne sont jamais montrés.
- Se retirer efface immédiatement les données de classement de l'utilisateur.
- Les non-participants n'ont aucune donnée de classement.

Limite à connaître : l'XP est calculé par le navigateur puis envoyé au serveur, et un utilisateur averti peut envoyer une valeur fausse. Le plafond journalier réduit l'écart possible sans l'empêcher : les scores affichés restent déclaratifs.

Commandes :

```
php parcours/api/sync.php board-list                  # participants, nom affiché, métier, XP
php parcours/api/sync.php board-hide <courriel>       # retirer quelqu'un du classement
php parcours/api/sync.php board-reset week            # remettre à zéro la semaine en cours (ou month)
```

## Skills

L'application enseigne l'existence des skills et ne les installe pas. Le parcours indique aux salariés que les skills relèvent à ce stade des projets personnels et que l'ajout d'un skill nécessite l'aval du RSI ou du référent IA.

## Données conservées

Le fichier `parcours.sqlite` contient cinq tables :
- `users` : courriel, empreinte du mot de passe, compteur d'échecs ;
- `tokens` : empreintes des jetons, échéance ;
- `saves` : la progression au format JSON. On y trouve l'XP, les étapes validées, les réponses aux questions, les défis relevés et les notes libres du carnet d'étape ;
- `board` : participants au classement seulement (nom affiché, métier, XP retenu pour le classement) ;
- `board_snap` : XP de chaque participant au début de la semaine et du mois.

L'application demande de ne saisir aucune donnée de dossier dans le carnet. Ces données personnelles (courriel et progression de formation) relèvent du registre des traitements. Un utilisateur qui quitte la SATT se supprime avec la commande `delete`, qui efface aussi ses données de classement.

Sauvegarde : copier `parcours.sqlite`. Cette copie est sûre quand le serveur est arrêté, ou avec `sqlite3 parcours.sqlite ".backup copie.sqlite"`.

## Mises à jour

Le contenu de la formation est mis à jour chaque semaine. Pour une mise à jour, remplacer tout le dossier `parcours/` **sauf** trois éléments :
- `config.json` ;
- `api/config.php` ;
- le dossier de données.

Les navigateurs récupèrent la nouvelle version au prochain chargement, et la progression des utilisateurs est conservée.

Mise à jour depuis la version 1 : le `api/config.php` conservé reste valable ; le classement y est considéré comme désactivé. Pour le régler, recopier depuis le `api/config.php` fourni les cinq réglages du bloc « Classement ». Les deux nouvelles tables se créent seules au premier appel.

## Comportement de la synchronisation

- L'application synchronise à l'ouverture, au retour du réseau, et 2,5 secondes après chaque progression.
- Elle récupère d'abord la sauvegarde du serveur, la fusionne avec celle de l'appareil, puis renvoie le résultat.
- La fusion ne retire rien : une étape validée, un exercice coché ou un défi relevé sur un appareil le reste partout.

## Désinstallation

Supprimer le dossier `parcours/` et le dossier de données.
