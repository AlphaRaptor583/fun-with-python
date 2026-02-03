from flask import Flask, request, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import socket
import ipinfo

app = Flask(__name__)

# Replace with your actual token from ipinfo.io
IPINFO_TOKEN = '492d85d289a8c4'
ipinfo_handler = ipinfo.getHandler(IPINFO_TOKEN)

INTERCEPT_SCRIPT = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("a").forEach(function(link) {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const target = link.getAttribute("href");
            if (target && !target.startsWith("javascript:")) {
                const encoded = encodeURIComponent(target);
                window.location.href = `/embed?url=${encoded}`;
            }
        });
    });
});
</script>
"""

def resolve_ip(hostname):
    try:
        info = socket.getaddrinfo(hostname, None)
        ip = info[0][4][0]
        return ip
    except Exception:
        return "Unknown"

def get_ipinfo(ip):
    try:
        details = ipinfo_handler.getDetails(ip)
        return {
            "location": f"{details.city or 'Unknown'}, {details.region or 'Unknown'}, {details.country_name or 'Unknown'}",
            "org": details.org or "Unknown",
            "timezone": details.timezone or "Unknown",
            "privacy": details.privacy if hasattr(details, 'privacy') else {}
        }
    except Exception:
        return {
            "location": "Unknown",
            "org": "Unknown",
            "timezone": "Unknown",
            "privacy": {}
        }

def fetch_rendered_html(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        final_url = driver.current_url
        html = driver.page_source
    finally:
        driver.quit()

    hostname = urlparse(final_url).hostname
    ip_address = resolve_ip(hostname)
    ipinfo_data = get_ipinfo(ip_address)

    if "</body>" in html:
        html = html.replace("</body>", INTERCEPT_SCRIPT + "</body>")
    else:
        html += INTERCEPT_SCRIPT

    return html, final_url, ip_address, ipinfo_data

@app.route('/')
def home():
    return '''
        <form action="/embed" method="get" style="margin: 20px;">
            <input type="text" name="url" placeholder="Enter URL to embed" required style="width: 60%;">
            <button type="submit">Go</button>
        </form>
    '''

@app.route('/embed')
def embed():
    raw_url = request.args.get('url')
    if not raw_url:
        return "No URL provided."

    try:
        html, final_url, ip_address, info = fetch_rendered_html(raw_url)
        vpn_status = "Yes" if info["privacy"].get("vpn") else "No"
        proxy_status = "Yes" if info["privacy"].get("proxy") else "No"

        browser_bar = f"""
            <div style="padding: 10px; background-color: #003300; color: #00FF00; font-family: monospace; border-bottom: 2px solid #00FF00;">
                <form action="/embed" method="get" style="display: flex; gap: 10px;">
                    <input type="text" name="url" value="{final_url}" style="flex: 1; padding: 5px; background-color: black; color: #00FF00; border: 1px solid #00FF00;">
                    <button type="submit" style="background-color: black; color: #00FF00; border: 1px solid #00FF00;">Go</button>
                </form>
                <div style="margin-top: 5px; font-size: 0.9em;">
                    Server IP: <strong>{ip_address}</strong> |
                    Location: <strong>{info['location']}</strong> |
                    ISP: <strong>{info['org']}</strong> |
                    Timezone: <strong>{info['timezone']}</strong> |
                    VPN: <strong>{vpn_status}</strong> |
                    Proxy: <strong>{proxy_status}</strong>
                </div>
            </div>
        """
        full_page = browser_bar + html
        return Response(full_page, mimetype='text/html')
    except Exception as e:
        return f"Error fetching page: {e}"

if __name__ == '__main__':
    app.run(debug=True)
