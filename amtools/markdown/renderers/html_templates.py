
def indent(lines, n=1):
    spaces = "  "*n
    return spaces + lines.replace("\n", "\n" + spaces)

def info(**kwargs):
    if 'cls' in kwargs:
        kwargs['class'] = kwargs['cls']
        del kwargs['cls']
    return "".join(f" {k}=\"{v}\"" for k, v in kwargs.items())

class HtmlTemplates:

    def document(title, body, css_files=[], js_files=[]):
        styles = '\n'.join(f"<link rel=\"stylesheet\" href=\"{ss}\">" for ss in css_files)
        scripts = '\n'.join(f"<script src=\"{js}\"></script>" for js in js_files)
        return \
f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
{indent(styles, 2)}
{indent(scripts, 2)}
</head>
<body>
{indent(body, 2)}
</body>
</html>"""

    @staticmethod
    def div(body, **kwargs):
        return f"<div{info(**kwargs)}>\n{indent(body, 2)}\n</div>"

    @staticmethod
    def oneline_div(body, **kwargs):
        return f"<div{info(**kwargs)}>{body}</div>"

    @staticmethod
    def span(inner, **kwargs):
        return f"<span{info(**kwargs)}>{inner}</span>"

    @staticmethod
    def hr(**kwargs):
        return f"<hr{info(**kwargs)}>"

    @staticmethod
    def heading(lvl, title, **kwargs):
        h_ = "h" + str(lvl)
        return f"<{h_}{info(**kwargs)}>{title}</{h_}>"

    @staticmethod
    def unordered_list(list_items, **kwargs):
        return f"<ul{info(**kwargs)}>\n{indent(list_items, 2)}\n</ul>"

    @staticmethod
    def ordered_list(list_items, **kwargs):
        return f"<ol{info(**kwargs)}>\n{indent(list_items, 2)}\n</ol>"

    @staticmethod
    def list_item(text, **kwargs):
        return f"<li{info(**kwargs)}>{text}</li>"

    @staticmethod
    def task_list_item(text, task_symb, is_checked):
        if is_checked:
            return f"<li data-task='{task_symb}' class='task-list-item is-checked'><input checked='' type='checkbox' class='task-list-item-checkbox'>{text}</li>"
        else:
            return f"<li data-task='{task_symb}' class='task-list-item'><input type='checkbox' class='task-list-item-checkbox'>{text}</li>"

    @staticmethod
    def table(headings, rows, widths, **kwargs):
        head = HtmlTemplates.tr(headings, widths, is_heading=True, is_even=False)
        body = []
        for i, row in enumerate(rows):
            body.append(HtmlTemplates.tr(row, widths, is_heading=False, is_even=i%2==0))
        body = "\n".join(body)
        return \
f"""<table{info(**kwargs)}>
  <thead>
{indent(head, 4)}
  </thead>
  <tbody>
{indent(body, 4)}
  </tbody>
</table>
"""

    @staticmethod
    def tr(row, widths, is_heading, is_even):
        make_cell = HtmlTemplates.th if is_heading else HtmlTemplates.td

        cols = []
        for i in range(len(row)):
            cols.append(make_cell(row[i], style=widths[i]))
        col_text = '\n'.join(cols)
        if is_even:
            return f"<tr class=\"even\">\n{indent(col_text, 2)}\n</tr>"
        else:
            return f"<tr class=\"odd\">\n{indent(col_text, 2)}\n</tr>"


    @staticmethod
    def th(text, **kwargs):
        return f"<th{info(**kwargs)}>{text}</th>"

    @staticmethod
    def td(text, **kwargs):
        return f"<td{info(**kwargs)}>{text}</td>"


    @staticmethod
    def pre(inner, **kwargs):
        return f"<pre{info(**kwargs)}>{inner}</pre>"

    @staticmethod
    def blockquote(text, **kwargs):
        return f"<blockquote{info(**kwargs)}>\n{indent(text, 2)}\n</blockquote>"

    @staticmethod
    def img(filename, alt_text, **kwargs):
        return f"<img{info(**kwargs)} src=\"{filename}\" alt=\"{alt_text}\">"

    @staticmethod
    def p(text, **kwargs):
        return f"<p{info(**kwargs)}>\n{indent(text, 2)}\n</p>"

    @staticmethod
    def a(text, addr, **kwargs):
        href=f"href=\"{addr}\""
        return f"<a href=\"{addr}\"{info(**kwargs)}>{text}</a>"

    @staticmethod
    def bold(text, **kwargs):
        return f"<b{info(**kwargs)}>{text}</b>"

    @staticmethod
    def italics(text, **kwargs):
        return f"<i{info(**kwargs)}>{text}</i>"

    @staticmethod
    def code(text, **kwargs):
        return f"<code{info(**kwargs)}>{text}</code>"

    @staticmethod
    def delete(text, **kwargs):
        return f"<del{info(**kwargs)}>{text}</del>"

    @staticmethod
    def mark(text, **kwargs):
        return f"<mark{info(**kwargs)}>{text}</mark>"


