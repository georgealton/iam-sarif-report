from __future__ import annotations

import pathlib
from typing import Literal

import click

from .. import bootstrap
from ..domain import commands, definitions


@click.command()
@click.option(
    "--policy-type",
    type=click.Choice(list(definitions.POLICY_TYPES)),
    default="IDENTITY_POLICY",
    help="The type of policy to validate. Defaults to 'IDENTITY_POLICY'",
)
@click.option(
    "--locale",
    type=click.Choice(list(definitions.LOCALES)),
    default="EN",
    help="The locale to use for localizing the findings. Defaults to 'EN'",
)
@click.option(
    "--resource-type",
    type=click.Choice(list(definitions.RESOURCE_TYPES)),
    default=None,
    help="Specify a value for the policy validation resource type only if the policy type is RESOURCE_POLICY",
)
@click.argument("policies", nargs=-1)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(
        exists=False,
        path_type=pathlib.Path,
        dir_okay=False,
        allow_dash=True,
    ),
    default="-",
)
def generate_findings_and_report_sarif(
    policies: list[str] | Literal["-"],
    policy_type: str,
    locale: str,
    resource_type: str | None,
    output_file: pathlib.Path | Literal["-"],
) -> None:
    policy_locations: str | list[str]
    policy_locations = policies

    if resource_type is not None:
        resource_type = definitions.RESOURCE_TYPES(resource_type)

    command = commands.GenerateFindingsAndReportSarif(
        policy_locations=policy_locations,
        policy_type=definitions.POLICY_TYPES(policy_type),
        locale=definitions.LOCALES(locale),
        resource_type=resource_type,
        report=output_file,
    )

    bus = bootstrap.bootstrap()
    bus.put(command)
