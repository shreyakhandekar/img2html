from flask import *
import os

app = Flask(__name__, template_folder='templates',
            static_url_path='',
            static_folder='../img2html')
file = open(r'trial.py', 'r').read()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        img = request.files['file']
        img.save("sample.png")
        exec(file)
        with open("sample.html", "r") as f:
            content = f.read()
        return render_template("success.html",content=content,img = img)


if __name__ == '__main__':
    app.run(debug=True)