import requests
from assets.colors.colors import colors
import threading 

def saveLog(data, file_path):
    with open(file_path, 'a') as file:
        file.write(data + '\n')
def getFile(files):
    with open(files, 'r') as f:
        return f.read().splitlines()

def getUrl(url, path):
    getAdmin = f"{url}/{path}"
    try:
        response = requests.get(getAdmin)
        handleResponse(response, getAdmin)
    except requests.exceptions.SSLError:
        print(f"[{colors.red}✗{colors.reset}] {getAdmin} [{colors.red} SSL Error, trying HTTP  {colors.reset}]")
        getAdmin = getAdmin.replace("https://", "http://")
        try:
            response = requests.get(getAdmin)
            handleResponse(response, getAdmin)
        except:
            print(f"[{colors.red}✗{colors.reset}] {getAdmin} [{colors.red} Connection Error {colors.reset}]")
    except requests.exceptions.ConnectionError:
        print(f"[{colors.red}✗{colors.reset}] {getAdmin} [{colors.red} Connection Error {colors.reset}]")

def handleResponse(response, url):
    if response.status_code == 200:
        print(f"[{colors.green}✓{colors.reset}] {url} [{colors.green} Found {colors.reset}]")
        saveLog(f"{url}", 'result/foundAdminLogin.txt')
    else:
        print(f"[{colors.red}✗{colors.reset}] {url} [{colors.red} Not Found {colors.reset}]")

def scanUrl(urls, dirAdmin, num_threads=10):
    def worker():
        while True:
            try:
                url = urls.pop()
            except IndexError:
                break
            for file in dirAdmin:
                getUrl(url, file)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def AdminFinder():
    url_list = input("[卂] input your list of urls => ")
    files = "assets/path/dir/admin.txt"

    dirAdmin = getFile(files)
    urls = getFile(url_list)

    num_threads = input("[卂] Enter number of threads (default is 10): ")
    if not num_threads.isdigit():
        num_threads = 10 
    else:
        num_threads = int(num_threads)
    scanUrl(urls, dirAdmin, num_threads)
    print("log save to result/foundAdminLogin.txt")
