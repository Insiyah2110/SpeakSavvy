from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import french
import difflib
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-learn')
def start_learn():
    return render_template('startlearn.html')


@app.route('/french-practice')
def french_practice():
    sentence = french.get_random_sentence()
    return render_template('french.html', sentence=sentence)

@app.route('/assess-speech', methods=['POST'])
def assess_speech():
    app.logger.info("Assessing speech...")
    try:
        audio_file = request.files['audio_data']
        sentence = request.form['sentence']
        
        # Use tempfile to handle the audio file securely
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            score, feedback = french.assess_speech(sentence, tmp_file.name)

        return jsonify({'score': score, 'feedback': feedback})
    except Exception as e:
        app.logger.error(f"Error in assess_speech: {e}")
        # Log the exception for debugging
        print(f"Error in assess_speech: {e}")
        # Return a generic error message to the user
        return jsonify({'score': 0, 'feedback': 'Error processing your speech. Please try again.'}), 500


@app.route('/spanish')
def spanish():
    return render_template('spanish.html')

@app.route('/russian')
def russian():
    return render_template('russian.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
