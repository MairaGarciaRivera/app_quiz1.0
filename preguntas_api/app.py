from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import psycopg2

app = Flask(__name__)
CORS(app)

def load_questions():
    questions = []
    categories = {
        1: "matematicas.json",
        2: "acertijos_logicos.json",
        3: "historia.json",
        4: "cultura_general.json"
    }
    
    for category_id, filename in categories.items():
        filepath = os.path.join('data', filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                category_questions = json.load(f)
                for question in category_questions:
                    question['category_id'] = category_id
                questions.extend(category_questions)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
    
    return questions

all_questions = load_questions()

@app.route('/api/preguntas', methods=['GET'])
def get_questions():
    category_id = request.args.get('category_id', type=int)
    difficulty = request.args.get('difficulty', type=str)
    
    filtered_questions = all_questions
    
    if category_id:
        filtered_questions = [q for q in filtered_questions if q['category_id'] == category_id]
    
    if difficulty:
        difficulty_lower = difficulty.lower()
        difficulty_mappings = {
            'facil': ['fácil', 'facil'],
            'medio': ['medio'],
            'dificil': ['difícil', 'dificil']
        }
        
        matched_difficulties = []
        for key, variants in difficulty_mappings.items():
            if difficulty_lower in variants:
                matched_difficulties.append(key)
                break
        
        if matched_difficulties:
            filtered_questions = [
                q for q in filtered_questions 
                if q['difficulty'].lower() in matched_difficulties
                or q['difficulty'].lower() in difficulty_mappings.get(matched_difficulties[0], [])
            ]
    
    return jsonify(filtered_questions)

if __name__ == '__main__':
    app.run(debug=True)
