#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='mysql://darkib_admin:its2forme@localhost/darkib', debug='False', repository='db_repo')
