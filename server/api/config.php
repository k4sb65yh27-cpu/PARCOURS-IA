<?php
// Réglages de la synchronisation du Parcours IA. Seul fichier à adapter.
return [
    // Dossier des données (base SQLite). De préférence HORS de la racine web.
    'data_dir' => __DIR__ . '/data',

    // 'local' : comptes créés dans l'application (courriel professionnel + mot de passe).
    // 'remote_user' : identité fournie par le serveur web (SSO, LDAP, authentification HTTP) via REMOTE_USER ; aucun mot de passe géré ici.
    'auth_mode' => 'local',

    // Domaines de courriel autorisés à créer un compte (mode local). Vide = tous.
    'allowed_domains' => ['sattse.com'],

    // Création de compte ouverte (true) ou réservée à l'administrateur en ligne de commande (false).
    'open_registration' => true,

    // Durée de validité d'une connexion, en jours.
    'token_days' => 180,

    // Taille maximale d'une sauvegarde, en octets.
    'max_bytes' => 2 * 1024 * 1024,

    // Classement des points d'XP entre salariés volontaires. DÉSACTIVÉ par défaut.
    // À n'activer qu'après accord écrit du référent IA (information des salariés, CSE le cas échéant,
    // registre des traitements) : voir GUIDE_INSTALLATION.md, section « Classement ».
    'leaderboard' => false,

    // Hausse d'XP maximale prise en compte par jour et par participant dans le classement
    // (la progression personnelle n'est jamais plafonnée).
    'max_xp_per_day' => 800,

    // Objectif collectif hebdomadaire affiché, en XP.
    'board_goal_week' => 1000,

    // Un score par métier n'est affiché qu'à partir de ce nombre de participants du métier.
    'board_min_group' => 3,

    // Durée de conservation des instantanés de début de semaine et de mois, en mois.
    'board_snap_months' => 13,
];
