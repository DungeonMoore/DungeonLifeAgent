# HITO 2: Pipeline de Búsqueda Híbrido Mejorado

## Información General

**Hito**: 2 de 5  
**Estado**: Pendiente  
**Duración Estimada**: 1-2 semanas  
**Propietario**: [Asignar desarrollador]  
**Dependencias**: Hito 1 (Embeddings Avanzados)

## Objetivo Específico

Implementar un pipeline de búsqueda híbrido avanzado con multi-stage retrieval, query expansion automática y context-aware reranking.

## Arquitectura del Pipeline

### Etapas del Nuevo Pipeline

┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE HÍBRIDO AVANZADO                │
├─────────────────────────────────────────────────────────────┤
│  ETAPA 1: LEXICAL RETRIEVAL                                 │
│  ├── BM25 mejorado con expansión de términos                │
│  ├── Búsqueda por n-gramas y frases                         │
│  └── Ranking inicial por relevancia textual                 │
│                                                             │
│  ETAPA 2: SPARSE RETRIEVAL                                  │
│  ├── TF-IDF avanzado con expansión de sinónimos             │
│  ├── Búsqueda por conceptos relacionados                    │
│  └── Filtrado por categorías y metadatos                    │
│                                                             │
│  ETAPA 3: DENSE RETRIEVAL                                   │
│  ├── Embeddings semánticos densos                           │
│  ├── Similitud de coseno avanzada                           │
│  └── Clustering semántico de resultados                     │
│                                                             │
│  ETAPA 4: FUSION Y RE-RANKING                               │
│  ├── Fusión híbrida con pesos dinámicos                     │
│  ├── Re-ranking basado en contexto de usuario              │
│  └── Selección final de documentos relevantes              │
└─────────────────────────────────────────────────────────────┘


## Entregables Específicos

### DE-2.1: Multi-Stage Retrieval
- [ ] Implementar búsqueda léxica mejorada (BM25 + expansión)
- [ ] Crear sistema de sparse retrieval con TF-IDF avanzado
- [ ] Implementar dense retrieval con embeddings mejorados
- [ ] Crear mecanismo de transición suave entre etapas

### DE-2.2: Query Expansion Automática
- [ ] Implementar expansión usando wordnet/synonyms
- [ ] Crear expansión basada en contexto semántico
- [ ] Agregar expansión por reformulación automática
- [ ] Implementar pesos dinámicos para términos expandidos

### DE-2.3: Context-Aware Re-ranking
- [ ] Crear re-ranking basado en rol de usuario
- [ ] Implementar re-ranking por contexto de consulta
- [ ] Agregar señales de calidad de documento
- [ ] Crear sistema de pesos adaptativos

### DE-2.4: Optimización de Performance
- [ ] Implementar early stopping en etapas
- [ ] Crear paralelización de búsquedas
- [ ] Agregar límites inteligentes por etapa
- [ ] Optimizar uso de memoria en pipeline

## Criterios de Aceptación

### Funcionales
- [ ] Pipeline ejecuta todas las etapas automáticamente
- [ ] Query expansion mejora cobertura de resultados
- [ ] Re-ranking context-aware funciona correctamente
- [ ] Compatible con modos existentes (consultor, colaborador, etc.)

### No Funcionales
- [ ] Latencia total del pipeline: < 500ms para consultas típicas
- [ ] Uso de CPU: < 50% durante ejecución normal
- [ ] Memoria: < 200MB adicional al sistema base
- [ ] Throughput: > 100 consultas/segundo

## Tareas Detalladas

### Semana 1: Core del Pipeline
- [ ] Día 1-2: Diseño e implementación de multi-stage retrieval
- [ ] Día 3-4: Desarrollo de query expansion automática
- [ ] Día 5: Integración inicial de etapas

### Semana 2: Optimización y Testing
- [ ] Día 1-2: Implementación de context-aware re-ranking
- [ ] Día 3-4: Optimización de performance y memoria
- [ ] Día 5: Testing completo y ajustes finales

