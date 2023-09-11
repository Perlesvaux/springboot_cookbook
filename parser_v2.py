from re import findall
from sys import argv

def format_code(dump, color, template=""):
    for item in color.matches:
        txt=item.strip(color.markup).replace("<", "&lt;").replace(">", "&gt;")
        dump=dump.replace(item, template.format(txt=txt, css=color.css))
    return dump


def add_popover(dump, text, comment, template=""):
    for i, val in enumerate(text.matches):
        pop=comment.matches[i].replace(comment.markup, "")
        txt=val.strip().replace(text.markup, "")
        dump=dump.replace(val, template.format(pop=pop, txt=txt))
    return dump


class color:
    def __init__(self, doc, rgx, markup="none", css=""):
        self.matches = findall(rgx, doc)
        self.markup  = markup
        self.css     = css


if len(argv) == 2:

    with open(argv[1], 'r') as fp:

        document= fp.read()

        code_tag_template    = """<code style="color:{css};">{txt}</code>"""
        comm_tag_template    = """<span class="commented" data-toggle="popover" data-content="{pop}">{txt}</span>"""
        link_tag_template    = """<a href="{pop}">{txt}</a>"""
        # link_tag_template    = """<h1>{pop}{txt}</h1>"""
        titl_tag_template    = """<h2>{txt}</h2>"""

        pink = color(document, "PNK\*\*\*.*\n", "PNK***", "pink")
        blue = color(document, "BLU\*\*\*.*\n", "BLU***", "lightskyblue")
        comm = color(document, "##.*"         , "##")
        tuto = color(document, ".+(?=##)")
        link = color(document, "###\*.+###\*"   , "###*")
        href = color(document, "\^\^\^.+\^\^\^"       , "^^^")
        titl = color(document, "\d+.*:")

        if len(comm.matches) != len(tuto.matches):
            print("Error: commentaries and tutorials aren't the same length!")
            exit(1)

        document = add_popover(document, link, href, link_tag_template)
        document = format_code(document, href)
        document = format_code(document, pink, code_tag_template)
        document = format_code(document, blue, code_tag_template)
        document = format_code(document, comm)
        document = add_popover(document, tuto, comm, comm_tag_template)
        document = format_code(document, titl, titl_tag_template)


        bootstrap = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
"""

        css = """<style>
body{
    background-color: #313636;
}
  span{
    color:#82b74b;
  }

  h2{
    color:olive;
  }

  pre{
    margin: 0 auto;
    width: fit-content;
    color:#fff;
    background:#252828;
    white-space: pre-wrap;
    border-style: none;
  }

  .commented{
    width:fit-content;
    text-shadow: .1px .1px black;
  }

  .commented:hover{
    background-color:#82b74b;
    color:black;
    cursor: help;
  }

  /* Popover */
  .popover {
    border: 2px inset white;
    border-radius: 25px;
  }
  /* Popover Header */
  .popover-title {
    background-color: #73AD21;
    color: #FFFFFF;
    font-size: 28px;
    text-align:center;
    border-radius: 25px;
  }
  /* Popover Body */
  .popover-content {
    color:#fff;
    background:#405d27;
    padding: 25px;
    width:fit-content;
    border-radius: 25px;
  }
  /* Popover Arrow */
  .arrow {
    border-right-color: white !important;
  }
  </style>"""

        JS = """<script>
$(document).ready(function(){
  $('[data-toggle="popover"]').popover();
});
</script>
  """
        template = f"""<!DOCTYPE html>
        <head>
           {bootstrap}
           {css}
           <title>{argv[1]}</title>
        </head>
        <body>
        <pre>
{document}
        </pre>
            {JS}
        </body>
        </html>
        """

        print(template)
        # print(link.matches)
        # print(href.matches)
        # print(len(tutorials), len(commentaries))
        # print(pnks)
