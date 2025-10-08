---
title: "Dungeon Life Agent - Agente IA Especializado para el Ecosistema Dungeon Life"
version: "1.0.0"
date: "2025-10-07"
status: "active"
author: "Dungeon Life Agent Team"
tags: ["agente-ia", "dungeon-life-ecosystem", "atlas-integration", "especializacion-roles"]
machine_readable_spec:
  schema_version: "1.0"
  ai_compatibility: true
  export_formats: ["markdown", "html", "pdf"]
  role_specialization:
    guionistas_narrativos: "Centro en entidades y narrativa"
    desarrolladores_backend_ia: "Dominio técnico y datasets"
    desarrolladores_unreal: "Integración con motor de juego"
    disenadores_sistemas: "Mecánicas y balance"
    productores_lideres: "Roadmap y gestión"
---

# 🤖 Dungeon Life Agent - Tu Compañero IA en el Ecosistema

## 🎯 ¿Qué es el Dungeon Life Agent?

El **Dungeon Life Agent** es un agente de IA local especializado que "vive" dentro del repositorio de Dungeon Life y opera como extensión natural de tu flujo de trabajo. Diseñado específicamente para el ecosistema DLE, entiende profundamente la estructura del proyecto, los roles del equipo y puede adaptarse automáticamente a tu especialización profesional.

## 🏠 ¿Dónde Vive y Qué Hace?

**Ubicación:** `A:\07_Tools\DungeonLifeAgent\`
**Función:** Opera en tres modos especializados con acceso completo al ecosistema Dungeon Life, desde documentación hasta assets de producción.

## ✨ ¿Por Qué es Único?

- **🔗 Integración Total con DLE**: Entiende y navega el Atlas de 6 pilares como un miembro más del equipo
- **👥 Especialización por Roles**: Se adapta automáticamente a tu función (guionista, desarrollador, diseñador, etc.)
- **🧠 Modelos Locales**: Completamente offline usando llama.cpp + GGUF, sin dependencia de servicios externos
- **🎭 Tres Modos Inteligentes**: Consultor, Asistente Taxonómico y Colaborador Activo
- **🔒 Seguridad Total**: Operaciones controladas con trazabilidad completa vía Willow

---

## 🚀 Inicio Rápido

### Instalación (5 minutos)
```bash
# 1. Crear entorno virtual
python -m venv dungeon_life_agent
source dungeon_life_agent/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configuración inicial
python scripts/setup_agent.py
```

### Configuración por Rol (10 minutos)
El agente detecta automáticamente tu especialización basada en:
- **Guionistas**: Centro en `02_Entidades/` y narrativa
- **Desarrolladores IA**: Dominio en `03_Data/` y `01_SourceCode/`
- **Desarrolladores Unreal**: Integración con `05_Builds/`
- **Diseñadores**: Mecánicas en `04_Game_Design/`
- **Productores**: Roadmap en `06_ProjectManagement/`

### Primer Uso (2 minutos)
```bash
# Iniciar agente en modo automático (detecta tu contexto)
python run_agent.py

