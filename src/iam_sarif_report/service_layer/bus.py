from typing import Mapping, final

from attrs import frozen

from ..domain import commands
from . import handlers

COMMAND_HANDLERS = Mapping[type[commands.Command], handlers.Handler]


@final
@frozen(kw_only=True)
class Bus:
    command_handlers: COMMAND_HANDLERS

    def __call__(self, operation: commands.Command) -> None:
        handler = self.command_handlers[type(operation)]
        handler(operation)

    put = __call__
