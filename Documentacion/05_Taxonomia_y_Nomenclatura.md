---
title: "Taxonomía y Nomenclatura del Dungeon Life Agent"
version: "1.0.0"
date: "2025-10-07"
status: "active"
author: "Dungeon Life Agent Team"
tags: ["taxonomia", "nomenclatura", "clasificacion", "dominios", "roles-especificos"]
machine_readable_spec:
  schema_version: "1.0"
  ai_compatibility: true
  export_formats: ["markdown", "html", "pdf", "json"]
  taxonomy_system:
    roles_based: "Clasificación primaria por especialización del equipo"
    domains_based: "Clasificación secundaria por dominio de conocimiento"
    adaptive_routing: "Ruteo automático según contexto y rol"
---

# 📚 Taxonomía y Nomenclatura del Dungeon Life Agent

## 🎯 Introducción al Sistema de Taxonomía

El sistema de taxonomía del Dungeon Life Agent está diseñado para proporcionar una clasificación precisa y útil del conocimiento dentro del ecosistema DLE. Se organiza en **dos dimensiones principales**:

1. **Por Roles Específicos**: Clasificación primaria según la especialización del usuario
2. **Por Dominios de Conocimiento**: Clasificación secundaria según el área temática

Esta organización dual permite máxima precisión en el ruteo de consultas y adaptación automática de respuestas.

---

## 👥 Clasificación de Consultas por Roles Específicos

### 🎭 Guionista - Especialista en Narrativa y Diálogos

**Dominios de Conocimiento Específicos:**

#### Dominio de Guion (Narrativa Especializada)
```yaml
guionista_taxonomy:
  argumento:
    palabras_clave: ["argumento", "trama", "arco principal", "historia central"]
    archivos_tipo: ["DLE_400_*.md", "ARGUMENTO.md", "Flow_Argumento.md"]
    ejemplos_consultas:
      - "¿Cuál es el arco principal del Acto 1?"
      - "¿Cómo evoluciona la trama en Eldertown?"
      - "¿Cuál es el conflicto central de la historia?"

  world_building:
    palabras_clave: ["mundo", "cosmogonía", "lore", "cosmología", "razas","geografía"]
    archivos_tipo: ["WLD_*.md", "DLE_400_World_*.md"]
    ejemplos_consultas:
      - "¿Cómo funciona la magia en este universo?"
      - "¿Cuáles son las reglas del mundo establecido?"
      - "¿Qué lugares están definidos para esta región?"

  historia_personajes:
    palabras_clave: ["personaje", "arco personaje", "desarrollo", "motivación"]
    archivos_tipo: ["ECH_*.md", "CHAR_*.fes.yml", "REL_CHAR_*.md"]
    ejemplos_consultas:
      - "¿Cuál es el arco de desarrollo de Bromar?"
      - "¿Qué motiva al personaje Grim?"
      - "¿Cómo evolucionó la relación entre Juan y Aeliana?"

  quests_misiones:
    palabras_clave: ["quest", "misión", "objetivo", "aventura"]
    archivos_tipo: ["QUE_*.md", "EQUE_*.md", "DLE_400_Quest_*.md"]
    ejemplos_consultas:
      - "¿Qué quests están disponibles en Eldertown?"
      - "¿Cómo estructurar esta cadena de misiones?"
      - "¿Qué objetivos tiene el personaje en esta aventura?"

  eventos_temporales:
    palabras_clave: ["evento", "suceso", "cronología", "timeline"]
    archivos_tipo: ["EVT_*.md", "DLE_400_Event_*.md"]
    ejemplos_consultas:
      - "¿Qué eventos ocurren en esta cronología?"
      - "¿Cómo se conecta este suceso con la trama principal?"
      - "¿Qué eventos históricos afectan a este personaje?"

  dialogos_conversaciones:
    palabras_clave: ["diálogo", "conversación", "habla", "interacción"]
    archivos_tipo: ["DLE_400_Dialogo_*.md", "Escena_*_Testigo.md"]
    ejemplos_consultas:
      - "¿Dónde está el diálogo inicial de Juan y Bromar?"
      - "¿Qué conversaciones están definidas para esta escena?"
      - "¿Cómo habla este personaje según su personalidad?"
```

