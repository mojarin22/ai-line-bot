from . import db_manager

# 利用可能なモード一覧（必要に応じて拡張）
AVAILABLE_MODES = ['normal', 'diary', 'consult', 'mote_check', 'training']

# ユーザーのモードを設定
def set_mode(user_id, mode):
    if mode not in AVAILABLE_MODES:
        raise ValueError(f"モードは {AVAILABLE_MODES} の中から指定してください。")
    db_manager.set_user_mode(user_id, mode)
    return f"モードを「{mode}」に設定しました！👍"

# ユーザーのモードを取得
def get_mode(user_id):
    mode = db_manager.get_user_mode(user_id)
    return mode

# モード変更コマンドを処理（リッチメニューからのコマンド用）
def handle_mode_command(user_id, mode_command):
    mode_map = {
        'モテ診断スタート': 'mote_check',
        '日記を書く': 'diary',
        '相談したい': 'consult',
        '特訓モード開始': 'training',
        '通常モードに戻る': 'normal'
    }

    mode = mode_map.get(mode_command, None)
    if mode:
        message = set_mode(user_id, mode)
        return message
    else:
        return "指定されたモードが見つかりませんでした。🤔もう一度お試しください。"
