import json
import os
from core import db_manager

QUESTIONS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "mote_questions.json")
FEEDBACK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "mote_feedbacks.json")

# 質問を取得する
def get_questions():
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions

# 点数に応じたフィードバックを取得する
def get_feedback(score):
    with open(FEEDBACK_PATH, 'r', encoding='utf-8') as file:
        feedbacks = json.load(file)
    for range_key, feedback in feedbacks.items():
        low, high = map(int, range_key.split('-'))
        if low <= score <= high:
            return feedback
    return "結果が見つかりませんでした。"

# 採点を行う（簡略版）
def evaluate_answers(answers):
    correct_answers = {"1": "話題を振る"}  # 模範回答を追加
    score = 0
    for q_id, answer in answers.items():
        if correct_answers.get(q_id) == answer:
            score += 10
    return score

# モテ診断実行（回答を受け取り結果を返す）
def perform_mote_check(user_id, answers):
    score = evaluate_answers(answers)
    feedback = get_feedback(score)
    db_manager.set_user_mode(user_id, 'normal')  # 診断終了で通常モードに戻す
    return f"あなたのモテ点数は {score}点！\n{feedback}"
