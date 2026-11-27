<?php
/*
 * Parcours IA : synchronisation de la progression par compte.
 * Un seul fichier, PHP 8.1 ou plus avec pdo_sqlite. Aucune dépendance.
 *
 * Web (JSON, même origine que l'application) :
 *   POST sync.php?a=register  {email, password}      -> {token, email}
 *   POST sync.php?a=login     {email, password}      -> {token, email}
 *   POST sync.php?a=logout                           -> {ok}
 *   GET  sync.php?a=me                               -> {email, mode}
 *   GET  sync.php?a=pull                             -> {data, updatedAt}
 *   PUT  sync.php?a=push      {data, updatedAt}      -> {ok, updatedAt}
 *   GET  sync.php?a=board&p=week|month|all           -> classement (si leaderboard activé)
 *   PUT  sync.php?a=board-optin {optin, display}     -> participation au classement
 *   Jeton : en-tête « Authorization: Bearer <jeton> » (mode local).
 *
 * Ligne de commande (administrateur) :
 *   php sync.php list
 *   php sync.php add <courriel> <mot de passe>
 *   php sync.php passwd <courriel> <mot de passe>
 *   php sync.php delete <courriel>
 *   php sync.php board-list | board-hide <courriel> | board-reset week|month
 *   php sync.php selftest
 */
declare(strict_types=1);

$C = require __DIR__ . '/config.php';
// Valeurs par défaut des réglages ajoutés en version 2 : un config.php de version 1 reste valable.
$C += ['leaderboard' => false, 'max_xp_per_day' => 800, 'board_goal_week' => 1000, 'board_min_group' => 3, 'board_snap_months' => 13];

function db(array $C): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    if (!is_dir($C['data_dir']) && !mkdir($C['data_dir'], 0700, true)) throw new RuntimeException('data_dir');
    $pdo = new PDO('sqlite:' . $C['data_dir'] . '/parcours.sqlite', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    $pdo->exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=3000;');
    $pdo->exec('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, hash TEXT, created INTEGER, fails INTEGER DEFAULT 0, fail_at INTEGER DEFAULT 0)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS tokens (hash TEXT PRIMARY KEY, email TEXT, expires INTEGER)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS saves (email TEXT PRIMARY KEY, data TEXT, updated INTEGER, saved_at INTEGER)');
    // Classement : une ligne par participant volontaire, rien pour les autres.
    $pdo->exec('CREATE TABLE IF NOT EXISTS board (email TEXT PRIMARY KEY, display TEXT, display_key TEXT UNIQUE, profil TEXT, xp_board INTEGER DEFAULT 0, day TEXT DEFAULT \'\', day_xp INTEGER DEFAULT 0, joined INTEGER)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS board_snap (email TEXT, period TEXT, xp_start INTEGER, created INTEGER, PRIMARY KEY (email, period))');
    return $pdo;
}

function norm_email(string $e): string { return strtolower(trim($e)); }

function valid_email(array $C, string $e): bool {
    if (!filter_var($e, FILTER_VALIDATE_EMAIL)) return false;
    if (!$C['allowed_domains']) return true;
    $dom = substr(strrchr($e, '@'), 1);
    return in_array($dom, $C['allowed_domains'], true);
}

function set_password(array $C, string $email, string $pw): void {
    $st = db($C)->prepare('INSERT INTO users(email, hash, created) VALUES(?, ?, ?) ON CONFLICT(email) DO UPDATE SET hash = excluded.hash, fails = 0');
    $st->execute([$email, password_hash($pw, PASSWORD_DEFAULT), time()]);
}

function new_token(array $C, string $email): string {
    $t = bin2hex(random_bytes(32));
    db($C)->prepare('INSERT INTO tokens VALUES(?, ?, ?)')->execute([hash('sha256', $t), $email, time() + 86400 * $C['token_days']]);
    db($C)->prepare('DELETE FROM tokens WHERE expires < ?')->execute([time()]);
    return $t;
}

