---
title: "Instalación y Configuración del Dungeon Life Agent"
version: "1.0.0"
date: "2025-10-07"
status: "active"
author: "Dungeon Life Agent Team"
tags: ["instalacion", "configuracion", "tecnologias", "herramientas", "setup"]
machine_readable_spec:
  schema_version: "1.0"
  ai_compatibility: true
  export_formats: ["markdown", "html", "pdf", "json"]
  installation_type: "local_offline"
  compatibility:
    os: ["Windows 11", "Linux", "macOS"]
    python_version: ">=3.9"
    hardware_requirements:
      ram: "16GB minimum, 32GB recommended"
      storage: "50GB for models and data"
      gpu: "NVIDIA GPU with CUDA support (optional, for acceleration)"
---

# 🔧 Instalación y Configuración del Dungeon Life Agent

## 🎯 Visión General de Tecnologías

El Dungeon Life Agent está diseñado para operar completamente **offline** utilizando tecnologías locales de vanguardia. Esta sección detalla todas las tecnologías, herramientas y dependencias necesarias para implementar el agente según los requisitos especificados.

---

## 🏗️ Tecnologías Principales

### 🤖 Motor de IA Local: llama.cpp + llama-cpp-python

**Tecnología Elegida:** `llama.cpp` con bindings Python

**Razón de Elección:**
- ✅ Control total del modelo desde Python
- ✅ Funcionamiento 100% offline sin servidor
- ✅ Integración directa con herramientas y modos
- ✅ Compatibilidad nativa con modelos `.gguf`
- ✅ Alto rendimiento y optimización de memoria

**Características Técnicas:**
```yaml
llama_cpp_specs:
  arquitectura: "C++ con bindings Python"
  modelo_soporte: "GGUF, GGML, GPTQ"
  backend: "CPU, CUDA, Metal, Vulkan"
  memoria: "Gestión eficiente para modelos grandes"
  velocidad: "Inferencia optimizada con cuantización"
  licencia: "MIT License"
```

**Instalación:**
```bash
# Instalación principal
pip install llama-cpp-python

# Para aceleración GPU (NVIDIA)
pip install llama-cpp-python[cuda]

# Para aceleración GPU (AMD)
pip install llama-cpp-python[hip]

# Para aceleración Apple Silicon
pip install llama-cpp-python[metal]
```

### 📦 Gestión de Dependencias: Poetry

**Tecnología Elegida:** `Poetry` para gestión de dependencias

**Razón de Elección:**
- ✅ Manejo determinístico de dependencias
- ✅ Entornos virtuales aislados
- ✅ Lock files para reproducibilidad
- ✅ Gestión de versiones precisa

**Instalación:**
```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Verificar instalación
poetry --version
```

### 🔧 Herramientas de Desarrollo

#### Git y Control de Versiones
```yaml
git_requirements:
  version: ">=2.34.0"
  configuracion:
    user_name: "Configurar con datos del desarrollador"
    user_email: "Configurar con email del desarrollador"
    default_branch: "main"
    remote_origin: "Repositorio Dungeon Life Ecosystem"
```

#### Herramientas de Shell y Scripting
```yaml
shell_tools:
  bash: "Para scripts de automatización"
  powershell: "Para entorno Windows específico"
  python_subprocess: "Para ejecución de comandos externos"
  pathlib: "Para manejo de rutas multiplataforma"
```

---

## 💾 Modelos de IA Locales

### Modelo Inicial Recomendado

**Opción 1: Llama 3 8B (Recomendado para inicio)**
```yaml
llama3_8b_specs:
  nombre: "Llama-3-8B-Instruct"
  formato: "GGUF"
  cuantizacion: "Q4_K_M"
  tamaño: "~4.7GB"
  memoria_requerida: "8GB RAM"
  contexto_maximo: "8192 tokens"
  calidad: "Excelente para tareas generales"
  velocidad: "Rápida en CPU moderno"
  fuente: "Hugging Face Hub"
```

