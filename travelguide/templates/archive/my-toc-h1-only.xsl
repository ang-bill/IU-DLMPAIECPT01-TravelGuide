<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="/">
    <html>
      <head>
        <title>Table of Contents</title>
        <style type="text/css">
          body { font-family: sans-serif; }
          h1 { text-align: center; }
          .toc-level-1 { margin-left: 0em; }
        </style>
      </head>
      <body>
        <h1>Table of Contents</h1>
        <xsl:apply-templates select="//outline[@level=1]" />
      </body>
    </html>
  </xsl:template>

  <xsl:template match="outline">
    <div class="toc-level-{level}">
      <a href="{@link}"><xsl:value-of select="@title"/></a>
    </div>
  </xsl:template>

</xsl:stylesheet>
