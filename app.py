from flask import Flask, render_template, request
from vuln_scanner import scan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        url = request.form["url"]
        if not url.startswith("http"):
            url = "http://" + url
        results = scan(url)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
