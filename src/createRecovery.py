import zipfile
import os

def createRecovery(folder):
    """Creates a zip file of the folder"""
    zipf = zipfile.ZipFile(f"recovery.dc", "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

createRecovery("data")