**Opción 2: Phi-3-mini (Alternativa ligera)**
```yaml
phi3_mini_specs:
  nombre: "Phi-3-mini-4k-instruct"
  formato: "GGUF"
  cuantizacion: "Q4_K_M"
  tamaño: "~2.2GB"
  memoria_requerida: "4GB RAM"
  contexto_maximo: "4096 tokens"
  calidad: "Buena para tareas especializadas"
  velocidad: "Muy rápida"
  fuente: "Hugging Face Hub"
```

### Instalación de Modelos

**Método Automatizado (Recomendado):**
```python
# Script de descarga automática
import requests
import os
from pathlib import Path

class ModelDownloader:
    def __init__(self, models_dir="A:/07_Tools/DungeonLifeAgent/models/"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def download_llama3_8b(self):
        """Descarga Llama 3 8B GGUF"""
        model_url = "https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"
        model_path = self.models_dir / "llama-3-8b-instruct.q4_k_m.gguf"

        print(f"Descargando modelo a {model_path}...")
        response = requests.get(model_url, stream=True)

        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("✅ Modelo descargado exitosamente")
        return model_path

    def download_phi3_mini(self):
        """Descarga Phi-3-mini GGUF"""
        model_url = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
        model_path = self.models_dir / "phi-3-mini-4k-instruct-q4.gguf"

        print(f"Descargando modelo a {model_path}...")
        response = requests.get(model_url, stream=True)

        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("✅ Modelo descargado exitosamente")
        return model_path
```

**Método Manual:**
```bash
# Crear directorio de modelos
mkdir -p "A:/07_Tools/DungeonLifeAgent/models/"

# Descargar modelo Llama 3 8B
wget "https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf" -O "A:/07_Tools/DungeonLifeAgent/models/llama-3-8b-instruct.q4_k_m.gguf"

# Descargar modelo Phi-3-mini (alternativa)
wget "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf" -O "A:/07_Tools/DungeonLifeAgent/models/phi-3-mini-4k-instruct-q4.gguf"
```

---

## 📋 Especificaciones de Hardware

### Requisitos Mínimos
```yaml
hardware_minimum:
  procesador: "Intel i5-10xxx o AMD Ryzen 5 equivalente"
  memoria_ram: "16GB DDR4"
  almacenamiento: "50GB SSD disponible"
  sistema_operativo: "Windows 11, Ubuntu 20.04+, macOS 12.0+"
  red: "No requerida para funcionamiento básico"
```

### Requisitos Recomendados
```yaml
hardware_recommended:
  procesador: "Intel i7-12xxx o AMD Ryzen 7 equivalente"
  memoria_ram: "32GB DDR4 o superior"
  almacenamiento: "100GB SSD NVMe"
  gpu: "NVIDIA RTX 30xx/40xx series (opcional, para aceleración)"
  sistema_operativo: "Windows 11 Pro, Ubuntu 22.04 LTS, macOS 13.0+"
```

### Configuración GPU (Opcional)
```yaml
gpu_acceleration:
  nvidia_cuda:
    version_requerida: "CUDA 11.8+"
    drivers: "NVIDIA drivers 525+"
    memoria_vram: "8GB mínimo"

  apple_metal:
    compatibilidad: "Apple Silicon M1/M2/M3"
    performance: "Optimización automática"

  amd_hip:
    soporte: "Limitado, en desarrollo"
    alternativa: "Usar modo CPU"
```

---

## 🔧 Herramientas de Integración Local

### 🛠️ Herramientas de Sistema

#### Exploración de Archivos
```yaml
file_tools:
  pathlib: "Manejo avanzado de rutas del sistema de archivos"
  os: "Operaciones básicas del sistema operativo"
  shutil: "Operaciones de archivos de alto nivel"
  glob: "Búsqueda avanzada de archivos por patrones"
  fnmatch: "Coincidencia de patrones de archivos"
```

#### Procesamiento de Texto y Documentos
```yaml
text_processing:
  pypdf: "Extracción de texto de PDFs"
  python_docx: "Procesamiento de documentos Word"
  markdown: "Procesamiento de archivos Markdown"
  yaml: "Manejo de archivos YAML"
  json: "Procesamiento de JSON nativo"
  chardet: "Detección automática de encoding"
```

