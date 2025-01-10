import random
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# Sample data for quizzes and questions
quizzes = {
    0: {
        'title': 'Phrase Identification Quiz',
        'questions': {
            0: {
                'question_id': 0,
                'text': 'The quick brown fox jumps over the lazy dog.',
                'answers': [
                    {'answer_id': 0, 'text': 'jumps over the lazy dog.', 'correct': True},
                    {'answer_id': 1, 'text': 'jumps over the dog!', 'correct': False},
                    {'answer_id': 2, 'text': 'jumps over a lazy dog.', 'correct': False},
                    {'answer_id': 3, 'text': 'jumps over the lazy cat.', 'correct': False}
                ]
            },
            1: {
                'question_id': 2,
                'text': 'A stitch in time saves nine.',
                'answers': [
                    {'answer_id': 0, 'text': 'saves nine.', 'correct': True},
                    {'answer_id': 1, 'text': 'saves time.', 'correct': False},
                    {'answer_id': 2, 'text': 'saves a stitch.', 'correct': False},
                    {'answer_id': 3, 'text': 'saves a stitch in time.', 'correct': False}
                ]
            },
        }
    }
}

def convert_nested_dict_to_object(d):
    class ObjectView(object):
        def __init__(self, d):
            self.__dict__ = d
    return ObjectView(d)

@app.route('/')
def home():
    return redirect(url_for('show_question', quiz_id=0, question_id=0))

@app.route('/quiz/<int:quiz_id>/question/<int:question_id>')
def show_question(quiz_id, question_id):
    question = quizzes[quiz_id]['questions'][question_id]
    answer_ids = ','.join(str(answer['answer_id']) for answer in question['answers'])
    answers_url = url_for('show_answers', quiz_id=quiz_id, question_id=question_id, answer_ids=answer_ids)
    return render_template('question.html', question=question, answers_url=answers_url)

@app.route('/quiz/<int:quiz_id>/question/<int:question_id>/answers/<answer_ids>')
def show_answers(quiz_id, question_id, answer_ids):
    question = quizzes[quiz_id]['questions'][question_id]
    answers = [question['answers'][int(i)] for i in answer_ids.split(',')]
    return render_template('answers.html', question=question, answers=answers)

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
