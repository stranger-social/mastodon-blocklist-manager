from setuptools import setup

setup(
    name="mastodon-blocklist-manager",
    version="1.0",
    packages=["mbm", "mbm.commands"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        mbm=mbm.cli:cli
    """,
)