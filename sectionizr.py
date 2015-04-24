# Copyright (c) 2015 André von Kugland

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


"""
Creates sections in multiple languages.

Like this:

// ----------------------------- //
//       This is a section       //
// ----------------------------- //
"""


import re
import sublime
import sublime_plugin


class SectionizrCommand(sublime_plugin.TextCommand):

    """Creates sections in multiple languages."""

    def window_ruler(self, index):
        """Get rulers."""
        rulers = sublime.active_window().active_view().settings().get('rulers')
        return sorted(rulers)[index]

    def tab_size(self):
        """Get tab size."""
        return sublime.active_window().active_view().settings().get('tab_size')

    def comment_format(self, region):
        """Select comment format according to scope."""
        syntax_names = self.view.scope_name(region.a).split()
        syntaxes = {
            'source.c':                       ('/* ',   ' */',  '-'),
            'source.c++':                     ('// ',   ' //',  '-'),
            'source.c++.11':                  ('// ',   ' //',  '-'),
            'source.camlp4.ocaml':            ('(* ',   ' *)',  '-'),
            'source.cs':                      ('// ',   ' //',  '-'),
            'source.css':                     ('/* ',   ' */',  '-'),
            'source.erlang':                  ('% ',    ' %',   '-'),
            'source.go':                      ('// ',   ' //',  '-'),
            'source.java':                    ('// ',   ' //',  '-'),
            'source.js':                      ('// ',   ' //',  '-'),
            'source.js.jquery':               ('// ',   ' //',  '-'),
            'source.lilypond':                ('% ',    ' %',   '-'),
            'source.objc':                    ('// ',   ' //',  '-'),
            'source.objc++':                  ('// ',   ' //',  '-'),
            'source.ocaml':                   ('(* ',   ' *)',  '-'),
            'source.ocamllex':                ('(* ',   ' *)',  '-'),
            'source.ocamlyacc':               ('(* ',   ' *)',  '-'),
            'source.perl':                    ('# ',    ' #',   '-'),
            'source.php.embedded.block.html': ('// ',   ' //',  '-'),
            'source.python':                  ('# ',    ' #',   '-'),
            'source.ruby':                    ('# ',    ' #',   '-'),
            'source.scala':                   ('// ',   ' //',  '-'),
            'source.shell':                   ('# ',    ' #',   '-'),
            'source.sql':                     ('-- ',   ' --',  '-'),
            'source.yaml':                    ('# ',    ' #',   '-'),
            'text.html.basic':                ('<!-- ', ' -->', '–'),
            'text.tex':                       ('% ',    ' %',   '-'),
            'text.tex.latex':                 ('% ',    ' %',   '-'),
            'text.tex.latex.beamer':          ('% ',    ' %',   '-'),
            'text.tex.latex.memoir':          ('% ',    ' %',   '-'),
            'text.xml':                       ('<!-- ', ' -->', '–'),
            'text.xml.xsl':                   ('<!-- ', ' -->', '–')
        }

        for key in syntaxes.keys():
            if key in syntax_names:
                return syntaxes[key]

        raise RuntimeError('Unsupported syntax: ' + str(syntax_names))

    def run(self, edit):
        """Apply Sectionizr to each selected line."""
        for region in self.view.sel():
            line = self.view.line(region)
            str = self.view.substr(line)
            (space, contents) = re.search('^(\s*)(.*)', str).groups()
            title_format = u'{0}'
            title = title_format.format(contents)
            (prefix, suffix, ln) = self.comment_format(line)
            ruler = self.window_ruler(0)
            center_width = ruler - len(prefix) - len(suffix) \
                - len(space.expandtabs(self.tab_size())) - 1
            full_line = prefix + ''.center(center_width, ln) + suffix
            comment_line = prefix + title.center(center_width, ' ') + suffix
            self.view.replace(edit, line, "\n" + space + full_line +
                              "\n" + space + comment_line + "\n" + space +
                              full_line + "\n")
