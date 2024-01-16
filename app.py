from flask import Flask, render_template, request, jsonify
from french import get_random_sentence_fr
from russian import get_random_sentence_ru
from spanish import get_random_sentence_es

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-learn')
def start_learn():
    return render_template('startlearn.html')


@app.route('/french-practice')
def french_practice():
    sentence_dict = get_random_sentence_fr()
    return render_template('french.html', sentence=sentence_dict)

@app.route('/fr/next-question', methods=['GET'])
def fr_next_question():
    sentence_dict = get_random_sentence_fr()  # This should return a dict with 'original' and 'translation'
    return jsonify(sentence_dict)

@app.route('/spanish-practice')
def spanish_practice():
    sentence_dict = get_random_sentence_es()
    return render_template('spanish.html', sentence=sentence_dict)

@app.route('/es/next-question', methods=['GET'])
def es_next_question():
    sentence_dict = get_random_sentence_es()  # This should return a dict with 'original' and 'translation'
    return jsonify(sentence_dict)

@app.route('/russian-practice')
def russian_practice():
    sentence_dict = get_random_sentence_ru()
    return render_template('russian.html', sentence=sentence_dict)

@app.route('/ru/next-question', methods=['GET'])
def ru_next_question():
    sentence_dict = get_random_sentence_ru()  # This should return a dict with 'original' and 'translation'
    return jsonify(sentence_dict)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
