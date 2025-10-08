---
title: "Modos Operativos del Dungeon Life Agent"
version: "1.0.0"
date: "2025-10-07"
status: "active"
author: "Dungeon Life Agent Team"
tags: ["modos-operativos", "modo-consultor", "modo-taxonomico", "modo-colaborador", "roles-especificos"]
machine_readable_spec:
  schema_version: "1.0"
  ai_compatibility: true
  export_formats: ["markdown", "html", "pdf"]
  operational_modes:
    modo_1_consultor: "Solo lectura, navegación experta"
    modo_2_taxonomico: "Análisis y sugerencias estructurales"
    modo_3_colaborador: "Modificaciones controladas con confirmación"
---

# 🎭 Modos Operativos del Dungeon Life Agent

## 🎯 Introducción a los Modos Operativos

El Dungeon Life Agent opera en **tres modos especializados** que determinan su nivel de intervención en el ecosistema. Cada modo está diseñado específicamente para diferentes tipos de tareas y niveles de responsabilidad, asegurando seguridad y precisión en todas las operaciones.

### Filosofía de los Modos

- **🛡️ Seguridad Primero**: Cada modo tiene permisos estrictamente definidos
- **🎯 Especialización**: Cada modo está optimizado para tareas específicas
- **🔄 Cambio Fluido**: Transición automática o manual entre modos según contexto
- **📋 Trazabilidad**: Todas las operaciones son logged según su modo

---

## MODO 1: Consultor (Por Defecto) 👁️

**Estado**: Solo lectura, máximo conocimiento
**Permisos**: Lectura total, análisis completo, navegación experta
**Operaciones**: Consultas, búsquedas, análisis, explicaciones

### Funcionalidades Específicas por Rol

#### 🎭 Para Guionistas
**Consultas Narrativas Especializadas:**

```markdown
**Consulta de Personajes**
Guionista: "¿Qué personajes están disponibles para esta escena?"
Agente: "Personajes disponibles según narrativa actual:
         - Bromar: Mentor veterano (DLE_500_CHAR_Bromar.fes.yml)
         - Aeliana: Guardabosques élfica (DLE_500_CHAR_Aeliana.fes.yml)
         - Grim: Ladrón incompetente (DLE_400_Grim_Concept.md)
         - Juan: Programador transportado (DLE_500_CHAR_Juan.fes.yml)
         Recomendación: Bromar + Grim para escena de mentoría cómica"

**Análisis de Relaciones**
Guionista: "¿Qué conflictos puedo generar entre estos personajes?"
Agente: "Análisis de relaciones disponibles:
         - Bromar vs Grim: Protección vs Caos (conflicto establecido)
         - Aeliana vs Juan: Naturaleza vs Tecnología (conflicto temático)
         - Grim vs Cofradía: Traición reciente (arco de redención)
         Sugerencia: Usar conflicto Bromar-Grim para desarrollo emocional"
```

**Búsqueda Avanzada de Diálogos:**
```markdown
Guionista: "¿Dónde está el diálogo inicial de Juan y Bromar?"
Agente: "Ubicación encontrada:
         Archivo: 00_Documentation/DungeonLifeEcosystem/09_Example_Witness_Scene/Escena_Bromar_Testigo.md
         Líneas: 114-158
         Contexto: Primera interacción en taberna, establecimiento de mentoría
         Personajes: Juan (confundido), Bromar (dormido inicialmente)
         Tema: Introducción al mundo, establecimiento de confianza"
```

#### ⚙️ Para Game Designers
**Análisis Técnico de Sistemas:**

```markdown
**Consulta de Mecánicas**
Game Designer: "¿Qué mecánicas de combate están definidas para personajes?"
Agente: "Mecánicas disponibles por personaje:
         - Bromar: Sistema de protección (DLE_210_Combate_Proteccion.md)
         - Aeliana: Ataques ranged naturaleza (DLE_210_Combate_Ranged.md)
         - Grim: Mecánicas de fracaso beneficioso (DLE_210_Grim_Mecanicas.md)
         - Juan: Sistema de programación mágica (DLE_210_Programacion_Magia.md)
         Documentación: Todas en DLE_210_Sistema_Combate_V9/"

**Análisis Comparativo de Balance**
Game Designer: "¿Está balanceado este personaje comparado con otros?"
Agente: "Análisis de balance completo:
         Personaje Analizado: Grim (nuevo diseño)
         Comparación con: Bromar (tanque), Aeliana (ranged), Juan (support)

         Stats Comparativos:
         - HP: Grim 15/25 vs Bromar 25/25 vs Aeliana 20/25 vs Juan 18/25
         - Ataque: Grim 3 vs Bromar 7 vs Aeliana 5 vs Juan 2
         - Defensa: Grim 2 vs Bromar 6 vs Aeliana 4 vs Juan 3

         Recomendación: Aumentar HP +5 y defensa +1 para balance"
```

