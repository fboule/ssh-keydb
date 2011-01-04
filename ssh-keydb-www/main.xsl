<?xml version="1.0" encoding="ISO-8859-1"?>
<html xsl:version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:lxslt="http://xml.apache.org/xslt"
    xmlns="http://www.w3.org/1999/xhtml">

<head>
    <link rel='StyleSheet' href="basics.css" type="text/css" />
</head>

<body>
    <div id='header'>
        <p class='title'> 
            <a href='?page=main'>[H]</a> SSH-KEYDB
        </p>
    </div>

    <table>
        <tr>
            <td>
                <div>
                    <p>
                        <strong>ssh-keydb</strong> is a database to store users OpenSSH public keys as well as servers host keys. 
                        Its purpose is to ease the management of the authorized_keys for clouds of servers. It allows you to
                        provide groups of users (with the same role) access to any account/server pair.
                    </p>

                    <p class='step'> The first step to setup the system is to define the roles, groups of servers and permissions. </p>
                    <p>
                        Let's shortly summarize the concepts:
                        <ul>
                            <li><strong>Role:</strong> It is used to define groups of users. A role has a specific set of rights down to the account level.</li>
                            <li><strong>Group (of servers):</strong> Users can have a different role depending on which group they are connecting.</li>
                            <li><strong>Permission:</strong> This is what binds a role, login, server and location. To each permission can be associated a command
                            for the user to access something else than a shell (e.g. svnserve for a Subversion service). Arguments placeholders can be used
                            to substitute per-user settings (e.g. %(login)s, see users management below for more information on providing the argument value)</li>
                            <li><strong>Location:</strong> Because users with the same role on a group may need to access an account differently.
                            It allows to subdivide group of users by location (i.e. Europe, USA, etc.).</li>
                        </ul>
                    </p>

                    <p class='step'> Let the feast begin... </p>
                    <p>
                        Now we can start managing the users:
                        <ul>
                            <li><em>Add a user</em> by simply providing a (unique) name and a location. The section field is optional.</li>
                            <li>Display the user's page to <em>modify his/her profile.</em></li>
                            <li>A user can have <em>several public keys</em>. Note that the comment part of the key (last part) is used to 
                            identify the key. Make sure to provide a relevant identifier. It is recommended to have only one key per
                            user, identified with the user's login.</li>
                            <li>Grant the user's <em>memberships</em>. It tells the role of the user for a group when he/she uses 
                            a specific public key. Multiple roles can be given a user provided he/she uses a different public key.</li>
                        </ul>
                    </p>

                    <p class='step'> Pushing the keys </p>
                    <p>
                        The last step in the workflow is to generate the authorized_keys file. It is done by providing the role and group.
                        The files are generated on the web server in the keys subfolder.
                    </p>
                    <p>
                        The filename pattern is: 
                        <p class='quote'><tt>new_&lt;login&gt;_&lt;server&gt;</tt></p>
                    </p>
                    <p>
                        Allowing to push the files on the servers has implications. The idea is to copy each generated file on the targeted
                        account and server in the $HOME/.ssh subfolder. File ACL is also checked (644 is required, or sshd will complain).
                        Now to proceed with it, to tool accesses the root account of the server. You therefore need to (manually) setup 
                        the authorized_keys file of the root account with the webtool's public key.
                    </p>

                    <p class='step'> Hostkeys </p>
                    <p>
                        SSH stores the hostkeys' public key in the known_hosts file. Upon server reinstallation/replacement, two approaches 
                        are possible: either to update all the known_hosts files with the new public key or to restore the hostkeys. You know
                        what? ssh-keydb manages it too.
                    </p>
                    <p>
                        It is quite simplistic for the time being though: select the server (no group management... yet?) and select either
                        Get or Set.
                    </p>
                </div>
                <div class='footer'>
                    04-Jan-2011 - fboule
                </div>
            </td>
            <td>
                <div>
                    <xsl:for-each select='page/menu/item'>
                        <a>
                            <xsl:attribute name='href'>index.py?page=<xsl:value-of select='@name' /> </xsl:attribute>
                            <xsl:attribute name='class'>menu</xsl:attribute>
                            <xsl:attribute name='alt'><xsl:value-of select='.' /></xsl:attribute>
                            <xsl:attribute name='style'>
                                <xsl:text>background-image: url(img/</xsl:text>
                                <xsl:value-of select='@name' />
                                <xsl:text>.gif);</xsl:text>
                            </xsl:attribute>
                        </a> <br />
                    </xsl:for-each>
                </div>
            </td>
        </tr>
    </table>
</body>

</html>