#### Búsqueda y Análisis
```yaml
search_analysis:
  whoosh: "Motor de búsqueda de texto completo"
  sentence_transformers: "Embeddings para búsqueda semántica"
  faiss: "Índices vectoriales para búsqueda rápida"
  numpy: "Computación numérica para análisis"
  pandas: "Análisis de datos estructurados"
```

### 🖥️ Herramientas de Shell

#### Git Integration
```python
# Funciones para integración con Git
import subprocess
import git

class GitIntegration:
    def __init__(self, repo_path="A:/"):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def get_status(self):
        """Obtener estado del repositorio"""
        return {
            "modified": [item.a_path for item in self.repo.index.diff(None)],
            "untracked": [item for item in self.repo.untracked_files],
            "staged": [item.a_path for item in self.repo.index.diff("HEAD")]
        }

    def create_backup_branch(self, branch_name=None):
        """Crear rama de respaldo antes de modificaciones"""
        if branch_name is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            branch_name = f"backup_agent_{timestamp}"

        current_branch = self.repo.active_branch.name
        self.repo.git.checkout('-b', branch_name)
        return branch_name, current_branch

    def commit_changes(self, message="Cambios realizados por Dungeon Life Agent"):
        """Commit de cambios realizados por el agente"""
        self.repo.index.add(['*'])
        self.repo.index.commit(message)
        return self.repo.head.commit.hexsha
```

#### Shell Commands Execution
```python
# Ejecución segura de comandos del sistema
import subprocess
import shlex
from pathlib import Path

class ShellIntegration:
    def __init__(self, working_directory="A:/"):
        self.working_directory = Path(working_directory)

    def execute_command(self, command, timeout=300):
        """Ejecutar comando del sistema de forma segura"""
        try:
            result = subprocess.run(
                shlex.split(command),
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "return_code": e.returncode,
                "error": str(e)
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out"
            }

    def safe_file_operations(self, operation, file_path, content=None):
        """Operaciones seguras con archivos"""
        file_path = self.working_directory / file_path

        if operation == "read":
            return file_path.read_text(encoding='utf-8')
        elif operation == "write" and content:
            file_path.write_text(content, encoding='utf-8')
            return True
        elif operation == "backup":
            backup_path = file_path.with_suffix(f'{file_path.suffix}.backup')
            file_path.replace(backup_path)
            return backup_path
```

---

## ⚙️ Configuración del Sistema

### Archivo de Configuración Principal

**Ubicación:** `A:/07_Tools/DungeonLifeAgent/config.yaml`

```yaml
# Configuración General del Dungeon Life Agent
system_config:
  # Información básica
  agent_name: "Dungeon Life Agent"
  version: "1.0.0"
  installation_path: "A:/07_Tools/DungeonLifeAgent/"

  # Configuración del modelo de IA
  model_config:
    model_path: "models/llama-3-8b-instruct.q4_k_m.gguf"
    # Alternativa: "models/phi-3-mini-4k-instruct-q4.gguf"
    context_length: 8192
    max_tokens: 2048
    temperature: 0.7
    top_p: 0.9
    repetition_penalty: 1.1

    # Configuración de hardware
    hardware_acceleration: "auto"  # auto, cuda, metal, cpu
    gpu_layers: -1  # -1 para automático
    threads: -1     # -1 para automático

  # Configuración de modos operativos
  modes_config:
    default_mode: 1  # 1=Consultor, 2=Taxonómico, 3=Colaborador
    confirmation_required: true
    backup_before_changes: true
    log_operations: true

  # Configuración de conocimiento y memoria
  knowledge_config:
    repository_root: "A:/"
    taxonomy_file: "Doc/Repository_Taxonomy.yaml"
    embeddings_cache: "memory/embeddings_cache.pkl"
    conversation_history: "memory/conversation_history.json"
    max_context_files: 50

  # Configuración de herramientas externas
  tools_config:
    git_integration: true
    shell_commands: true
    file_operations: true
    search_enabled: true

    # Límites de seguridad
    max_file_size: "100MB"
    allowed_extensions: [".md", ".txt", ".py", ".json", ".yaml", ".yml"]
    blocked_paths: ["system32", "Windows", "Program Files"]

  # Configuración de logging
  logging_config:
    log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
    log_file: "memory/agent.log"
    max_log_size: "10MB"
    backup_logs: true

  # Configuración de seguridad
  security_config:
    require_confirmation_mode3: true
    create_backups: true
    validate_changes: true
    operation_timeout: 300  # segundos

  # Configuración de performance
  performance_config:
    cache_embeddings: true
    preload_common_files: true
    optimize_memory_usage: true
    parallel_processing: false
```