# O especificar modo directamente
python run_agent.py --modo 1  # Modo Consultor
python run_agent.py --modo 2  # Modo Taxonómico
python run_agent.py --modo 3  # Modo Colaborador
```

---

## 🎭 Características Principales

### 🧠 Tres Modos Operativos

#### **MODO 1: Consultor (Por Defecto)**
- ✅ Navegación experta del Atlas de 6 Pilares
- ✅ Búsqueda semántica usando vectores DMTE
- ✅ Resolución de entidades FES complejas
- ✅ Consulta de documentación técnica profunda
- ✅ Navegación de estructura material completa

#### **MODO 2: Asistente Taxonómico**
- ✅ Análisis de estructura usando taxonomía propia
- ✅ Sugerencias basadas en `Repository_Taxonomy.yaml`
- ✅ Validación de compliance con Atlas
- ✅ Organización automática de assets
- ✅ Detección de inconsistencias estructurales

#### **MODO 3: Colaborador Activo**
- ✅ Modificaciones controladas con confirmación estricta
- ✅ Creación de documentación usando plantillas
- ✅ Operaciones seguras sobre archivos materiales
- ✅ Integración con herramientas de desarrollo
- ✅ Generación automática de reportes

### 🔗 Integración con Atlas del Proyecto

El agente entiende perfectamente la estructura de 6 pilares:
- **000**: Manifiesto y Principios (filosofía)
- **100**: Arquitectura y Reglas (técnico)
- **200**: Taxonomía y Formatos (clasificación)
- **300**: Nomenclatura y Convenciones (estándares)
- **400**: Ecosistema Narrativo (C.R.A.F.T.)
- **500**: Formato de Entidad Semántica (FES)

---

## 👥 Navegación por Roles del Equipo DLE

El agente se adapta automáticamente a tu especialización según el README principal del proyecto:

### 🎭 Guionistas y Diseñadores Narrativos
**Tu centro de operaciones:** `02_Entidades/` y narrativa

**Ejemplos de consultas típicas:**
```
"¿Dónde están los perfiles de personajes para continuar la historia?"
"Muéstrame las relaciones de Bromar para desarrollar su arco narrativo"
"¿Qué entidades FES están disponibles para esta ubicación?"
"Crea una nueva entidad FES para mi personaje Grim"
```

**Modo recomendado:** 1 (Consultor) → 3 (Colaborador) para creación narrativa

### 💻 Desarrolladores Backend e Ingenieros de IA
**Tu dominio principal:** `03_Data/` y `01_SourceCode/`

**Ejemplos de consultas típicas:**
```
"¿Qué datasets están disponibles para entrenar el sistema de diálogos?"
"Muéstrame la estructura de la base de datos para personajes"
"¿Cómo integro este personaje en el sistema C.R.A.F.T.?"
"Analiza el código del sistema de combate para optimizaciones"
```

**Modo recomendado:** 1 (Consultor) → 2 (Taxonómico) para organización técnica

### 🎮 Desarrolladores Unreal Engine
**Tu integración:** `05_Builds/` y motor de juego

**Ejemplos de consultas típicas:**
```
"¿Cómo convierto esta entidad FES en DataTable de Unreal?"
"Muéstrame qué assets están listos para importar al proyecto"
"¿Qué estructura de Blueprints necesito para este personaje?"
"Valida que estos modelos 3D sean compatibles con Unreal"
```

**Modo recomendado:** 1 (Consultor) → 3 (Colaborador) para integración técnica

### ⚙️ Diseñadores de Juego y Sistemas
**Tu hogar:** `04_Game_Design/` y mecánicas

**Ejemplos de consultas típicas:**
```
"¿Qué mecánicas de combate están definidas para este personaje?"
"Muéstrame el sistema de progresión para balancear personajes"
"¿Cómo integro esta habilidad en el sistema de cartas?"
"Analiza el equilibrio de este personaje comparado con otros"
```

**Modo recomendado:** 1 (Consultor) → 2 (Taxonómico) para análisis de sistemas

### 📋 Productores y Líderes de Proyecto
**Tus carpetas clave:** `06_ProjectManagement/` y roadmap

**Ejemplos de consultas típicas:**
```
"¿Cuál es el estado actual de implementación de personajes?"
"Muéstrame qué assets faltan para completar esta milestone"
"¿Qué dependencias existen entre estos sistemas?"
"Genera un reporte de progreso del proyecto"
```

**Modo recomendado:** 1 (Consultor) → 2 (Taxonómico) para gestión estratégica

---

## 🎯 Taxonomía de Consultas por Especialización

### Clasificación Automática por Contexto

El agente analiza automáticamente tu consulta y la rutaa al dominio apropiado:

| Tipo de Consulta | Detecta Automáticamente | Ejemplo |
|------------------|------------------------|---------|
| **Narrativa** | Palabras como "personaje", "historia", "arco", "diálogo" | → Pilar 400 + 500 |
| **Técnica** | Palabras como "sistema", "código", "base de datos", "API" | → Pilar 100 + 200 |
| **Assets** | Palabras como "modelo", "textura", "animación", "concept" | → Estructura material |
| **Diseño** | Palabras como "mecánica", "balance", "progresión", "reglas" | → Pilar 100 + 400 |
| **Gestión** | Palabras como "estado", "progreso", "dependencias", "roadmap" | → Gestión proyecto |

### Adaptación de Respuestas por Rol

```yaml
respuesta_adaptativa:
  guionista:
    enfoque: "narrativo y creativo"
    profundidad: "detalles de personajes y relaciones"
    formato: "ejemplos narrativos y sugerencias creativas"

  desarrollador:
    enfoque: "técnico y estructural"
    profundidad: "detalles de implementación y dependencias"
    formato: "código, configuraciones y especificaciones técnicas"

  disenador:
    enfoque: "mecánico y balanceado"
    profundidad: "sistemas de juego y equilibrio"
    formato: "comparaciones, métricas y propuestas de balance"
