from __future__ import annotations

import sys
from typing import TYPE_CHECKING, get_type_hints

from attr import define

if sys.version_info >= (3, 8):
    from typing import final
else:
    from typing_extensions import final

from ..domain import commands

if TYPE_CHECKING:
    from ..adapters.reader import Reader
    from ..adapters.reporter import Reporter
    from ..adapters.validator import Validator
    from ..converter import Converter


class Handler:
    registry: dict[type[commands.Command], type[Handler]] = {}

    def __init_subclass__(cls) -> None:
        command_type: type[commands.Command] = get_type_hints(cls.__call__)["command"]
        Handler.registry[command_type] = cls

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