### Configuración de Entorno Python

**Archivo:** `pyproject.toml`
```toml
[tool.poetry]
name = "dungeon-life-agent"
version = "1.0.0"
description = "Agente de IA local para el ecosistema Dungeon Life"
authors = ["Dungeon Life Team <team@dungeonlife.eco>"]

[tool.poetry.dependencies]
python = "^3.9"
llama-cpp-python = {version = "^0.2.0", extras = ["cuda"]}
pyyaml = "^6.0"
python-dotenv = "^1.0"
gitpython = "^3.1"
colorama = "^0.4"  # Para colores en terminal Windows
tqdm = "^4.66"     # Para barras de progreso
whoosh = "^2.7"    # Motor de búsqueda
sentence-transformers = "^2.2"  # Para embeddings
faiss-cpu = "^1.7"  # Índices vectoriales
pypdf = "^3.17"    # Procesamiento PDF
python-docx = "^1.1"  # Procesamiento Word
pandas = "^2.1"    # Análisis de datos
numpy = "^1.25"    # Computación numérica

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
black = "^23.0"
isort = "^5.12"
mypy = "^1.5"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
dungeon-life-agent = "agent_core.main:main"
```

---

## 🚀 Proceso de Instalación Paso a Paso

### Paso 1: Preparación del Entorno

```bash
# 1. Crear directorio del agente
mkdir -p "A:/07_Tools/DungeonLifeAgent"
cd "A:/07_Tools/DungeonLifeAgent"

# 2. Inicializar repositorio Git (opcional)
git init

# 3. Crear entorno virtual con Poetry
poetry init --no-interaction --name dungeon-life-agent --version 1.0.0 --description "Agente de IA local para Dungeon Life" --author "Dungeon Life Team <team@dungeonlife.eco>" --python "^3.9"

# 4. Instalar dependencias
poetry install
```

### Paso 2: Configuración Inicial

```python
# Script de configuración inicial
from pathlib import Path
import yaml
import json

class InitialSetup:
    def __init__(self, base_path="A:/07_Tools/DungeonLifeAgent/"):
        self.base_path = Path(base_path)

    def create_directory_structure(self):
        """Crear estructura completa de directorios"""
        directories = [
            "agent_core",
            "models",
            "tools",
            "memory",
            "Doc",
            "config",
            "logs",
            "backups"
        ]

        for dir_name in directories:
            (self.base_path / dir_name).mkdir(parents=True, exist_ok=True)

    def create_config_file(self):
        """Crear archivo de configuración inicial"""
        config = {
            "system_config": {
                "agent_name": "Dungeon Life Agent",
                "version": "1.0.0",
                "installation_path": str(self.base_path),
                "model_config": {
                    "model_path": "models/llama-3-8b-instruct.q4_k_m.gguf",
                    "context_length": 8192,
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                "modes_config": {
                    "default_mode": 1,
                    "confirmation_required": True,
                    "backup_before_changes": True,
                    "log_operations": True
                }
            }
        }

        config_path = self.base_path / "config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        return config_path

    def setup_logging(self):
        """Configurar sistema de logging"""
        import logging

        log_config = {
            'version': 1,
            'formatters': {
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': str(self.base_path / 'logs' / 'agent.log'),
                    'formatter': 'detailed'
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'detailed'
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['console', 'file']
            }
        }

        import logging.config
        logging.config.dictConfig(log_config)

    def run_setup(self):
        """Ejecutar configuración completa"""
        print("🚀 Iniciando configuración del Dungeon Life Agent...")

        self.create_directory_structure()
        print("✅ Estructura de directorios creada")

        config_path = self.create_config_file()
        print(f"✅ Archivo de configuración creado: {config_path}")

        self.setup_logging()
        print("✅ Sistema de logging configurado")

        print("🎉 Configuración inicial completada!")
        print(f"📁 Directorio del agente: {self.base_path}")
        print("📖 Consulte el archivo config.yaml para personalizar la configuración"
```

