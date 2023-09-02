from re import findall
from sys import argv
if len(argv) == 2:

    with open(argv[1], 'r') as fp:

        document= fp.read()

        commentary = "##.*"
        tutorial   = ".+(?=##)"    #.+(?= \/\/)
        link       = "\bhttps?://\S+\b"
        javacode   = "\*\*\*.*\n"

        commentaries = findall(commentary, document)
        tutorials    = findall(tutorial, document)
        links        = findall(link, document)
        javacodes    = findall(javacode, document)

        if len(commentaries) != len(tutorials):
            print("Error: commentaries and tutorials aren't the same length!")
            exit(1)

        # document=document.replace("<", "&lt;")
        # document=document.replace(">", "&gt;")

        # document=document.replace("<", "LESSTHAN")
        # document=document.replace(">", "MORETHAN")

        #adding hyperlinks!
        for l in links:
            if l != "":
                document=document.replace(l, f"""<a href="{l}">{l}</a>""")

        """ <a href="https://www.w3schools.com">Visit W3Schools.com!</a> """

        #adding color to java-code!
        for j in javacodes:
            if j != "":
                document=document.replace(j, f"""<code class="javacode">{j.strip("***").replace("<", "&lt;").replace(">", "&gt;")}</code>""")


        #Now that commentaries can be retrieved from a list, let's remove them from the document's body
        for x in commentaries:
            if x != "":
                document=document.replace(x, "")


        for i, tuto in enumerate(tutorials):
            if tuto != "" and commentaries[i] != "":
                document=document.replace(tuto, f"""<span class="commented" data-toggle="popover"    data-content="{commentaries[i].replace('##', '')}">{tuto.strip()}</span>""")


        # document=document.replace("<", "&lt;")
        # document=document.replace(">", "&gt;")

        # document=document.replace("LESSTHAN", "&lt;")
        # document=document.replace("MORETHAN", "&gt;")
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
  span{
    color:#82b74b;
  }

  pre{
    color:#fff;
    background:#3e4444;
    white-space: pre-wrap;
  }

  .commented{
    width:fit-content;
    text-shadow: .1px .1px black;
  }

  .javacode{
    color: pink;

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
        <body><pre><code>
{document}
            </code></pre>
            {JS}
        </body>
        </html>
        """

        print(template)
        # print(len(tutorials), len(commentaries))
        # print(javacodes)
