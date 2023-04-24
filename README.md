# pulumi-python-s3state

Python Pulumi program that defines S3 state bucket and KMS key

## Initial configuration

1. Create new project directory and go to it

1. Execute `pulumi new https://github.com/peterkowalski/pulumi-template-aws-python`

1. Open workspace in Visual Studio Code using Dev Container

1. Configure [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

1. Remove `venv` directory

1. Remove virtual environment configuration from `Pulumi.yaml`

    BEFORE:

    ```yaml
    name: pulumi-python-s3state
    runtime:
    name: python
    options:
        virtualenv: venv
    main: src/
    description: Python Pulumi program that defines S3 state bucket and KMS key
    ```

    AFTER:

    ```yaml
    name: pulumi-python-s3state
    runtime:
      name: python
    main: src/
    description: Python Pulumi program that defines S3 state bucket and KMS key
    ```

1. Install Python packages: `poetry install`

1. Initialize git repository: `git init`

1. Execute `fix_template.py`

1. Install `pre-commit` hooks: `pre-commit install`

1. Make an initial commit

## Roadmap

* Automatically remove initially created `venv` directory with `fix_template.py`
* Automatically remove virtual environment configuration from
  `Pulumi.yaml` with `fix_template.py`