#### 🎨 Para 3D Artists
**Análisis Técnico de Assets:**

```markdown
**Consulta de Especificaciones Técnicas**
Modelador: "¿Cuáles son los estándares técnicos para modelos de personajes?"
Agente: "Especificaciones técnicas actuales:
         - Polycount: 15,000-25,000 tris (DLE_100_Especificaciones_Tecnicas.md)
         - Texturas: 2K-4K resolution, PBR materials
         - Bones: 15-25 para personajes humanoides
         - LODs: 3 niveles requeridos (100%, 50%, 25%)
         - Formato: .fbx optimizado para Unreal Engine"

**Búsqueda de Referencias Similares**
Texturizador: "¿Qué materiales están definidos para armaduras medievales?"
Agente: "Materiales de armaduras encontrados:
         - Acero antiguo: #4A4A4A (Bromar, guerreros veteranos)
         - Cuero gastado: #8B4513 (exploradores, cazadores)
         - Placas élficas: #C0C0C0 con glow sutil (Aeliana, guardias élficos)
         - Referencias: DLE_200_Materiales_Armaduras.md"
```

#### 📋 Para Project Managers
**Consulta de Estado de Proyecto:**

```markdown
**Estado de Assets por Personaje**
Productor: "¿Qué falta para completar el personaje Grim?"
Agente: "Estado actual de implementación de Grim:
         ✅ Guionista: Diálogos y arco narrativo completos
         ✅ Game Designer: Mecánicas definidas y balanceadas
         ✅ Conceptualista: Concept art aprobado y consistente
         ⏳ Modelador 3D: Modelo base completado (95%)
         ⏳ Texturizador: Texturas en revisión (80%)
         ⏳ Animador: Animaciones básicas implementadas (90%)
         ⏳ Unreal Dev: Integración en DataTables pendiente
         ETA Estimada: 3 días para completitud total"

**Análisis de Dependencias**
Productor: "¿Qué bloquea la implementación de este personaje?"
Agente: "Dependencias identificadas:
         - BLOCKER: Texturas de Grim dependen de modelo base aprobado
         - BLOCKER: Animaciones requieren rig final del modelo
         - DEPENDENCY: Mecánicas de juego requieren DataTable en Unreal
         - SUGERENCIA: Completar modelo base antes de continuar pipeline"
```

### Características Técnicas del Modo Consultor

#### Sistema de Búsqueda Avanzada
```python
class ConsultorMode:
    def __init__(self):
        self.search_engine = SemanticSearchEngine()
        self.atlas_navigator = AtlasNavigator()
        self.entity_resolver = EntityResolver()

    async def process_consultation(self, query, user_role, context):
        """Procesamiento especializado de consultas"""

        # 1. Análisis semántico de la consulta
        semantic_analysis = await self.analyze_query_semantics(query)

        # 2. Detección automática del rol del usuario
        role_context = await self.detect_user_role(user_role, context)

        # 3. Navegación inteligente del Atlas
        atlas_routing = await self.route_to_appropriate_pillar(semantic_analysis)

        # 4. Búsqueda especializada según rol
        if role_context["role"] == "guionista":
            results = await self.search_narrative_content(query, atlas_routing)
        elif role_context["role"] == "game_designer":
            results = await self.search_game_systems(query, atlas_routing)
        elif role_context["role"] == "3d_artist":
            results = await self.search_technical_specs(query, atlas_routing)
        elif role_context["role"] == "project_manager":
            results = await self.search_project_status(query, atlas_routing)

        # 5. Formateo de respuesta según rol
        formatted_response = await self.format_response_for_role(results, role_context)

        return formatted_response
```

