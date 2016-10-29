import sublime, sublime_plugin, re

from collections import OrderedDict

class SectionizrCommand(sublime_plugin.TextCommand):
  def str_width(str):
    width = 0
    for char in str:
      code = ord(char)
      if (0xFF21 <= code <= 0xFF3A) or (0xFF41 <= code <= 0xFF5A):
        width = width + 1
      width = width + 1
    return width

  def window_ruler(self, index):
    return sorted(sublime.active_window().active_view().settings().get('rulers'))[index]

  def tab_size(self):
    return sublime.active_window().active_view().settings().get('tab_size')

  def comment_format(self, region):
    syntax_names = self.view.scope_name(region.a).split()
    fmt = OrderedDict([
      ('source.python',                  ('# ',    ' #'  )),
      ('source.ruby',                    ('# ',    ' #'  )),
      ('source.js',                      ('// ',   ' //' )),
      ('source.js.jquery',               ('// ',   ' //' )),
      ('source.json',                    ('// ',   ' //' )),
      ('source.java',                    ('// ',   ' //' )),
      ('source.c++',                     ('// ',   ' //' )),
      ('source.c++.11',                  ('// ',   ' //' )),
      ('source.cs',                      ('// ',   ' //' )),
      ('source.objc++',                  ('// ',   ' //' )),
      ('source.objc',                    ('// ',   ' //' )),
      ('source.c',                       ('/* ',   ' */' )),
      ('source.css',                     ('/* ',   ' */' )),
      ('source.php.embedded.block.html', ('// ',   ' //' )),
      ('text.html.basic',                ('<!-- ', ' -->')),
      ('text.xml',                       ('<!-- ', ' -->')),
      ('text.xml.xsl',                   ('<!-- ', ' -->')),
      ('source.shell',                   ('# ',    ' #'  )),
      ('source.perl',                    ('# ',    ' #'  )),
      ('source.sql',                     ('-- ',   ' --' ))
    ])
    for k in fmt.keys():
      if k in syntax_names:
        return fmt[k]

    raise NotImplementedError('Unsupported syntax: ' + str(syntax_names))

  def run(self, edit, level):
    for region in self.view.sel():
      line = self.view.line(region)
      str = self.view.substr(line)
      (space, contents) = re.search('^(\s*)(.*)', str).groups()
      (prefix, suffix) = self.comment_format(line)
      ruler = self.window_ruler(0)
      center_width = ruler - len(prefix) - len(suffix) \
                   - len(space.expandtabs(self.tab_size())) - 1

      if level == 0:
        title        = contents.upper()
        comment_line = prefix + title.center(center_width, ' ') + suffix
        hr_line      = prefix + '*' * center_width + suffix
        res          = space + hr_line + "\n" \
                     + space + comment_line + "\n" \
                     + space + hr_line
      elif level >= 1:
        title        = '[ {0} ]'.format(contents)
        comment_line = prefix + title.center(center_width, '*') + suffix
        hr_line      = prefix + '*' * center_width + suffix
        res          = space + comment_line

      self.view.replace(edit, line, "\n" + res + "\n")
