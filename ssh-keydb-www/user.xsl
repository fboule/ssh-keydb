<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
    <link rel='StyleSheet' href="user.css" type="text/css" />
</head>

<body>

<div id='user'>
    <p class='title'> 
        <a href='?page=users'> [U] </a>
        <a href='?page=main'> SSH-KEYDB </a> - 
        <a>
            <xsl:attribute name='href'>?page=user&amp;user=<xsl:value-of select='/page/user'/></xsl:attribute>
            <xsl:value-of select='/page/user' />/<xsl:value-of select='/page/user/@location' />
            <xsl:if test="/page/user/@section != ''"> (<xsl:value-of select='/page/user/@section' />)</xsl:if> 
        </a>
    </p>
</div>

<xsl:if test="count(errors) > 0"> 
    <div id='errors'>
    <xsl:for-each select="errors">
        <p> Membership still refers to key: <xsl:value-of select='.' /> </p>
    </xsl:for-each>
    </div>
</xsl:if>

<div id='keys'>
    <form method='post'>
    <xsl:attribute name='action'>?page=user&amp;user=<xsl:value-of select='/page/user' /></xsl:attribute>
        <p class='title'> Keys: </p>
        <table>
            <tr> 
                <th> - </th>
                <th> Id </th>
                <th> Key </th>
            </tr>
            <xsl:for-each select='/page/keys/key'>
            <tr> 
                <td> 
                    <input type='submit' value='-'> 
                        <xsl:attribute name='name'>del_key_<xsl:value-of select='name' /></xsl:attribute>
                    </input>
                </td>
                <td> <xsl:value-of select='name' /> </td>
                <td> <xsl:value-of select='public' /> </td>
            </tr>
            </xsl:for-each>
            <tr>
                <td> <input type='submit' name='add_key' value='+'/> </td>
                <td> - </td>
                <td> <input size='80' type='text' name='keystring'/> </td>
            </tr>
        </table>

    </form>
</div>

<div id='memberships'>
    <form method='post'>
    <xsl:attribute name='action'>?page=user&amp;user=<xsl:value-of select='/page/user' /></xsl:attribute>
        <p class='title'> Memberships: </p>
        <table>
            <tr>
                <th> - </th>
                <th>Group</th>
                <th>Role</th>
                <th>Key</th>
                <th>Args</th>
            </tr>
            <xsl:for-each select='/page/memberships/membership'>
                <tr>
                    <td> 
                        <input type='submit' value='-'> 
                            <xsl:attribute name='name'>del_membership_<xsl:value-of select='servergroup/@name' />_<xsl:value-of select='role' />_<xsl:value-of select='key/name' /> </xsl:attribute>
                        </input>
                    </td>
                    <td> <xsl:value-of select='servergroup/@name' /> </td>
                    <td> <xsl:value-of select='role' /> </td>
                    <td> <xsl:value-of select='key/name' /> </td>
                    <td> <xsl:value-of select='args' />  </td>
                </tr>
            </xsl:for-each>
            <tr>
                <td> <input type='submit' name='add_membership' value='+'/> </td>
                <td>
                    <select name='group'>
                        <xsl:for-each select='/page/all_groups/servergroup'>
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
                <td>
                    <select name='key'>
                        <xsl:for-each select='/page/all_keys/key'>
                            <option><xsl:value-of select='name' /></option>
                        </xsl:for-each>
                    </select>
                </td>
                <td> <input size='40' type='text' name='args'/> </td>
            </tr>
        </table>
    </form>
</div>

<div id='groups'>
    <p class='title'> Groups: </p>
    <table>
        <tr>
            <th> Group </th>
            <th> Servers </th>
        </tr>
        <xsl:for-each select='/page/groups/servergroup'>
        <tr>
            <td> <xsl:value-of select='@name' /> </td>
            <td> 
                <xsl:for-each select='server'>
                    <xsl:value-of select='@name' /><xsl:value-of select="string(' ')"/>
                </xsl:for-each>
            </td>
        </tr>
        </xsl:for-each>
    </table>
</div>

<div id='permissions'>
    <p class='title'> Permissions: </p>
    <table>
        <tr>
            <th> Server </th>
            <th> Role </th>
            <th> Login </th>
            <th> Location </th>
            <th> Command </th>
        </tr>
        <xsl:for-each select='/page/permissions/permission'>
        <tr>
            <td> <xsl:value-of select='server/@name' /> </td>
            <td> <xsl:value-of select='role' /> </td>
            <td> <xsl:value-of select='login' /> </td>
            <td> <xsl:value-of select='location' /> </td>
            <td> <xsl:value-of select='command' /> </td>
        </tr>
        </xsl:for-each>
    </table>
</div>

</body>

</html>
