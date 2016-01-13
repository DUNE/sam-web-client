from setuptools import setup, find_packages
setup(
    name = 'sam-web-client',
    version = '2.0',
    description = 'Python client and command line interface to SAM Web Services',

    # upstream:
    author = 'SAM Team',
    author_email = 'sam-users@listserv.fnal.gov',
    url = 'https://cdcvs.fnal.gov/redmine/projects/sam-web-client',

    # packaging fork:
    maintainer = 'Brett Viren',
    maintainer_email = 'bv@bnl.gov',
    download_url = 'https://github.com/DUNE/sam-web-client',

    package_dir = {'':'python'},
    
    py_modules = ['samweb_cli'],
    packages = ['samweb_client', 'simplejson_209'],

    ## ignore this some ad-hoc, brokenness
    #scripts = ['bin/samweb'],
    entry_points = {
        'console_scripts' : [ 'samweb = samweb_cli:main', ],
    },
)
