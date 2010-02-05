#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

based on pdfjam (http://go.warwick.ac.uk/pdfjam)
'''

__version__ = '0.2'

import optparse
import os
import tempfile
import subprocess
import shutil
import re

def check_requisites():
    '''
    Helper function for checking the requisites and dependencies for pdfnup
    '''
    # @TODO: check if pdflatex is available
    # @TODO: check other requisites and use this function
#    pdflatex="/usr/bin/pdflatex"
#    PATH=`dirname "$pdflatex"`:$PATH
#    export PATH
#    case `kpsewhich pdfpages.sty` in
#        "") echo "pdfnup: pdfpages.sty not installed"; exit 1;;
#    esac
#    case `kpsewhich eso-pic.sty` in
#        "") echo \
#            "pdfnup: eso-pic.sty not installed (see the pdfpages manual)"
#            exit 1;;
#    esac
#    case `kpsewhich everyshi.sty` in
#        "") echo \
#            "pdfnup: everyshi.sty not installed (see the pdfpages manual)"
#            exit 1;;
#    esac

def build_option_parser():
    '''
    Build the command line interface.
    '''
    cliparser = optparse.OptionParser(
        '''usage: %prog [options] file.pdf [another.pdf ...]
        Rearrange/stack pages of a PDF file.
        ''',
        version='%%prog %s' % __version__,
    )
    # Specify the output file.
    cliparser.add_option(
        '-o', '--output',
        action='store', dest='output_file', default=None,

        help='The output file name.',
    )
    # Main options.
    cliparser.add_option(
        '-n', '--nup', metavar='MxN',
        action='store', dest='nup', default='2x1',
        help='Specification of how to stack the pages. E.g. "--nup" 2x1 for two pages side by side, "--num 1x2" for two pages stacked vertically, etc',
    )
    cliparser.add_option(
        '-p', '--pages', metavar='RANGE',
        action='store', dest='pages', default='all',
        help='The range of pages to be included. E.g. "--pages 3-6", "--pages 2,8,4,5" or "--pages all".',
    )
    # Layout options
    cliparser.add_option(
        '--papersize',
        default='a4paper',
        action='store', dest='papersize',
        help='The output paper size (LaTeX specification). E.g. a4paper or letterpaper',
    )
    cliparser.add_option(
        '--orientation',
        default='auto',
        action='store', dest='orientation',
        help='The output page orientation: landscape, portrait or auto.',
    )

    cliparser.add_option(
        '-f', '--frame',
        default=False,
        action='store_true', dest='frame',
        help='Set a thin frame around the stacked pages.',
    )
    cliparser.add_option(
        '--trim',
        default=None,
        action='store', dest='trim',
        help='A page trimming specification. E.g --trim "1cm 1cm 1cm 1cm".  Note that trimming does not mix well with --frame.',
    )

    cliparser.add_option(
        '--offset',
        default=None,
        action='store', dest='offset',
        help='An page offset specification to set the position of output pages. E.g --offset "1cm 0.5cm".',
    )
    cliparser.add_option(
        '--delta',
        default=None,
        action='store', dest='delta',
        help='Put space between logical pages. E.g. --delta "1cm 1cm"',
    )
    cliparser.add_option(
        '--noautoscale',
        default=False,
        action='store_true', dest='noautoscale',
        help='Disable the automatic scaling of the logical pages. Use --scale to set the scaling factor explicitly.',
    )
    cliparser.add_option(
        '--scale',
        default=None,
        action='store', dest='scale',
        help='Specify the scaling factor for the logical pages. E.g. --scale 0.91.',
    )
    cliparser.add_option(
        '-c', '--column',
        default=False,
        action='store_true', dest='column',
        help='Put successive logical pages along columns (instead of along rows).',
    )
    cliparser.add_option(
        '--openright',
        default=False,
        action='store_true', dest='openright',
        help='Put an empty page before first page, so that first page is at right hand side.',
    )

    # Various options
    cliparser.add_option(
        '--tidy',
        action='store_true', dest='tidy', default=True,
        help='Clean up the temporary files when ready.',
    )
    cliparser.add_option(
        '--untidy',
        action='store_false', dest='tidy', default=True,
        help='Do not clean up the temporary files.',
    )

    return cliparser


def main():

    cliparser = build_option_parser()

    # Parse the command line.
    (clioptions, cliargs) = cliparser.parse_args()

    # Check options and arguments
    if len(cliargs) == 0:
        raise ValueError('At least one input file should be given')
    if len(cliargs) > 1 and clioptions.output_file != None:
        raise ValueError('--outfile cannot be used with multiple input files')

    # Set the fitpaper setting and handle the orient setting
    clioptions.fitpaper = 'false'
    if clioptions.orientation == 'auto':
        x, y = parse_nup(clioptions.nup)
        if x > y:
            clioptions.orientation = 'landscape'
        elif x < y:
            clioptions.orientation = 'portrait'
        else:
            clioptions.fitpaper = 'true'


    for input_file in cliargs:
        print 'Processing', input_file

        output_file = clioptions.output_file
        if output_file == None:
            output_file = '%s-%s.pdf' % (os.path.splitext(input_file)[0], clioptions.nup)
        assert output_file != input_file


        # Create a temp directory for doing our work
        work_dir = tempfile.mkdtemp(prefix='pdfnuppy')
        print 'working in', work_dir
        # Create a symbolic link to the PDF file to include
        os.symlink(os.path.abspath(input_file), os.path.join(work_dir, 'input.pdf'))
        # Generate the LaTeX file.
        tex_file_name = os.path.join(work_dir, 'pdfnuppy.tex')
        with file(tex_file_name, 'w') as f:
            f.write(generate_tex(clioptions))

        # Call pdflatex (run it in the working directory).
        p = subprocess.Popen(
            ['pdflatex', '--interaction', 'batchmode', tex_file_name],
            cwd=work_dir,
            )
        p.communicate()
        # Check if the PDF was generated and copy it over to the output file
        generated_pdf = os.path.join(work_dir, 'pdfnuppy.pdf')
        if os.path.isfile(generated_pdf):
            shutil.copyfile(generated_pdf, output_file)
            print 'Finished: output is', output_file
        else:
            print 'Failed: output file was not written'

        # clean up
        if clioptions.tidy:
            shutil.rmtree(work_dir)


def parse_nup(nup):
    '''Helper function to parse the nup specification'''
    mo = re.match(r'(\d)x(\d)', nup)
    x = int(mo.group(1))
    y = int(mo.group(2))
    return x, y


def generate_tex(clioptions, input_pdf_file='input.pdf'):
    '''
    Generate the LaTeX code for PdfNuppy
    '''
    # Dictionary of options for the includepdf command
    option_dict = {}
    # Handle the 'all pages' option
    if clioptions.pages == 'all':
        option_dict['pages'] = '-'
    else:
        option_dict['pages'] = clioptions.pages
    # String clioptions just to copy over (when not None).
    for field in ['nup', 'orientation', 'frame', 'trim', 'delta', 'offset', 'scale']:
        value = clioptions.__dict__[field]
        if value != None:
            option_dict[field] = value
    # Boolean clioptions to copy over.
    for field in ['frame', 'fitpaper', 'noautoscale', 'column', 'openright']:
        option_dict[field] = str(clioptions.__dict__[field]).lower()

    options = ','.join('%s=%s' % kv for kv in option_dict.items())

    return  r'''\documentclass[%(papersize)s,%(orientation)s]{article}
        \usepackage{pdfpages}
        \begin{document}
        \includepdf[%(options)s]{%(input_pdf_file)s}
        \end{document}
    ''' % {
            'papersize': clioptions.papersize,
            'orientation': clioptions.orientation,
            'options': options,
            'input_pdf_file': input_pdf_file,
        }




if __name__ == '__main__':
    main()
