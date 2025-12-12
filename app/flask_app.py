from flask import Flask, jsonify, request
import app.core as core
import app.data as data

app = Flask(__name__)

@app.route('/')
def home():
    return """Welcome to the Dice API!<br>
                Use the endpoint <code>/random</code> to get a random number between 1 and 100.<br>
                Try <code>/roll/d6?n=3</code> to roll three 6-sided dice.<br>
                To get some interesting facts about dice, visit <code>/facts</code>."""

@app.route('/random')
def random_number():
    return jsonify({ "random_number" : core.rand100() })

@app.route('/roll/d<int:num_faces>')
def roll_dice(num_faces):
    num_dice = request.args.get('n', default=1, type=int)
    if num_faces < 1 or num_dice < 1:
        return jsonify({'error': 'Number of faces and number of dice must be positive integers.'}), 400

    result = core.roll_dice(num_faces, num_dice)

    data.save_roll_history(result, source='flask_app')

    return jsonify(result)

@app.route('/facts')
def dice_facts():
    facts = [
        "Dice have been used since ancient times for gaming and divination.",
        "The oldest known dice were excavated from a site in Mesopotamia and date back to 3000 BC.",
        "A standard die has six faces, numbered from 1 to 6.",
        "The probability of rolling any specific number on a fair six-sided die is 1/6.",
        "Dice are commonly used in board games, role-playing games, and gambling."
    ]
    return jsonify({ "facts": facts })
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)