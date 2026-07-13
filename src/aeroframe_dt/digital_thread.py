"""SQLite-backed revision-aware evidence graph."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Iterable

SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS artifact(id TEXT PRIMARY KEY, kind TEXT NOT NULL, revision TEXT NOT NULL, uri TEXT, sha256 TEXT, status TEXT NOT NULL DEFAULT 'CURRENT', metadata_json TEXT NOT NULL DEFAULT '{}');
CREATE TABLE IF NOT EXISTS link(parent_id TEXT NOT NULL, child_id TEXT NOT NULL, relation TEXT NOT NULL, PRIMARY KEY(parent_id,child_id,relation), FOREIGN KEY(parent_id) REFERENCES artifact(id), FOREIGN KEY(child_id) REFERENCES artifact(id));
CREATE TABLE IF NOT EXISTS invalidation(id INTEGER PRIMARY KEY, artifact_id TEXT NOT NULL, reason TEXT NOT NULL, created_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(artifact_id) REFERENCES artifact(id));
CREATE TABLE IF NOT EXISTS revision_event(id INTEGER PRIMARY KEY, artifact_id TEXT NOT NULL, old_revision TEXT, new_revision TEXT NOT NULL, rationale TEXT NOT NULL, created_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(artifact_id) REFERENCES artifact(id));
'''

class EvidenceGraph:
    def __init__(self,path:str|Path): self.path=Path(path); self.db=sqlite3.connect(path); self.db.row_factory=sqlite3.Row; self.db.executescript(SCHEMA); self._migrate()
    def _migrate(self):
        columns={row[1] for row in self.db.execute('PRAGMA table_info(artifact)')}
        if 'metadata_json' not in columns: self.db.execute("ALTER TABLE artifact ADD COLUMN metadata_json TEXT NOT NULL DEFAULT '{}'")
        self.db.commit()
    def close(self): self.db.close()
    def add_artifact(self,id,kind,revision,uri=None,sha256=None,metadata=None):
        if not all(str(value).strip() for value in (id,kind,revision)): raise ValueError('id, kind, and revision are required')
        self.db.execute("INSERT OR REPLACE INTO artifact(id,kind,revision,uri,sha256,status,metadata_json) VALUES(?,?,?,?,?,'CURRENT',?)",(id,kind,revision,uri,sha256,json.dumps(metadata or {},sort_keys=True))); self.db.commit()
    def link(self,parent_id,child_id,relation):
        if parent_id==child_id: raise ValueError('self-links are not allowed')
        self.db.execute('INSERT OR REPLACE INTO link VALUES(?,?,?)',(parent_id,child_id,relation)); self.db.commit()
    def descendants(self,id):
        q='''WITH RECURSIVE d(id) AS (SELECT child_id FROM link WHERE parent_id=? UNION SELECT link.child_id FROM link JOIN d ON link.parent_id=d.id) SELECT id FROM d ORDER BY id'''
        return [r[0] for r in self.db.execute(q,(id,))]
    def invalidate_downstream(self,id,reason):
        ids=[id]+self.descendants(id)
        self.db.executemany("UPDATE artifact SET status='STALE' WHERE id=?",[(x,) for x in ids])
        self.db.executemany('INSERT INTO invalidation(artifact_id,reason) VALUES(?,?)',[(x,reason) for x in ids]); self.db.commit(); return ids
    def revise_artifact(self,id,new_revision,rationale,uri=None,sha256=None):
        row=self.db.execute('SELECT revision FROM artifact WHERE id=?',(id,)).fetchone()
        if row is None: raise KeyError(id)
        old=row['revision']
        self.db.execute("UPDATE artifact SET revision=?,uri=COALESCE(?,uri),sha256=COALESCE(?,sha256),status='CURRENT' WHERE id=?",(new_revision,uri,sha256,id))
        self.db.execute('INSERT INTO revision_event(artifact_id,old_revision,new_revision,rationale) VALUES(?,?,?,?)',(id,old,new_revision,rationale)); self.db.commit()
        return self.invalidate_downstream(id,f'{id} revised {old}->{new_revision}: {rationale}')
    def artifact(self,id):
        row=self.db.execute('SELECT * FROM artifact WHERE id=?',(id,)).fetchone()
        if row is None: raise KeyError(id)
        result=dict(row); result['metadata']=json.loads(result.pop('metadata_json')); return result
    def audit(self):
        issues=[]
        for row in self.db.execute('SELECT * FROM link'):
            for key in ('parent_id','child_id'):
                if self.db.execute('SELECT 1 FROM artifact WHERE id=?',(row[key],)).fetchone() is None: issues.append(f"missing artifact {row[key]}")
        cycles=self.db.execute('''WITH RECURSIVE walk(start,id) AS (SELECT parent_id,child_id FROM link UNION ALL SELECT walk.start,link.child_id FROM walk JOIN link ON walk.id=link.parent_id WHERE link.child_id!=walk.start) SELECT DISTINCT start FROM walk WHERE start=id''').fetchall()
        issues.extend(f"dependency cycle involving {row[0]}" for row in cycles)
        return issues
    def export_json(self):
        return {'artifacts':[self.artifact(row['id']) for row in self.db.execute('SELECT id FROM artifact ORDER BY id')], 'links':[dict(row) for row in self.db.execute('SELECT * FROM link ORDER BY parent_id,child_id,relation')], 'audit_issues':self.audit()}
    def export_dot(self):
        lines=['digraph AeroFrameDT {','  rankdir=LR;']
        for row in self.db.execute('SELECT id,kind,revision,status FROM artifact ORDER BY id'):
            label=f"{row['id']}\\n{row['kind']} rev {row['revision']}\\n{row['status']}"; lines.append(f'  "{row["id"]}" [label="{label}"];')
        for row in self.db.execute('SELECT * FROM link ORDER BY parent_id,child_id'):
            lines.append(f'  "{row["parent_id"]}" -> "{row["child_id"]}" [label="{row["relation"]}"];')
        lines.append('}'); return '\n'.join(lines)+'\n'
