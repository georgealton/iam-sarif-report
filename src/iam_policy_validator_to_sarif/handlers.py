from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from attr import define

try:
    from typing import final
except ImportError:
    from typing_extensions import final

from . import commands

if TYPE_CHECKING:
    from typing import Mapping, Type

    from .converter import Converter
    from .reporter import Reporter
    from .validator import Validator


class Handler:
    ...


@final
@define(frozen=True)
class GenerateFindingsAndReportSarif(Handler):
    validator: Validator
    converter: Converter
    reporter: Reporter

    def __call__(self, command: commands.GenerateFindingsAndReportSarif) -> None:
        findings = self.validator(
            locale=command.locale,
            policy_type=command.policy_type,
            policy=command.policy_document,
            resource_type=command.resource_type,
        )
        results = self.converter(command.policy_path, findings)
        self.reporter(command.report, results)

CommandToHandlerMap = Mapping[Type[commands.Command], Type[Handler]]

COMMAND_HANDLERS: CommandToHandlerMap = MappingProxyType(
    {commands.GenerateFindingsAndReportSarif: GenerateFindingsAndReportSarif}
)
