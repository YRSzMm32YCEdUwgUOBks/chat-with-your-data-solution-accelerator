class QuestionAnswerTool:
    @staticmethod
    async def handle_message(session_id: str, user_message: str):
        # existing shared orchestration:
        # - load history
        # - embed + pgvector search
        # - call Azure OpenAI chat
        # - append to chat_history
        # - return { choices, citations }
        ...