### Paso 3: Instalación del Modelo

```bash
# Opción A: Descarga automática
cd "A:/07_Tools/DungeonLifeAgent"
python -c "
from tools.model_downloader import ModelDownloader
downloader = ModelDownloader()
model_path = downloader.download_llama3_8b()
print(f'Modelo instalado en: {model_path}')
"

# Opción B: Descarga manual (ver sección anterior)
# Colocar el archivo .gguf en A:/07_Tools/DungeonLifeAgent/models/
```

### Paso 4: Verificación de Instalación

```python
# Script de verificación
import sys
from pathlib import Path

class InstallationVerifier:
    def __init__(self, base_path="A:/07_Tools/DungeonLifeAgent/"):
        self.base_path = Path(base_path)
        self.issues = []

    def check_python_version(self):
        """Verificar versión de Python"""
        version = sys.version_info
        if version.major == 3 and version.minor >= 9:
            print("✅ Python 3.9+ detectado")
            return True
        else:
            self.issues.append(f"❌ Python {version.major}.{version.minor} detectado. Se requiere Python 3.9+")
            return False

    def check_dependencies(self):
        """Verificar dependencias críticas"""
        required_packages = [
            'llama_cpp',
            'yaml',
            'git',
            'pathlib'
        ]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('_', ''))
                print(f"✅ {package} instalado")
            except ImportError:
                missing_packages.append(package)
                self.issues.append(f"❌ Paquete faltante: {package}")

        return len(missing_packages) == 0

    def check_model_file(self):
        """Verificar archivo de modelo"""
        model_path = self.base_path / "models" / "llama-3-8b-instruct.q4_k_m.gguf"
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024*1024)
            print(f"✅ Modelo encontrado: {size_mb:.1f} MB")
            return True
        else:
            self.issues.append("❌ Archivo de modelo no encontrado")
            return False

    def check_directory_structure(self):
        """Verificar estructura de directorios"""
        required_dirs = [
            "agent_core",
            "models",
            "tools",
            "memory",
            "Doc"
        ]

        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                print(f"✅ Directorio {dir_name} encontrado")
            else:
                missing_dirs.append(dir_name)
                self.issues.append(f"❌ Directorio faltante: {dir_name}")

        return len(missing_dirs) == 0

    def run_verification(self):
        """Ejecutar verificación completa"""
        print("🔍 Verificando instalación del Dungeon Life Agent...")
        print("=" * 60)

        all_checks_passed = True

        # Verificaciones básicas
        all_checks_passed &= self.check_python_version()
        all_checks_passed &= self.check_directory_structure()
        all_checks_passed &= self.check_model_file()
        all_checks_passed &= self.check_dependencies()

        print("=" * 60)

        if all_checks_passed:
            print("🎉 ¡Instalación verificada exitosamente!")
            print("🚀 El agente está listo para usar")
        else:
            print("⚠️ Problemas encontrados durante la verificación:")
            for issue in self.issues:
                print(f"  {issue}")
            print("\n📖 Consulte la documentación para solucionar estos problemas")

        return all_checks_passed
```

---

## 🔧 Configuración Avanzada

### Configuración Multi-Modelo

