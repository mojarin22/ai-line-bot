from core import db_manager, error_handler

# 日記を記録する
@error_handler.handle_errors
def log_diary(user_id, diary_text):
    db_manager.save_diary(user_id, diary_text)
    return "日記を保存しました！いつもありがとう😊"
