from app.domains.chat.schemas import MessageRead


def _message_to_read(message) -> MessageRead | None:
    if message.type == "human":
        return MessageRead(
            role="user",
            content=message.text,
        )

    if message.type == "ai" and message.text:
        return MessageRead(
            role="assistant",
            content=message.text,
        )

    return None