### ⚙️ Game Designer (GDD) - Diseñador de Mecánicas y Sistemas

**Dominios de Conocimiento Específicos:**

```yaml
game_designer_taxonomy:
  mecanicas_juego:
    palabras_clave: ["mecánica", "regla", "sistema", "gameplay"]
    archivos_tipo: ["GDD_*.md", "DLE_210_*.md", "MECHANICS_*.md"]
    ejemplos_consultas:
      - "¿Qué mecánicas de combate están definidas?"
      - "¿Cómo funciona el sistema de cartas?"
      - "¿Cuáles son las reglas del modo de juego?"

  balance_equilibrio:
    palabras_clave: ["balance", "equilibrio", "stats", "poder"]
    archivos_tipo: ["GDD_214_DECK_30_Balanceo.md", "BALANCE_*.md"]
    ejemplos_consultas:
      - "¿Está balanceado este personaje?"
      - "¿Cómo equilibrar estas mecánicas?"
      - "¿Qué stats necesita ajuste?"

  progresion_desarrollo:
    palabras_clave: ["progresión", "nivel", "evolución", "crecimiento"]
    archivos_tipo: ["GDD_301_PROG_*.md", "PROGRESION_*.md"]
    ejemplos_consultas:
      - "¿Cómo progresa el jugador en el juego?"
      - "¿Qué niveles están definidos?"
      - "¿Cómo evoluciona este personaje?"

  economia_recursos:
    palabras_clave: ["economía", "moneda", "recursos", "tienda"]
    archivos_tipo: ["GDD_304_ECON_*.md", "ECONOMIA_*.md"]
    ejemplos_consultas:
      - "¿Cómo funciona la economía del juego?"
      - "¿Qué recursos están disponibles?"
      - "¿Cómo se obtienen las monedas?"

  crafting_creacion:
    palabras_clave: ["crafting", "creación", "fabricación", "construcción"]
    archivos_tipo: ["GDD_305_CRAFT_*.md", "CRAFTING_*.md"]
    ejemplos_consultas:
      - "¿Qué sistemas de crafting existen?"
      - "¿Cómo se fabrica este objeto?"
      - "¿Qué materiales se necesitan?"
```

### 🎨 Conceptualista - Artista Conceptual y Visión Visual

**Dominios de Conocimiento Específicos:**

```yaml
conceptualista_taxonomy:
  concept_art_general:
    palabras_clave: ["concept", "arte conceptual", "boceto", "diseño"]
    archivos_tipo: ["Concept_*.png", "Moodboard_*.md", "Design_*.psd"]
    ejemplos_consultas:
      - "¿Qué concept art existe para este personaje?"
      - "¿Dónde están los bocetos iniciales?"
      - "¿Qué diseños están aprobados?"

  mood_paleta_colores:
    palabras_clave: ["mood", "paleta", "colores", "atmósfera", "ambiente"]
    archivos_tipo: ["Moodboard_*.png", "Palette_*.md", "Color_*.json"]
    ejemplos_consultas:
      - "¿Cuál es la paleta de colores para esta ubicación?"
      - "¿Qué mood está definido para esta escena?"
      - "¿Qué colores representan esta facción?"

  estilo_visual_guias:
    palabras_clave: ["estilo", "guía", "referencia", "inspiración"]
    archivos_tipo: ["Style_Guide_*.md", "Referencias_*.md", "Inspiration_*.png"]
    ejemplos_consultas:
      - "¿Qué guía de estilo debo seguir?"
      - "¿Dónde están las referencias visuales?"
      - "¿Qué inspiraciones están definidas?"

  arquitectura_ambientes:
    palabras_clave: ["arquitectura", "ambiente", "escenario", "ubicación"]
    archivos_tipo: ["LOC_*.md", "Environment_*.md", "Architecture_*.png"]
    ejemplos_consultas:
      - "¿Cómo es la arquitectura de Eldertown?"
      - "¿Qué ambientes están definidos?"
      - "¿Dónde están los diseños de ubicaciones?"
```

### 🏗️ 3D Artists - Especialistas en Producción 3D

**Dominios de Conocimiento Específicos por Sub-Rol:**

