"""An AWS Python Pulumi program."""

import json

import pulumi_aws as aws
from pulumi import export
from pulumi.resource import ResourceOptions

import configuration
from common import register_auto_tags

config = configuration.load()
register_auto_tags({
    "Project": config["metadata"]["project"],
    "Stack": config["metadata"]["stack"],
    "Owner": config["tagging"]["owner"],
    "Environment": str(config["tagging"]["environment"]),
})

resource_name_prefix = f'{config["metadata"]["project"]}-{config["metadata"]["stack"]}'

account_public_access_block_resource = aws.s3.AccountPublicAccessBlock(
    resource_name=f"{resource_name_prefix}-account-public-access-block",
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True,
)

remote_state_bucket_name = f"{resource_name_prefix}-remote-state"
remote_state_bucket = aws.s3.Bucket(
    resource_name=remote_state_bucket_name,
    force_destroy=True,
    server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
        rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=aws.s3.
            BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(sse_algorithm="AES256"))),
    acl="private",
    versioning=aws.s3.BucketVersioningArgs(enabled=True),
    tags={
        "Name": remote_state_bucket_name,
    },
    opts=ResourceOptions(delete_before_replace=True,),
)

remote_state_bucket_policy = aws.s3.BucketPolicy(resource_name=f"{remote_state_bucket_name}-bucket-policy",
                                                 bucket=remote_state_bucket.id,
                                                 policy=remote_state_bucket.arn.apply(lambda bucket_arn: json.dumps({
                                                     "Version":
                                                         "2012-10-17",
                                                     "Statement": [{
                                                         "Sid": "EnforceHttps",
                                                         "Effect": "Deny",
                                                         "Principal": "*",
                                                         "Action": "s3:*",
                                                         "Resource": [f"{bucket_arn}", f"{bucket_arn}/*"],
                                                         "Condition": {
                                                             "Bool": {
                                                                 "aws:SecureTransport": "false"
                                                             },
                                                         },
                                                     }],
                                                 })),
                                                 opts=ResourceOptions(parent=remote_state_bucket,))

secrets_provider_name = f"{resource_name_prefix}-secrets-provider"
secrets_provider = aws.kms.Key(
    resource_name=secrets_provider_name,
    description=f'Pulumi secrets provider KMS key for stack {config["metadata"]["stack"]}',
    deletion_window_in_days=7,
    enable_key_rotation=True,
    tags={
        "Name": secrets_provider_name,
    },
)

secrets_provider_alias_name = f'alias/{config["metadata"]["stack"].capitalize()}PulumiSecretsProvider'

secrets_provider_alias = aws.kms.Alias(
    resource_name=f"{secrets_provider_name}-alias",
    name=secrets_provider_alias_name,
    target_key_id=secrets_provider.key_id,
    opts=ResourceOptions(parent=secrets_provider),
)

export("bucket_uri", remote_state_bucket.id.apply(lambda bucket_id: f"s3://{bucket_id}"))
export(
    "secrets_provider_uri",
    secrets_provider_alias.name.apply(
        lambda alias_name: f'awskms://{alias_name}?region={config["metadata"]["region"]}'),
)
