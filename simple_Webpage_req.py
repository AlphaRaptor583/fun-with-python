# Python 3, Flask example
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

@app.route("/proxy")
def proxy():
    # Fetch website content
    url = "https://mygiis.org"
    response = requests.get(url)
    content = response.text

    # Optionally modify content if necessary
    return render_template_string(content)

if __name__ == "__main__":
    app.run(debug=True)