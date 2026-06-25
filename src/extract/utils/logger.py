import logging
import os
import sys
from typing import Any

import structlog
from structlog.processors import CallsiteParameter

from src.extract.utils.constants import Constants


def _rename_callsite_fields(
    _logger: Any,
    _method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    func_name = event_dict.pop("func_name", None)
    if func_name is not None:
        event_dict["function"] = func_name

    return event_dict


class Logger:
    """Custom structlog wrapper for extraction jobs."""

    def __init__(
        self,
        name: str = Constants.LOGGER_DEFAULT_NAME,
        level: str | int | None = None,
        json_logs: bool | None = None,
        **default_context: Any,
    ) -> None:
        self.name = name
        self.level = self._resolve_level(level)
        self.json_logs = self._resolve_json_logs(json_logs)
        self._configure_structlog()
        self._logger = structlog.get_logger(name).bind(**default_context)

    @property
    def raw_logger(self) -> structlog.BoundLogger:
        """Expose the underlying structlog logger for advanced use cases."""

        return self._logger

    def bind(self, **context: Any) -> "Logger":
        self._logger = self._logger.bind(**context)
        return self

    def debug(self, message: str, **context: Any) -> None:
        self._logger.debug(message, **context)

    def info(self, message: str, **context: Any) -> None:
        self._logger.info(message, **context)

    def warning(self, message: str, **context: Any) -> None:
        self._logger.warning(message, **context)

    def error(self, message: str, **context: Any) -> None:
        self._logger.error(message, **context)

    def exception(self, message: str, **context: Any) -> None:
        self._logger.exception(message, **context)

    def _configure_structlog(self) -> None:
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.CallsiteParameterAdder(
                {
                    CallsiteParameter.FUNC_NAME,
                    CallsiteParameter.MODULE,
                    CallsiteParameter.LINENO,
                },
                additional_ignores=[__name__],
            ),
            _rename_callsite_fields,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
        ]

        renderer: structlog.types.Processor
        if self.json_logs:
            renderer = structlog.processors.JSONRenderer()
        else:
            renderer = structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty())

        structlog.configure(
            processors=[*processors, renderer],
            wrapper_class=structlog.make_filtering_bound_logger(self.level),
            logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
            cache_logger_on_first_use=True,
        )

    @staticmethod
    def _resolve_level(level: str | int | None) -> int:
        configured_level = level or os.getenv("LOG_LEVEL", "INFO")

        if isinstance(configured_level, int):
            return configured_level

        resolved_level = logging.getLevelNamesMapping().get(configured_level.upper())
        if resolved_level is not None:
            return resolved_level

        raise ValueError(f"Unsupported log level: {configured_level}")

    @staticmethod
    def _resolve_json_logs(json_logs: bool | None) -> bool:
        if json_logs is not None:
            return json_logs

        return os.getenv("LOG_FORMAT", "text").lower() == "json"


def get_logger(
    name: str = Constants.LOGGER_DEFAULT_NAME,
    level: str | int | None = None,
    json_logs: bool | None = None,
    **default_context: Any,
) -> Logger:
    return Logger(
        name=name,
        level=level,
        json_logs=json_logs,
        **default_context,
    )
