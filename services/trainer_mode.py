from core import db_manager, error_handler

@error_handler.handle_errors
def start_training(user_id):
    db_manager.set_user_mode(user_id, "training")
    return "特訓モードを開始しました！💪準備はいいですか？"

@error_handler.handle_errors
def complete_training(user_id, points):
    db_manager.set_user_mode(user_id, "normal")
    rank = get_rank(points)
    return f"特訓終了！あなたの今回のスコアは {points} 点で、ランクは「{rank}」です！🏅"

def get_rank(points):
    if points >= 90:
        return "モテマスター✨"
    elif points >= 70:
        return "あと一歩のモテ男子👍"
    elif points >= 50:
        return "成長中の男子😊"
    else:
        return "努力が必要です😅"
