<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
    <link rel='StyleSheet' href="users.css" type="text/css" />
</head>

<form action='?page=users' method='POST'>

<div id='filter'>
    <xsl:variable name="location" select="normalize-space(/page/location)"/>
    <xsl:variable name="section" select="normalize-space(/page/section)"/>

    <xsl:if test="$location != 'None'">
        <span class='set'>
            Filter set on the location <xsl:value-of select="$location" />
            <a href='?page=users'> [Reset] </a>
        </span>
    </xsl:if>

    <xsl:if test="$section != 'None'">
        <span class='set'>
            Filter set on the section <xsl:value-of select="$section" />
            <a href='?page=users'> [Reset] </a>
        </span>
    </xsl:if>

    <xsl:if test="($section = 'None') and ($location = 'None')">
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
        <th> Section </th>
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
                <a>
                    <xsl:attribute name='href'> index.py?page=users&amp;section=<xsl:value-of select='@section' /> </xsl:attribute>
                    <xsl:value-of select='@section' /> 
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
    <tr>
        <th> Section: </th>
        <td> <input name='addsection' type='text' /> </td>
    </tr>
</table>
<input type='submit' name='submit' value='Add' />

</form>

</html>

