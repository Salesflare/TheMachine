"""A project's organization from what the project is about, not from where its people work (2026-11-10). The Machine
fills one in from a project's people (graph.fill_orgs: 'auto', 'backfill'), so a home internet project with a friend got
the friend's employer. Each review gets a batch of those ("Project organizations to check") and keeps or drops each by
what the project is about (finish_analysis orgs); that also goes over the ones stored before this. What the owner or a
review set is never asked about. A drop is logged here and undo_org_checks puts it back."""
import datetime as dt

import graph

SCHEMA = ('CREATE TABLE IF NOT EXISTS project_org_checks(project_id INTEGER PRIMARY KEY,org TEXT NOT NULL,before_by TEXT NOT NULL,run_id TEXT,'
          'tries INTEGER NOT NULL DEFAULT 0,verdict TEXT,decided_at TEXT)')
BATCH = 20  # project organizations for one review to keep or drop
TRIES = 3   # reviews that get one before it is left as it is


def ensure(db):
    db.execute(SCHEMA)


def org_checks_due(db, limit=BATCH):
    """Projects whose organization the Machine filled in from their people (fill_orgs: 'auto', 'backfill') and no review
    has kept or dropped yet: open ones first. What the owner or a review set is never asked about."""
    ensure(db)
    return db.execute("SELECT p.id,p.name,p.org,p.org_by FROM projects p LEFT JOIN project_org_checks c ON c.project_id=p.id "
                      "WHERE p.org IS NOT NULL AND p.org_by IN ('auto','backfill') AND (c.project_id IS NULL OR c.verdict IS NULL AND c.tries<? "
                      "OR c.org<>p.org) ORDER BY p.closed_at IS NOT NULL,p.id DESC LIMIT ?", (TRIES, limit)).fetchall()


def org_check_brief(db, run_id, limit=BATCH):
    """The "Project organizations to check" block for review run_id: each project with the organization the Machine
    gave it and whose work that came from (their names and what they are to the owner), for the review to keep or drop
    by what the project is about (org_check_answer). Marks them as given to this run."""
    lines = []
    for p in org_checks_due(db, limit):
        org = graph.project_org(db, p['org'])
        if not org:
            continue
        people = db.execute("SELECT DISTINCT n.name,json_extract(n.info,'$.role') role FROM graph_nodes n WHERE n.kind='person' "
                            "AND json_extract(n.info,'$.org')=? AND (n.id IN (SELECT node_id FROM project_people WHERE project_id=?) "
                            "OR n.id IN (SELECT a FROM graph_links WHERE b=? AND kind='project') OR n.id IN (SELECT g2.node_id FROM graph_events g "
                            "JOIN graph_events g2 ON g2.event_id=g.event_id WHERE g.node_id=? AND g.probable=0)) LIMIT 3",
                            ('org:' + p['org'], p['id'], 'project:' + str(p['id']), 'project:' + str(p['id']))).fetchall()
        db.execute('INSERT INTO project_org_checks(project_id,org,before_by,run_id,tries) VALUES(?,?,?,?,1) ON CONFLICT(project_id) DO UPDATE SET '
                   'org=excluded.org,before_by=excluded.before_by,run_id=excluded.run_id,verdict=NULL,decided_at=NULL,'
                   'tries=CASE WHEN project_org_checks.org=excluded.org THEN project_org_checks.tries+1 ELSE 1 END', (p['id'], p['org'], p['org_by'], run_id))
        who = ', '.join(r['name'] + (f" ({r['role']})" if r['role'] else '') for r in people)
        lines.append(f"- {p['name']} (project:{p['id']}): {org['name']}" + (f' (where they work: {who})' if who else ''))
    return '\n'.join(lines)


def org_check_answer(db, run_id, answer, now=None):
    """A review that got "Project organizations to check" keeps or drops each one before it finishes: finish_analysis
    orgs [{"project": node_id, "org": "keep" or "drop"}]. Kept: the review's word now (org_by 'review'). Dropped: the
    project has no organization, and fill_orgs leaves it so; logged in project_org_checks (undo_org_checks puts it back).
    One the owner changed since is left as it is. Raises while one is left; returns how many it dropped."""
    ensure(db)
    given = db.execute("SELECT c.project_id,c.org,c.before_by,p.name FROM project_org_checks c JOIN projects p ON p.id=c.project_id "
                       "WHERE c.run_id=? AND c.verdict IS NULL", (run_id,)).fetchall()
    if not given:
        return 0
    if answer is not None and not (isinstance(answer, list) and all(isinstance(a, dict) for a in answer)):
        raise ValueError('finish_analysis orgs is [{"project": "project:<id>", "org": "keep" or "drop"}]')
    said = {}
    for a in answer or []:
        verdict = str(a.get('org') or '').strip().lower()
        if verdict not in ('keep', 'drop'):
            raise ValueError('finish_analysis orgs: each one says "org": "keep" (the project is about that organization) or "drop" (only where someone on it works)')
        said[str(a.get('project') or '').casefold()] = verdict
    left, dropped, now = [], 0, now or dt.datetime.now(dt.timezone.utc).isoformat()
    for r in given:
        verdict = said.get(('project:' + str(r['project_id'])).casefold()) or said.get(r['name'].casefold())
        if not verdict:
            left.append(f"{r['name']} (project:{r['project_id']})")
            continue
        if verdict == 'keep':
            db.execute("UPDATE projects SET org_by='review' WHERE id=? AND org=? AND org_by=?", (r['project_id'], r['org'], r['before_by']))
        elif db.execute("UPDATE projects SET org=NULL,org_by='review' WHERE id=? AND org=? AND org_by=?", (r['project_id'], r['org'], r['before_by'])).rowcount:
            dropped += 1
        db.execute('UPDATE project_org_checks SET verdict=?,decided_at=? WHERE project_id=?', (verdict, now, r['project_id']))
    if left:
        raise ValueError('Project organizations to check: answer ' + ', '.join(left) + ' in finish_analysis orgs [{"project", "org": "keep" or "drop"}]')
    return dropped


def undo_org_checks(db):
    """Puts back the organizations reviews dropped (org_check_answer), where nobody set one since."""
    ensure(db)
    undone = db.execute("UPDATE projects SET org=(SELECT c.org FROM project_org_checks c WHERE c.project_id=projects.id),"
                        "org_by=(SELECT c.before_by FROM project_org_checks c WHERE c.project_id=projects.id) "
                        "WHERE org IS NULL AND org_by='review' AND id IN (SELECT project_id FROM project_org_checks WHERE verdict='drop')").rowcount
    db.execute("DELETE FROM project_org_checks WHERE verdict='drop'")
    return undone