#### Modeladores 3D
```yaml
modelador_taxonomy:
  geometria_topologia:
    palabras_clave: ["geometría", "topología", "mesh", "polígonos"]
    archivos_tipo: [".blend", ".ztl", "Model_*.fbx"]
    ejemplos_consultas:
      - "¿Este modelo tiene buena topología?"
      - "¿Cuántos polígonos tiene este mesh?"
      - "¿Dónde están los modelos similares?"

  rigging_bones:
    palabras_clave: ["rig", "bones", "esqueleto", "animación"]
    archivos_tipo: ["Rig_*.blend", "Skeleton_*.fbx"]
    ejemplos_consultas:
      - "¿Este rig es correcto para el personaje?"
      - "¿Cuántos bones tiene este esqueleto?"
      - "¿Dónde están los rigs de referencia?"
```

#### Texturizadores 3D
```yaml
texturizador_taxonomy:
  materiales_texturas:
    palabras_clave: ["material", "textura", "shader", "pbr"]
    archivos_tipo: [".spp", "Texture_*.png", "Material_*.json"]
    ejemplos_consultas:
      - "¿Qué materiales están definidos?"
      - "¿Dónde están las texturas base?"
      - "¿Qué shaders debo usar?"

  optimizacion_rendimiento:
    palabras_clave: ["optimización", "rendimiento", "performance", "LOD"]
    archivos_tipo: ["Optimization_*.md", "Performance_*.json"]
    ejemplos_consultas:
      - "¿Cómo optimizar este material?"
      - "¿Qué LODs están definidos?"
      - "¿Dónde están las guías de rendimiento?"
```

#### Animadores 3D
```yaml
animador_taxonomy:
  animaciones_movimiento:
    palabras_clave: ["animación", "movimiento", "timeline", "keyframes"]
    archivos_tipo: ["Animation_*.fbx", "Anim_*.blend"]
    ejemplos_consultas:
      - "¿Qué animaciones están disponibles?"
      - "¿Dónde están las animaciones de referencia?"
      - "¿Cómo se mueve este personaje?"

  cinematica_escenas:
    palabras_clave: ["cinemática", "escena", "cámara", "secuencia"]
    archivos_tipo: ["Cinematic_*.md", "Scene_*.fbx"]
    ejemplos_consultas:
      - "¿Qué escenas cinemáticas están definidas?"
      - "¿Dónde están las referencias de cámara?"
      - "¿Cómo se estructura esta secuencia?"
```

#### Technicals 3D (Artistas Técnicos)
```yaml
technical_taxonomy:
  pipeline_produccion:
    palabras_clave: ["pipeline", "producción", "workflow", "estándares"]
    archivos_tipo: ["Pipeline_*.md", "Technical_*.md"]
    ejemplos_consultas:
      - "¿Cuál es el pipeline de producción?"
      - "¿Qué estándares técnicos debo seguir?"
      - "¿Dónde está la guía técnica?"

  optimizacion_tecnica:
    palabras_clave: ["optimización", "técnico", "performance", "eficiencia"]
    archivos_tipo: ["Optimization_*.md", "Technical_Specs_*.json"]
    ejemplos_consultas:
      - "¿Cómo optimizar este asset?"
      - "¿Qué especificaciones técnicas aplicar?"
      - "¿Dónde están las métricas de performance?"
```

### 📋 Project Managers/Productores - Gestión y Coordinación

**Dominios de Conocimiento Específicos:**

```yaml
project_manager_taxonomy:
  estado_progreso:
    palabras_clave: ["estado", "progreso", "avance", "completitud"]
    archivos_tipo: ["Status_*.md", "Progress_*.json"]
    ejemplos_consultas:
      - "¿Cuál es el estado actual del proyecto?"
      - "¿Qué tareas están completadas?"
      - "¿Dónde está el reporte de progreso?"

  dependencias_tareas:
    palabras_clave: ["dependencia", "bloqueo", "prerrequisito", "orden"]
    archivos_tipo: ["Dependencies_*.md", "Tasks_*.json"]
    ejemplos_consultas:
      - "¿Qué bloquea esta tarea?"
      - "¿Qué depende de este entregable?"
      - "¿Cuál es el orden de tareas?"

  recursos_asignacion:
    palabras_clave: ["recurso", "asignación", "equipo", "capacidad"]
    archivos_tipo: ["Resources_*.md", "Team_*.json"]
    ejemplos_consultas:
      - "¿Qué recursos están disponibles?"
      - "¿Quién está asignado a esta tarea?"
      - "¿Dónde está la planificación de recursos?"

  timeline_fechas:
    palabras_clave: ["timeline", "fecha", "entrega", "milestone"]
    archivos_tipo: ["Timeline_*.md", "Milestones_*.json"]
    ejemplos_consultas:
      - "¿Cuál es el timeline del proyecto?"
      - "¿Cuándo está planificada esta entrega?"
      - "¿Dónde están los milestones definidos?"
```