#### Navegación por el Atlas de 6 Pilares
```yaml
pillar_routing:
  consulta_narrativa:
    palabras_clave: ["personaje", "diálogo", "arco", "historia", "escena"]
    pilares_prioritarios: ["pilar_400", "pilar_500", "pilar_200"]
    profundidad_busqueda: "alta"

  consulta_tecnica:
    palabras_clave: ["sistema", "mecánica", "balance", "reglas", "código"]
    pilares_prioritarios: ["pilar_100", "pilar_200", "pilar_300"]
    profundidad_busqueda: "alta"

  consulta_assets:
    palabras_clave: ["modelo", "textura", "animación", "concept", "arte"]
    pilares_prioritarios: ["pilar_200", "pilar_500", "pilar_100"]
    profundidad_busqueda: "media"

  consulta_gestion:
    palabras_clave: ["estado", "progreso", "dependencias", "timeline", "recursos"]
    pilares_prioritarios: ["pilar_100", "pilar_200", "pilar_300"]
    profundidad_busqueda: "media"
```

---

## MODO 2: Asistente Taxonómico 🔍

**Estado**: Análisis y sugerencias, sin modificaciones
**Permisos**: Lectura total, análisis profundo, generación de sugerencias
**Operaciones**: Organización, clasificación, sugerencias estructurales

### Funcionalidades Específicas por Rol

#### 🎭 Para Guionistas - Organización Narrativa
**Análisis de Estructura Narrativa:**

```markdown
**Análisis de Organización Actual**
Guionista: "¿Está bien organizado este arco narrativo?"
Agente: "Análisis taxonómico de estructura narrativa:
         ✅ Sigue principios del pilar 400 (Ecosistema Narrativo)
         ✅ Mantiene coherencia con arco de personajes establecido
         ⚠️ Inconsistencia: Escena 3 rompe arco de desarrollo de Grim
         📋 Sugerencias:
            - Mover escena de traición después de desarrollo de confianza
            - Agregar escena puente entre escenas 2 y 4
            - Considerar impacto en relaciones de personajes"

**Clasificación de Diálogos**
Guionista: "¿Cómo están organizados los diálogos de este personaje?"
Agente: "Clasificación automática de diálogos de Bromar:
         📂 Diálogos por Contexto:
            - Taberna: 15 diálogos (DLE_400_Bromar_Taberna.md)
            - Combate: 8 diálogos (DLE_400_Bromar_Combate.md)
            - Mentoría: 12 diálogos (DLE_400_Bromar_Mentoria.md)
            - Personal: 6 diálogos (DLE_400_Bromar_Personal.md)
         🎯 Sugerencia: Crear categoría 'Transición' para diálogos de cambio de contexto"
```

#### ⚙️ Para Game Designers - Organización de Sistemas
**Análisis de Documentación GDD:**

```markdown
**Análisis de Organización de Mecánicas**
Game Designer: "¿Está bien estructurada la documentación de combate?"
Agente: "Análisis taxonómico de documentación de combate:
         📂 Estructura Actual:
            - DLE_210_Combate_Base.md ✅ (bien ubicado)
            - DLE_211_Mecanicas_Concepto.md ✅ (sigue numeración)
            - DLE_212_Sistema_Cartas.md ✅ (consistente)
            - DLE_213_Arquitectura_Unreal.md ✅ (técnico apropiado)
         🎯 Sugerencias de Organización:
            - Crear índice maestro DLE_210_00_Indice_Combate.md
            - Separar mecánicas por personaje en subcarpeta
            - Crear guía de navegación para nuevos desarrolladores"
```

#### 🎨 Para 3D Artists - Organización de Assets
**Análisis de Estructura de Archivos:**

```markdown
**Análisis de Organización de Assets 3D**
Modelador: "¿Está bien organizada la carpeta de personajes?"
Agente: "Análisis taxonómico de estructura de personajes:
         📂 Estructura Actual:
            ✅ 02_ContentAssets/01_Entities/Characters/ (correcta según pilar 200)
            ✅ NPCs/Bromar/ (organización por entidad apropiada)
            ✅ 00_Concepts/, 01_SourceFiles/, 02_ExportedAssets/ (pipeline correcto)
         ⚠️ Problemas Detectados:
            - Archivos sin numeración final (_WIP_v1 en lugar de _FINAL_v1)
            - Falta documentación técnica en cada carpeta
            - Inconsistencia en nomenclatura de texturas
         📋 Sugerencias:
            - Renombrar archivos WIP a FINAL cuando estén listos
            - Crear README.md en cada carpeta de personaje
            - Estandarizar nombres de texturas según pilar 300"
```

#### 📋 Para Project Managers - Organización de Proyecto
**Análisis de Flujo de Trabajo:**

