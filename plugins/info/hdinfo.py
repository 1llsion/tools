import urllib.request
from assets.colors.colors import colors
import socket

class WebsiteHeaders:
    def __init__(self, target_url):
        self.target_url = target_url
        self.sec_headers = {
            'X-XSS-Protection': 'deprecated',
            'X-Frame-Options': 'warning',
            'X-Content-Type-Options': 'warning',
            'Strict-Transport-Security': 'error',
            'Content-Security-Policy': 'warning',
            'X-Permitted-Cross-Domain-Policies': 'deprecated',
            'Referrer-Policy': 'warning',
            'Expect-CT': 'deprecated',
            'Permissions-Policy': 'warning',
            'Cross-Origin-Embedder-Policy': 'warning',
            'Cross-Origin-Resource-Policy': 'warning',
            'Cross-Origin-Opener-Policy': 'warning'
        }

    def get_information_headers(self):
        try:
            req = urllib.request.Request(self.target_url, method='HEAD')
            response = urllib.request.urlopen(req)
            headers = dict(response.info())
            return headers

        except Exception as e:
            print(f"Error: {e}")
            return None

    def analyze_headers(self):
        headers = self.get_information_headers()

        if headers:
            effective_url = self.target_url
            print(f"[*] Analyzing headers of {colors.cyan}{self.target_url}{colors.reset}")
            print(f"[*] Effective URL: {colors.cyan}{effective_url}{colors.reset}")

            missing_sec_headers = []
            present_sec_headers = []
            info_disclosure_headers = []
            cache_control_headers = []

            for key, value in self.sec_headers.items():
                if key in headers:
                    present_sec_headers.append(f"[*] Header {colors.green}{key}{colors.reset} is present! (Value: {headers[key]})")
                else:
                    missing_sec_headers.append(f"[{colors.red}!{colors.reset}] Missing security header: {colors.magenta}{key}{colors.reset}")

            for key in headers:
                if key.lower().startswith('server'):
                    info_disclosure_headers.append(f"[{colors.red}!{colors.reset}] Possible information disclosure: header {colors.magenta}{key}{colors.reset} is present! (Value: {headers[key]})")
                elif key.lower() == 'cache-control':
                    cache_control_headers.append(f"[{colors.green}+{colors.reset}] Cache control header {colors.cyan}{key}{colors.reset} is present! (Value: {headers[key]})")

            print("\n".join(missing_sec_headers))
            print("\n".join(present_sec_headers))
            print("\n".join(info_disclosure_headers))
            print("\n".join(cache_control_headers))
            print("-" * 55)
            print(f"[{colors.cyan}!{colors.reset}] Headers analyzed for {colors.cyan}{effective_url}{colors.reset}")
            print(f"[{colors.green}+{colors.reset}] There are {colors.green}{len(present_sec_headers)}{colors.reset} security headers")
            print(f"[{colors.red}-{colors.reset}] There are not {colors.red}{len(missing_sec_headers)}{colors.reset} security headers")
        else:
            print("\nFailed to retrieve headers.")

    def get_cookie(self):
        headers = self.get_information_headers()
        if headers and 'Set-Cookie' in headers:
            return headers['Set-Cookie']
        else:
            return None

    def get_ip(self):
        try:
            
            parsed_url = urllib.parse.urlparse(self.target_url)
            domain = parsed_url.netloc
            ip = socket.gethostbyname(domain)
            return ip
        except (socket.gaierror, ValueError):
            print(f"Error: Unable to resolve IP address for {self.target_url}")
            return None

    def get_sharing_domains_from_ip(self):
        ip = self.get_ip()
        if ip:
            try:
                shared_domains = []
                hostnames, _, _ = socket.gethostbyaddr(ip)
                for hostname in hostnames:
                    shared_domains.append(hostname)
                return shared_domains
            except socket.herror:
                print(f"Error: Unable to resolve hostnames for IP {ip}")
                return None
        else:
            return None

def hdInfo():
    target_url = input("Masukkan URL target: ")
    website = WebsiteHeaders(target_url)

    website.analyze_headers()
    cookie = website.get_cookie()
    if cookie:
        print(f"\n[{colors.green}+{colors.reset}] Cookie: {colors.magenta}{cookie}{colors.reset}")

    ip = website.get_ip()
    if ip:
        print(f"\n[{colors.green}+{colors.reset}] IP Address: {colors.magenta}{ip}{colors.reset}")
        shared_domains = website.get_sharing_domains_from_ip()
        if shared_domains:
            print("\nSharing Domains:")
            for domain in shared_domains:
                print(domain)
        else:
            print("No sharing domains found.")

if __name__ == "__main__":
    hdInfo()