import os
from backend import Translator
from flask import Flask, flash, request, render_template, redirect, url_for

app = Flask(__name__, template_folder="templates")

openai_key = os.getenv('OPENAI_API_KEY')
slangmachine = Translator(api_key=openai_key)

@app.route('/', methods=["GET", "POST"])
def main_page():
    with open('langs.txt') as langs_in:
        languages = langs_in.read().splitlines()
        
    if request.method == "POST":
        if not request.form.get("user-input"):
            flash("you did not enter anything into the input field")
            return render_template("index.html", available_languages=languages)
        
        if not request.form.get("original-languages"):
            flash("you did not enter anything into the input field")
            return render_template("index.html", available_languages=languages)
            
        user_input = request.form.get("user-input")
        user_lang = request.form.get("original-languages")
        desired_lang = request.form.get("translated-languages")
        
        if "slang" in user_lang:
            # translate slang to language
            translated_output = slangmachine.translate_to_language(user_input, user_lang, desired_lang)
            
        else:
            # translate language to language
            translated_output = slangmachine.translate_language_to_language(user_input, user_lang, desired_lang)

        return render_template("index.html", translated=translated_output, available_languages=languages)
    
    return render_template("index.html", available_languages=languages)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = "8080"
    app.secret_key = "the secret"
    app.debug = True
    
    app.run(host=host, port=port)