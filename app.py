from flask import Flask, render_template
import random
import platform

app = Flask(__name__)

# list of cat images
images = [
"https://media.giphy.com/media/H4DjXQXamtTiIuCcRU/giphy.gif",
"https://media.giphy.com/media/MCfhrrNN1goH6/giphy.gif",
"https://media.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy.gif",
"https://media.giphy.com/media/LqON4xbn2u0JDWRniQ/giphy.gif",
"https://media.giphy.com/media/IWG1kktEJFFDy/giphy.gif",
"https://media.giphy.com/media/QGwIkEl3QbIY0/giphy.gif",
"https://media.giphy.com/media/2eKoCnqFwHpD5W7RW6/giphy.gif",
"https://media.giphy.com/media/1BGwLa5CRz8pZK6bbH/giphy.gif",
"https://media.giphy.com/media/11s7Ke7jcNxCHS/giphy.gif",
"https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif",
"https://media.giphy.com/media/Nm8ZPAGOwZUQM/giphy.gif",
"https://media.giphy.com/media/Jjo6WPW26zDdS/giphy.gif"
]

@app.route('/')
def index():
    url = random.choice(images)
    hostname = platform.node()
    return render_template('index.html', url=url, hostname=hostname)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
