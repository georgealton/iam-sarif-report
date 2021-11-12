import pathlib

import click

from . import run

policy_types = (
    "IDENTITY_POLICY",
    "RESOURCE_POLICY",
    "SERVICE_CONTROL_POLICY",
)
locales = (
    "DE",
    "EN",
    "ES",
    "FR",
    "IT",
    "JA",
    "KO",
    "PT_BR",
    "ZH_CN",
    "ZH_TW",
)


@click.command()
@click.option(
    "--policy-type",
    type=click.Choice(policy_types),
    default="IDENTITY_POLICY",
    help="The type of policy to validate. Defaults to 'IDENTITY_POLICY'",
)
@click.option(
    "--locale",
    type=click.Choice(locales),
    default="EN",
    help="The locale to use for localizing the findings. Defaults to 'EN'",
)
@click.argument(
    "policy",
    type=click.Path(
        exists=True, path_type=pathlib.Path, dir_okay=False, allow_dash=True
    ),
    default="-",
)
@click.argument("result", type=click.File("w"), default="-")
def validate_as_sarif(policy, policy_type, locale, result):

    with click.open_file(policy) as data:
        policy_document = data.read()

    run.validate_as_sarif(
        policy_location=policy,
        policy_document=policy_document,
        policy_type=policy_type,
        locale=locale,
        output_location=result,
    )
    result.write("\n")