/* ---------- Classement (désactivé par défaut, voir config.php) ---------- */
function board_on(array $C): bool { return !empty($C['leaderboard']); }
/** Minuscules UTF-8 sans dépendre de l'extension mbstring (absente de certains serveurs). */
function lower_utf8(string $s): string {
    if (function_exists('mb_strtolower')) return mb_strtolower($s, 'UTF-8');
    return strtolower(strtr($s, ['À' => 'à', 'Â' => 'â', 'Ä' => 'ä', 'Ç' => 'ç', 'É' => 'é', 'È' => 'è', 'Ê' => 'ê', 'Ë' => 'ë', 'Î' => 'î', 'Ï' => 'ï', 'Ô' => 'ô', 'Ö' => 'ö', 'Ù' => 'ù', 'Û' => 'û', 'Ü' => 'ü', 'Ÿ' => 'ÿ', 'Œ' => 'œ', 'Æ' => 'æ']));
}
function period_keys(int $t): array { return ['week' => date('o', $t) . '-S' . date('W', $t), 'month' => date('Y-m', $t)]; }
function save_info(array $C, string $email): array {
    $st = db($C)->prepare('SELECT data FROM saves WHERE email = ?'); $st->execute([$email]);
    $d = json_decode((string)$st->fetchColumn(), true);
    $s = is_array($d) ? ($d['state'] ?? []) : [];
    return ['xp' => max(0, (int)($s['xp'] ?? 0)), 'profil' => preg_replace('/[^a-z]/', '', (string)($s['settings']['profil'] ?? ''))];
}
/** Ouvre la semaine et le mois en cours pour un participant, au niveau d'XP donné ; purge les instantanés anciens. */
function board_snaps(array $C, string $email, int $xpStart): void {
    $ins = db($C)->prepare('INSERT OR IGNORE INTO board_snap VALUES(?, ?, ?, ?)');
    foreach (period_keys(time()) as $k) $ins->execute([$email, $k, $xpStart, time()]);
    db($C)->prepare('DELETE FROM board_snap WHERE created < ?')->execute([time() - 86400 * 31 * (int)$C['board_snap_months']]);
}
/** Appelé à chaque sauvegarde : la hausse d'XP compte au classement dans la limite du plafond journalier. */
function board_on_push(array $C, string $email, int $oldXp, int $newXp, string $profil): void {
    if (!board_on($C)) return;
    $st = db($C)->prepare('SELECT xp_board, day, day_xp FROM board WHERE email = ?'); $st->execute([$email]);
    $b = $st->fetch(PDO::FETCH_ASSOC);
    if (!$b) return;
    $today = date('Y-m-d');
    $dayXp = $b['day'] === $today ? (int)$b['day_xp'] : 0;
    $delta = max(0, $newXp - $oldXp);
    $allowed = max(0, min($delta, (int)$C['max_xp_per_day'] - $dayXp));
    if ($allowed < $delta) error_log("parcours classement : hausse de $delta XP plafonnée à $allowed pour $email");
    board_snaps($C, $email, (int)$b['xp_board']);
    db($C)->prepare('UPDATE board SET xp_board = ?, day = ?, day_xp = ?, profil = ? WHERE email = ?')
        ->execute([(int)$b['xp_board'] + $allowed, $today, $dayXp + $allowed, $profil, $email]);
}
/** Participation volontaire. Le retrait efface immédiatement les données de classement. Renvoie [code HTTP, corps]. */
function board_optin(array $C, string $email, bool $optin, string $display): array {
    if (!board_on($C)) return [403, ['error' => 'Classement désactivé.']];
    if (!$optin) {
        foreach (['board', 'board_snap'] as $t) db($C)->prepare("DELETE FROM $t WHERE email = ?")->execute([$email]);
        return [200, ['optin' => false]];
    }
    $display = trim(preg_replace('/\s+/u', ' ', $display));
    if (!preg_match('/^[\p{L}\p{N} \-]{2,24}$/u', $display)) return [400, ['error' => 'Nom affiché : 2 à 24 lettres, chiffres, espaces ou tirets.']];
    $key = lower_utf8($display);
    $st = db($C)->prepare('SELECT email FROM board WHERE display_key = ? AND email <> ?'); $st->execute([$key, $email]);
    if ($st->fetchColumn()) return [409, ['error' => 'Ce nom est déjà pris : choisissez-en un autre.']];
    $i = save_info($C, $email);
    $st = db($C)->prepare('SELECT 1 FROM board WHERE email = ?'); $st->execute([$email]);
    if ($st->fetchColumn()) {
        db($C)->prepare('UPDATE board SET display = ?, display_key = ? WHERE email = ?')->execute([$display, $key, $email]);
    } else {
        // L'acquis antérieur compte « depuis le début » ; la semaine et le mois partent de zéro.
        db($C)->prepare('INSERT INTO board VALUES(?, ?, ?, ?, ?, ?, 0, ?)')->execute([$email, $display, $key, $i['profil'], $i['xp'], date('Y-m-d'), time()]);
        board_snaps($C, $email, $i['xp']);
    }
    return [200, ['optin' => true, 'display' => $display]];
}
function board_me(array $C, string $email): array {
    $st = db($C)->prepare('SELECT display FROM board WHERE email = ?'); $st->execute([$email]);
    $d = $st->fetchColumn();
    return ['optin' => $d !== false, 'display' => $d === false ? '' : (string)$d];
}
/** Classement d'une période : score collectif, scores par profil (groupes d'au moins N participants), dix premiers, position personnelle. */
function board_view(array $C, string $email, string $p): array {
    if (!board_on($C)) return [403, ['error' => 'Classement désactivé.']];
    if (!in_array($p, ['week', 'month', 'all'], true)) $p = 'week';
    $key = $p === 'all' ? '' : period_keys(time())[$p];
    $st = db($C)->prepare('SELECT b.email, b.display, b.profil, b.xp_board, s.xp_start FROM board b LEFT JOIN board_snap s ON s.email = b.email AND s.period = ?');
    $st->execute([$key]);
    $rows = [];
    foreach ($st->fetchAll(PDO::FETCH_ASSOC) as $r) {
        $xp = $p === 'all' ? (int)$r['xp_board'] : ($r['xp_start'] === null ? 0 : max(0, (int)$r['xp_board'] - (int)$r['xp_start']));
        $rows[] = ['email' => $r['email'], 'display' => $r['display'], 'profil' => (string)$r['profil'], 'xp' => $xp];
    }
    usort($rows, fn($a, $b) => $b['xp'] <=> $a['xp'] ?: strcmp($a['display'], $b['display']));
    $rank = 0; $prev = null; $moi = null; $top = [];
    foreach ($rows as $i => $r) {
        if ($r['xp'] !== $prev) { $rank = $i + 1; $prev = $r['xp']; }
        if ($i < 10) $top[] = ['rang' => $rank, 'display' => $r['display'], 'xp' => $r['xp']];
        if ($r['email'] === $email) $moi = ['rang' => $rank, 'xp' => $r['xp']];
    }
    $groups = [];
    foreach ($rows as $r) if ($r['profil'] !== '') { $g = &$groups[$r['profil']]; $g['n'] = ($g['n'] ?? 0) + 1; $g['xp'] = ($g['xp'] ?? 0) + $r['xp']; unset($g); }
    $profils = [];
    foreach ($groups as $k => $g) if ($g['n'] >= (int)$C['board_min_group']) $profils[] = ['profil' => $k, 'n' => $g['n'], 'xp' => $g['xp']];
    usort($profils, fn($a, $b) => $b['xp'] <=> $a['xp']);
    return [200, [
        'period' => $p, 'at' => time(), 'participants' => count($rows),
        'collectif' => ['xp' => array_sum(array_column($rows, 'xp')), 'objectif' => $p === 'week' ? (int)$C['board_goal_week'] : null],
        'profils' => $profils, 'top' => $top, 'moi' => $moi,
    ]];
}