```

---

## 📚 Documentación Relacionada

### Documentos Core del Agente
- **[01_Concepto_y_Vision.md](./01_Concepto_y_Vision.md)** - Visión general y objetivos
- **[02_Arquitectura_Tecnica.md](./02_Arquitectura_Tecnica.md)** - Arquitectura detallada
- **[03_Especificaciones_Funcionales.md](./03_Especificaciones_Funcionales.md)** - Requisitos funcionales
- **[04_Modos_Operativos.md](./04_Modos_Operativos.md)** - Modos 1, 2, 3 en detalle

### Documentos Especializados por Rol
- **[Guia_Guionistas.md](./guias/Guia_Guionistas.md)** - Flujo de trabajo narrativo
- **[Guia_Desarrolladores.md](./guias/Guia_Desarrolladores.md)** - Integración técnica
- **[Guia_Unreal.md](./guias/Guia_Unreal.md)** - Pipeline con motor de juego
- **[Guia_Disenadores.md](./guias/Guia_Disenadores.md)** - Sistemas y balance

### Recursos Externos
- **[Atlas del Proyecto](../../../00_Documentation/DungeonLifeEcosystem/00_Atlas_del_Proyecto/)** - Sistema de 6 pilares
- **[README Principal](../../../00_Documentation/README.md)** - Especialización del equipo DLE
- **[Taxonomy Creation Hub](../../../00_Documentation/DungeonLifeEcosystem/98_Recursos_y_Anexos/Taxonomy_Creation_Hub/)** - Herramientas de clasificación

---

## 🛠️ Instalación Técnica

### Requisitos del Sistema
- **Python**: 3.8+
- **RAM**: 8GB mínimo, 16GB recomendado
- **Espacio**: 10GB para modelos + datos
- **Sistema Operativo**: Windows 10/11, Linux, macOS

### Configuración Inicial
```bash
# 1. Clonar el agente en su ubicación
git clone [repositorio] A:\07_Tools\DungeonLifeAgent\

# 2. Configurar integración con DLE
python scripts/setup_dle_integration.py

# 3. Configurar modelos locales
python scripts/download_models.py

# 4. Verificar instalación
python run_agent.py --test --role-detection
```

### Configuración por Especialización
El agente detecta automáticamente tu rol basado en:
- Archivos recientes que has modificado
- Estructura de directorios donde trabajas
- Tipo de consultas que realizas
- Configuración manual en `config/role_preferences.yaml`

---

## 🤝 Soporte y Contacto

### Reportar Problemas
```bash
# Generar reporte automático de errores
python run_agent.py --report-error

# Crear issue con contexto completo
python scripts/create_issue.py --context-especializacion
```

### Contribuir al Agente
1. **Fork** el repositorio del agente
2. **Crear rama** con tu especialización: `feature/guionistas-nuevas-entidades`
3. **Implementar** mejoras específicas para tu rol
4. **Testear** con casos de uso de tu especialización
5. **PR** con descripción detallada del beneficio por rol

### Soporte por Especialización

| Rol | Canal de Soporte | Tiempo de Respuesta |
|-----|------------------|-------------------|
| Guionistas | `#narrativa-agente` | 2-4 horas |
| Desarrolladores | `#tecnico-agente` | 1-2 horas |
| Diseñadores | `#diseno-agente` | 2-4 horas |
| Productores | `#gestion-agente` | 4-8 horas |

### Recursos Adicionales
- **Wiki del Agente**: Casos de uso por especialización
- **Foro de Comunidad**: Discusiones entre roles
- **Sesiones de Training**: Capacitación específica por rol
- **Feedback Loop**: Mejora continua basada en uso real

---

## 📈 Evolución y Roadmap

### Versión Actual (1.0.0)
- ✅ Integración básica con Atlas de 6 pilares
- ✅ Detección automática de roles del equipo
- ✅ Tres modos operativos funcionales
- ✅ Navegación de estructura material completa

### Próximas Versiones
- **1.1.0**: Especialización avanzada por sub-roles
- **1.2.0**: Integración con herramientas externas (Blender, Unreal)
- **2.0.0**: Agente autónomo para tareas recurrentes

### Métricas de Éxito
- **Adopción por Rol**: >80% de uso activo en cada especialización
- **Precisión de Respuestas**: >90% de respuestas útiles por rol
- **Tiempo de Resolución**: <5 minutos para consultas típicas
- **Satisfacción del Equipo**: >4.5/5 en feedback por especialización

---

## 🌟 Filosofía del Agente

El Dungeon Life Agent no es solo una herramienta - es un **compañero de equipo especializado** que entiende tu rol, respeta tu flujo de trabajo y se adapta a tu forma de pensar. Diseñado desde el principio para integrarse perfectamente con la filosofía del DLE de especialización por roles, el agente se convierte en una extensión natural de tu expertise profesional.

**"El agente no reemplaza al equipo - amplifica su capacidad creativa y técnica dentro del ecosistema."**

---

## 📋 Información de Versión

**Versión:** 1.0.0 - Lanzamiento Inicial Especializado
**Fecha:** 2025-10-07
**Estado:** Activo y en evolución
**Compatibilidad:** Total con Atlas del Proyecto v3.1

**Últimos Cambios:**
- ✅ Integración completa con especialización del equipo DLE
- ✅ Sistema de adaptación automática por rol
- ✅ Taxonomía de consultas específica por especialización
- ✅ Ejemplos prácticos contextualizados

**Próximos Pasos:**
1. Recopilar feedback de cada especialización del equipo
2. Ajustar respuestas según patrones de uso reales
3. Expandir capacidades específicas por rol
4. Integración con herramientas especializadas

---

*El Dungeon Life Agent es más que IA - es un miembro especializado del equipo DLE que entiende tu rol y potencia tu trabajo dentro del ecosistema.*