## Recursos Necesarios

### Software
- [ ] Librerías: nltk (para wordnet), scipy (para cálculos avanzados)
- [ ] Modelos de lenguaje para query expansion
- [ ] Base de datos de sinónimos en español

### Datos
- [ ] Corpus de prueba para validar mejoras
- [ ] Queries de ejemplo para benchmarking
- [ ] Ground truth para evaluación

## Riesgos y Mitigación

### Riesgos
1. **Sobre-expansión**: Query expansion puede traer ruido excesivo
2. **Latencia acumulada**: Múltiples etapas pueden sumar latencia
3. **Complejidad de debugging**: Pipeline complejo difícil de debuggear

### Mitigación
1. **Límites inteligentes**: Limitar expansión a términos más relevantes
2. **Early stopping**: Parar etapas cuando se encuentren buenos resultados
3. **Logging granular**: Logging detallado por etapa para debugging

## Comparación con Baseline

### Métricas a Medir
- **Precisión**: NDCG@5, NDCG@10
- **Cobertura**: Recall@10, Recall@20  
- **Diversidad**: Medidas de diversidad de resultados
- **Latencia**: Tiempo total de respuesta

### Benchmarking
- [ ] Crear suite de queries de prueba representativas
- [ ] Medir métricas antes/después de cada mejora
- [ ] Establecer baselines claros para comparación
- [ ] Documentar mejoras obtenidas

## Telemetría Operativa y Contexto para el LLM

- **Trazabilidad del pipeline**: Cada ejecución genera un `PipelineTrace` con etapas (`Recuperación Léxica`, `Fusión Recíproca`, `MMR Diversificación`, `Segmentación`, `Scoring Semántico`, `Selección Final`). Incluye conteos de entrada/salida, parámetros vigentes y highlights de los documentos con puntajes léxicos/semánticos.
- **Acceso programático**: `HybridSearchPipeline.last_trace` y `PipelineTrace.to_prompt()` permiten incorporar la explicación paso a paso en el prompt inicial del LLM, habilitando depuración y respuestas explicables.
- **Calidad de embeddings**: Se captura `EmbeddingQuality` por lote (media, desviación y similitud coseno promedio) para correlacionar resultados con las estrategias de embeddings activas.

## Métricas Offline y Grid Search Recomendado

- **Suite de evaluación** (`dungeon_life_agent.offline_metrics`): provee `evaluate_offline` para calcular Recall@K, MRR@10 y nDCG@10 sobre 30-50 queries representativas antes de llevar cambios a producción.
- **Hiperparámetros a sintonizar**: realizar grid-search sobre `α ∈ {0.4,0.5,0.6,0.7,0.8}`, `N ∈ {30,50,80}` (entrada a MMR), `M ∈ {10,20,30}` (salida MMR), `λ ∈ {0.7,0.8,0.9}` y `β ∈ {0,0.03,0.05,0.1}` mediante `grid_search_hyperparameters`.
- **Reportes**: cada combinación produce `EvaluationReport` con métricas macro y detalle por consulta, facilitando comparativas y decisiones de fine-tuning.

## Estado del Hito

### Checklist de Preparación
- [ ] Hito 1 completado y estable
- [ ] Recursos asignados
- [ ] Entorno de testing listo
- [ ] Métricas de baseline establecidas

### Checklist de Desarrollo
- [ ] DE-2.1 completado
- [ ] DE-2.2 completado
- [ ] DE-2.3 completado  
- [ ] DE-2.4 completado

### Checklist de Validación
- [ ] Tests de integración pasan
- [ ] Benchmarks muestran mejora significativa
- [ ] Performance dentro de límites aceptables
- [ ] Documentación técnica completada

---

*Especificación detallada para el Hito 2 - Pipeline de Búsqueda Híbrido Mejorado*
