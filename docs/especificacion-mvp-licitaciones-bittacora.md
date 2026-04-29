# Especificación funcional MVP — Gestor de licitaciones Bittácora

## 1. Objetivo
Construir una aplicación que ingeste licitaciones de la Plataforma de Contratación del Sector Público (PLACSP), filtre automáticamente oportunidades con encaje para Bittácora, las priorice con scoring y alerte con tiempo suficiente para preparar oferta.

## 2. Alcance del MVP
- Ingesta automática cada 6 horas (configurable).
- Normalización de datos de expediente/lotes/plazos.
- Motor de reglas con:
  - Filtros excluyentes (go/no-go).
  - Filtros de preferencia.
  - Scoring 0–100.
- Dashboard de seguimiento con estados:
  - Nueva
  - En análisis
  - Decidida (sí/no)
  - Presentada
- Alertas por email y Telegram para licitaciones “top”.
- Registro de trazabilidad de decisiones y cambios de estado.

## 3. Perfil Bittácora (reglas de negocio)

### 3.1 Sectores y servicios objetivo
**Principales**
- Desarrollo web corporativo a medida
- Desarrollo eCommerce
- Marketing digital (SEO/SEM/Social)
- Diseño gráfico y branding
- Automatización de procesos (Make, CRM, integraciones)
- Consultoría de transformación digital (Kit Digital / Consulting)

**Secundarios**
- Hosting y mantenimiento web
- Apps web internas
- Analítica web / BI
- Copywriting y contenidos SEO
- Implantación de herramientas digitales (ERP/CRM básicos)
- Formación en digitalización

### 3.2 Palabras clave
**Positivas (boost):**
desarrollo web, diseño web, ecommerce, tienda online, SEO, marketing digital, redes sociales, branding, identidad corporativa, transformación digital, automatización procesos, CRM, UX/UI, posicionamiento web, analítica digital.

**Excluyentes (hard/soft según contexto):**
obra civil, construcción, mantenimiento urbano, limpieza, seguridad, suministro hardware masivo, renting equipos, licencias software cerradas masivas, telecom infra, electricidad, climatización, transporte, catering, sanidad, servicios jurídicos.

### 3.3 CPV
**Núcleo (imprescindible, al menos 1):**
- 72413000
- 72415000
- 72212200
- 72262000
- 79340000
- 79342000
- 79415200

**Adyacentes (score adicional):**
- 72000000
- 72267100
- 72300000
- 79341000
- 80500000
- 48400000

**Excluidos (hard reject salvo lote claramente separado):**
- 45000000
- 50000000
- 60000000
- 90000000
- 30000000
- 48000000

### 3.4 Rango económico
- Mínimo objetivo: 3.000 €
- Máximo objetivo: 120.000 €
- Rango ideal: 8.000 € a 45.000 €
- Lotes pequeños: admitir desde 2.500 € si son rápidos o estratégicos.
- Riesgo de baja temeraria interna: penalizar oportunidades históricamente con expectativa de baja >15–20%.

### 3.5 Geografía
- Cobertura: nacional.
- Preferencias: Extremadura, Andalucía, Madrid, Castilla-La Mancha.
- Penalización: licitaciones con presencialidad intensiva lejos de base operativa.

### 3.6 Requisitos excluyentes
- Solvencia técnica mínima: 2–3 proyectos similares en 3 años + portfolio demostrable.
- Solvencia económica mínima: facturación >= 1x contrato (ideal 1.5x).
- Clasificación empresarial: no obligatoria; descartar si exigen clasificación alta no disponible.
- UTE: permitida solo con socio complementario y margen garantizado.
- Certificaciones: ISO 9001/27001 deseable, no excluyente salvo exigencia explícita.
- Procedimientos admitidos: abierto, abierto simplificado, simplificado abreviado.
- Evitar: negociado sin publicidad.
- Plazo mínimo para oferta: 10 días naturales (ideal 15+).

### 3.7 Reglas estratégicas
1. **Filtro anti-licitación trampa**
   - Descarta si hay requisitos desproporcionados para importe o pliego excesivamente ambiguo con precio bajo.
2. **Filtro cliente interesante**
   - Bonifica administraciones recurrentes, posibilidad de continuidad y escalabilidad.
3. **Filtro encaje real**
   - Penaliza si >40% del objeto está fuera del core Bittácora.

## 4. Motor de decisión: reglas exactas

### 4.1 Filtro duro (go/no-go)
Descartar licitación si se cumple cualquier condición:
1. No contiene CPV núcleo ni CPV adyacente.
2. Contiene CPV excluido como objeto principal (si no hay separación por lotes).
3. Presupuesto < 2.500 € o > 120.000 €.
4. Procedimiento no admitido.
5. Plazo < 10 días naturales.
6. Requiere clasificación empresarial no disponible para Bittácora.
7. Solvencia exigida no alcanzable (técnica o económica).

### 4.2 Filtro blando
- Penalizar presencialidad alta fuera de zonas preferentes.
- Penalizar objetos mixtos con más del 40% no-core.
- Bonificar cliente recurrente o estratégico.

