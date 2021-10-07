%define name pptp-linux

Summary:	VPN client 
Name:		pptp-linux
Version:	1.10.0
Release:	3
License:	GPLv2+
Group:		Networking/Other
Url:		http://pptpclient.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pptpclient/pptp-%{version}.tar.gz
Source1:	pptp-command
Source2:	options.pptp
Source3:	pptp_fe.pl
Source4:	xpptp_fe.pl
Source6:	pptp-tmpfs.conf
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

%package -n pptp-command
Summary:       PPTP Tunnel Command Line Script
Group:         Networking/Other
Requires:      %{name} = %{version}-%{release}
Conflicts:     %{name} < 1.10.0-3

%description -n pptp-command
This package provides a command line tool for using PPTP.

%prep
%setup -qn pptp-%{version}
%autopatch -p1

# Pacify rpmlint
perl -pi -e 's/install -o root -m 555 pptp/install -m 755 pptp/;' Makefile
# use our CFLAGS and LDFLAGS
sed -i -e "/CFLAGS  =/ c\CFLAGS = %{optflags}" Makefile
sed -i -e "/LDFLAGS =/ c\LDFLAGS = %{ldflags}" Makefile
sed -i "s!gcc!%{__cc}!g" Makefile
# adjust ip path
sed -i 's#/bin/ip#/sbin/ip#' routing.c Makefile

%build
%make_build

%install
%make_install

install -d -m 750 %{buildroot}%{_localstatedir}/run/pptp
install -d %{buildroot}%{_sysconfdir}/pptp.d
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/ppp/options.pptp
install -m644 pptp.8 -D %{buildroot}%{_mandir}/man8/pptp.8
install -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
install -p -m 644 %{SOURCE6} %{buildroot}%{_prefix}/lib/tmpfiles.d/pptp.conf
install -m755 %{SOURCE1} -D %{buildroot}%{_sbindir}/pptp-command

%files
%doc AUTHORS NEWS README TODO USING Documentation/[D,P]*
%{_sbindir}/pptp
%{_mandir}/man8/pptp.8*
%{_prefix}/lib/tmpfiles.d/pptp.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/ppp/options.pptp
%attr(0755,root,root) %dir %{_sysconfdir}/pptp.d

%files setup
%{_sbindir}/pptpsetup
%{_mandir}/man8/pptpsetup.8*

%files -n pptp-command
%{_sbindir}/pptp-command
