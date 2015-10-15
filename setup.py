"""Setup for totem_otr XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='totem_otr-xblock',
    version='0.1',
    description='Totem OTR Assessment', 
    packages=[
        'totem_otr',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'totem_otr_jid_input = totem_otr:TotemOTR_JIDInput',
            'totem_otr_trust = totem_otr:TotemOTR_Trust',
        ]
    },
    package_data=package_data("totem_otr", ["static", "public"]),
)
