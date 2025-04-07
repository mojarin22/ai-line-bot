from . import db_manager

# ニックネームと敬称を設定または変更
def set_nickname(user_id, nickname, honorific='さん'):
    if honorific not in ['さん', '君', '']:
        raise ValueError("敬称は「さん」「君」「呼び捨て(空文字)」のみ有効です。")
    db_manager.upsert_user(user_id, nickname, honorific)
    return f"呼び名を「{nickname}{honorific}」に設定しました！✨"

# 現在設定されているニックネームと敬称を取得
def get_nickname(user_id):
    user = db_manager.get_user(user_id)
    if user:
        nickname, honorific = user[1], user[2]
        return f"{nickname}{honorific}"
    else:
        return "お名前未設定さん"  # 未設定時のデフォルト表示

# ユーザーの呼び名コマンドを処理（LINEメッセージと連動）
def handle_nickname_command(user_id, text):
    parts = text.strip().split()
    if len(parts) == 1:
        # 「名前教えて」コマンド
        current_name = get_nickname(user_id)
        return f"あなたの呼び名は「{current_name}」ですよ😊"
    elif len(parts) >= 2:
        # 「〇〇って呼んで [さん|君|呼び捨て]」コマンド
        nickname = parts[0]
        honorific = parts[1] if len(parts) > 2 else 'さん'
        if honorific == '呼び捨て':
            honorific = ''
        try:
            message = set_nickname(user_id, nickname, honorific)
            return message
        except ValueError as e:
            return str(e)
    else:
        return "使い方： 「〇〇って呼んで さん|君|呼び捨て」で教えてください😉"
