# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import re
import jinja2
import codecs
import argparse
from arpeggio import NoMatch
import bibreport
from bibreport.parser import parse_bibtex

if sys.version < '3':
    text = unicode
else:
    text = str


class MyParser(argparse.ArgumentParser):
    """
    Custom arugment parser for printing help message in case of error.
    See http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()


# Points per rank. Used in Serbia.
points_table = {
    'M11': 15,
    'M12': 10,
    'M13': 6,
    'M14': 4,
    'M21': 8,
    'M22': 5,
    'M23': 3,
    'M24': 3,
    'M31': 3,
    'M32': 1.5,
    'M33': 1,
    'M34': 0.5,
    'M41': 7,
    'M42': 5,
    'M43': 3,
    'M44': 2,
    'M45': 1.5,
    'M51': 2,
    'M52': 1.5,
    'M53': 1,
    'M55': 2,
    'M56': 1,
    'M61': 1.5,
    'M62': 1,
    'M63': 0.5,
    'M66': 1,
    'M71': 6,
    'M72': 3,
    'M81': 8,
    'M82': 6,
    'M83': 4,
    'M84': 3,
    'M85': 2,
    'M91': 10,
    'M92': 8,
}


def points(type):
    return points_table.get(type, '')


def format_reference(ref):
    """
    Filter for formating reference according to its type.
    """
    rank = ref['rank']

    ret = ''

    if rank != 'M66':
        ret = ', '.join(ref['author']) + ', '

    ret += '"' + ref['title'] + '"'

    if rank == 'M66':
        ret += 'Edt.' + ', ' + ', '.join(ref['editor'])
        ret += ', ' + ref['publisher']
    else:
        if 'journal' in ref:
            ret += ', ' + ref['journal']
        elif 'booktitle' in ref:
            ret += ', ' + ref['booktitle']

    if 'institution' in ref:
        ret += ', ' + ref['institution']

    if 'school' in ref:
        ret += ', ' + ref['school']

    if 'pages' in ref:
        ret += ', pp. ' + ref['pages']

    if 'doi' in ref:
        ret += ', DOI: ' + ref['doi']

    ret += ', ' + ref['year'] + '.'

    return ret


def check_keys(refs):
    """
    Check mandatory keys.
    """
    mandatory = [('rank',), ('title',), ('booktitle', 'journal'),
                 ('author', 'editors'), ('year',), ('isbn', 'issn'),
                 ('publisher',), ('pages',)]
    for r in refs:
        for key in mandatory:
            if all([x not in r or not r[x] for x in key]):
                print("  Warning: There is no field {} in reference {}"
                      .format(" or ".join(key), r['bibkey']))
                r['uncomplete'] = True


def gen_html(refs, yearfilter, total_points):

    # Sort references by year and then by rank
    def rank_rev(r):
        return str(100 - int(r[1:]))
    refs.sort(key=lambda r: "{}-{}".format(r['year'], rank_rev(r['rank'])),
              reverse=True)

    # Initialize template engine.
    template_folder = os.path.join(os.path.dirname(bibreport.__file__),
                                   'templates')

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_folder))

    # Filters
    jinja_env.filters['points'] = points
    jinja_env.filters['format_reference'] = format_reference

    template = jinja_env.get_template('bibreport.template')
    with codecs.open('bibreport.html', 'w', encoding="utf-8") as f:
        f.write(template.render(refs=refs, yearfilter=yearfilter,
                                total_points=total_points))


def main():
    """
    Main console entry point.
    """

    arg_parser = MyParser(description="bibtex reporting tool")
    arg_parser.add_argument('bibfile', help="The bibtex file.")
    arg_parser.add_argument('yearfilter',
                            help="Filter by years (e.g. 2011 or 2010-2015)",
                            nargs="?")

    args = arg_parser.parse_args()

    if args.bibfile:

        refs = []

        def check_year(yearfilter):
            def filter_for_years(ref):
                if '-' in yearfilter:
                    _from, to = yearfilter.split('-')
                    _from, to = int(_from), int(to)
                    return _from <= int(ref['year']) <= to
                else:
                    return int(ref['year']) == int(yearfilter)
            return filter_for_years

        try:
            refs_f = parse_bibtex(args.bibfile)

            # If year filter is given do the filtering
            if args.yearfilter:
                refs_f = list(filter(check_year(args.yearfilter), refs_f))

            check_keys(refs_f)

            total_points = 0
            for r in refs_f:
                # Convert author string to list
                if 'author' in r:
                    r['author'] = [x.strip() for x in
                                   re.split(' and |,', r['author'])]
                elif 'editor' in r:
                    r['editor'] = [x.strip() for x in
                                   re.split(' and |,', r['editor'])]
                else:
                    print("Warning: No autor or editor for {}"
                          .format(r['title']))

                # Calculate points
                rank = r['rank']
                if rank in points_table:
                    total_points += points_table[rank]
                else:
                    print("Warning: No points for paper rank {}".format(rank))

            refs.extend(refs_f)
        except NoMatch as e:
            print(text(e))

        gen_html(refs, args.yearfilter, total_points)
