# Fungsi Shell Finder 

import os
import requests
import concurrent.futures
from colorama import Fore, Style, init

init()
red = Fore.RED
green = Fore.LIGHTGREEN_EX
yellow = Fore.YELLOW
reset = Style.RESET_ALL
blue = Fore.BLUE
DEFAULT_THREADS = 10

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_to_file(data, file_path):
    with open(file_path, 'a') as file:
        file.write(data + '\n')

def scan_directory(url, directory_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=DEFAULT_THREADS) as executor:
        futures = {executor.submit(scan_directory_worker, url, dir_name): dir_name for dir_name in directory_list}
        concurrent.futures.wait(futures)

def scan_directory_worker(url, dir_name):
    dir_url = f"{url}/{dir_name}"

    try:
        response = requests.get(dir_url)
        handle_response(response, dir_url)

    except requests.exceptions.SSLError:
        print(f"[{red}✗{reset}] {dir_url} [{red} SSL Error, trying HTTP  {reset}]")
        dir_url = dir_url.replace("https://", "http://")
        response = requests.get(dir_url)
        handle_response(response, dir_url)

def handle_response(response, url):
    if response.status_code == 403:
        print(f"[{green}={reset}] {url} [{green} Found Dir {reset}]")
        detect_cms(url)
        scan_files(url, "found")
    elif response.status_code == 200:
        print(f"[{yellow}={reset}] {url} [{yellow} Directory Listening {reset}]")
        scan_files(url, "listening")
    else:
        print(f"[{red}={reset}] {url} [{red} not found {reset}]")

def detect_cms(url):
    cms_directories = ['/wp-content', '/administrator', '/admin', '/catalog', '/pkp', '/sites', '/whmcms']

    for cms_dir in cms_directories:
        cms_url = f"{url}/{cms_dir}"
        response = requests.get(cms_url)

        if response.status_code == 200:
            print(f"[{blue}✗{reset}] {cms_url} [{blue} found {get_cms_name(cms_dir)} {reset}]")
            save_to_file(f"[✗] {cms_url} [ found {get_cms_name(cms_dir)} ]", 'found_outputs/cms_found.txt')

def get_cms_name(cms_dir):
    cms_mapping = {
        '/wp-content': 'Wordpress',
        '/administrator': 'Joomla',
        '/admin': 'OpenCart',
        '/catalog': 'Pkp',
        '/sites': 'Drupal',
        '/whmcms': 'WHMCMS'
    }

    return cms_mapping.get(cms_dir, 'Unknown CMS')

def scan_files(url, scan_type):
    files_url = f"{url}"

    if scan_type == "found" or scan_type == "listening":
        file_list = read_file_content('assets/path/file/fileshell.txt')

        with concurrent.futures.ThreadPoolExecutor(max_workers=DEFAULT_THREADS) as executor:
            futures = {executor.submit(scan_files_worker, f"{files_url}{file_name}"): file_name for file_name in file_list}
            concurrent.futures.wait(futures)

def scan_files_worker(file_url):
    try:
        response = requests.get(file_url)

        if response.status_code == 200:
            print(f"[{green}✓{reset}] {file_url} [{green} Found Shell {reset}]")
            save_to_file(f"{file_url}", 'result/foundShell.txt')
        else:
            print(f"[{red}✓{reset}] {file_url} [{red} Not Found {reset}]")

    except requests.exceptions.SSLError:
        print(f"[{red}‽{reset}] {file_url} [{red} SSL Error {reset}]")

def shell():
    create_directory('result')
    target_file_path = input(f"{yellow}Input your target file => {reset}")
    target_urls = read_file_content(target_file_path)

    for target_url in target_urls:
        print(f"\n===== Scanning {yellow}{target_url}{reset} =====")
        dir_list = read_file_content('assets/path/dir/dirshell.txt')
        scan_directory(target_url, dir_list)

if __name__ == "__main__":
    shell()