from types import MappingProxyType
from typing import Mapping
import boto3
import punq


from . import reporter, converter, validator, handlers, commands

from typing import Type
def bootstrap() -> "Mapping[Type[commands.Command], handlers.Handler]" :
    container = punq.Container()
    container.register("Reporter", reporter.CLIReporter)
    container.register("Converter", converter.SarifConverter)
    container.register("boto3.Session", boto3.Session)
    container.register("Validator", validator.AWSAccessAnalyzerValidator)

    return MappingProxyType(
        {
            Command: container.resolve(Handler)
            for Command, Handler in handlers.COMMAND_HANDLERS.items()
        }
    )
