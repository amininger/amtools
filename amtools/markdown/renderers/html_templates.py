
def indent(lines, n=1):
    spaces = "  "*n
    return spaces + lines.replace("\n", "\n" + spaces)

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
        id_str = '' if id is None else f"id='{id}'"
        cls_str = '' if classes is None else f"class='{classes}'"
        return \
f"""<div {id_str} {cls_str} >
{indent(body, 2)}
</div>"""

    code = lambda text: f"<pre><code>{text}</code></pre>"


    oneline_div = lambda classes, text: f"<div class={classes}>{text}</div>"

    span = lambda classes, text: f"<span class={classes}>{text}</span>"

    hr = lambda: "<hr>"

    heading = lambda lvl, title: f"<h{lvl}> {title} </h{lvl}>"

    unordered_list = lambda list_items: \
f"""<ul>
{indent(list_items, 2)}
</ul>"""

    ordered_list = lambda list_items: \
f"""<ol>
{indent(list_items, 2)}
</ol>"""

    list_item = lambda text: f"<li>{text}</li>"

    p = lambda text: \
f"""<p>
{indent(text, 2)}
</p>"""

    bold = lambda text: f"<b>{text}</b>"

    italics = lambda text: f"<i>{text}</i>"

    inline_code = lambda text: f"""<span class="inline-code">{text}</span>"""

    a = lambda text, addr: f"<a href=\"{addr}\">{text}</a>"

