<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
    <link rel='StyleSheet' href="hostkey.css" type="text/css" />
</head>

<body>

<div id='header'>
    <p class='title'> 
        <a href='?page=main'>[H]</a> SSH-KEYDB - Retrieve host keys
    </p>
</div>

<div id='groups'>
    <form method='post' action='?page=hostkey'>
    <p class='title'> Server: </p>
    <table>
        <tr>
            <th> Server </th>
            <td> 
                <select name='server'>
                    <xsl:for-each select='/page/all_servers/server'>
                        <option><xsl:value-of select='@name' /></option>
                    </xsl:for-each>
                </select>
            </td>
        </tr>
    </table>
    <p> <input type='submit' name='hostkey_pull' value='Get'/>
    <input type='submit' name='hostkey_push' value='Set'/> </p>
    </form>
</div>

<xsl:if test="count(errors) > 0"> 
    <div id='errors'>
    <xsl:for-each select="errors">
        <p> <xsl:value-of select='.' /> </p>
    </xsl:for-each>
    </div>
</xsl:if>

<xsl:if test="count(updated) > 0"> 
    <div id='updated'>
    <xsl:for-each select="updated">
        <p> Updated <xsl:value-of select='.' /> </p>
    </xsl:for-each>
    </div>
</xsl:if>

</body>

</html>
