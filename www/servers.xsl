<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
    <link rel='StyleSheet' href="servers.css" type="text/css" />
</head>

<body>

<div id='header'>
    <p class='title'> 
        <a href='?page=main'>[H]</a>
        SSH-KEYDB - Servers
    </p>
</div>

<div id='groups'>
    <form method='post' action='?page=servers'>
    <p class='title'> Groups: </p>
    <table>
        <tr>
            <th> Group </th>
            <th> Servers </th>
            <th> - </th>
        </tr>
        <xsl:for-each select='/page/all_groups/servergroup'>
        <tr>
            <td> <xsl:value-of select='@name' /> </td>
            <td> 
                <xsl:for-each select='server'>
                    <xsl:value-of select='@name' /><xsl:value-of select="string(' ')"/>
                </xsl:for-each>
            </td>
            <td> 
                <input type='submit' value='-'> 
                    <xsl:attribute name='name'>del_group_<xsl:value-of select='@name' /></xsl:attribute>
                </input>
            </td>
        </tr>
        </xsl:for-each>
        <tr>
            <td> <input size='40' type='text' name='group'/> </td>
            <td> <input size='80' type='text' name='servers' /> </td>
            <td> <input type='submit' name='add_group' value='+'/> </td>
        </tr>
    </table>
    </form>
</div>

<div id='roles'>
    <form method='post' action='?page=servers'>
    <p class='title'> Roles: </p>
    <table>
        <tr>
            <th> Role </th>
            <th> - </th>
        </tr>
        <xsl:for-each select='/page/all_roles/role'>
        <tr>
            <td> <xsl:value-of select='.' /> </td>
            <td>
                <input type='submit' value='-'> 
                    <xsl:attribute name='name'>del_role_<xsl:value-of select='.' /></xsl:attribute>
                </input>
            </td>
        </tr>
        </xsl:for-each>
        <tr>
            <td> <input size='40' type='text' name='role'/> </td>
            <td> <input type='submit' name='add_role' value='+'/> </td>
        </tr>
    </table>
    </form>
</div>

<div id='permissions'>
    <form method='post' action='?page=servers'>
    <p class='title'> Permissions: </p>
    <table>
        <tr>
            <th> Server </th>
            <th> Role </th>
            <th> Login </th>
            <th> Location </th>
            <th> Command </th>
            <th> - </th>
        </tr>
        <xsl:for-each select='/page/all_permissions/permission'>
        <tr>
                <td> <xsl:value-of select='server/@name' /> </td>
                <td> <xsl:value-of select='role' /> </td>
                <td> <xsl:value-of select='login' /> </td>
                <td> <xsl:value-of select='location' /> </td>
                <td> <xsl:value-of select='command' /> </td>
                <td> 
                    <input type='submit' value='-'>
                        <xsl:attribute name='name'>del_perm_<xsl:value-of select='login' />_<xsl:value-of select='server/@name' />_<xsl:value-of select='role' />_<xsl:value-of select='location' /></xsl:attribute>
                    </input>
                </td>
        </tr>
        </xsl:for-each>
        <tr>
            <td>
                <select name='server'>
                    <xsl:for-each select='/page/all_servers/server'>
                        <option><xsl:value-of select='@name' /></option>
                    </xsl:for-each>
                </select>
            </td>
            <td>
                <select name='role'>
                    <xsl:for-each select='/page/all_roles/role'>
                        <option><xsl:value-of select='.' /></option>
                    </xsl:for-each>
                </select>
            </td>
            <td> <input size='20' type='text' name='login' /> </td>
            <td>
                <select name='location'>
                    <xsl:for-each select='/page/all_locations/location'>
                        <option><xsl:value-of select='.' /></option>
                    </xsl:for-each>
                </select>
            </td>
            <td> <input size='100' type='text' name='command' /> </td>
            <td> <input type='submit' name='add_permission' value='+'/> </td>
        </tr>
    </table>
    </form>
</div>

</body>

</html>
