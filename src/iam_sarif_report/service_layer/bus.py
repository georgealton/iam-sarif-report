from typing import Mapping, final

from attrs import define

from ..domain import commands
from . import handlers

COMMAND_HANDLERS = Mapping[type[commands.Command], handlers.Handler]


@final
@define(frozen=True, kw_only=True)
class Bus:
    command_handlers: COMMAND_HANDLERS

    def __call__(self, operation: commands.Command):
        handler = self.command_handlers[type(operation)]
        handler(operation)

    put = __call__
