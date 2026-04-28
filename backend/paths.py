from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

# Основные папки
BACKEND_DIR = ROOT_DIR / "backend"
DATA_DIR = BACKEND_DIR / "data"

# Создаём если нет
BACKEND_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Основные файлы
AUTH_LOG = BACKEND_DIR / "auth.log"
INCIDENTS_FILE = DATA_DIR / "incidents.json.gz"

CONFIG_FILE = ROOT_DIR / "config.json"
IOC_FILE = ROOT_DIR / "ioc_list.json"
ML_BASELINE_FILE = ROOT_DIR / "ml_baseline.json"
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"

# Автосоздание файлов при необходимости
AUTH_LOG.touch(exist_ok=True)