### 🎬 Director - Visión Creativa General y Dirección Artística

**Dominios de Conocimiento Específicos:**

```yaml
director_taxonomy:
  vision_creativa:
    palabras_clave: ["visión", "creativa", "artística", "dirección"]
    archivos_tipo: ["Vision_*.md", "Creative_*.md"]
    ejemplos_consultas:
      - "¿Cuál es la visión creativa del proyecto?"
      - "¿Qué dirección artística seguir?"
      - "¿Dónde está definida la visión general?"

  coherencia_estilo:
    palabras_clave: ["coherencia", "estilo", "consistencia", "unidad"]
    archivos_tipo: ["Coherence_*.md", "Style_*.md"]
    ejemplos_consultas:
      - "¿Es coherente este elemento con la visión?"
      - "¿Mantiene el estilo establecido?"
      - "¿Dónde están las guías de coherencia?"

  calidad_artistica:
    palabras_clave: ["calidad", "estándar", "excelencia", "producción"]
    archivos_tipo: ["Quality_*.md", "Standards_*.json"]
    ejemplos_consultas:
      - "¿Está este asset a nivel de producción?"
      - "¿Qué estándares de calidad aplicar?"
      - "¿Dónde están las métricas de calidad?"
```

### 🌳 Willow Assistant - Análisis de Coherencia y Trazabilidad FES

**Dominios de Conocimiento Específicos:**

```yaml
willow_taxonomy:
  coherencia_conceptual:
    palabras_clave: ["coherencia", "consistencia", "conceptual", "filosofía"]
    archivos_tipo: ["Coherence_*.md", "Conceptual_*.md"]
    ejemplos_consultas:
      - "¿Es coherente este concepto con el universo?"
      - "¿Mantiene la consistencia filosófica?"
      - "¿Dónde están los análisis de coherencia?"

  trazabilidad_fes:
    palabras_clave: ["trazabilidad", "historia", "evolución", "cambios"]
    archivos_tipo: ["Trace_*.md", "History_*.json"]
    ejemplos_consultas:
      - "¿Cómo ha evolucionado esta entidad?"
      - "¿Cuál es la historia de cambios?"
      - "¿Dónde está el registro de trazabilidad?"

  relaciones_fes:
    palabras_clave: ["relación", "conexión", "dependencia", "red"]
    archivos_tipo: ["Relations_*.md", "Network_*.json"]
    ejemplos_consultas:
      - "¿Qué entidades están relacionadas?"
      - "¿Cómo se conectan estos conceptos?"
      - "¿Dónde está el mapa de relaciones?"
```

---

## 🌍 Clasificación de Consultas por Dominio Específico

### Dominio de Producción - Estado de Procesos y Tareas
```yaml
produccion_taxonomy:
  estado_assets:
    palabras_clave: ["estado", "asset", "completitud", "listo"]
    archivos_tipo: ["Status_*.md", "Assets_*.json"]
    ejemplos_consultas:
      - "¿Qué assets están listos para producción?"
      - "¿Cuál es el estado del personaje Bromar?"
      - "¿Dónde está el reporte de completitud?"

  procesos_activos:
    palabras_clave: ["proceso", "activo", "trabajando", "desarrollo"]
    archivos_tipo: ["Process_*.md", "Active_*.json"]
    ejemplos_consultas:
      - "¿Qué procesos están activos actualmente?"
      - "¿Quién está trabajando en qué?"
      - "¿Dónde está el flujo de trabajo actual?"

  tareas_pendientes:
    palabras_clave: ["tarea", "pendiente", "todo", "por hacer"]
    archivos_tipo: ["Tasks_*.md", "Todo_*.json"]
    ejemplos_consultas:
      - "¿Qué tareas están pendientes?"
      - "¿Qué necesita completarse?"
      - "¿Dónde está la lista de tareas?"
```

