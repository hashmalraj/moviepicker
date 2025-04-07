from flask import Flask, render_template, url_for
import random
import json, requests, re

app = Flask(__name__)

def code():
    with open("thelist.json", "r") as file:
        data = json.load(file)
    slug = random.choice(data)
    movie = (slug[0].replace('-', " ")).title()
    minutes = slug[1]
    duration = f"{minutes//60} hr {minutes%60}"
    response = requests.get("https://www.letterboxd.com/film/"+slug[0])
    pattern = r'"ratingValue":(.*?),"description"'
    posterpattern = r'img src="(.*?)" class="image" width="230"'
    posterurl = re.findall(posterpattern, response.text)
    rating = re.findall(pattern, response.text)
    r = float(rating[0])
    if r>= 4.5:
        stars = "⭐⭐⭐⭐½"
    elif r>=4.0:
        stars = "⭐⭐⭐⭐"
    elif r>= 3.5:
        stars = "⭐⭐⭐½"
    elif r>=3.0:
        stars="⭐⭐⭐"
    output = f'{movie} - {duration} min {stars}'
    return output

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/run-code', methods=['POST'])
def run_code():
    output = code()
    return render_template('index.html', result=output)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)