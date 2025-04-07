from datetime import datetime
from core import db_manager, error_handler

# 新しいリマインダーを設定
@error_handler.handle_errors
def set_reminder(user_id, reminder_text, remind_at_str):
    remind_at = datetime.strptime(remind_at_str, "%Y-%m-%d %H:%M")
    db_manager.add_reminder(user_id, reminder_text, remind_at)
    return f"{remind_at.strftime('%Y年%m月%d日 %H:%M')} に通知を設定しました！🔔"

# 未送信のリマインダーを送信
def send_pending_reminders(line_bot_api, TextSendMessage):
    reminders = db_manager.get_pending_reminders()
    for reminder_id, user_id, reminder_text, remind_at in reminders:
        message = f"🔔リマインダーです！\n「{reminder_text}」の時間になりました！"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        db_manager.mark_reminder_sent(reminder_id)
