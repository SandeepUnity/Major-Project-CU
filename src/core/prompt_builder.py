from __future__ import annotations

from src.core.vector_store import RetrievedChunk


DEFAULT_SYSTEM = (
    "You are a helpful educational assistant for EmpowerTech Solutions. "
    "You answer questions about courses, enrollment, technical issues, and policies. "
    "You MUST only use information provided in the knowledge base context. "
    "If you don't have relevant information, respond exactly: "
    "\"I'm sorry, I don't have that information. Would you like to speak with an advisor?\" "
    "Be concise, friendly, and accurate."
)

SMALL_TALK_SYSTEM = (
    "You are a friendly support assistant for EmpowerTech Solutions (courses, enrollment, "
    "technical help, and policies). The user sent a short greeting or casual message — no "
    "knowledge base lookup was used. Reply naturally: greet back if appropriate, briefly "
    "say you are here to help with EmpowerTech questions, and invite them to ask about "
    "courses or support. Do not invent specific policies, prices, or dates. "
    "Keep it to 2–4 short sentences."
)


class PromptBuilder:
    def build_small_talk(self, query: str, history: list[dict]) -> tuple[str, str]:
        hist_lines: list[str] = []
        for m in history:
            role = m.get("role", "")
            content = m.get("content", "")
            hist_lines.append(f"{role}: {content}")
        hist = "\n".join(hist_lines).strip()
        user = (
            f"CHAT HISTORY:\n{hist if hist else '(none)'}\n\n"
            f"USER MESSAGE:\n{query}\n"
        )
        return SMALL_TALK_SYSTEM, user

    def build(self, query: str, history: list[dict], chunks: list[RetrievedChunk]) -> tuple[str, str]:
        context_lines: list[str] = []
        for i, c in enumerate(chunks, start=1):
            src = c.metadata.get("source_id") or c.metadata.get("source") or c.metadata.get("file") or c.id
            context_lines.append(f"[{i}] (source={src}, score={c.score:.3f}) {c.text}")
        context = "\n".join(context_lines).strip()

        hist_lines: list[str] = []
        for m in history:
            role = m.get("role", "")
            content = m.get("content", "")
            hist_lines.append(f"{role}: {content}")
        hist = "\n".join(hist_lines).strip()

        user = (
            f"KNOWLEDGE BASE CONTEXT:\n{context if context else '(none)'}\n\n"
            f"CHAT HISTORY:\n{hist if hist else '(none)'}\n\n"
            f"USER QUESTION:\n{query}\n"
        )
        return DEFAULT_SYSTEM, user

