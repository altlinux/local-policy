%define _unpackages_files_terminate_build 1

Name: local-policy
Version: 0.0.1
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

%files
%_sysconfdir/control.d/facilities/sshd-allow-gssapi

%changelog
* Tue Sep 17 2019 Igor Chudov <nir@altlinux.org> 0.0.1-alt1
- Initial release with `sshd-allow-gssapi` script

