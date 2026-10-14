-- ScopeShield Tiger seed — run README §7.1 DDL first, then this.
-- Inserts the 14-clause demo SOW skeleton (embeddings filled by backend).
-- Usage: psql $DATABASE_URL -f scripts/seed_tiger.sql
INSERT INTO projects (project_id, project_name, client_name, contracted_hourly_rate)
VALUES ('00000000-0000-0000-0000-000000000001', 'BrightKart Website', 'BrightKart Retail', 60.00)
ON CONFLICT (project_id) DO NOTHING;

-- NOTE: embeddings are 768-d from nomic-embed-text at runtime.
-- This seed only proves the table shape; backend upserts real vectors.
SELECT 'seed ok — index demo SOW via POST /api/projects/{id}/sow' AS status;
