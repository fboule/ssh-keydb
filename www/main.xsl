<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
</head>

<body>
    <div id='header'>
        <p class='title'> 
            <a href='?page=main'>[H]</a> SSH-KEYDB
        </p>
    </div>

    <div>
        <xsl:for-each select='page/menu/item'>
            <a>
                <xsl:attribute name='href'> index.py?page=<xsl:value-of select='@name' /> </xsl:attribute>
                <xsl:value-of select='.' />
            </a> <br />
        </xsl:for-each>
    </div>

</body>

</html>
