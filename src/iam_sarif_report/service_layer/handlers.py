from __future__ import annotations

import sys
from types import MappingProxyType
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
    from ..domain.converter import Converter


class Handler:
    __registry: dict[type[commands.Command], type[Handler]] = {}
    registry = MappingProxyType(__registry)

    def __init_subclass__(cls) -> None:
        command_type: type[commands.Command] = get_type_hints(cls.__call__)["command"]
        Handler.__registry[command_type] = cls

    def __call__(self, command: commands.Command):
        ...


@final
@define(frozen=True)
class GenerateFindingsAndReportSarif(Handler):
    reader: Reader
    validator: Validator
    converter: Converter
    reporter: Reporter

    def __call__(self, command: commands.GenerateFindingsAndReportSarif) -> None:  # type: ignore[override]
        policy_findings = (
            (
                location,
                self.validator(
                    locale=command.locale.value,
                    policy_type=command.policy_type.value,
                    policy=self.reader(location),
                    resource_type=getattr(command.resource_type, "value", None),
                ),
            )
            for location in command.policy_locations
        )
        results = self.converter(policy_findings)
        self.reporter(command.report, results)
