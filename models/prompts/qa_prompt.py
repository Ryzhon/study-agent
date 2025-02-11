from langchain_core.prompts import ChatPromptTemplate

def get_decision_prompt()-> ChatPromptTemplate:
     return ChatPromptTemplate.from_template(
        """
        あなたはユーザーの要望を解析するアシスタントです。

        ユーザーの入力:
        {query}

        ユーザーの意図は以下のいずれかです:
        1. 「問題を出題してほしい」
        2. 「回答を送ったので解説してほしい」

        それぞれに対応して、以下の文字列だけを1行で出力してください:
        - ユーザーが問題を求めているなら "problem"
        - ユーザーが回答の解説を求めているなら "answer"

        余計な説明は不要で、必ず "problem" または "answer" のどちらかのみ出力してください。
        """.strip()
    )


def get_answer_explanation_prompt(problem_text: str, user_answer: str) -> ChatPromptTemplate:

    safe_problem_text = problem_text.replace("{", "{{").replace("}", "}}")
    safe_user_answer = user_answer.replace("{", "{{").replace("}", "}}")

    return ChatPromptTemplate.from_template(
        f"""あなたは「解説エキスパート（大学受験）」です。

        以下の問題文とユーザーの回答に基づき、模範解答と解説を作成してください。

        問題文:
        {safe_problem_text}

        ユーザーの回答:
        {safe_user_answer}

        [出力例]
        解答:
        解説:
        """.strip()
    )

def get_explanation_quality_check_prompt(explanation_text: str) -> ChatPromptTemplate:
    safe_explanation_text = explanation_text.replace("{", "{{").replace("}", "}}")

    return ChatPromptTemplate.from_template(
        f"""あなたは「解説品質検証エキスパート（大学受験）」です。

        以下の解説をチェックし、誤りや不足があれば修正案を提示してください。
        解説:
        {safe_explanation_text}

        [指示]
        - OKの場合、"OK"とコメント
        - 修正案がある場合、「修正案:」の後に修正バージョンを提示
        - コメントも付け加えてください
        """.strip()
    )


def get_problem_maker_prompt(user_query: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(
        f"""あなたは「問題作成エキスパート（大学受験）」です。

        ユーザーの要望:
        {user_query}

        この要望に合った大学受験レベルの問題を1問作成してください。
        問題文のみ生成し、解説や解答は不要です。
        """.strip()
    )

def get_problem_quality_check_prompt(problem_text: str) -> ChatPromptTemplate:
    safe_problem_text = problem_text.replace("{", "{{").replace("}", "}}")

    return ChatPromptTemplate.from_template(
        f"""あなたは「品質検証エキスパート（大学受験）」です。

        以下の問題文をレビューし、大学受験レベルとして妥当かチェックしてください。
        問題文:
        {safe_problem_text}

        [指示]
        - OKの場合、"OK"とコメントを返す
        - 修正案がある場合は「修正案:」の後に改良した問題文を提示
        - 短いコメントも添えてください
        """.strip()
    )

