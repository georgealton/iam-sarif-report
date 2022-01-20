import pathlib
import boto3
import click

from . import bootstrap, converter, handlers, validator, commands


@click.command()
@click.option(
    "--policy-type",
    type=click.Choice(POLICY_TYPES),
    default="IDENTITY_POLICY",
    help="The type of policy to validate. Defaults to 'IDENTITY_POLICY'",
)
@click.option(
    "--locale",
    type=click.Choice(LOCALES),
    default="EN",
    help="The locale to use for localizing the findings. Defaults to 'EN'",
)
@click.option(
    "--resource-type",
    type=click.Choice(RESOURCE_TYPES),
    default=None,
    help="Specify a value for the policy validation resource type only if the policy type is RESOURCE_POLICY",
)
@click.argument(
    "policy",
    type=click.Path(
        exists=True, path_type=pathlib.Path, dir_okay=False, allow_dash=True
    ),
    default="-",
)
@click.argument("result", type=click.File("w"), default="-")
def validate_as_sarif(policy, policy_type, locale, resource_type, result):

    with click.open_file(policy) as data:
        policy_document = data.read()

    command = commands.GenerateFindingsAndReportSarif(
        policy_path=policy,
        policy_document=policy_document,
        policy_type=policy_type,
        locale=locale,
        resource_type=resource_type,
    )
    
    reporter = reporter.CLIReporter(result)
    converter = converter.SarifConverter()
    validator = validator.AWSAccessAnalyzerValidator(boto3.session.Session())
    Handler = handlers.COMMAND_HANDLERS[type(command)]
    handler = Handler(validator=validator, converter=converter, reporter=reporter)

    handler(command)