/* Contrôle de l'autotest, actif quel que soit le réglage zend.assertions du serveur. */
function chk(bool $ok): void {
    if (!$ok) { $l = debug_backtrace()[0]['line'] ?? 0; fwrite(STDERR, "selftest ÉCHEC ligne $l\n"); exit(1); }
}

/* ---------- Ligne de commande ---------- */
if (PHP_SAPI === 'cli') {
    [$cmd, $a, $b] = array_pad(array_slice($argv, 1), 3, '');
    $email = norm_email($a);
    switch ($cmd) {
        case 'list':
            foreach (db($C)->query('SELECT u.email, s.saved_at FROM users u LEFT JOIN saves s ON s.email = u.email ORDER BY u.email') as $r)
                echo $r['email'], "\t", $r['saved_at'] ? date('Y-m-d H:i', (int)$r['saved_at']) : 'jamais synchronisé', "\n";
            break;
        case 'add':
        case 'passwd':
            if (!$email || strlen($b) < 10) exit("Courriel et mot de passe de 10 caractères minimum.\n");
            set_password($C, $email, $b);
            db($C)->prepare('DELETE FROM tokens WHERE email = ?')->execute([$email]);
            echo "OK\n";
            break;
        case 'delete':
            foreach (['users', 'tokens', 'saves', 'board', 'board_snap'] as $t) db($C)->prepare("DELETE FROM $t WHERE email = ?")->execute([$email]);
            echo "Supprimé (compte, connexions, progression et classement).\n";
            break;
        case 'board-list':
            foreach (db($C)->query('SELECT email, display, profil, xp_board FROM board ORDER BY xp_board DESC') as $r)
                echo $r['display'], "\t", $r['email'], "\t", $r['profil'], "\t", $r['xp_board'], " XP\n";
            break;
        case 'board-hide':
            foreach (['board', 'board_snap'] as $t) db($C)->prepare("DELETE FROM $t WHERE email = ?")->execute([$email]);
            echo "Retiré du classement.\n";
            break;
        case 'board-reset':
            if (!in_array($a, ['week', 'month'], true)) exit("Usage : board-reset week|month\n");
            $k = period_keys(time())[$a];
            db($C)->prepare('DELETE FROM board_snap WHERE period = ?')->execute([$k]);
            db($C)->prepare('INSERT INTO board_snap SELECT email, ?, xp_board, ? FROM board')->execute([$k, time()]);
            echo "Période remise à zéro : $k\n";
            break;
        case 'selftest':
            $C['data_dir'] = sys_get_temp_dir() . '/parcours-selftest-' . getmypid();
            set_password($C, 'test@sattse.com', 'motdepasse-test');
            $u = db($C)->query("SELECT hash FROM users WHERE email = 'test@sattse.com'")->fetch();
            chk(password_verify('motdepasse-test', $u['hash']));
            chk(valid_email($C, 'a@sattse.com') && !valid_email($C, 'a@gmail.com'));
            $t = new_token($C, 'test@sattse.com');
            chk(strlen($t) === 64);
            // Classement
            $C['leaderboard'] = false;
            chk(board_optin($C, 'test@sattse.com', true, 'Testeur')[0] === 403);
            chk(board_view($C, 'test@sattse.com', 'week')[0] === 403);
            $C['leaderboard'] = true; $C['max_xp_per_day'] = 800;
            $save = fn($e, $xp, $pr) => db($C)->prepare('INSERT OR REPLACE INTO saves VALUES(?, ?, 0, 0)')->execute([$e, json_encode(['state' => ['xp' => $xp, 'settings' => ['profil' => $pr]]])]);
            $save('test@sattse.com', 500, 'juriste');
            chk(board_optin($C, 'test@sattse.com', true, 'x')[0] === 400);
            chk(board_optin($C, 'test@sattse.com', true, 'Testeur')[0] === 200);
            $save('b@sattse.com', 0, 'juriste');
            chk(board_optin($C, 'b@sattse.com', true, 'TESTEUR')[0] === 409);
            chk(board_optin($C, 'b@sattse.com', true, 'Bêta')[0] === 200);
            [, $v] = board_view($C, 'test@sattse.com', 'all');
            chk($v['top'][0]['xp'] === 500 && $v['moi']['rang'] === 1);
            [, $v] = board_view($C, 'test@sattse.com', 'week');
            chk($v['moi']['xp'] === 0 && $v['participants'] === 2 && $v['profils'] === []);
            board_on_push($C, 'b@sattse.com', 0, 120, 'juriste');
            board_on_push($C, 'test@sattse.com', 500, 1700, 'juriste');
            [, $v] = board_view($C, 'test@sattse.com', 'week');
            chk($v['top'][0]['display'] === 'Testeur' && $v['top'][0]['xp'] === 800 && $v['top'][1]['xp'] === 120);
            board_on_push($C, 'test@sattse.com', 1700, 1800, 'juriste');
            [, $v] = board_view($C, 'test@sattse.com', 'week');
            chk($v['moi']['xp'] === 800 && $v['collectif']['xp'] === 920);
            chk(board_optin($C, 'b@sattse.com', false, '')[0] === 200);
            [, $v] = board_view($C, 'test@sattse.com', 'week');
            chk($v['participants'] === 1 && board_me($C, 'b@sattse.com')['optin'] === false);
            $n = db($C)->query("SELECT COUNT(*) FROM board_snap WHERE email = 'b@sattse.com'")->fetchColumn();
            chk((int)$n === 0);
            echo "selftest OK\n";
            break;
        default:
            echo "Commandes : list | add <courriel> <mdp> | passwd <courriel> <mdp> | delete <courriel> | board-list | board-hide <courriel> | board-reset week|month | selftest\n";
    }
    exit;
}

