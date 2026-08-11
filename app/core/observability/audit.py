from typing import Any

import structlog

logger = structlog.get_logger("audit")


class AuditService:
    """
    Records business audit events.
    """

    def record(
        self,
        event: str,
        **attributes: Any,
    ) -> None:
        logger.info(
            event,
            **attributes,
        )


audit = AuditService()
