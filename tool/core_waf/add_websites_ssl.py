import sys

f = open("/etc/apache2/sites-available/"+sys.argv[1]+"-ssl.conf", "wb")
content = """
<VirtualHost *:443>
        ServerName """+ sys.argv[1] +"""
        ServerAlias """+ sys.argv[1] +"""
        AddDefaultCharset UTF-8

        <IfModule mod_security2.c>
                Include /opt/modsecurity/etc/group/group_websites_waf_"""+ sys.argv[2] +""".conf
        </IfModule>

        SSLEngine on
        SSLProxyEngine On
        SSLProxyCheckPeerCN Off
        SSLProxyCheckPeerName Off
        SSLCertificateFile /etc/ssl/certs/"""+ sys.argv[1] +""".pem
        SSLCertificateKeyFile /etc/ssl/private/"""+ sys.argv[1] +""".key

        ProxyPass / https://"""+ sys.argv[1] +""":"""+ sys.argv[4] +"""/
        ErrorLog ${APACHE_LOG_DIR}/error_"""+sys.argv[1]+""".log
        CustomLog ${APACHE_LOG_DIR}/access_"""+sys.argv[1]+""".log combined
        ProxyErrorOverride On


# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
</VirtualHost>
"""
f.write(content)
f.close()