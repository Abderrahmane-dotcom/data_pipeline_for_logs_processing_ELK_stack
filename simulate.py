import time
from pathlib import Path

# --- Configurations ---
SOURCE_ROOT = Path("./logs_data/OneDrive_1_21-10-2025")
DEST_DIR = Path("./logs")
DELAY_BETWEEN_LINES = 0.08  # secondes entre chaque ligne

# Création du dossier logs si n'existe pas
DEST_DIR.mkdir(parents=True, exist_ok=True)
print(f"📝 Les fichiers seront écrits dans : {DEST_DIR.resolve()}")

# Parcours des dossiers log-*
folders = sorted([f for f in SOURCE_ROOT.iterdir() if f.is_dir() and f.name.startswith("log-")])
print(f"📁 Dossiers trouvés : {[f.name for f in folders]}")

# Boucle sur chaque dossier
for folder in folders:
    print(f"\n▶️ Traitement du dossier : {folder.name}")

    log_files = sorted(folder.glob("*.*"))  # prend tous les fichiers
    if not log_files:
        print("   ⚠️ Aucun fichier trouvé dans ce dossier.")
        continue

    for src_file in log_files:
        print(f"   ➜ Lecture du fichier source : {src_file.name}")
        dest_file = DEST_DIR / (src_file.stem + ".txt")

        # Supprimer un ancien fichier s'il existe
        if dest_file.exists():
            dest_file.unlink()

        # Écriture ligne par ligne
        with open(src_file, "r", encoding="utf-8", errors="ignore") as src, \
             open(dest_file, "a", encoding="utf-8") as dest:

            for line in src:
                dest.write(line)
                dest.flush()  # pour que Filebeat détecte immédiatement la ligne
                print(f"      Ligne ajoutée : {line.strip()}")
                time.sleep(DELAY_BETWEEN_LINES)

        print(f"   ✅ Fichier {dest_file.name} terminé.")
        time.sleep(1)
        
print("\n🎉 Simulation terminée : tous les fichiers ont été écrits ligne par ligne.")
