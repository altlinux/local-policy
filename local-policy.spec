%define _unpackages_files_terminate_build 1

Name: local-policy
Version: 0.0.4
Release: alt1

Summary: Local policies
License: MIT
Group: Other
Url: http://git.altlinux.org

BuildArch: noarch

Requires: control

Source0: %name-%version.tar

%description
Local policies

%prep
%setup -q

%install
install -pD -m755 controls/sshd-gssapi-auth \
	%buildroot%_sysconfdir/control.d/facilities/sshd-gssapi-auth
install -pD -m755 controls/ssh-gssapi-auth \
	%buildroot%_sysconfdir/control.d/facilities/ssh-gssapi-auth
install -pD -m755 controls/ldap-reverse-dns-lookup \
	%buildroot%_sysconfdir/control.d/facilities/ldap-reverse-dns-lookup
install -pD -m755 controls/ldap-tls-cert-check \
	%buildroot%_sysconfdir/control.d/facilities/ldap-tls-cert-check

%files
%_sysconfdir/control.d/facilities/sshd-gssapi-auth
%_sysconfdir/control.d/facilities/ssh-gssapi-auth
%_sysconfdir/control.d/facilities/ldap-reverse-dns-lookup
%_sysconfdir/control.d/facilities/ldap-tls-cert-check

%changelog
* Mon Oct 14 2019 Igor Chudov <nir@altlinux.org> 0.0.4-alt1
- ssh-gssapi-auth added
- Package made architecture-independent
- sshd-allow-gssapi renamed to sshd-gssapi-auth

* Thu Oct 10 2019 Igor Chudov <nir@altlinux.org> 0.0.3-alt1
- ldap-tls-cert-check control for 'tls_reqcert' option
- Build fixes

* Wed Oct 09 2019 Igor Chudov <nir@altlinux.org> 0.0.2-alt1
- ldap-reverse-dns-lookup control for 'sasl_nocanon' option of OpenLDAP

* Tue Sep 17 2019 Igor Chudov <nir@altlinux.org> 0.0.1-alt1
- Initial release with `sshd-allow-gssapi` script

