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

@cli.command("list", short_help="List public Blocklist entries on a server.")
@click.option("-p", "--prefix", required=True, type=str, help="Prefix of filename to write to.")
@click.option("-s", "--sort", required=False, default=True, type=bool, help="Sort by severity and reason.")
@pass_environment
def list(ctx, prefix, sort):
    """List public Blocklist entries on a server.
    Assigns a prefix to the filename to write to.
    Creates files based on severity level and reason.
    <prefix>-<severity>-<reason>.txt"""
    ctx.log("Retrieving Domain Blocks.")
    data = {
        "limit": 1000
    }
    # read json from server and no headers
    query = requests.get(ctx.url + "/api/v1/instance/domain_blocks", data=data)
    if query.status_code == 200:
        ctx.vlog("Query successful.")
        # Parse json
        json = query.json()
        # Extract domain id for each domain in domain_list
        count = 0
        skipped = 0
        for domain in json:
            if sort == True:
                
                # if statement to check for asterisk in domain name and skip it
                if "*" in domain["domain"]:
                    skipped += 1
                    ctx.log(domain["domain"] + "[Skipping]")
                else:
                    # Create filname based on prefix, severity, and reason (concantenate comment to 10 characters)
                    # concantenate comment to 10 characters and sanitize filename (no spaces, or invalid characters)
                    if domain['comment'] == None:
                        comment_sanitized = str("None")
                    else:
                        comment_sanitized = domain["comment"][:10].replace(" ", "_").replace("/", "_")                    
                    filename = ctx.home + "/" + prefix + "-" + domain["severity"] + "-" + comment_sanitized + ".txt"
                    ctx.log(domain["domain"] + " " + domain["severity"] + " " + comment_sanitized)
                    # Write domain to file
                    with open(filename, "a") as f:
                        # Write domain to file with newline
                        f.write(domain["domain"] + "\n")
            else:
                ctx.log(domain["domain"])
                # if statement to check for asterisk in domain name and skip it
                if "*" in domain["domain"]:
                    skipped += 1
                    ctx.log(domain[domain] + "[Skipping]")
                else:
                    # Create filname based on prefix, severity, and reason (concantenate comment to 10 characters)
                    filename = ctx.home + "/" + prefix + ".txt"
                    # Write domain to file
                    with open(filename, "a") as f:
                        # Write domain to file with newline
                        f.write(domain["domain"] + "\n")
            # Increment count                    
            count += 1
            added = count - skipped
        ctx.log(f"Done! {added} domains added. {skipped} domains skipped.")