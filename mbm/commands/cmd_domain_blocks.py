from mbm.cli import pass_environment

import click
import requests

@click.group("domain_blocks", short_help="Domain Blocks management.")
@pass_environment
def cli(ctx):
    """Domain Blocks management."""
    pass

@cli.command("add", short_help="Upload Blocklist entries to the server from a list.")
@click.argument("domain_list", required=True, type=click.File("r"))
@click.option("--severity", "-s", type=click.Choice(["silence", "suspend", "noop"]), required=True, help="Severity of the entries.")
@click.option("--public", "-pub", required=True, type=str, help="Public Comment")
@click.option("--private", "-priv", required=True, type=str, help="Private Comment")
@click.option("--reject_media", "-rm", required=True, type=bool, help="Reject Media")
@click.option("--reject_reports", "-rr", required=True, type=bool, help="Reject Reports")
@click.option("--obfuscate", "-obf", required=True, type=bool, help="Obfuscate")
@pass_environment
def add(ctx, domain_list, severity, public, private, reject_media, reject_reports, obfuscate):
    """Upload Blocklist entries to the server from a list."""
    # Refernce to the API https://docs.joinmastodon.org/methods/admin/domain_allows/
    # Read blocklist
    domain_list = domain_list.read().splitlines()
    # Upload blocklist
    for line in domain_list:
        ctx.log("Uploading %s" % line)
        data = {
            "domain": line,
            "severity": severity,
            "public_comment": public,
            "private_comment": private,
            "reject_media": reject_media,
            "reject_reports": reject_reports,
            "obfuscate": obfuscate
        }
        headers = {
            "Authorization": "Bearer %s" % ctx.token
            }
        response = requests.post(ctx.url + "/api/v1/admin/domain_blocks", data=data, headers=headers)
        if response.status_code == 200:
            ctx.log("Upload successful.")
        else:
            ctx.log("Upload failed.")
            ctx.vlog("Response: %s" % response.text)
    ctx.log("Done!")

@cli.command("remove", short_help="Remove Blocklist entries on the server from a list.")
@click.argument("domain_list", required=True, type=click.File('r'))
@pass_environment
def remove(ctx, domain_list):
    """Remove Blocklist entries on the server from a list."""
    ctx.log("Removing domains from server blocked domains...")
    ctx.log("Domain list: %s" % domain_list.name)
    # Read domain list
    domain_list = domain_list.read().splitlines()
    '''Read server json and extract domain id for each domain in domain_list
    if domain is not found, we need to skip it
    if domain is found, we need to delete it'''
    # Get server json
    ctx.log("Retrieving Domain Blocks.")
    data = {
        "limit": 1000
    }
    headers = {
        "Authorization": "Bearer %s" % ctx.token
        }
    query = requests.get(ctx.url + "/api/v1/admin/domain_blocks", data=data, headers=headers)
    ctx.vlog("Query: %s" % query)
    if query.status_code == 200:
        ctx.vlog("Query successful.")
        ctx.vlog("Query: %s" % query.text)
        # Parse json
        json = query.json()
        # Extract domain id for each domain in domain_list
        count = 0
        for line in domain_list:
            ctx.log("Removing %s" % line)
            for domain in json:
                if domain["domain"] == line:
                    ctx.vlog("Domain found.")
                    ctx.vlog("Domain ID: %s" % domain["id"])
                    # Delete domain
                    headers = {
                        "Authorization": "Bearer %s" % ctx.token
                        }
                    response = requests.delete(ctx.url + "/api/v1/admin/domain_blocks/" + domain["id"], data=data, headers=headers)
                    if response.status_code == 200:
                        ctx.log("Delete successful.")
                        count += 1
                    else:
                        ctx.log("Delete failed.")
                        ctx.vlog("Response: %s" % response.text)
        ctx.log(f"Done! {count} domains removed.")

@cli.command("purge", short_help="Purge Blocklist entries on the server.")
@pass_environment
def purge(ctx):
    """Purge Blocklist entries on the server."""
    click.confirm("Are you sure you want to purge the server's blocked domains?", abort=True)
    ctx.log("Purging server blocked domains...")
    # Get server json
    ctx.log("Retrieving Domain Blocks.")
    data = {
        "limit": 1000
    }
    headers = {
        "Authorization": "Bearer %s" % ctx.token
        }
    query = requests.get(ctx.url + "/api/v1/admin/domain_blocks", data=data, headers=headers)
    ctx.vlog("Query: %s" % query)
    if query.status_code == 200:
        ctx.vlog("Query successful.")
        ctx.vlog("Query: %s" % query.text)
        # Parse json
        json = query.json()
        # Extract domain id for each domain in domain_list
        count = 0
        for domain in json:
            ctx.log("Removing %s" % domain["domain"])
            # Delete domain
            headers = {
                "Authorization": "Bearer %s" % ctx.token
                }
            response = requests.delete(ctx.url + "/api/v1/admin/domain_blocks/" + domain["id"], data=data, headers=headers)
            if response.status_code == 200:
                ctx.vlog("Delete successful.")
                count += 1
            else:
                ctx.log("Delete failed.")
                ctx.vlog("Response: %s" % response.text)
        ctx.log(f"Done! {count} domains removed.")
