from __future__ import annotations

from types import MappingProxyType
from typing import final, get_type_hints

from attrs import frozen

from ..adapters.reader import Reader
from ..adapters.reporter import Reporter
from ..adapters.validator import Validator
from ..domain import commands
from ..domain.converter import Converter


class Handler:
    __registry: dict[type[commands.Command], type[Handler]] = {}
    registry = MappingProxyType(__registry)

    def __init_subclass__(cls) -> None:
        command_type: type[commands.Command] = get_type_hints(cls.__call__)["command"]
        Handler.__registry[command_type] = cls

    def __call__(self, command: commands.Command) -> None:
        ...


@final
@frozen
class GenerateFindingsAndReportSarif(Handler):
    reader: Reader
    validator: Validator
    converter: Converter
    reporter: Reporter

    # type: ignore[override]
    def __call__(self, command: commands.GenerateFindingsAndReportSarif) -> None:
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
