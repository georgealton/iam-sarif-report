from __future__ import annotations

from types import MappingProxyType
from typing import Mapping
import punq


from . import reporter, converter, validator, handlers, commands, checks

from typing import Type


def bootstrap() -> Mapping[Type[commands.Command], handlers.Handler]:
    container = punq.Container()
    container.register("Reporter", reporter.CLIReporter)
    container.register("Converter", converter.SarifConverter)
    container.register("Validator", validator.AWSAccessAnalyzerValidator)
    container.register("ChecksRepository", checks.ChecksPackageDataRepository)
    return MappingProxyType(
        {
            Command: container.instantiate(Handler)
            for Command, Handler in handlers.COMMAND_HANDLERS.items()
        }
    )