```yaml
# Configuración para múltiples modelos
multi_model_config:
  modelos_disponibles:
    modelo_principal:
      nombre: "llama-3-8b-instruct.q4_k_m.gguf"
      descripcion: "Modelo general para todas las tareas"
      contexto_maximo: 8192
      temperatura: 0.7

    modelo_rapido:
      nombre: "phi-3-mini-4k-instruct-q4.gguf"
      descripcion: "Modelo ligero para respuestas rápidas"
      contexto_maximo: 4096
      temperatura: 0.8

    modelo_creativo:
      nombre: "llama-3-8b-instruct.q4_k_m.gguf"
      descripcion: "Modelo ajustado para tareas creativas"
      contexto_maximo: 8192
      temperatura: 0.9

  reglas_seleccion:
    consultas_simples: "modelo_rapido"
    consultas_creativas: "modelo_creativo"
    consultas_complejas: "modelo_principal"
```

### Configuración de Memoria y Caché

```yaml
# Configuración avanzada de memoria
memory_config:
  embeddings:
    modelo: "all-MiniLM-L6-v2"
    dimensiones: 384
    cache_size: 10000
    actualizar_en_cambios: true

  cache_conversaciones:
    max_conversaciones: 1000
    max_mensajes_por_conversacion: 100
    compresion_automatica: true

  conocimiento_repository:
    indexar_automaticamente: true
    actualizar_periodicamente: true
    intervalo_actualizacion: 3600  # segundos
```

---

## 🛠️ Herramientas de Desarrollo Incluidas

### Scripts de Utilidad

#### Script de Actualización de Modelo
```python
# tools/update_model.py
import argparse
from model_downloader import ModelDownloader

def main():
    parser = argparse.ArgumentParser(description="Actualizar modelo de IA")
    parser.add_argument("--model", choices=["llama3", "phi3"], default="llama3",
                       help="Modelo a descargar")

    args = parser.parse_args()

    downloader = ModelDownloader()
    if args.model == "llama3":
        model_path = downloader.download_llama3_8b()
    else:
        model_path = downloader.download_phi3_mini()

    print(f"Modelo actualizado: {model_path}")

if __name__ == "__main__":
    main()
```

#### Script de Optimización de Memoria
```python
# tools/optimize_memory.py
import psutil
import GPUtil
from config_manager import ConfigManager

class MemoryOptimizer:
    def __init__(self):
        self.config = ConfigManager()

    def optimize_for_hardware(self):
        """Optimizar configuración según hardware disponible"""
        # Detectar RAM disponible
        ram_gb = psutil.virtual_memory().available / (1024**3)

        # Detectar GPU disponible (si aplica)
        gpus = GPUtil.getGPUs()

        if ram_gb < 8:
            print("⚠️ RAM limitada detectada. Usando configuración mínima.")
            self.config.set("model_config.gpu_layers", 0)
            self.config.set("model_config.threads", 2)
        elif ram_gb < 16:
            print("ℹ️ RAM moderada. Configuración balanceada.")
            self.config.set("model_config.gpu_layers", 20)
            self.config.set("model_config.threads", 4)
        else:
            print("✅ RAM suficiente. Configuración óptima.")
            self.config.set("model_config.gpu_layers", -1)
            self.config.set("model_config.threads", -1)

        return self.config.save()
```

---

## 🔒 Seguridad y Permisos

### Configuración de Seguridad

```yaml
# Configuración de seguridad estricta
security_config:
  permisos_archivos:
    lectura_permitida: true
    escritura_permitida: false  # Requiere confirmación explícita
    eliminacion_permitida: false

  rutas_protegidas:
    - "C:/Windows"
    - "C:/Program Files"
    - "C:/Users/*/AppData"

  operaciones_requieren_confirmacion:
    - "archivo_creacion"
    - "archivo_modificacion"
    - "archivo_eliminacion"
    - "directorio_creacion"
    - "git_commit"

  validacion_contenido:
    max_tamano_archivo: "100MB"
    extensiones_permitidas: [".md", ".txt", ".py", ".json", ".yaml"]
    contenido_malicioso: false
```

### Sistema de Backups Automáticos

