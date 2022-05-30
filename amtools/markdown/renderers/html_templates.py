
def indent(lines, n=1):
    spaces = "  "*n
    return spaces + lines.replace("\n", "\n" + spaces)

def open_el(el_name: str, id:str=None, classes:str=None):
    id_str = '' if id is None else f" id='{id}'"
    cls_str = '' if classes is None else f" class='{classes}'"
    return f"<{el_name}{id_str}{cls_str}>"


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

    def div(body, id=None, classes=None):
        return f"{open_el('div', id, classes)}\n{indent(body, 2)}\n</div>"

    def oneline_div(body, id=None, classes=None):
        return f"{open_el('div', id, classes)}{body}</div>"

    oneline_div = lambda classes, text: f"<div class={classes}>{text}</div>"

    span = lambda classes, text: f"<span class={classes}>{text}</span>"

    hr = lambda: "<hr>"

    heading = lambda lvl, title: f"<h{lvl}> {title} </h{lvl}>"

    def unordered_list(list_items, id=None, classes=None):
        return f"{open_el('ul', id, classes)}\n{indent(list_items, 2)}\n</ul>"

    def ordered_list(list_items, id=None, classes=None):
        return f"{open_el('ol', id, classes)}\n{indent(list_items, 2)}\n</ol>"

    def list_item(text, id=None, classes=None):
        return f"{open_el('li', id, classes)}{text}</li>"

    def task_list_item(text, task_symb, is_checked):
        if is_checked:
            return f"<li data-task='{task_symb}' class='task-list-item is-checked'><input checked='' type='checkbox' class='task-list-item-checkbox'>{text}</li>"
        else:
            return f"<li data-task='{task_symb}' class='task-list-item'><input type='checkbox' class='task-list-item-checkbox'>{text}</li>"

    pre_code = lambda text: f"<pre><code>{text}</code></pre>"

    blockquote = lambda text: f"<blockquote>{text}</blockquote>"

    p = lambda text: \
f"""<p>
{indent(text, 2)}
</p>"""

    a = lambda text, addr: f"<a href=\"{addr}\">{text}</a>"

    bold = lambda text: f"<b>{text}</b>"

    italics = lambda text: f"<i>{text}</i>"

    code = lambda text: f"""<code>{text}</code>"""

    delete = lambda text: f"""<del>{text}</del>"""

    mark = lambda text: f"""<mark>{text}</mark>"""


