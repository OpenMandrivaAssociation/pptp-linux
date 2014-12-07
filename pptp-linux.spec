%define name pptp-linux

Summary:	VPN client 
Name:		pptp-linux
Version:	1.8.0
Release:	4
License:	GPLv2+
Group:		Networking/Other
Url:		http://pptpclient.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pptpclient/pptp-%{version}.tar.gz
Source1:	pptp-command
Source2:	options.pptp
Source3:	pptp_fe.pl
Source4:	xpptp_fe.pl
Source5:	pptp.initd
Source6:	pptp-tmpfs.conf

Patch0:		pptp-1.7.2-pptpsetup-mppe.patch
Requires:	ppp >= 2.4.3
Conflicts:	pptp-adsl-alcatel
%rename		pptp-client

%description
PPTP-linux allows you to connect to a PPTP server from a Linux or other
Unix box (ports of pptp-linuxto other Unix variants should be trivial,
but have not yet been performed). See the IPfwd page
(http://www.pdos.lcs.mit.edu/~cananian/Projects/IPfwd) for information
on tunnelling PPTP through Linux firewalls.

%package setup
Summary:	PPTP Tunnel Configuration Script
Group:		Networking/Other
Requires:	%{name} = %{version}-%{release}

%description setup
This package provides a simple configuration script for setting up PPTP
tunnels.

%prep
%setup -qn pptp-%{version}
%apply_patches

# Pacify rpmlint
perl -pi -e 's/install -o root -m 555 pptp/install -m 755 pptp/;' Makefile

%build
OUR_CFLAGS="-Wall %{optflags} -Wextra -Wstrict-aliasing=2 -Wnested-externs -Wstrict-prototypes"
%make CFLAGS="$OUR_CFLAGS" IP=/sbin/ip

%install
%makeinstall_std
install -d -m 750 %{buildroot}%{_localstatedir}/run/pptp

install -m755 pptp -D %{buildroot}%{_sbindir}/pptp
install -m755 %{SOURCE1} -D %{buildroot}%{_sbindir}/pptp-command
install -d %{buildroot}%{_sysconfdir}/pptp.d
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/ppp/options.pptp
install -m644 pptp.8 -D %{buildroot}%{_mandir}/man8/pptp.8
install -d %{buildroot}%{_initrddir}
install -m755 %{SOURCE5} -D %{buildroot}%{_initrddir}/pptp
install -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
install -p -m 644 %{SOURCE6} %{buildroot}%{_prefix}/lib/tmpfiles.d/pptp.conf

%post
%tmpfiles_create pptp
%_post_service pptp

%preun
%_preun_service pptp

%files
%doc AUTHORS NEWS README TODO USING Documentation/[D,P]*
%{_sbindir}/pptp-*
%{_sbindir}/pptp
%{_initrddir}/pptp
%{_mandir}/man8/pptp.8*
%{_prefix}/lib/tmpfiles.d/pptp.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/ppp/options.pptp
%attr(0755,root,root) %dir %{_sysconfdir}/pptp.d

%files setup
%{_sbindir}/pptpsetup
%{_mandir}/man8/pptpsetup.8*