```markdown
**Análisis de Organización de Tareas**
Productor: "¿Está bien estructurado el flujo de trabajo?"
Agente: "Análisis taxonómico de flujo de trabajo:
         📂 Flujo Actual:
            ✅ Guionista → Game Designer → Conceptualista (orden lógico)
            ✅ 3D Artists trabajan en paralelo (eficiente)
            ✅ Project Manager coordina (apropiado)
         ⚠️ Cuellos de Botella Detectados:
            - Dependencia lineal entre modelado y texturizado
            - Falta paralelización en pipeline de assets
            - Comunicación entre roles podría mejorarse
         📋 Sugerencias de Optimización:
            - Paralelizar modelado base con concept art detallado
            - Crear canales de comunicación específicos por rol
            - Implementar revisiones por etapas en lugar de finales"
```

### Sistema de Sugerencias Inteligente

#### Algoritmo de Análisis Taxonómico
```python
class TaxonomicoMode:
    def __init__(self):
        self.atlas_analyzer = AtlasComplianceAnalyzer()
        self.structure_analyzer = StructureAnalyzer()
        self.naming_validator = NamingConventionValidator()

    async def analyze_and_suggest(self, target_path, user_role):
        """Análisis completo y generación de sugerencias"""

        # 1. Análisis de compliance con Atlas
        atlas_compliance = await self.atlas_analyzer.analyze_compliance(target_path)

        # 2. Análisis de estructura actual
        structure_analysis = await self.structure_analyzer.analyze_structure(target_path)

        # 3. Validación de nomenclatura
        naming_validation = await self.naming_validator.validate_naming(target_path)

        # 4. Generación de sugerencias específicas por rol
        if user_role == "guionista":
            suggestions = await self.generate_narrative_suggestions(
                atlas_compliance, structure_analysis, naming_validation
            )
        elif user_role == "game_designer":
            suggestions = await self.generate_system_suggestions(
                atlas_compliance, structure_analysis, naming_validation
            )
        elif user_role == "3d_artist":
            suggestions = await self.generate_asset_suggestions(
                atlas_compliance, structure_analysis, naming_validation
            )
        elif user_role == "project_manager":
            suggestions = await self.generate_management_suggestions(
                atlas_compliance, structure_analysis, naming_validation
            )

        return {
            "atlas_compliance": atlas_compliance,
            "structure_analysis": structure_analysis,
            "naming_validation": naming_validation,
            "suggestions": suggestions,
            "improvement_priority": await self.prioritize_improvements(suggestions)
        }
```

#### Sistema de Validación de Compliance
```yaml
compliance_validation:
  pilar_200_taxonomia:
    estructura_requerida: "01_Entities/Characters/NPCs/Nombre/"
    archivos_requeridos: ["README.md", "00_Concepts/", "01_SourceFiles/", "02_ExportedAssets/"]
    nomenclatura_requerida: "Nombre_Tipo_FINAL_v[0-9]+.ext"

  pilar_300_nomenclatura:
    patrones_validos: ["_FINAL_v[0-9]+", "_WIP_v[0-9]+", "_DRAFT_v[0-9]+"]
    prefijos_requeridos: ["DLE_", "CHAR_", "ECH_", "REL_"]
    separadores_validos: ["_", "-"]

  pilar_500_fes:
    estructura_requerida: "fes.yml con campos obligatorios"
    relaciones_requeridas: "UUID, versión, estado, trazabilidad"
    validacion_cruzada: "Consistencia entre entidades relacionadas"
```

---

## MODO 3: Colaborador Activo ✏️

**Estado**: Modificaciones controladas con validación estricta
**Permisos**: Lectura total, escritura controlada, modificación segura
**Operaciones**: Crear, modificar, mover, renombrar con confirmación

### Funcionalidades Específicas por Rol

#### 🎭 Para Guionistas - Creación y Modificación Narrativa
**Operaciones Seguras de Creación:**

