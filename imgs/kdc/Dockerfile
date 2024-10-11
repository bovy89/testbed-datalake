FROM almalinux:8

RUN yum install krb5-server krb5-libs krb5-workstation python3 -y

RUN rm -f /etc/krb5.conf /var/kerberos/krb5kdc/kdc.conf /var/kerberos/krb5kdc/kadm5.acl


EXPOSE 88

# entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
