# Rename file to config.py and add your token and url
API_TOKEN="<YOUR_API_TOKEN>"
SERVER_URL="<YOUR_SERVER_URL>"
HOME="<YOUR_HOME_DIRECTORY>" # This is where the blocklist will be stored

# domain_blocks defaults https://docs.joinmastodon.org/entities/Admin_DomainBlock/
DOMAIN_BLOCKS_SEVERITY="suspend" # suspend, silence, limit, or noop
DOMAIN_BLOCKS_PUBLIC_COMMENT="This domain has been blocked by the instance admin."
DOMAIN_BLOCKS_PRIVATE_COMMENT="This domain has been blocked by the instance admin."
DOMAIN_BLOCKS_REJECT_MEDIA="True"
DOMAIN_BLOCKS_REJECT_REPORTS="True"
DOMAIN_BLOCKS_OBFUSCATE="False"
