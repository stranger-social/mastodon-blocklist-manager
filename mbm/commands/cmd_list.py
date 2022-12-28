from mbm.cli import pass_environment

import click


@click.group("list", short_help="List managment.")
@pass_environment
def cli(ctx):
    """List management."""
    pass

@cli.command("merge", short_help="Merge two Blocklist lists.")
@click.option("--whitelist", "-w", type=click.File("r"), required=False, help="Whitelist to prevent merge.")
@click.option("-i", "--input", required=True, multiple=True, type=click.File("r"))
@click.option("-o", "--output", required=True, type=click.File("w"))
@pass_environment
def merge(ctx, input, whitelist, output):
    """Merge multiple Blocklist lists into one file.
    Will erase the output file if it exists."""
    ctx.vlog("Merging lists...")
    if len(input) < 2:
        ctx.log("You need at least two input files.")
        return
    for i in input:
        ctx.vlog("Input: %s" % i.name)
    ctx.vlog("Output: %s" % output.name)
    # Read lists
    merged = []
    for i in input:
        merged += i.read().splitlines()
    # Remove duplicates
    merged = list(set(merged))
    # Remove whitelist
    if whitelist:
        ctx.vlog("Whitelist: %s" % whitelist.name)
        whitelist = whitelist.read().splitlines()
        merged = [i for i in merged if i not in whitelist]
    # Sort list
    merged.sort()
    # Write output and count lines
    count = 0
    for line in merged:
        output.write(line + "\n")
        count += 1
    ctx.log("Done! %d lines written." % count)


@cli.command("remove", short_help="Remove lines from a Blocklist list.")
@click.option("--whitelist", "-w", type=click.File("r"), required=False, help="Whitelist to prevent merge.")
@click.argument("list1", required=True, type=click.File("r"))
@click.argument("list2", required=True, type=click.File("r"))
@click.argument("output", required=True, type=click.File("w"))
@pass_environment
def remove(ctx, list1, list2, whitelist, output):
    """Remove Blockist 1 from a Blocklist 2.
    Will erase the output file if it exists."""
    ctx.vlog("Removing lines from list...")
    ctx.vlog("List 1: %s" % list1.name)
    ctx.vlog("List 2: %s" % list2.name)
    ctx.vlog("Output: %s" % output.name)
    # Read lists
    list1 = list1.read().splitlines()
    list2 = list2.read().splitlines()
    # Remove List1 from List2
    removed = list(set(list2) - set(list1))
    # Remove whitelist
    if whitelist:
        ctx.vlog("Whitelist: %s" % whitelist.name)
        whitelist = whitelist.read().splitlines()
        removed = [i for i in removed if i not in whitelist]
    # Sort list
    removed.sort()
    # Write output and count lines
    count = 0
    for line in removed:
        output.write(line + "\n")
        count += 1
    ctx.log("Done! %d lines written." % count)

@cli.command("sort", short_help="Sort a Blocklist list.")
@click.argument("input", required=True, type=click.File("r+"))
@click.argument("output", required=False, type=click.File("w"))
@pass_environment
def sort(ctx, input, output):
    """Sort a Blocklist list file and remove duplicates.
    If output is not specified, will overwrite the input file."""
    ctx.vlog("Sorting list...")
    ctx.vlog("Input: %s" % input.name)
    if output:
        ctx.vlog("Output: %s" % output.name)
    else:
        ctx.vlog("Output: %s" % input.name)
    # Read list
    lines = input.read().splitlines()
    # Remove duplicates lines
    lines = list(set(lines))
    # Sort list alphabetically
    lines.sort()
    # Write output and count lines
    # If output is not specified, overwrite input file
    if not output:
        input.seek(0)
        input.truncate()
    count = 0
    for line in lines:
        if output:
            output.write(line + "\n")
        else:
            # open input file as write using click.File
            input.write(line + "\n")
        count += 1
    ctx.log("Done! %d lines written." % count)
