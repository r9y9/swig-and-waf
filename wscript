APPNAME = 'SWIG_WAF_EXAMPLE'
VERSION = '0.0.1'

from waflib import Options
import sys
import os
import re
import waflib

subdirs = [
    'src',
]

top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_c python')
        
def configure(conf):
    conf.load('compiler_c')

    conf.load('swig')
    if conf.check_swig_version() < (1, 2, 27):
        conf.fatal('this swig version is too old')
        
    conf.load('python')
    conf.check_python_version((2,4,2))
    conf.check_python_headers()
    
    conf.recurse(subdirs)

    print """
SWIG_WAF has been configured as follows:

[Build information]
Package:                 %s
build (compile on):      %s
host endian:             %s
Compiler:                %s
Compiler version:        %s
CFLAGS:                %s
""" % (
        APPNAME + '-' + VERSION,
        conf.env.DEST_CPU + '-' + conf.env.DEST_OS,
        sys.byteorder,
        conf.env.COMPILER_CC,
        '.'.join(conf.env.CC_VERSION),
        ' '.join(conf.env.CFLAGS)
        )
            
def build(bld):
    bld.recurse(subdirs)

    libs = []
    for tasks in bld.get_build_iterator():
        if tasks == []:
            break
        for task in tasks:
            if isinstance(task.generator, waflib.TaskGen.task_gen) and 'cshlib' in task.generator.features:
                libs.append(task.generator.target)
    ls = ''
    for l in set(libs):
        ls = ls + ' -l' + l
    ls += ' -lm'

    bld(source = 'SWIG_WAF.pc.in',
        prefix = bld.env['PREFIX'],
        exec_prefix = '${prefix}',
        libdir = bld.env['LIBDIR'],
        libs = ls,
        includedir = '${prefix}/include',
        PACKAGE = APPNAME,
        VERSION = VERSION)
