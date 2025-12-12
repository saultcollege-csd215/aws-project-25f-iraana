import json
import app.core as core
import app.data as data

def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }

def main(event, context):
    path = event.get('rawPath', event.get('path', ''))
    query = event.get('queryStringParameters', {}) or {}
    
    if path == '/hello':
        return response(200, {"message": "Hello, World!"})
    
    if path == '/facts':
        facts = [
            "Dice have been used since ancient times for gaming and divination.",
            "The oldest known dice were excavated from a site in Mesopotamia and date back to 3000 BC.",
            "A standard die has six faces, numbered from 1 to 6.",
            "The probability of rolling any specific number on a fair six-sided die is 1/6.",
            "Dice are commonly used in board games, role-playing games, and gambling."
        ]
        return response(200, {"facts": facts})

    if path == '/random':
        return response(200, {"random_number": core.rand100()})
    
    if path.startswith('/roll/d'):
        try:
            num_faces = int(path.split('/roll/d')[-1])
        except ValueError:
            return response(400, {'error': 'Invalid number of faces.'})

        num_dice = int(query.get('n', 1))
        if num_faces < 1 or num_dice < 1:
            return response(400, {'error': 'Number of faces and dice must be positive integers.'})

        result = core.roll_dice(num_faces, num_dice)

        data.save_roll_history(result, 'lambda_app')

        return response(200, result)
    
    return response(404, {'error': 'Not found'})