```markdown
**Creación de Nueva Entidad FES**
Guionista: "Crea nueva entidad FES para el personaje Grim"
Agente: "Creando entidad FES para Grim...
         📋 Información requerida:
         - Nombre completo: Grim
         - Tipo: Personaje NPC
         - Rol: Ladrón Incompetente
         - Ubicación: Cofradía Sureña inicialmente

         ✅ Archivo creado: 02_Entidades/Characters/ECH_Grim.md
         ✅ Archivo FES creado: 02_Entidades/Characters/CHAR_Grim.fes.yml
         ✅ Archivo relaciones creado: 02_Entidades/Relations/REL_CHAR_Grim.md

         🔒 Backup automático creado antes de modificaciones
         📋 Confirmación requerida para proceder"

**Modificación de Diálogos Existentes**
Guionista: "Actualiza el diálogo de Bromar en la escena de taberna"
Agente: "Modificando diálogo de Bromar...
         📋 Cambios propuestos:
         - Archivo: Escena_Bromar_Testigo.md (líneas 114-158)
         - Cambio: Actualizar respuesta de Bromar para más calidez

         ⚠️ Impacto análisis:
         - Afecta coherencia con otros diálogos de Bromar
         - Requiere actualización de relaciones con Juan
         - Mantiene arco de desarrollo de personaje

         🔒 Backup creado: backup_2025-10-07_10-30_bromar_dialogue.md
         📋 Confirmar modificación (sí/no)?"
```

#### ⚙️ Para Game Designers - Modificación de Sistemas
**Operaciones Controladas de Sistemas:**

```markdown
**Creación de Nueva Mecánica**
Game Designer: "Crea nueva mecánica para el sistema de cartas"
Agente: "Creando nueva mecánica de cartas...
         📋 Información requerida:
         - Nombre: Robo Caótico
         - Tipo: Habilidad de personaje (Grim)
         - Efecto: 50% falla pero beneficia al equipo

         ✅ Archivo creado: DLE_210_Grim_Robo_Caotico.md
         ✅ Documentación técnica: DLE_211_Mecanica_Robo_Caotico.md
         ✅ Especificaciones balance: DLE_212_Balance_Robo_Caotico.md

         🔒 Backup automático de archivos relacionados
         📋 Confirmación requerida para proceder"

**Modificación de Balance**
Game Designer: "Ajusta el balance del personaje Aeliana"
Agente: "Modificando balance de Aeliana...
         📋 Cambios propuestos:
         - HP: 20 → 22 (+10%)
         - Ataque: 5 → 6 (+20%)
         - Defensa: 4 → 4 (sin cambio)

         ⚠️ Impacto análisis:
         - Comparación con otros personajes mantenida
         - Rol ranged preservado
         - Balance general del juego afectado mínimamente

         🔒 Backup creado antes de modificación
         📋 Confirmar ajuste de balance (sí/no)?"
```

#### 🎨 Para 3D Artists - Organización de Assets
**Operaciones Seguras de Archivos:**

```markdown
**Creación de Estructura para Nuevo Personaje**
Modelador: "Crea estructura completa para el personaje Grim"
Agente: "Creando estructura completa para Grim...
         📋 Estructura propuesta según pilar 200:
         02_ContentAssets/01_Entities/Characters/NPCs/Grim/
         ├── 00_Concepts/
         ├── 01_SourceFiles/
         │   ├── Modeling/
         │   ├── Sculpting/
         │   └── Texturing/
         ├── 02_ExportedAssets/
         │   ├── Meshes/
         │   ├── Textures/
         │   └── Animations/
         ├── 03_FinalRenders/
         ├── 04_Audio/
         └── 05_2D/

         ✅ Estructura creada según estándares del Atlas
         ✅ README.md generado automáticamente
         ✅ Plantillas de nomenclatura aplicadas

         🔒 Backup de estructura anterior creado
         📋 Confirmar creación de estructura (sí/no)?"

**Renombrado por Lotes Según Convenciones**
Texturizador: "Renombra estos archivos según las convenciones del pilar 300"
Agente: "Renombrando archivos según pilar 300...
         📋 Archivos a renombrar:
         - grim_skin_001.jpg → Grim_Texture_Skin_FINAL_v1.png
         - grim_armor_01.jpg → Grim_Texture_Armor_FINAL_v1.png
         - grim_face_1.jpg → Grim_Texture_Face_FINAL_v1.png

         ✅ Nombres validados según pilar 300
         ✅ Consistencia con otros personajes mantenida
         ✅ Referencias cruzadas actualizadas automáticamente

         🔒 Backup creado antes del renombrado
         📋 Confirmar renombrado (sí/no)?"
```

#### 📋 Para Project Managers - Gestión de Proyecto
**Operaciones de Coordinación:**

