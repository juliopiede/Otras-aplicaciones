CREATE TABLE IF NOT EXISTS tenders (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    cpv_code TEXT,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    priority TEXT NOT NULL CHECK (priority IN ('top', 'media', 'baja')),
    status TEXT NOT NULL CHECK (status IN ('Nueva', 'En análisis', 'Decidida', 'Presentada')),
    budget NUMERIC(12,2) NOT NULL DEFAULT 0,
    deadline_at TIMESTAMPTZ,
    source_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tenders_status ON tenders(status);
CREATE INDEX IF NOT EXISTS idx_tenders_priority ON tenders(priority);
CREATE INDEX IF NOT EXISTS idx_tenders_score ON tenders(score DESC);