### Dominio de World Building - Construcción de Mundo Independiente
```yaml
world_building_taxonomy:
  cosmologia_magia:
    palabras_clave: ["cosmología", "magia", "universo", "realidad"]
    archivos_tipo: ["WLD_000_*.md", "WLD_001_*.md", "Cosmologia_*.md"]
    ejemplos_consultas:
      - "¿Cómo funciona la magia en este universo?"
      - "¿Cuál es la cosmología establecida?"
      - "¿Dónde están las reglas del mundo?"

  historia_geografia:
    palabras_clave: ["historia", "geografía", "ubicación", "lugar"]
    archivos_tipo: ["WLD_101_*.md", "WLD_LOC_*.md", "Historia_*.md"]
    ejemplos_consultas:
      - "¿Cuál es la historia de Eldertown?"
      - "¿Qué ubicaciones están definidas?"
      - "¿Dónde están los mapas geográficos?"

  religiones_cultos:
    palabras_clave: ["religión", "culto", "fe", "creencia"]
    archivos_tipo: ["WLD_200_*.md", "EREL_*.md", "Religion_*.md"]
    ejemplos_consultas:
      - "¿Qué religiones están definidas?"
      - "¿Dónde están los cultos establecidos?"
      - "¿Cuál es el sistema de fe del mundo?"

  facciones_culturas:
    palabras_clave: ["facción", "cultura", "clan", "sociedad"]
    archivos_tipo: ["WLD_300_*.md", "EFAC_*.md", "ECUL_*.md"]
    ejemplos_consultas:
      - "¿Qué facciones existen?"
      - "¿Dónde están las culturas definidas?"
      - "¿Cuál es la estructura social?"

  razas_especies:
    palabras_clave: ["raza", "especie", "pueblo", "habitante"]
    archivos_tipo: ["WLD_400_*.md", "Raza_*.md", "Especie_*.md"]
    ejemplos_consultas:
      - "¿Qué razas están definidas?"
      - "¿Dónde están los perfiles de especies?"
      - "¿Cuál es la diversidad biológica?"
```

### Dominio de Red de Relaciones FES - Conexiones entre Entidades
```yaml
fes_network_taxonomy:
  relaciones_personajes:
    palabras_clave: ["relación", "personaje", "conexión", "vínculo"]
    archivos_tipo: ["REL_CHAR_*.md", "REL_*.md", "Relationship_*.md"]
    ejemplos_consultas:
      - "¿Qué relaciones tiene Bromar?"
      - "¿Cómo se conecta este personaje?"
      - "¿Dónde están los vínculos definidos?"

  relaciones_ubicaciones:
    palabras_clave: ["ubicación", "lugar", "espacio", "geografía"]
    archivos_tipo: ["LOC_*.md", "Place_*.md", "Location_*.md"]
    ejemplos_consultas:
      - "¿Qué lugares están conectados?"
      - "¿Dónde se ubica este personaje?"
      - "¿Cuál es la red geográfica?"

  relaciones_items:
    palabras_clave: ["item", "objeto", "artefacto", "equipamiento"]
    archivos_tipo: ["ITM_*.md", "Item_*.md", "Equipment_*.md"]
    ejemplos_consultas:
      - "¿Qué objetos están relacionados?"
      - "¿Dónde se obtiene este item?"
      - "¿Cuál es la cadena de objetos?"

  relaciones_facciones:
    palabras_clave: ["facción", "organización", "grupo", "alianza"]
    archivos_tipo: ["EFAC_*.md", "Faction_*.md", "Organization_*.md"]
    ejemplos_consultas:
      - "¿Qué facciones están conectadas?"
      - "¿Dónde están las alianzas definidas?"
      - "¿Cuál es la red política?"

  relaciones_religiones:
    palabras_clave: ["religión", "creencia", "fe", "espiritual"]
    archivos_tipo: ["EREL_*.md", "Religion_*.md", "Belief_*.md"]
    ejemplos_consultas:
      - "¿Qué religiones están relacionadas?"
      - "¿Dónde están las conexiones espirituales?"
      - "¿Cuál es la red de creencias?"
```

