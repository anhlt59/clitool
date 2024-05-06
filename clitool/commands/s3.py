import os

import click
from click_shell import shell

from clitool.commands.base import validate_file, validate_required_value
from clitool.console import console
from clitool.services import S3Service, SessionService
from clitool.types.s3 import S3BucketTable

session = SessionService()
s3 = S3Service(session)


# CLI commands ---------------------------------------------------------------
@shell("s3", prompt="AWS ❯ S3 ❯ ")
def cli():
    """AWS S3."""
    pass


@cli.command()
@click.option("-p", "--prefix", help="S3 bucket name prefix", type=str, default="")
def list_buckets(prefix: str):
    """List S3 buckets."""
    with console.status("Listing S3 bucket ...", spinner="dots"):
        try:
            buckets = s3.bucket.list(prefix)
        except Exception as e:
            console.log(f"🔥 Failed to list buckets: {e}", style="red")
        else:
            bucket_table = S3BucketTable(items=buckets.items)
            console.print_table(bucket_table)


@cli.command()
@click.option("-b", "--bucket", help="S3 bucket name", required=False, default="", callback=validate_required_value)
@click.option("-p", "--prefix", help="S3 bucket name prefix", type=str, default="")
def list_objects(bucket: str, prefix: str):
    """List S3 objects in a bucket."""
    with console.status("Listing S3 objects ...", spinner="dots"):
        try:
            objs = s3.object.list(bucket, prefix)
        except Exception as e:
            console.log(f"🔥 Failed to list objects: {e}", style="red")
        else:
            console.print(objs.extract())


@cli.command()
@click.option("-p", "--bucket", help="S3 bucket name", type=str, required=True)
@click.option("-p", "--prefix", help="S3 object prefix", type=str, required=True)
@click.option("-d", "--directory", help="Directory path", type=str, required=True)
def upload_folder(bucket: str, prefix: str, directory: str):
    """Upload files from a directory to S3 bucket."""

    with console.status(f"Uploading files to {bucket} bucket ...", spinner="dots"):
        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    try:
                        s3_obj = s3.object.put(bucket, f"{prefix}/{file_name}", file_path)
                    except KeyboardInterrupt:
                        console.log("Stopped uploading files", style="yellow")
                        raise click.Abort()
                    except Exception as e:
                        console.log(f"🔥 Failed to upload files: {e}", style="red")
                        raise click.Abort()
                    else:
                        console.log(f"{s3_obj.bucket}:{s3_obj.key} done", style="green")
            console.log(f"Upload files to [b]{bucket}[/b] bucket successfully", style="green")


@cli.command()
@click.option("-b", "--bucket", help="S3 bucket name", type=str, required=True)
@click.option("-k", "--key", help="S3 object key", type=str, required=True)
@click.option("-f", "--file", help="File path", type=str, required=True, callback=validate_file)
def upload_file(bucket: str, key: str, file: str):
    """Upload a file to S3 bucket."""
    with console.status(f"Uploading file to {bucket} bucket ...", spinner="dots"):
        try:
            s3_obj = s3.bucket.put(bucket, key, file)
        except Exception as e:
            console.log(f"🔥 Failed to upload file: {e}", style="red")
        else:
            console.log(f"🚀 Upload file to [b]{s3_obj.bucket}:{s3_obj.key}[/b] successfully", style="green")
