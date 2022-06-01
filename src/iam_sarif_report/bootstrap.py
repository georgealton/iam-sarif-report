from __future__ import annotations

import punq

from .adapters import checks, reader, reporter, validator
from .domain import converter
from .service_layer import bus, handlers


def bootstrap() -> bus.Bus:
    container = punq.Container()

    container.register("Reader", reader.LocalFileReader)
    container.register("ChecksRepository", checks.ChecksPackageDataRepository)
    container.register("Reporter", reporter.CLIReporter)
    container.register("Converter", converter.SarifConverter)
    container.register("Validator", validator.AWSAccessAnalyzerValidator)

    return bus.Bus(
        command_handlers={
            Command: container.instantiate(Handler)
            for Command, Handler in handlers.Handler.registry.items()
        }
    )
