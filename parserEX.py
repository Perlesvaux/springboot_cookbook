from re import findall
from sys import argv

"""
Custom markup mappings:

@java ...        @javaq -> encircles java-code
@python ...      @pythonq -> encircles python-code
@js ...          @jsq -> encircles java-code
@bash ...        @bashq -> encircles bash-code
@markup ...      @markupq -> encircles css/html/xml code
      --and so on--

@# ...           @#q -> encircles h2
@a ...           @aq -> encircles links
@href ...        @hrefq -> encircles link references
"""


def format_code(dump, lang):
    for item in lang.matches:
        txt=item.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        dump=dump.replace(item, lang.template.format(txt=txt, language=lang.language))
    return dump.replace(f"@{lang.language}q", "").replace(f"@{lang.language}", "")


def add_link(dump, link):
    for i, val in enumerate(link.a_matches):
        dump=dump.replace(link.href_matches[i], "")
        dump=dump.replace(val, link.template.format(a=val.strip("@a "), href=link.href_matches[i]))
    return dump.replace("@aq", "").replace("@a", "").replace("@hrefq", "").replace("@href", "")


class lang:
    def __init__(self, doc, language, template="""<pre><code class="language-{language}">{txt}</code></pre>"""):
        self.language = language
        self.rgx = """@{language}\\b([\s\S]*?)@{language}q\\b""".format(language=language)
        self.matches = findall(self.rgx, doc)
        self.template = template


class link:
    def __init__(self, doc, template="""<a href="{href}">{a}</a>"""):
        self.a = """@a\\b.*@aq\\b"""
        self.href = """@href\\b([\s\S]*?)@hrefq\\b"""
        self.a_matches = findall(self.a, doc)
        self.href_matches = findall(self.href, doc)
        self.template = template


if len(argv) == 2:

    with open(argv[1], 'r') as fp:

        document= fp.read()

        #Mapping custom markup '#' to h2
        h2 = lang(document, "#", """<h2>{txt}</h2>""")
        document = format_code(document, h2)


        #Mapping links to their respective href's
        links = link(document)
        document = add_link(document, links)

        #Mapping each code snippet to its lang-specific css
        all_languages = ["java", "bash", "markup", "python", "css", "js", "csharp", "sql", "json", "php"]
        for each in all_languages:
            document = format_code(document, lang(document, each))


        bootstrap = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link href="prism.css" rel="stylesheet" />
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
    color: BurlyWood;
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
  	    <script src="prism.js"></script>
        </body>
        </html>
        """

        print(template)
        # print(links.a_matches)
        # print(links.href_matches)
