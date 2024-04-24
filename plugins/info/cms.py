from assets.colors.colors import colors
import requests
import builtwith
from concurrent.futures import ThreadPoolExecutor

def detect_framework_single(url):
    try:
        technologies = builtwith.builtwith(url)

        if technologies:
            print("\nDetected Technologies for", url)
            for tech, version in technologies.items():
                print(f"[{colors.green}?{colors.reset}] {tech}: {colors.yellow}{version[0]}{colors.reset}")
        else:
            print(f"\n[*] No technologies detected for {url}.")

    except requests.exceptions.RequestException as e:
        print("\n[ ! ] Failed to detect framework for", url, ":", e)

def detect_framework_mass(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(detect_framework_single, [url.strip() for url in urls])

    except FileNotFoundError:
        print("\n[ ! ] File not found:", file_path)
    except Exception as e:
        print("\n[ ! ] Error:", e)

def cmsScanner():
    input_type = input("Pilih tipe input (single/mass): ").lower()

    if input_type == 'single':
        target_url = input("Masukkan URL target: ")
        detect_framework_single(target_url)

    elif input_type == 'mass':
        file_path = input("Masukkan path file TXT: ")
        detect_framework_mass(file_path)

    else:
        print("\n[ ! ] Tipe input tidak valid.")
    
