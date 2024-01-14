from flask import Flask, render_template, request, jsonify
import french
import difflib

app = Flask(__name__)

@app.route('/check_pronunciation', methods=['POST'])
def check_pronunciation():
    data = request.get_json()
    spoken_text = data.get('spokenText', '')
    
    # Call a modified version of prompt_and_repeat or its logic here
    feedback = french.process_spoken_text(spoken_text)  # Example function

    return jsonify({'feedback': feedback})
# # Determine the feedback message based on the similarity score
# def determine_feedback(similarity):
#     if similarity > 0.95:
#         print("Great Job! Next Question")
#     elif similarity > 0.8:
#         print("You're Getting There! Keep Practicing.")
#     else:
#         print("Don't Lose Hope. You'll Get There!")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-learn')
def start_learn():
    return render_template('startlearn.html')


@app.route('/french')
def french():
    return render_template('french.html')

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
