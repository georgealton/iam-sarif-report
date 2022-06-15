from __future__ import annotations

import pathlib

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
@click.argument(
    "policies",
    type=click.Path(
        exists=True,
        path_type=pathlib.Path,
        dir_okay=False,
    ),
    nargs=-1,
)
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
    policies, policy_type, locale, resource_type, output_file
):

    command = commands.GenerateFindingsAndReportSarif(
        policy_locations=policies,
        policy_type=policy_type,
        locale=locale,
        resource_type=resource_type,
        report=output_file,
    )

    bus = bootstrap.bootstrap()
    bus.handle(command)
