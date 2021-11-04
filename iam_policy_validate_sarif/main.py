# import boto3
from . import converter


def main(findings):
    converter = converter.SarifConverter('')
    log = converter.convert()
    with open('output.sarif', 'w') as sarif_file:
        sarif_file.write(log)

if __name__ == '__main__':
    main('f')
