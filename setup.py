from setuptools import setup

setup(
    name="mastodon-blocklist-manager",
    version="0.1.1",
    author="azcoigreach@gmail.com",
    packages=["mbm", "mbm.commands"],
    include_package_data=True,
    install_requires=["click>=8.1.3",
                      "requests>=2.28.1",
                      ],
    python_requires='>=3.8',
    entry_points="""
        [console_scripts]
        mbm=mbm.cli:cli
    """,
)