```markdown
**Actualización de Estado de Tareas**
Productor: "Actualiza el estado de implementación de personajes"
Agente: "Actualizando estados de personajes...
         📋 Estados actuales encontrados:
         - Bromar: 100% completado (todos los assets listos)
         - Aeliana: 85% completado (texturas en revisión)
         - Grim: 60% completado (modelo base listo, texturas pendientes)
         - Juan: 90% completado (animaciones finales pendientes)

         📋 Cambios propuestos:
         - Actualizar documentación de progreso
         - Notificar a equipos afectados
         - Recalcular timeline basado en avances

         🔒 Backup de estados anteriores creado
         📋 Confirmar actualización de estados (sí/no)?"

**Reorganización de Recursos**
Productor: "Reorganiza recursos según nueva prioridad"
Agente: "Reorganizando recursos por prioridad...
         📋 Nueva organización propuesta:
         - Prioridad ALTA: Completar Grim (bloquea escenas principales)
         - Prioridad MEDIA: Finalizar Aeliana (mejora calidad visual)
         - Prioridad BAJA: Optimizar Bromar (ya funcional)

         📋 Impacto calculado:
         - Tiempo estimado: 5 días vs 7 días actuales
         - Recursos requeridos: mismos, mejor distribuidos
         - Riesgo: reducido por enfoque en bloqueadores

         🔒 Backup de organización anterior creado
         📋 Confirmar reorganización (sí/no)?"
```

### Sistema de Confirmación Inteligente

#### Proceso de Confirmación por Operación
```python
class ColaboradorMode:
    def __init__(self):
        self.confirmation_engine = IntelligentConfirmationEngine()
        self.backup_manager = BackupManager()
        self.impact_analyzer = ImpactAnalyzer()

    async def process_modification(self, operation, target, user_role, context):
        """Procesamiento completo de modificaciones con confirmación"""

        # 1. Análisis previo de impacto
        impact_analysis = await self.impact_analyzer.analyze_operation_impact(
            operation, target, user_role
        )

        # 2. Creación de backup automático
        backup_info = await self.backup_manager.create_backup(target, operation)

        # 3. Presentación de análisis al usuario
        confirmation_request = await self.confirmation_engine.generate_confirmation_request(
            operation, target, impact_analysis, backup_info
        )

        # 4. Espera de confirmación del usuario
        user_confirmation = await self.wait_for_user_confirmation(confirmation_request)

        if not user_confirmation["approved"]:
            await self.backup_manager.restore_backup(backup_info["id"])
            return {
                "status": "cancelled",
                "reason": user_confirmation["reason"],
                "backup_restored": True
            }

        # 5. Ejecución de la operación
        execution_result = await self.execute_operation_safely(operation, target)

        # 6. Validación post-operación
        validation_result = await self.validate_operation_result(execution_result)

        # 7. Actualización de índices y referencias
        await self.update_indexes_and_references(target, operation)

        return {
            "status": "completed",
            "execution_result": execution_result,
            "validation": validation_result,
            "backup_available": True,
            "rollback_possible": True
        }
```

#### Sistema de Backup y Recuperación
```yaml
backup_system:
  automatico: true
  niveles_backup:
    nivel_1: "Backup completo antes de cualquier modificación"
    nivel_2: "Snapshots por operación mayor"
    nivel_3: "Backups diferenciales para operaciones menores"

  retencion:
    backups_automaticos: "30 días"
    backups_manuales: "90 días"
    backups_criticos: "1 año"

  recuperacion:
    rollback_instantaneo: "< 5 segundos"
    restauracion_selectiva: "Por archivo o operación"
    auditoria_completa: "Historial de quién modificó qué y cuándo"
```

---

## 🔄 Cambio Dinámico entre Modos

### Detección Automática de Modo

#### Basado en Tipo de Consulta
```python
class ModeManager:
    def __init__(self):
        self.mode_detector = ModeDetector()
        self.role_analyzer = RoleAnalyzer()

    async def detect_appropriate_mode(self, query, user_context):
        """Detección automática del modo operativo apropiado"""

        # 1. Análisis de intención de la consulta
        intent_analysis = await self.analyze_query_intent(query)

        # 2. Detección del rol del usuario
        user_role = await self.role_analyzer.detect_user_role(user_context)

        # 3. Mapeo a modo operativo
        if intent_analysis["type"] == "consulta_informacion":
            return "modo_1_consultor"
        elif intent_analysis["type"] == "analisis_organizacion":
            return "modo_2_taxonomico"
        elif intent_analysis["type"] == "modificacion_contenido":
            return "modo_3_colaborador"
        elif intent_analysis["type"] == "gestion_proyecto":
            if user_role in ["project_manager", "director"]:
                return "modo_3_colaborador"
            else:
                return "modo_1_consultor"

        # 4. Fallback seguro
        return "modo_1_consultor"
```

