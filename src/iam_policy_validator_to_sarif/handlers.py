from __future__ import annotations

import sys
from types import MappingProxyType
from typing import TYPE_CHECKING, Mapping, Type

from attr import define

if sys.version_info >= (3, 8):
    from typing import final
else:
    from typing_extensions import final

from . import commands

if TYPE_CHECKING:
    from .converter import Converter
    from .reader import Reader
    from .reporter import Reporter
    from .validator import Validator


class Handler:
    def __call__(self, command):
        ...


@final
@define(frozen=True)
class GenerateFindingsAndReportSarif(Handler):
    reader: Reader
    validator: Validator
    converter: Converter
    reporter: Reporter

    def __call__(self, command: commands.GenerateFindingsAndReportSarif) -> None:
        policy = self.reader(command.policy_path)
        findings = self.validator(
            locale=command.locale,
            policy_type=command.policy_type,
            policy=policy,
            resource_type=command.resource_type,
        )
        results = self.converter(command.policy_path, findings)
        self.reporter(command.report, results)


CommandToHandlerMap = Mapping[Type[commands.Command], Type[Handler]]

COMMAND_HANDLERS: CommandToHandlerMap = MappingProxyType(
    {commands.GenerateFindingsAndReportSarif: GenerateFindingsAndReportSarif}
)
