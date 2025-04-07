from .system_prompt import AI_CHARACTER_PROMPT

# プロンプトを生成する関数
def build_prompt(user_message, conversation_history=None):
    messages = [{"role": "system", "content": AI_CHARACTER_PROMPT}]
    
    # 過去の会話履歴を追加
    if conversation_history:
        messages.extend(conversation_history)
    
    # 今回のユーザー発言を追加
    messages.append({"role": "user", "content": user_message})
    
    return messages
