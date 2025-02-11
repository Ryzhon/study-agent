from pydantic import BaseModel, Field

class QAState(BaseModel):
    query: str = Field(..., description="ユーザーの入力（質問 or 回答）")
    current_flow: str = Field(default="", description="現在のフロー (problem or answer)")
    problem_text: str = Field(default="", description="最終採用された問題文")
    explanation_text: str = Field(default="", description="最終採用された解説文")
    user_answer: str = Field(default="", description="ユーザーが入力した回答")
    final_message: str = Field(default="", description="フローが作った最終的な出力")
