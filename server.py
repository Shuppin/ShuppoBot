from flask import Flask
from threading import Thread
from waitress import serve

app = Flask('')

@app.route('/')
def home():
  return "wagwan my g, i am alive"

def run():
  serve(app, host="0.0.0.0", port=8081)

def keep_alive():
  t = Thread(target=run)
  t.start()

if __name__ == "__main__":
    keep_alive()