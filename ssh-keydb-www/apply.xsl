<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
    <link rel='StyleSheet' href="apply.css" type="text/css" />
</head>

<body>

<div id='header'>
    <p class='title'> 
        <a href='?page=main'>[H]</a>
        <a href='?page=main'> SSH-KEYDB </a> - 
        Generate and deploy authorized_keys files
    </p>
</div>

<div id='groups'>
    <form method='post' action='?page=apply'>
    <p class='title'> Groups: </p>
    <p>Select the role and server group to be processed. The authorized_keys files will then be generated for each server in the group and appropriate login, as defined by the permissions.</p>
    <table>
        <tr>
            <th> Group </th>
            <td> 
                <select name='group'>
                    <xsl:for-each select='/page/all_groups/servergroup'>
                        <option><xsl:value-of select='@name' /></option>
                    </xsl:for-each>
                </select>
            </td>
        </tr>
        <tr>
            <th> Role </th>
            <td>
                <select name='role'>
                    <xsl:for-each select='/page/all_roles/role'>
                        <option><xsl:value-of select='.' /></option>
                    </xsl:for-each>
                </select>
            </td>
        </tr>
    </table>
    <p> <input type='checkbox' name='push' value='push'/>Push the files on the servers</p>
    <p> <input type='submit' name='apply' value='Proceed'/> </p>
    </form>
</div>

<div>
    <strong>Warning:</strong> By default, authorized_keys files are only generated locally on the server. The push checkbox will in addition put the generated files on the appropriate servers.
</div>

<xsl:if test="count(/page/updated) > 0">
<div>
    <xsl:for-each select='/page/updated/item'>
        <xsl:if test="/page/pushed">
            <p> Pushed <xsl:value-of select='.' /> </p>
        </xsl:if>
        <xsl:if test="not(/page/pushed)">
            <p> Updated <xsl:value-of select='.' /> </p>
        </xsl:if>
    </xsl:for-each>
</div>
</xsl:if>

</body>

</html>
