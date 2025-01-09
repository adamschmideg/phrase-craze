import random
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# Sample data for quizzes and questions
quizzes = {
    1: {
        'title': 'Phrase Identification Quiz',
        'questions': {
            1: {
                'phrase': 'The quick brown fox jumps over the lazy dog.',
                'answers': [
                    'The quick brown fox jumps over the lazy dog.',
                    'A quick brown fox jumps over a lazy dog.',
                    'The quick brown fox jumped over the lazy dog.',
                    'The quick brown fox jumps over the lazy cat.'
                ]
            },
            2: {
                'phrase': 'A journey of a thousand miles begins with a single step.',
                'answers': [
                    'A journey of a thousand miles begins with a single step.',
                    'A journey of one thousand miles begins with a single step.',
                    'A journey of a thousand miles starts with one step.',
                    'A journey of many miles begins with one step.'
                ]
            }
            # Add more questions as needed
        }
    }
}

@app.route('/')
def home():
    return redirect(url_for('question', quiz_id=1, question_id=1))

@app.route('/quiz/<int:quiz_id>/question/<int:question_id>')
def question(quiz_id, question_id):
    question = quizzes[quiz_id]['questions'][question_id]
    return render_template('question.html', question=question, question_id=question_id, quiz_id=quiz_id)

@app.route('/quiz/<int:quiz_id>/question/<int:question_id>/answers/<ids>')
def answers(quiz_id, question_id, ids):
    question = quizzes[quiz_id]['questions'][question_id]
    answers = [question['answers'][int(i)] for i in ids.split(',')]
    return render_template('answers.html', question=question['phrase'], answers=answers)

@app.route('/quiz/<int:quiz_id>/question/<int:question_id>/answer/<int:answer_id>', methods=['POST'])
def submit_answer(quiz_id, question_id, answer_id):
    # Here you would handle answer submission logic (e.g., scoring)

    # Get all question IDs for the quiz
    question_ids = list(quizzes[quiz_id]['questions'].keys())

    # Remove current question ID from list to avoid repetition
    question_ids.remove(question_id)

    # Redirect to a random next question if available
    if question_ids:
        next_question_id = random.choice(question_ids)
        return redirect(url_for('question', quiz_id=quiz_id, question_id=next_question_id))

    return redirect(url_for('quiz', quiz_id=quiz_id))  # Redirect to quiz if no more questions

if __name__ == '__main__':
    app.run(debug=True)
