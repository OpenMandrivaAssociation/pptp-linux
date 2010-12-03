%define name pptp-linux
%define version 1.7.2

Summary:	PPTP-linux VPN client 
Name:		%{name}
Version:	%{version}
Release:	%mkrel 5
License:	GPLv2+
Group:		Networking/Other

Source0:	http://prdownloads.sourceforge.net/pptpclient/pptp-%{version}.tar.gz
Source1: 	pptp-command
Source2: 	options.pptp
Source3: 	pptp_fe.pl
Source4: 	xpptp_fe.pl
Source5:	pptp.initd
Patch0: 	pptp-1.7.2-fix-ip-path.patch

URL:		http://pptpclient.sourceforge.net/
Requires:	ppp >= 2.4.3
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Conflicts:	pptp-adsl-alcatel
Obsoletes:	pptp-client
Provides:	pptp-client

%description
PPTP-linux allows you to connect to a PPTP server from a Linux or other
Unix box (ports of pptp-linuxto other Unix variants should be trivial,
but have not yet been performed). See the IPfwd page
(http://www.pdos.lcs.mit.edu/~cananian/Projects/IPfwd) for information
on tunnelling PPTP through Linux firewalls.

%prep
%setup -q -n pptp-%{version}
%patch0 -p1 -b .ip-path

%build
%make OPTIMIZE="$RPM_OPT_FLAGS" DEBUG=""

%install
rm -rf $RPM_BUILD_ROOT

install -m755 pptp -D $RPM_BUILD_ROOT%{_sbindir}/pptp
install -m755 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sbindir}/pptp-command
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pptp.d
install -m644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_sysconfdir}/ppp/options.pptp
install -m644 pptp.8 -D $RPM_BUILD_ROOT%{_mandir}/man8/pptp.8
install -d $RPM_BUILD_ROOT%{_initrddir}
install -m755 %{SOURCE5} -D $RPM_BUILD_ROOT%{_initrddir}/pptp

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service pptp

%preun
%_preun_service pptp

%files
%defattr (-,root,root)
%doc AUTHORS NEWS README TODO USING Documentation/[D,P]*
%{_sbindir}/*
%{_initrddir}/pptp
%{_mandir}/man8/pptp.8*
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/ppp/options.pptp
%attr(0755,root,root) %dir %{_sysconfdir}/pptp.d

