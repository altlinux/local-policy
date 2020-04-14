%define _unpackaged_files_terminate_build 1

Name: local-policy
Version: 0.2.0
Release: alt1

Summary: ALT Local policies
License: GPLv2+
Group: Other
Url: http://git.altlinux.org/people/sin/packages/local-policy.git

BuildArch: noarch

Requires: control

Source0: %name-%version.tar

%description
Local policies for ALT solutions based on Sisyphus
includes additional control facilities and default policies
templates in PReg format converted to XML.

%prep
%setup -q

%install
for i in sshd-gssapi-auth \
         sshd-allow-groups-list \
         ssh-gssapi-auth \
         ldap-reverse-dns-lookup \
         ldap-tls-cert-check
do
        install -pD -m755 "controls/$i" \
                "%buildroot%_sysconfdir/control.d/facilities/$i"
done

mkdir -p "%buildroot%_datadir/%name"
cp -r policies/* "%buildroot%_datadir/%name"
ln -s "%_datadir/%name/server" "%buildroot%_datadir/%name/default"

%pre
%_sbindir/groupadd -r -f remote 2> /dev/null ||:

%files
%_sysconfdir/control.d/facilities/*
%_datadir/%name/*

%changelog
* Mon Apr 13 2020 Igor Chudov <nir@altlinux.org> 0.2.0-alt1
- Multiple policy templates introduced

* Wed Feb 12 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.1.0-alt3
- Update project URL

* Fri Feb 07 2020 Ivan Savin <iv17@altlinux.org> 0.1.0-alt2
- Add gpupdate to local.xml

* Thu Nov 28 2019 Evgeny Sinelnikov <sin@altlinux.org> 0.1.0-alt1
- Add default policies templates in PReg format converted to XML
- Change license to GPLv2+

* Fri Nov 08 2019 Evgeny Sinelnikov <sin@altlinux.org> 0.0.5-alt1
- sshd-allow-groups-list added
- sshd-gssapi-auth: remove kill -HUP from control
- create group "remote" for sshd allow groups list policy

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