---

## 📁 Sistema de Nomenclatura Específico

### Convenciones Generales del Atlas
```yaml
nomenclatura_base:
  prefijo_entidad: "DLE_"           # Dungeon Life Ecosystem
  separador: "_"                   # Separador estándar
  formato_version: "_v[0-9]+"      # Versionado

  estructura_documentos:
    formato: "DLE_[Pilar][Secuencia]_[Tipo]_[Nombre].[ext]"
    ejemplo: "DLE_501_FES_Character.md"

  estructura_assets:
    formato: "[Entidad]_[Tipo]_[Subtipo]_[Descriptor]_v[Version].[ext]"
    ejemplo: "Bromar_Portrait_FullBody_FINAL_v1.png"

  estados_archivo:
    work_in_progress: "_WIP_v[0-9]+"
    draft: "_DRAFT_v[0-9]+"
    review: "_REVIEW_v[0-9]+"
    final: "_FINAL_v[0-9]+"
    legacy: "_LEGACY_v[0-9]+"
```

### Nomenclatura Específica del Agente
```yaml
agent_nomenclatura:
  operaciones_agente:
    consultas: "QRY_[Fecha]_[Rol]_[Dominio].[ext]"
    sugerencias: "SGG_[Fecha]_[Rol]_[Dominio].[ext]"
    modificaciones: "MOD_[Fecha]_[Rol]_[Dominio].[ext]"

  archivos_internos:
    contexto_conversacion: "CTX_[Usuario]_[Fecha]_[Tema].json"
    historial_operaciones: "LOG_[Fecha]_[Operacion].json"
    backups_automaticos: "BKP_[Fecha]_[ArchivoOriginal].bak"

  reportes_generados:
    analisis_completo: "RPT_[Fecha]_ANALYSIS_[Dominio].md"
    estado_proyecto: "RPT_[Fecha]_STATUS_[Rol].md"
    recomendaciones: "RPT_[Fecha]_RECOMMENDATIONS_[Especialidad].md"
```

### Estados de Archivo Especializados
```yaml
archivo_estados:
  documentos_narrativos:
    borrador_guion: "_DRAFT_v[0-9]+"
    escena_completa: "_SCENE_v[0-9]+"
    arco_definido: "_ARC_v[0-9]+"
    final_aprobado: "_FINAL_v[0-9]+"

  assets_3d:
    modelado_base: "_MODEL_v[0-9]+"
    sculpt_completo: "_SCULPT_v[0-9]+"
    texturizado: "_TEXTURE_v[0-9]+"
    rigged: "_RIGGED_v[0-9]+"
    animado: "_ANIMATED_v[0-9]+"
    optimizado: "_OPTIMIZED_v[0-9]+"
    final_produccion: "_FINAL_v[0-9]+"

  documentos_tecnicos:
    especificacion: "_SPEC_v[0-9]+"
    implementacion: "_IMPL_v[0-9]+"
    validacion: "_VALID_v[0-9]+"
    documentacion: "_DOC_v[0-9]+"
```

---

## 🎯 Taxonomía de Respuestas por Rol

### Adaptación Automática de Formato

#### Para Guionistas - Respuestas Narrativas
```yaml
guionista_response_format:
  enfoque: "narrativo y creativo"
  estructura_respuesta:
    contexto_narrativo: "Referencia al arco o escena relacionada"
    elementos_clave: "Personajes, conflictos, motivaciones"
    sugerencias_creativas: "Ideas para desarrollo narrativo"
    referencias_cruzadas: "Conexiones con otros elementos"

  ejemplo_formato:
    "¿Cuál es el arco de desarrollo de Bromar?"
    → "Contexto: Bromar es el mentor veterano (DLE_500_CHAR_Bromar.fes.yml)
        Arco: Veterano traumado → Mentor sabio → Guardián legendario
        Elementos clave: Narcolepsia, Ruperto, relación con Juan
        Sugerencia: Desarrollar más la relación mentor-aprendiz"
```

