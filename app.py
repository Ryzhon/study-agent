from flask import Flask
from views import views_blueprint
import openai
import os
from dotenv import load_dotenv



load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.register_blueprint(views_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
