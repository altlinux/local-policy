%define _unpackaged_files_terminate_build 1

Name: local-policy
Version: 0.6.3
Release: alt1

Summary: ALT Local Policies Default templates
License: GPLv2+
Group: Other
Url: http://git.altlinux.org/gears/l/local-policy.git

BuildArch: noarch

Requires: control
Requires: control-sshd-permit-root-login

Source0: %name-%version.tar

# https://bugzilla.altlinux.org/45002 :
%filter_from_requires /xmlbeans-scripts/d

%description
Local policies for ALT solutions based on Sisyphus
includes additional control facilities and default policies
templates in PReg format converted to XML.

%prep
%setup -q

%install
for i in sshd-gssapi-auth \
         sshd-allow-groups-list \
         sshd-permit-empty-passwords \
         sshd-x11-forwarding \
         ssh-gssapi-auth \
         krb5-conf-ccache \
         ldap-reverse-dns-lookup \
         ldap-tls-cert-check \
         local-policy-system-access \
         sssd-ad-gpo-access-control \
         sssd-ad-gpo-ignore-unreadable \
         sssd-ad-update-machine-password \
         sssd-cache-credentials \
         sssd-drop-privileges \
         sssd-dyndns-update \
         sssd-dyndns-update-ptr \
         sssd-dyndns-refresh-interval \
         sssd-dyndns-ttl \
         autofs-browse-mode \
         smb-conf-idmap-backend \
         smb-conf-idmap-range \
         smb-conf-machine-password-timeout \
         oddjob-gpupdate-dbus-timeout
do
        install -pD -m755 "controls/$i" \
                "%buildroot%_sysconfdir/control.d/facilities/$i"
done

install -pD -m755 "controls/functions-local-policy" \
        "%buildroot%_sysconfdir/control.d/"

mkdir -p "%buildroot%_datadir/%name"
cp -r policies/* "%buildroot%_datadir/%name"
mkdir -p "%buildroot%_sysconfdir/%name"
mkdir -p "%buildroot%_sysconfdir/%name-system"

%pre
%_sbindir/groupadd -r -f remote 2> /dev/null ||:
%pre_control local-policy-system-access
if [ ! -f "/var/run/control/local-policy-system-access" ]; then
    [ ! -d "/var/run/control" ] ||
        echo restricted > "/var/run/control/local-policy-system-access"
fi

%post
%post_control -s restricted local-policy-system-access

%files
%dir %attr(0700, root, root) %_sysconfdir/%name-system
%dir %_sysconfdir/%name
%_sysconfdir/control.d/facilities/*
%_sysconfdir/control.d/functions-local-policy
%dir %_datadir/%name
%_datadir/%name/*

%changelog
* Thu Feb 29 2024 Evgeny Sinelnikov <sin@altlinux.org> 0.6.3-alt1
- Improve oddjob-gpupdate-dbus-timeout control.
- Initial support build for debian.

* Wed Jan 24 2024 Andrey Limachko <liannnix@altlinux.org> 0.6.2-alt1
- Add oddjob-gpupdate-dbus-timeout control

* Wed Dec 13 2023 Evgeny Sinelnikov <sin@altlinux.org> 0.6.1-alt1
- Fix krb5-conf-ccache control:
 * Incorrect file presence check when option not found has been fixed.
 * Avoid grep warning with 'stray \ before /' pattern (ALT#47648).

* Mon Jan 23 2023 Ivan A. Melnikov <iv@altlinux.org> 0.6.0-alt1.1
- NMU: ensure this package doesn't require
  xmlbeans-scripts (ALT#45002).

* Fri Aug 26 2022 Evgeny Sinelnikov <sin@altlinux.org> 0.6.0-alt1
- New directory /etc/local-policy-system with Local Group Policy Template (GPT)
- Add control local-policy-system-access

* Mon Jul 04 2022 Ivan Savin <svn17@altlinux.org> 0.5.1-alt1
- Add control smb-conf-machine-password-timeout
- Add control sssd-ad-update-machine-password

* Tue Sep 14 2021 Evgeny Sinelnikov <sin@altlinux.org> 0.5.0-alt1
- Adjust local policy templates
- Add control system-policy for gpupdate

* Fri Mar 05 2021 Evgeny Sinelnikov <sin@altlinux.org> 0.4.8-alt1
- Add sssd-drop-privileges control
- Fix sssd-ad-gpo-access-control with more appropriate designations

* Fri Jan 29 2021 Evgeny Sinelnikov <sin@altlinux.org> 0.4.7-alt1
- Add sssd-dyndns-{update,update-ptr,refresh-interval,ttl} controls

* Mon Oct 05 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.6-alt1
- Fix control_subst_with_file_check regression and improve default
  variants of controls facilities use it

* Wed Sep 30 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.5-alt1
- Revert winbind service enabling by default on server and workstation
  due it depends on samba configuration and could be unconsistent
- Add smb-conf-idmap-backend and smb-conf-idmap-range controls

* Sat Sep 12 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.4-alt2
- Add requires to control with OpenSSH server PermitRootLogin configuration

* Sat Sep 12 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.4-alt1
- Add winbind service enabled by default on server and workstation

* Sun Sep 06 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.3-alt1
- Fixed controls in case appropriate configs are missing
- Add check default sssd-ad options and create it if not exists

* Sat Jul 04 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.2-alt1
- Add sssd-ad-gpo-access-control control

* Wed Jul 01 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.1-alt1
- Add sssd-cache-credentials control
- Update sssd-ad-gpo-ignore-unreadable control

* Wed Jul 01 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.4.0-alt1
- Add autofs-browse-mode and sssd-ad-gpo-ignore-unreadable controls
- Open SSH port by default for all templates

* Tue Apr 21 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.3.0-alt1
- Replace machine local Registry policy in Samba backup format
- krb5-conf-ccache control added for Kerberos client default credential cache:
 + keyring: Keyring persistent cache stored in unswappable kernel memory
 + tmpfile: Traditional, simplest and most portable cache stored in temporary file
 + rundir: Directory cache stored in run-time variable data
 + kcm: Kerberos credential manager (requires service like sssd-kcm)
 + default: Default credential cache (usualy same as temporary file)
- Add ad-domain-controller policy template

* Thu Apr 16 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.2.0-alt4
- Add empty default local-policy

* Thu Apr 16 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.2.0-alt3
- Add local-policy sysconfig directory to package

* Thu Apr 16 2020 Evgeny Sinelnikov <sin@altlinux.org> 0.2.0-alt2
- Add data directory to package
- Remove default symlink (it is a bad idea to pack it due rpm limitations)

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

