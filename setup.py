from setuptools import setup

setup(
    name="mastodon-blocklist-manager",
    version="0.1.1",
    packages=["mbm", "mbm.commands"],
    include_package_data=True,
    install_requires=["click",
                      "requests",
                      ],
    entry_points="""
        [console_scripts]
        mbm=mbm.cli:cli
    """,
)