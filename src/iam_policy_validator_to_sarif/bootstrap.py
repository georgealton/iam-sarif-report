def bootstrap():
    reporter = reporter.CLIReporter(result)
    converter = converter.SarifConverter()
    validator = validator.AWSAccessAnalyzerValidator(boto3.session.Session())

    Handler = handlers.COMMAND_HANDLERS[type(command)]
    return Handler