/* ---------- Web ---------- */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function out(int $code, array $body): never { http_response_code($code); echo json_encode($body, JSON_UNESCAPED_UNICODE); exit; }
function body(array $C): array {
    $raw = file_get_contents('php://input', false, null, 0, $C['max_bytes'] + 1);
    if (strlen((string)$raw) > $C['max_bytes']) out(413, ['error' => 'Sauvegarde trop volumineuse.']);
    $j = json_decode((string)$raw, true);
    return is_array($j) ? $j : [];
}
function who(array $C): string {
    if ($C['auth_mode'] === 'remote_user') {
        $u = $_SERVER['REMOTE_USER'] ?? $_SERVER['REDIRECT_REMOTE_USER'] ?? '';
        if ($u === '') out(401, ['error' => 'Authentification du serveur absente.']);
        return norm_email($u);
    }
    $h = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
    if (!preg_match('/^Bearer\s+([a-f0-9]{64})$/', $h, $m)) out(401, ['error' => 'Connexion requise.']);
    $st = db($C)->prepare('SELECT email FROM tokens WHERE hash = ? AND expires > ?');
    $st->execute([hash('sha256', $m[1]), time()]);
    $e = $st->fetchColumn();
    if (!$e) out(401, ['error' => 'Connexion expirée.']);
    return (string)$e;
}

