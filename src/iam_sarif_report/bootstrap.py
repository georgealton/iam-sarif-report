from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

import punq

from . import converter
from .adapters import checks, reader, reporter, validator
from .domain import commands
from .service_layer import handlers


def bootstrap() -> Mapping[type[commands.Command], handlers.Handler]:
    container = punq.Container()

    container.register("Reader", reader.CLIReader)
    container.register("ChecksRepository", checks.ChecksPackageDataRepository)
    container.register("Reporter", reporter.CLIReporter)
    container.register("Converter", converter.SarifConverter)
    container.register("Validator", validator.AWSAccessAnalyzerValidator)

    return MappingProxyType(
        {
            Command: container.instantiate(Handler)
            for Command, Handler in handlers.COMMAND_HANDLERS.items()
        }
    )