```python
# Sistema de respaldo automático
class BackupManager:
    def __init__(self, backup_dir="A:/07_Tools/DungeonLifeAgent/backups/"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self, file_path, reason="Modificación por agente"):
        """Crear respaldo antes de modificaciones"""
        original_file = Path(file_path)
        if not original_file.exists():
            return None

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{original_file.name}_{timestamp}.bak"
        backup_path = self.backup_dir / backup_name

        import shutil
        shutil.copy2(original_file, backup_path)

        # Registrar backup
        backup_record = {
            "original_file": str(original_file),
            "backup_file": str(backup_path),
            "timestamp": timestamp,
            "reason": reason,
            "file_size": original_file.stat().st_size
        }

        with open(self.backup_dir / "backup_log.json", 'a') as f:
            f.write(json.dumps(backup_record) + '\n')

        return backup_path
```

---

## 🚨 Solución de Problemas Comunes

### Problemas de Instalación

#### Error: "No se puede instalar llama-cpp-python"
```bash
# Solución para Windows
# 1. Instalar Microsoft Visual C++ Build Tools
# 2. Usar alternativa más simple:
pip install llama-cpp-python --only-binary=all

# 3. Si persiste, usar versión CPU-only:
pip install llama-cpp-python --extra-index-url https://download.pytorch.org/whl/cpu
```

#### Error: "Modelo no encontrado"
```python
# Verificar ruta del modelo
model_path = Path("A:/07_Tools/DungeonLifeAgent/models/llama-3-8b-instruct.q4_k_m.gguf")
if not model_path.exists():
    print("Modelo no encontrado. Ejecutar descarga primero.")
    # Ejecutar script de descarga
```

#### Error: "Memoria insuficiente"
```yaml
# Soluciones:
memory_solutions:
  reducir_contexto: "Disminuir context_length en config.yaml"
  usar_modelo_mas_pequeno: "Cambiar a phi-3-mini"
  optimizar_gpu_layers: "Reducir número de capas en GPU"
  aumentar_memoria_virtual: "Agregar archivo de paginación en Windows"
```

### Problemas de Rendimiento

#### El agente responde lentamente
```yaml
# Optimizaciones:
performance_optimizations:
  reducir_context_length: 4096
  aumentar_gpu_layers: -1  # Usar GPU completamente
  habilitar_cache: true
  reducir_threads: 4  # Si causa problemas
```

#### Alto uso de memoria
```python
# Estrategias de optimización:
memory_strategies:
  1. Usar modelo cuantizado más pequeño (Q4_K_S vs Q4_K_M)
  2. Reducir contexto máximo a 4096 tokens
  3. Procesar archivos grandes en chunks
  4. Implementar limpieza periódica de caché
```

---

## 📊 Métricas de Instalación

### Verificación de Salud del Sistema

```python
class SystemHealthChecker:
    def __init__(self):
        self.metrics = {}

    def check_overall_health(self):
        """Verificar salud general del sistema"""
        self.metrics['memory_usage'] = self._check_memory_usage()
        self.metrics['disk_space'] = self._check_disk_space()
        self.metrics['model_integrity'] = self._check_model_integrity()
        self.metrics['dependencies_health'] = self._check_dependencies_health()

        return self.metrics

    def _check_memory_usage(self):
        """Verificar uso de memoria"""
        import psutil
        memory = psutil.virtual_memory()
        return {
            'total_gb': memory.total / (1024**3),
            'available_gb': memory.available / (1024**3),
            'usage_percent': memory.percent
        }

    def _check_disk_space(self):
        """Verificar espacio en disco"""
        import shutil
        disk_usage = shutil.disk_usage("A:/")
        return {
            'total_gb': disk_usage.total / (1024**3),
            'free_gb': disk_usage.free / (1024**3),
            'usage_percent': (disk_usage.used / disk_usage.total) * 100
        }

    def _check_model_integrity(self):
        """Verificar integridad del modelo"""
        model_path = Path("A:/07_Tools/DungeonLifeAgent/models/llama-3-8b-instruct.q4_k_m.gguf")
        if model_path.exists():
            file_size = model_path.stat().st_size
            expected_size = 4.7 * 1024**3  # ~4.7GB
            return abs(file_size - expected_size) / expected_size < 0.1
        return False

    def _check_dependencies_health(self):
        """Verificar salud de dependencias"""
        critical_packages = ['llama_cpp', 'yaml', 'git']
        healthy_packages = 0

        for package in critical_packages:
            try:
                __import__(package.replace('_', ''))
                healthy_packages += 1
            except ImportError:
                pass

        return healthy_packages / len(critical_packages)
```

