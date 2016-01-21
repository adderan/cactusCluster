from __future__ import absolute_import
from setuptools import setup, find_packages
from version import cgcloud_version, bd2k_python_lib_version, fabric_version

setup(
    name='cgcloud-cactusCluster',
    version=cgcloud_version,

    author='Alden Deran',
    author_email='adderan@ucsc.edu',
    url='https://github.com/adderan/cactusCluster',
    description='Cluster for running progressiveCactus',

    package_dir={ '': 'src' },
    packages=find_packages( 'src' ),
    namespace_packages=[ 'cgcloud' ],
    install_requires=[
        'cgcloud-lib==' + cgcloud_version,
        'cgcloud-core==' + cgcloud_version,
        'cgcloud-mesos==' + cgcloud_version,
        'cgcloud-toil==' + cgcloud_version,
        'bd2k-python-lib==' + bd2k_python_lib_version,
        'Fabric==' + fabric_version ] )
