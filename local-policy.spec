%define _unpackages_files_terminate_build 1

Name: local-policy
Version: 0.0.3
Release: alt1

Summary: Local policies
License: MIT
Group: Other
Url: http://git.altlinux.org

Requires: control

Source0: %name-%version.tar

%description
Local policies

%prep
%setup -q

%install
install -pD -m755 controls/sshd-allow-gssapi \
	%buildroot%_sysconfdir/control.d/facilities/sshd-allow-gssapi
install -pD -m755 controls/ldap-reverse-dns-lookup \
	%buildroot%_sysconfdir/control.d/facilities/ldap-reverse-dns-lookup
install -pD -m755 controls/ldap-tls-cert-check \
	%buildroot%_sysconfdir/control.d/facilities/ldap-tls-cert-check

%files
%_sysconfdir/control.d/facilities/sshd-allow-gssapi
%_sysconfdir/control.d/facilities/ldap-reverse-dns-lookup
%_sysconfdir/control.d/facilities/ldap-tls-cert-check

%changelog
* Thu Oct 10 2019 Igor Chudov <nir@altlinux.org> 0.0.3-alt1
- ldap-tls-cert-check control for 'tls_reqcert' option
- Build fixes

* Wed Oct 09 2019 Igor Chudov <nir@altlinux.org> 0.0.2-alt1
- ldap-reverse-dns-lookup control for 'sasl_nocanon' option of OpenLDAP

* Tue Sep 17 2019 Igor Chudov <nir@altlinux.org> 0.0.1-alt1
- Initial release with `sshd-allow-gssapi` script

