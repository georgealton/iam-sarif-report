from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, Type

import punq

from . import checks, commands, converter, handlers, reader, reporter, validator


def bootstrap() -> Mapping[Type[commands.Command], handlers.Handler]:
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
