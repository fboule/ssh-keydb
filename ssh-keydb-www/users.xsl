<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
    <link rel='StyleSheet' href="users.css" type="text/css" />
</head>

<body>
    <div id='header'>
        <p class='title'> 
            <a href='?page=main'>[H]</a>
            <a href='?page=main'> SSH-KEYDB </a> - 
            Edit users
        </p>
    </div>

    <form action='?page=users' method='POST'>
    
    <div id='filter'>
        <xsl:variable name="location" select="normalize-space(/page/location)"/>
    
        <xsl:if test="$location != 'None'">
            <span class='set'>
                Filter set on the location <xsl:value-of select="$location" />
                <a href='?page=users'> [Reset] </a>
            </span>
        </xsl:if>
    
        <xsl:if test="$location = 'None'">
            <span class='unset'>
                No filter set.
            </span>
        </xsl:if>
    </div>
    
    <div>
        <table>
        <tr>
            <th> Name </th>
            <th> Location </th>
            <th> Del. </th>
        </tr>
        <xsl:for-each select='/page/users/user'>
            <tr>
                <xsl:attribute name='class'> line<xsl:value-of select="position() mod 2"/> </xsl:attribute>
                <td>
                    <a>
                        <xsl:attribute name='href'> index.py?page=user&amp;user=<xsl:value-of select='.' /> </xsl:attribute>
                        <xsl:value-of select='.' /> 
                    </a>
                </td>
                <td> 
                    <a>
                        <xsl:attribute name='href'> index.py?page=users&amp;location=<xsl:value-of select='@location' /> </xsl:attribute>
                        <xsl:value-of select='@location' /> 
                    </a>
                </td>
                <td>
                    <input type='submit' 
                        value='-'>
                        <xsl:attribute name='name'>del_user_<xsl:value-of select="." />_<xsl:value-of select="@location" /></xsl:attribute>
                    </input>
                </td>
            </tr>
        </xsl:for-each>
        </table>
    </div>
    
    <table>
        <tr>
            <th> Name: </th>
            <td> <input name='addname' type='text' /> </td>
        </tr>
        <tr>
            <th> Location: </th>
            <td> 
                <select name='addlocation'> 
                    <xsl:for-each select='/page/all_locations/location'>
                        <option> <xsl:value-of select='.' /> </option>
                    </xsl:for-each>
                </select>
            </td>
        </tr>
    </table>
    <input type='submit' name='submit' value='Add' />
    
    </form>

</body>

</html>