---

## 🎯 Próximos Pasos Después de Instalación

1. **Verificar Instalación**: Ejecutar script de verificación incluido
2. **Personalizar Configuración**: Ajustar `config.yaml` según necesidades específicas
3. **Crear Taxonomía Inicial**: Desarrollar `Repository_Taxonomy.yaml` base
4. **Probar Modos Operativos**: Validar funcionamiento de los tres modos
5. **Integrar con Proyecto**: Conectar con el ecosistema Dungeon Life existente
6. **Configurar Backups**: Establecer estrategia de respaldos automáticos
7. **Documentar Procedimientos**: Crear guías específicas del proyecto

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Documentación llama.cpp](https://github.com/ggerganov/llama.cpp)
- [Guía llama-cpp-python](https://llama-cpp-python.readthedocs.io/)
- [Modelos GGUF en Hugging Face](https://huggingface.co/models?library=gguf)

### Comunidades y Soporte
- [Reddit r/LocalLLaMA](https://reddit.com/r/LocalLLaMA)
- [Discord Ollama](https://discord.gg/ollama)
- [Foro Hugging Face](https://discuss.huggingface.co/)

### Herramientas de Monitoreo
- [Glances](https://nicolargo.github.io/glances/) - Monitor del sistema
- [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) - Monitor GPU
- [htop](https://htop.dev/) - Monitor de procesos (Linux/macOS)

Este documento proporciona una guía completa para instalar y configurar el Dungeon Life Agent con todas las tecnologías necesarias para su funcionamiento óptimo dentro del ecosistema DLE.</result>
</attempt_completion>
---

## ⚙️ Puesta en Marcha del MVP Funcional

La versión mínima viable del Dungeon Life Agent incluida en este repositorio proporciona:

- Indexación local de toda la carpeta `Documentacion/` mediante `dungeon_life_agent.knowledge`.
- Gestión de modos y permisos alineada con el diseño original (`consultor`, `taxonomico`, `colaborador`).
- Herramientas de consulta accesibles desde CLI (`willow`) y una interfaz interactiva (`run_agent.py`).
- Autocompletado asistido, refresco incremental del índice y métricas de rendimiento durante la sesión.

### Pasos Rápidos

```bash
# Instalar en modo editable para mantener el código sincronizado
pip install -e .

# Ejecutar comprobaciones básicas de entorno
python scripts/setup_agent.py

# Lanzar la interfaz interactiva con autocompletado y métricas
python run_agent.py

# Alternativa: usar la CLI con selección de modo y rol
willow --mode taxonomico --role productor "Preparar entregables del MVP"

# Obtener sugerencias de consulta antes de lanzar una búsqueda
willow --suggest-queries "tax" --limit 8

# Reconstruir el índice tras actualizar documentación específica
willow --refresh-index Documentacion/05_Taxonomia_y_Nomenclatura.md

# Revisar métricas de latencia acumuladas (misma sesión de CLI)
willow --metrics
```

### Configuración Personalizada

- El archivo `dungeon_life_agent/config/default_config.json` describe roles, tonos y permisos.
- Puede duplicarse como `config.local.json` y pasarse con `--config` en la CLI.
- Los modos adicionales se pueden añadir extendiendo `default_config.json` y ajustando los permisos.

### Validación Rápida

```bash
# Ejecutar las pruebas automatizadas (requiere pytest)
PYTHONPATH=. pytest
```

Estas instrucciones garantizan que cualquier guardián pueda replicar el MVP funcional antes de avanzar a la integración con modelos GGUF.

### Comandos interactivos destacados (`run_agent.py`)

- `ayuda` → muestra el listado de comandos disponibles.
- `sugerencias <prefijo> [limite]` → despliega autocompletado contextual.
- `refrescar [ruta.md]` → fuerza la reindexación incremental (requiere modo colaborador en la configuración).
- `metricas` → imprime latencia promedio, máxima y número de resultados por modo recopilados en la sesión.
