from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
from utils.preprocessing import clean_message
import os

app = Flask(__name__)

# Load model and vectorizer
with open('model/spam_classifier.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)


# Helper function to read recent deleted messages
def get_recent_messages():
    if os.path.exists('deleted_messages.txt'):
        with open('deleted_messages.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-10:]]  # Last 10 messages
    else:
        return []



# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    message = ""
    deleted = False

    if request.method == 'POST':
        message = request.form['message']
        cleaned = clean_message(message)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        result = "Spam" if prediction == 1 else "Ham"

        # Save the message into deleted_messages.txt for recent list
        with open('deleted_messages.txt', 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    recent_messages = get_recent_messages()

    return render_template(
        'index.html',
        result=result,
        message=message,
        deleted=deleted,
        recent_messages=recent_messages
    )


# Route for deletion
@app.route('/delete', methods=['POST'])
def delete_message():
    message = request.form['message']

    # Save deleted messages to file
    with open('deleted_messages.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n')

    recent_messages = get_recent_messages()

    return render_template(
        'index.html',
        result=None,
        message="",
        deleted=True,
        recent_messages=recent_messages
    )



@app.route('/api/message', methods=['POST'])
def api_message():
    data = request.get_json()

    user_msg = data.get('text', '')

    cleaned = clean_message(user_msg)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    result = "Spam" if prediction == 1 else "Ham"

    return jsonify({
        "message": user_msg,
        "result": result
    })


@app.route('/api/delete', methods=['POST'])
def api_delete():
    data = request.get_json()
    msg_to_delete = data.get('text', '')

    with open('deleted_messages.txt', 'a', encoding='utf-8') as f:
        f.write(msg_to_delete + '\n')

    return jsonify({
        "message": msg_to_delete,
        "status": "Deleted"
    })


if __name__ == '__main__':
    app.run(debug=True)
