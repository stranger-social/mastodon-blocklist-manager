# mastodon-blocklist-manager

A CLI tool to manage your Mastodon blocklist.

## Installation

Requires Python 3.8 or higher.

```
git clone https://github.com/azcoigreach/mastodon-blocklist-manager.git
cd mastodon-blocklist-manager
pip install . --editable
```

## Configuration

mbm uses a configuration file to store your Mastodon instance and credentials. Copy the `example_settings.py` file to `settings.py` and add your Instance API Token and Instance URL.

This app require `admin:read:domain_blocks` and `admin:write:domain_blocks` scopes.

## Usage

```
mbm --help
```

The `mbm` command will show you the available commands. You can use `mbm <command> --help` or `mbm <command> <sub-commnd> --help` to get more information about each command.  The command below are examples of how to use the app and may not cover all of the features.  Use the in-app help for more information.

### Merge two blocklists

```
mbm list merge list1.txt list2.txt output_list.txt
```

Will merge and sort the two lists into the output file. The output file will overwritten if it already exists.

### Add a whitelist
    
```
mbm list merge list1.txt list2.txt output_list.txt -w whitelist.txt
```

Keep domains you don't want to block in the whitelist file.  These will be removed from the output file.

### Add blocklist domains to the Instance

```
mbm -v domain_blocks add blocklist.txt -s suspend -pub "Public reason" -priv "Private reason" -rm True -rr True -obf False
```

Add the domains in the blocklist file to the instance.  The `-s` option can be `suspend` or `silence`.  The `-pub` and `-priv` options are the public and private reasons for the block.  The `-rm` option will remove the domain from the blocklist file if the block was successful.  The `-rr` option will remove the domain from the blocklist file if the block failed.  The `-obf` option will obfuscate the domain before adding it to the blocklist.

Adding the `-v` option after `mbm` command will enable verbose output.


### Remove domains from the Instance

```
mbm domain_blocks remove blocklist.txt 
```

Will remove the domains in the blocklist file from the instance.

### Purge the Instance domain_blocks database

```
mbm domain_blocks purge
```

Will remove all domains from the instance domain_blocks database. Requires confirmation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
