from pathlib import Path

# Automatically resolve the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent

# Define subdirectories relative to root
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
CLEANED_DIR = DATA_DIR / "cleaned"
PROCESSED_DIR = DATA_DIR / "processed"
VISUALS_DIR = DATA_DIR / "visuals"
OUTPUTS_DIR = ROOT_DIR / "outputs"
MODELS_DIR = OUTPUTS_DIR / "models"
CHECKS_DIR = OUTPUTS_DIR / "checks"

# Create folders if they don't exist
for path in [
    RAW_DIR,
    CLEANED_DIR,
    PROCESSED_DIR,
    VISUALS_DIR,
    OUTPUTS_DIR,
    MODELS_DIR,
    CHECKS_DIR
]:
    path.mkdir(parents=True, exist_ok=True)
