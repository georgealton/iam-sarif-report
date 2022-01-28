from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, final

from . import commands

if TYPE_CHECKING:
    from typing import Mapping, Type

    from .converter import Converter
    from .validator import Validator
    from .reporter import Reporter


class Handler:
    def __call__(self):
        ...


@final
@dataclass(frozen=True)
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


COMMAND_HANDLERS: Mapping[Type[commands.Command], Type[Handler]] = MappingProxyType(
    {commands.GenerateFindingsAndReportSarif: GenerateFindingsAndReportSarif}
)
