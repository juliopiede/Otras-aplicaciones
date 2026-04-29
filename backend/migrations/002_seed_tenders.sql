INSERT INTO tenders (id, title, description, cpv_code, score, priority, status, budget, deadline_at, source_url)
VALUES
('mock-1', 'Servicio de desarrollo web corporativo', 'Portal institucional + SEO', '72413000', 82, 'top', 'Nueva', 18000, NOW() + INTERVAL '20 days', 'https://contrataciondelestado.es'),
('mock-2', 'Campaña de marketing digital', 'SEM + Social + analítica', '79342000', 74, 'media', 'En análisis', 12000, NOW() + INTERVAL '12 days', 'https://contrataciondelestado.es'),
('mock-3', 'Mantenimiento web municipal', 'Soporte y mejoras evolutivas', '72415000', 66, 'media', 'Decidida', 9000, NOW() + INTERVAL '18 days', 'https://contrataciondelestado.es')
ON CONFLICT (id) DO NOTHING;
