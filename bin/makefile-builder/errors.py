#!/usr/bin/python

import sys
from makefile_builder import MakefileBuilder
from builder_data import error_pages

m = MakefileBuilder()

def build_all_error_pages(error_pages):
    m.comment('build targets for all error pages, which require some munging.', block='header')
    m.newline(block='header')

    for page in error_pages:
        build = '$(public-branch-output)/meta/' + page + '/index.html'
        dep = '$(branch-output)/dirhtml/meta/' + page + '/index.html'

        m.append_var(variable='ERROR_PAGES',
                     value=build,
                     block='page')
        m.target(target=dep, dependency='$(branch-output)/dirhtml', block='page')
        m.target(target=build, dependency=dep, block='page')
        m.job('sed $(SED_ARGS_FILE) "s@\.\./\.\./@http://docs.mongodb.org/manual/@" $@', 
              block='page')
        m.msg('[web]: processed error page: $@', block='page')

        m.newline(block='page')

    m.comment('integration target for the error page guides:', block='meta')

    m.target(target='.PHONY',
             dependency='clean-error-pages error-pages $(ERROR_PAGES)',
             block='meta')
    m.newline(block='meta')
    m.target(target='error-pages',
             dependency='$(ERROR_PAGES)', block='meta')
    m.newline(block='meta')
    m.target(target='clean-error-pages', dependency=None, block='meta')
    m.job('rm -rf $(ERROR_PAGES)', True, block='meta')

def main():
    build_all_error_pages(error_pages)

    m.write(sys.argv[1])

    print('[meta-build]: built "' + sys.argv[1] + '" to specify error pages.')

if __name__ == '__main__':
    main()
