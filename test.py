import psutil

for proc in psutil.process_iter(['name', 'pid']):
    print(proc.info)  # Affiche les informations du processus