#### Para Game Designers - Respuestas Técnicas
```yaml
gamedesigner_response_format:
  enfoque: "técnico y sistémico"
  estructura_respuesta:
    especificaciones_tecnicas: "Mecánicas, reglas, sistemas"
    analisis_balance: "Stats, comparaciones, equilibrio"
    referencias_documentacion: "GDD específica, estándares"
    recomendaciones_implementacion: "Cómo aplicar técnicamente"

  ejemplo_formato:
    "¿Está balanceado este personaje?"
    → "Análisis técnico: Stats actuales vs estándares GDD
        Comparación: Similar a personajes establecidos
        Recomendación: Ajuste de HP +5 para balance óptimo
        Documentación: DLE_214_DECK_30_Balanceo.md"
```

#### Para 3D Artists - Respuestas Técnicas Visuales
```yaml
artist3d_response_format:
  enfoque: "técnico y visual"
  estructura_respuesta:
    especificaciones_tecnicas: "Polycount, texturas, performance"
    referencias_visuales: "Concept art, referencias similares"
    recomendaciones_tecnicas: "Optimización, estándares, mejores prácticas"
    alternativas_visuales: "Opciones creativas dentro de límites técnicos"

  ejemplo_formato:
    "¿Está optimizado este modelo?"
    → "Análisis técnico: 15,420 polígonos (dentro de límites ✅)
        Texturas: 2K PBR (óptimas ✅)
        Recomendación: Crear LODs para mejor performance
        Referencias: Modelos similares en carpeta NPCs/"
```

---

## 🧠 Sistema de Ruteo Inteligente

### Algoritmo de Clasificación Automática

```python
class IntelligentRouter:
    def __init__(self):
        self.role_classifier = RoleBasedClassifier()
        self.domain_classifier = DomainBasedClassifier()
        self.context_analyzer = ContextAnalyzer()

    async def route_query(self, query, user_context):
        """Ruteo inteligente de consultas"""

        # 1. Análisis de intención de consulta
        intent_analysis = await self.analyze_query_intent(query)

        # 2. Detección automática del rol del usuario
        detected_role = await self.role_classifier.detect_role(
            query, user_context, intent_analysis
        )

        # 3. Clasificación por dominio específico
        domain_classification = await self.domain_classifier.classify_domain(
            query, detected_role, intent_analysis
        )

        # 4. Ruteo a modo operativo apropiado
        operation_mode = await self.determine_operation_mode(
            intent_analysis, detected_role, domain_classification
        )

        # 5. Selección de respuesta especializada
        response_strategy = await self.select_response_strategy(
            detected_role, domain_classification, operation_mode
        )

        return {
            "detected_role": detected_role,
            "domain_classification": domain_classification,
            "operation_mode": operation_mode,
            "response_strategy": response_strategy,
            "confidence_score": await self.calculate_confidence(intent_analysis)
        }
```

### Matriz de Ruteo por Rol y Dominio

| Rol | Dominio Narrativa | Dominio Técnica | Dominio Assets | Dominio Producción |
|-----|-------------------|-----------------|----------------|-------------------|
| **Guionista** | Modo 1 → 3 | Modo 1 | Modo 1 | Modo 1 |
| **Game Designer** | Modo 1 | Modo 1 → 2 → 3 | Modo 1 | Modo 1 → 2 |
| **3D Artist** | Modo 1 | Modo 1 → 2 | Modo 1 → 2 → 3 | Modo 1 |
| **Project Manager** | Modo 1 | Modo 1 → 2 | Modo 1 | Modo 1 → 2 → 3 |

---

## 📊 Métricas de Efectividad de Taxonomía