## 5. Scoring (0–100)

### 5.1 Pesos base
- CPV coincidente: 35
- Rango económico: 20
- Ubicación: 10
- Tipo contrato/procedimiento: 15
- Solvencia/clasificación: 15
- Margen temporal: 5

### 5.2 Fórmula
`score_total = cpv + economico + ubicacion + procedimiento + solvencia + plazo + ajustes_estrategicos`

`ajustes_estrategicos` se acota en `[-10, +10]` y después se normaliza `0..100`.

### 5.3 Umbrales de prioridad
- **Top:** >= 75
- **Media:** 60–74
- **Baja:** < 60

### 5.4 Tabla de puntuación operativa
- `score_cpv`
  - 35: CPV núcleo
  - 22: solo CPV adyacente
  - 0: sin match
- `score_budget`
  - 20: 8.000–45.000 €
  - 14: 3.000–7.999 € o 45.001–120.000 €
  - 8: 2.500–2.999 € (solo estratégico)
  - 0: resto
- `score_geo`
  - 10: Extremadura/Andalucía/Madrid/CLM o remoto total
  - 6: resto nacional con baja presencialidad
  - 2: alta presencialidad fuera de preferentes
- `score_proc`
  - 15: abierto / abierto simplificado / simplificado abreviado
  - 0: resto
- `score_solvency`
  - 15: cumple sobrado (>=1.5x y experiencia clara)
  - 10: cumple mínimo
  - 0: no cumple
- `score_deadline`
  - 5: >=15 días
  - 3: 10–14 días
  - 0: <10 días

## 6. Arquitectura técnica recomendada
- **Backend:** FastAPI (Python)
- **DB:** PostgreSQL
- **Worker:** Celery + Redis (cola/tareas)
- **Scheduler:** Celery Beat (o cron externo)
- **Frontend:** Next.js (dashboard)
- **Notificaciones:** Telegram Bot API + SMTP
- **Infra:** Docker Compose (MVP), despliegue en VPS (Hetzner/Render/Fly)

## 7. Modelo de datos (MVP)

### 7.1 Tablas principales
- `tender_sources`
- `tenders`
- `tender_lots`
- `tender_documents`
- `tender_requirements`
- `tender_scores`
- `tender_status_history`
- `organizations`
- `alerts`
- `user_preferences`

### 7.2 Campos críticos
**tenders**
- `external_id` (único)
- `title`, `description`, `contracting_authority`
- `cpv_codes` (array)
- `procedure_type`
- `budget_base`, `budget_total`, `currency`
- `region`, `province`, `municipality`, `onsite_required`
- `published_at`, `deadline_at`
- `source_url`, `raw_payload` (jsonb)

**tender_scores**
- `tender_id`
- `score_total`
- `score_cpv`, `score_budget`, `score_geo`, `score_proc`, `score_solvency`, `score_deadline`
- `adjustment_trap`, `adjustment_client`, `adjustment_fit`
- `classification` (top/media/baja)
- `exclusion_reason` (nullable)
- `scored_at`

## 8. Flujo operativo
1. Ingesta (cada 6h) y deduplicación por `external_id`.
2. Parsing de campos y CPV.
3. Evaluación de filtros duros.
4. Scoring y clasificación.
5. Alta en dashboard con estado `Nueva`.
6. Alertas automáticas:
   - Enviar si `Top` o si `Media` con criterio estratégico.
7. Gestión interna del ciclo (análisis/decisión/presentación).

## 9. Alertas

### 9.1 Telegram
- Trigger inmediato en nuevas `Top`.
- Mensaje con título, organismo, presupuesto, plazo, score y enlace.

### 9.2 Email
- Resumen diario + alertas inmediatas `Top`.
- Plantilla con bloques por prioridad.

## 10. Roadmap de 4 semanas

### Semana 1 — Cimientos
- Esquema BD + migraciones.
- Cliente ingesta PLACSP y normalización básica.
- Dashboard mínimo (listado y detalle).

### Semana 2 — Reglas y scoring
- Implementar filtros hard/soft.
- Implementar scoring y clasificación.
- Persistencia de histórico de score.

### Semana 3 — Flujo operativo
- Estados de oportunidad + trazabilidad.
- Filtros en UI.
- Export CSV básico.

### Semana 4 — Alertas y hardening
- Telegram + email.
- Configuración de perfil editable.
- Observabilidad mínima (logs/errores/reintentos).
- Pruebas de regresión y checklist de despliegue.

## 11. Criterios de aceptación MVP
- Ingesta automática estable (>=95% ejecuciones sin error).
- Scoring reproducible y explicable por licitación.
- Alertas `Top` en <5 minutos tras ingesta.
- Capacidad de gestionar pipeline completo desde dashboard.

## 12. Pendientes abiertos para versión 1.1
- Conectar histórico de adjudicaciones para estimar presión de baja por organismo/CPV.
- Añadir explicación trazable “por qué entró/no entró” en UI por cada regla.
- Introducir aprendizaje de feedback comercial (ganada/perdida) para recalibrar pesos.
