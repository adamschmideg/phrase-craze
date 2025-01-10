import random
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Sample data for quizzes and questions
quizzes = {
    0: {
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
    return render_template('answers.html', quiz_id=quiz_id, question_id=question_id, answers=answers)

@app.route('/quiz/<int:quiz_id>/question/<int:question_id>/answer/<int:answer_id>', methods=['POST'])
def submit_answer(quiz_id, question_id, answer_id):
    question = quizzes[quiz_id]['questions'][question_id]
    answer = question['answers'][answer_id]
    if answer['correct']:
        # TODO: Score
        pass

    question_ids = quizzes[quiz_id]['questions'].keys()
    next_question_id = random.randint(0, len(question_ids) - 1)
    return redirect(url_for('show_question', quiz_id=quiz_id, question_id=next_question_id))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
