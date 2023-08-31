from re import findall
from sys import argv
if len(argv) == 2:

    with open(argv[1], 'r') as fp:

        document= fp.read()

        commentary = "##.*"
        tutorial   = ".+(?=##)"    #.+(?= \/\/)

        commentaries = findall(commentary, document)
        tutorials = findall(tutorial, document)

        if len(commentaries) != len(tutorials):
            print("Error: commentaries and tutorials aren't the same length!")
            exit(1)


        #Now commentaries can be retrieved from a list, let's remove them from the document's body
        for x in commentaries:
            if x != "":
                document=document.replace(x, "")

        #Let's trim it a bit!
        # trimmed = ""
        # for z in document.split("\n"):
        #     trimmed += f"{z.strip()}\n"

        # document = trimmed

        for i, tuto in enumerate(tutorials):
            if tuto != "" and commentaries[i] != "":
                document=document.replace(tuto, f"""<span data-toggle="popover" title="hint" data-content="{commentaries[i].replace('##', '')}">{tuto.strip()}</span>""")


        # for y in tutorials:
        #     if y != "": #prevent what seems as an infinite loop!
        #         # document=document.replace(y, f"<h2>{y}</h2>")
        #         document=document.replace(y, f"<h2>{y}</h2>")

        # for x in commentaries:
        #     if x != "":
        #         # document=document.replace(x, f"<h1>{x.replace('##', '')}</h1>")
        #         document=document.replace(x, f"<h1>{x.replace('##', '')}</h1>")
        """
          <span  data-toggle="popover" title="Popover Header" data-content="Some content inside the popover">Toggle popover</span>
        """


        bootstrap = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
"""

        css = """<style>
  /* Popover */
  .popover {
    border: 2px dotted red;
  }
  /* Popover Header */
  .popover-title {
    background-color: #73AD21;
    color: #FFFFFF;
    font-size: 28px;
    text-align:center;
  }
  /* Popover Body */
  .popover-content {
    background-color: coral;
    color: #FFFFFF;
    padding: 25px;
  }
  /* Popover Arrow */
  .arrow {
    border-right-color: red !important;
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
        <body><pre><code>
{document}
            </code></pre>
            {JS}
        </body>
        </html>
        """

        print(template)
        # print(len(tutorials), len(commentaries))