$a = $_GET['a'] ?? '';
$m = $_SERVER['REQUEST_METHOD'];
try {
    if ($a === 'register' && $m === 'POST') {
        if ($C['auth_mode'] !== 'local' || !$C['open_registration']) out(403, ['error' => 'Création de compte fermée : demandez un compte à votre administrateur.']);
        $j = body($C); $email = norm_email((string)($j['email'] ?? '')); $pw = (string)($j['password'] ?? '');
        if (!valid_email($C, $email)) out(400, ['error' => 'Utilisez votre adresse professionnelle.']);
        if (strlen($pw) < 10) out(400, ['error' => 'Mot de passe de 10 caractères minimum.']);
        $st = db($C)->prepare('SELECT 1 FROM users WHERE email = ?'); $st->execute([$email]);
        if ($st->fetchColumn()) out(409, ['error' => 'Ce compte existe déjà : connectez-vous.']);
        set_password($C, $email, $pw);
        out(200, ['token' => new_token($C, $email), 'email' => $email]);
    }
    if ($a === 'login' && $m === 'POST') {
        if ($C['auth_mode'] !== 'local') out(400, ['error' => 'Connexion gérée par le serveur.']);
        $j = body($C); $email = norm_email((string)($j['email'] ?? '')); $pw = (string)($j['password'] ?? '');
        $st = db($C)->prepare('SELECT hash, fails, fail_at FROM users WHERE email = ?'); $st->execute([$email]);
        $u = $st->fetch(PDO::FETCH_ASSOC);
        // Verrou après 10 échecs, levé au bout de 15 minutes.
        if ($u && $u['fails'] >= 10 && time() - (int)$u['fail_at'] < 900) out(429, ['error' => 'Trop d\'essais. Réessayez dans 15 minutes.']);
        if (!$u || !password_verify($pw, $u['hash'])) {
            if ($u) db($C)->prepare('UPDATE users SET fails = fails + 1, fail_at = ? WHERE email = ?')->execute([time(), $email]);
            usleep(400000);
            out(401, ['error' => 'Courriel ou mot de passe incorrect.']);
        }
        db($C)->prepare('UPDATE users SET fails = 0 WHERE email = ?')->execute([$email]);
        out(200, ['token' => new_token($C, $email), 'email' => $email]);
    }
    if ($a === 'logout' && $m === 'POST') {
        $h = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
        if (preg_match('/^Bearer\s+([a-f0-9]{64})$/', $h, $mm)) db($C)->prepare('DELETE FROM tokens WHERE hash = ?')->execute([hash('sha256', $mm[1])]);
        out(200, ['ok' => true]);
    }
    if ($a === 'me' && $m === 'GET') {
        $email = who($C);
        out(200, ['email' => $email, 'mode' => $C['auth_mode'], 'leaderboard' => board_on($C), 'board' => board_on($C) ? board_me($C, $email) : null]);
    }
    if ($a === 'board' && $m === 'GET') { [$code, $res] = board_view($C, who($C), (string)($_GET['p'] ?? 'week')); out($code, $res); }
    if ($a === 'board-optin' && $m === 'PUT') { $j = body($C); [$code, $res] = board_optin($C, who($C), !empty($j['optin']), (string)($j['display'] ?? '')); out($code, $res); }
    if ($a === 'pull' && $m === 'GET') {
        $st = db($C)->prepare('SELECT data, updated FROM saves WHERE email = ?'); $st->execute([who($C)]);
        $r = $st->fetch(PDO::FETCH_ASSOC);
        out(200, ['data' => $r ? json_decode($r['data'], true) : null, 'updatedAt' => $r ? (int)$r['updated'] : 0]);
    }
    if ($a === 'push' && $m === 'PUT') {
        $email = who($C); $j = body($C);
        if (!isset($j['data']['state']) || !is_array($j['data']['state'])) out(400, ['error' => 'Sauvegarde invalide.']);
        $old = save_info($C, $email)['xp'];
        $upd = (int)($j['updatedAt'] ?? 0);
        db($C)->prepare('INSERT INTO saves VALUES(?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET data = excluded.data, updated = excluded.updated, saved_at = excluded.saved_at')
            ->execute([$email, json_encode($j['data'], JSON_UNESCAPED_UNICODE), $upd, time()]);
        $new = save_info($C, $email);
        board_on_push($C, $email, $old, $new['xp'], $new['profil']);
        out(200, ['ok' => true, 'updatedAt' => $upd]);
    }
    out(404, ['error' => 'Action inconnue.']);
} catch (Throwable $e) {
    error_log('parcours sync: ' . $e->getMessage());
    out(500, ['error' => 'Erreur du serveur de synchronisation.']);
}
