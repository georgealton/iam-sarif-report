from typing import Mapping, final

from attrs import define

from ..domain import commands
from . import handlers


@final
@define(frozen=True, kw_only=True)
class Bus:
    command_handlers: Mapping[type[commands.Command], handlers.Handler]

    def __call__(self, operation: commands.Command):
        handler = self.command_handlers[type(operation)]
        handler(operation)

    handle = __call__
