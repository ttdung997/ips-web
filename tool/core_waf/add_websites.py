import sys

f = open("/etc/apache2/sites-available/"+sys.argv[1]+".conf", "wb")
content = """
<VirtualHost *:80>
        ServerName """+ sys.argv[1] +"""
        ServerAlias """+ sys.argv[1] +"""
        AddDefaultCharset UTF-8

        <IfModule mod_security2.c>
                Include /opt/modsecurity/etc/group/group_websites_waf_"""+ sys.argv[2] +""".conf
        </IfModule>


        ProxyPass / http://"""+ sys.argv[1] +""":"""+ sys.argv[4] +"""/
        ErrorLog ${APACHE_LOG_DIR}/error_"""+sys.argv[1]+""".log
        CustomLog ${APACHE_LOG_DIR}/access_"""+sys.argv[1]+""".log combined
        ProxyErrorOverride On


# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
</VirtualHost>
"""
f.write(content)
f.close()

