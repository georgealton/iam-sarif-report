from __future__ import annotations

import pathlib

import click

from .. import bootstrap, commands, definitions


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
    "policy_path",
    type=click.Path(
        exists=True, path_type=pathlib.Path, dir_okay=False, allow_dash=True
    ),
    default="-",
)
@click.argument("result", type=click.File("w"), default="-")
def generate_findings_and_report_sarif(
    policy_path, policy_type, locale, resource_type, result
):

    command = commands.GenerateFindingsAndReportSarif(
        policy_path=policy_path,
        policy_type=policy_type,
        locale=locale,
        resource_type=resource_type,
        report=result,
    )

    handlers = bootstrap.bootstrap()
    handler = handlers[type(command)]
    handler(command)