### Métricas de Precisión de Clasificación
```yaml
precision_metrics:
  role_detection_accuracy:
    objetivo: ">95%"
    medicion: "Porcentaje de detección correcta de rol del usuario"
    ejemplos:
      - "Consulta sobre diálogos" → Guionista (correcto)
      - "Consulta sobre mecánicas" → Game Designer (correcto)
      - "Consulta sobre modelos 3D" → 3D Artist (correcto)

  domain_classification_accuracy:
    objetivo: ">90%"
    medicion: "Porcentaje de clasificación correcta de dominio"
    ejemplos:
      - "Consulta sobre arco de personaje" → Dominio de Guion (correcto)
      - "Consulta sobre balance" → Dominio Técnico (correcto)
      - "Consulta sobre estado" → Dominio de Producción (correcto)

  response_relevance:
    objetivo: ">85%"
    medicion: "Porcentaje de respuestas relevantes según rol"
    ejemplos:
      - Guionista recibe ejemplos narrativos (relevante)
      - Game Designer recibe análisis técnicos (relevante)
      - 3D Artist recibe especificaciones técnicas (relevante)
```

### Métricas de Utilidad Práctica
```yaml
utility_metrics:
  tiempo_respuesta_promedio:
    objetivo: "<5 segundos"
    medicion: "Tiempo desde consulta hasta respuesta inicial"
    por_rol:
      guionista: "<4 segundos"
      game_designer: "<5 segundos"
      artist_3d: "<6 segundos"
      project_manager: "<4 segundos"

  completitud_informacion:
    objetivo: ">90%"
    medicion: "Porcentaje de consultas respondidas completamente"
    factores:
      - Información disponible en el ecosistema
      - Correcta navegación del Atlas
      - Aplicación apropiada de taxonomía

  utilidad_percibida:
    objetivo: ">4.5/5"
    medicion: "Satisfacción del usuario con la clasificación"
    encuesta: "¿La respuesta estuvo en el dominio correcto?"
```

---

## 🔄 Mantenimiento y Evolución

### Actualización Continua de Taxonomía

#### Proceso de Mejora de Clasificación
```python
class TaxonomyMaintenance:
    def __init__(self):
        self.feedback_collector = FeedbackCollector()
        self.pattern_analyzer = PatternAnalyzer()
        self.taxonomy_updater = TaxonomyUpdater()

    async def improve_taxonomy(self, usage_data):
        """Mejora continua del sistema de taxonomía"""

        # 1. Análisis de patrones de uso
        usage_patterns = await self.pattern_analyzer.analyze_usage_patterns(usage_data)

        # 2. Recolección de feedback de usuarios
        user_feedback = await self.feedback_collector.collect_role_feedback()

        # 3. Identificación de áreas de mejora
        improvement_areas = await self.identify_improvement_areas(
            usage_patterns, user_feedback
        )

        # 4. Propuestas de actualización
        update_proposals = await self.generate_update_proposals(improvement_areas)

        # 5. Validación con equipo especializado
        validated_updates = await self.validate_updates_with_specialists(update_proposals)

        # 6. Aplicación de mejoras
        await self.taxonomy_updater.apply_updates(validated_updates)

        return {
            "improvements_applied": validated_updates,
            "impact_metrics": await self.measure_improvement_impact(validated_updates),
            "next_review_date": await self.schedule_next_review()
        }
```

### Expansión de Dominios

#### Nuevos Dominios Según Necesidades del Proyecto
```yaml
future_domains:
  dominio_audio:
    palabras_clave: ["sonido", "audio", "música", "sfx", "voz"]
    roles_afectados: ["sound_designer", "audio_technician"]
    archivos_tipo: [".wav", ".mp3", ".ogg", "Audio_*.md"]

  dominio_testing:
    palabras_clave: ["testing", "qa", "validación", "pruebas"]
    roles_afectados: ["qa_tester", "test_lead"]
    archivos_tipo: ["Test_*.md", "QA_*.json", "Validation_*.md"]

  dominio_localizacion:
    palabras_clave: ["localización", "traducción", "idioma", "cultura"]
    roles_afectados: ["translator", "localization_manager"]
    archivos_tipo: ["Locale_*.md", "Translation_*.json", "Language_*.md"]
```

Este sistema de taxonomía proporciona una clasificación precisa y útil que permite al Dungeon Life Agent operar efectivamente dentro del complejo ecosistema DLE, adaptándose automáticamente a cada especialización del equipo mientras mantiene la precisión y relevancia de las respuestas.

¿Te parece adecuada esta taxonomía expandida? ¿Hay algún dominio o rol específico que te gustaría que profundice más?</result>
</attempt_completion>