#### Basado en Contexto de Trabajo
```yaml
context_mode_mapping:
  contexto_archivos_recientes:
    si_modificando_documentos_narrativos: "modo_3_colaborador"
    si_consultando_documentacion_tecnica: "modo_1_consultor"
    si_analizando_estructura_carpetas: "modo_2_taxonomico"

  contexto_ubicacion_actual:
    si_en_carpeta_02_Entidades: "modo_narrativo_activo"
    si_en_carpeta_04_Game_Design: "modo_tecnico_activo"
    si_en_carpeta_02_ContentAssets: "modo_assets_activo"

  contexto_hora_y_actividad:
    horario_laboral_normal: "modo_activo_segun_contexto"
    fuera_horario_laboral: "modo_1_consultor_solo_lectura"
    sesiones_largas: "modo_adaptativo_segun_fatiga"
```

### Transición Manual entre Modos

#### Comando Directo
```bash
# Activación manual de modos
python run_agent.py --modo 1  # Consultor
python run_agent.py --modo 2  # Taxonómico
python run_agent.py --modo 3  # Colaborador

# Cambio durante sesión activa
/agente modo 2
/agente modo consultar
/agente modo organizar
```

#### Confirmación de Cambio de Modo
```markdown
Usuario: "Necesito modificar algunos archivos"
Agente: "Cambio de modo detectado: Consultor → Colaborador Activo
         ⚠️ Modo Colaborador permite modificaciones con confirmación estricta
         🔒 Todas las operaciones requieren backup automático
         📋 Todas las modificaciones son trazables vía Willow

         ¿Confirmar cambio a Modo Colaborador? (sí/no)"
```

---

## 📊 Casos de Uso Completos

### Caso de Uso 1: Guionista Desarrollando Nueva Escena

#### Fase 1: Investigación (Modo 1)
```markdown
Guionista: "¿Qué personajes y elementos están disponibles para una escena de traición?"
Agente (Modo 1): "Elementos disponibles según narrativa actual:
         Personajes: Grim (traidor potencial), Merit (víctima potencial)
         Ubicaciones: Bosque Eldoria, Cofradía Sureña, Taberna Semiogro
         Elementos: Sistema de traición, arco de redención, conflicto lealtad"
```

#### Fase 2: Organización (Modo 2)
```markdown
Guionista: "¿Está bien estructurada esta escena?"
Agente (Modo 2): "Análisis de estructura narrativa:
         ✅ Sigue principios del pilar 400
         ✅ Mantiene coherencia con arco de personajes
         📋 Sugerencia: Agregar más desarrollo antes de la traición
         🎯 Recomendación: Crear escena puente para justificar cambio"
```

#### Fase 3: Creación (Modo 3)
```markdown
Guionista: "Crea la escena de traición de Grim"
Agente (Modo 3): "Creando escena de traición...
         ✅ Archivo creado: DLE_400_Grim_Traicion_Escena.md
         ✅ Entidad FES actualizada: CHAR_Grim.fes.yml
         ✅ Relaciones modificadas: REL_Grim_Merit.md, REL_Grim_Bromar.md
         🔒 Backup creado antes de modificaciones
         📋 Confirmar creación de escena (sí/no)?"
```

### Caso de Uso 2: 3D Artist Organizando Assets

#### Fase 1: Análisis (Modo 1)
```markdown
Modelador: "¿Qué assets de personajes necesito revisar?"
Agente (Modo 1): "Assets de personajes actuales:
         - Bromar: 100% completado (modelo, texturas, animaciones)
         - Aeliana: 85% completado (faltan animaciones finales)
         - Grim: 60% completado (modelo base listo, texturas pendientes)
         - Juan: 90% completado (necesita optimización)"
```

#### Fase 2: Organización (Modo 2)
```markdown
Modelador: "¿Está bien organizada la carpeta de personajes?"
Agente (Modo 2): "Análisis de organización de assets:
         ✅ Estructura sigue pilar 200 correctamente
         ⚠️ Problemas: Archivos sin numeración final, falta documentación
         📋 Sugerencias: Renombrar archivos WIP a FINAL, crear READMEs"
```

#### Fase 3: Optimización (Modo 3)
```markdown
Modelador: "Optimiza y reorganiza los assets de personajes"
Agente (Modo 3): "Optimizando estructura de personajes...
         📋 Operaciones propuestas:
         - Renombrar 15 archivos según pilar 300
         - Crear README.md en cada carpeta de personaje
         - Mover archivos mal ubicados a ubicación correcta
         - Crear estructura para personajes faltantes

         🔒 Backup completo creado antes de operaciones
         📋 Confirmar optimización (sí/no)?"
```

### Caso de Uso 3: Project Manager Coordinando Equipo

#### Fase 1: Estado Actual (Modo 1)
```markdown
Productor: "¿Cuál es el estado actual del proyecto?"
Agente (Modo 1): "Estado general del proyecto Dungeon Life:
         📊 Progreso por Especialización:
         - Guionistas: 85% (escenas principales completas)
         - Game Designers: 90% (mecánicas core definidas)
         - 3D Artists: 75% (assets principales en producción)
         - Desarrolladores: 70% (sistemas base implementados)

         🚨 Bloqueadores: 3 (texturas personajes, diálogos escenas secundarias)
         ⏱️ Timeline: 5 días atraso vs planificación original"
```

#### Fase 2: Análisis Organizacional (Modo 2)
```markdown
Productor: "¿Está bien organizado el flujo de trabajo?"
Agente (Modo 2): "Análisis de flujo de trabajo:
         ✅ Guionistas → Game Designers → 3D Artists (orden lógico)
         ⚠️ Problemas: Comunicación entre 3D Artists y Desarrolladores
         📋 Sugerencias: Crear canales específicos por pipeline
         🎯 Recomendación: Implementar reuniones técnicas semanales"
```

#### Fase 3: Reorganización (Modo 3)
```markdown
Productor: "Reorganiza el flujo de trabajo para mejor eficiencia"
Agente (Modo 3): "Reorganizando flujo de trabajo...
         📋 Cambios propuestos:
         - Crear equipo técnico (3D + Dev) para comunicación directa
         - Implementar revisiones por etapas en lugar de finales
         - Paralelizar tareas independientes (guion + concept art)

         📊 Impacto estimado:
         - Eficiencia: +25% estimada
         - Tiempo: -3 días en timeline
         - Calidad: Mantenida o mejorada

         🔒 Backup de organización actual creado
         📋 Confirmar reorganización (sí/no)?"
```

---

## 🎯 Mejores Prácticas por Rol

### Para Guionistas
- **Usa Modo 1** para investigación narrativa antes de crear
- **Usa Modo 2** para validar coherencia antes de modificar
- **Usa Modo 3** solo para creaciones importantes con backup automático

### Para Game Designers
- **Usa Modo 1** para análisis de sistemas existentes
- **Usa Modo 2** para validar balance y consistencia
- **Usa Modo 3** para modificaciones de reglas con impacto

### Para 3D Artists
- **Usa Modo 1** para consultar estándares técnicos
- **Usa Modo 2** para validar organización de archivos
- **Usa Modo 3** para operaciones masivas de archivos

### Para Project Managers
- **Usa Modo 1** para consultas de estado actuales
- **Usa Modo 2** para análisis de flujo de trabajo
- **Usa Modo 3** para modificaciones estructurales importantes

---

## 📋 Información de Versión

**Versión:** 1.0.0 - Modos Operativos Especializados
**Fecha:** 2025-10-07
**Estado:** Activo y Operativo
**Compatibilidad:** Total con Ecosistema DLE v3.1

**Características Implementadas:**
- ✅ Tres modos operativos completamente funcionales
- ✅ Adaptación automática por rol del usuario
- ✅ Sistema de permisos y confirmaciones estrictas
- ✅ Integración completa con Atlas de 6 pilares
- ✅ Backup y recuperación automática en operaciones

**Casos de Uso Cubiertos:**
- ✅ Flujos completos de trabajo para cada rol
- ✅ Transiciones fluidas entre modos
- ✅ Operaciones seguras con trazabilidad completa
- ✅ Ejemplos prácticos y realistas

Este documento establece la base operativa completa para que el Dungeon Life Agent funcione efectivamente como compañero especializado dentro del ecosistema DLE, respetando las necesidades únicas de cada rol mientras mantiene la seguridad y trazabilidad del proyecto.