%define name pptp-linux
%define version 1.7.2

Summary:	VPN client 
Name:		%{name}
Version:	%{version}
Release:	9
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
%make OPTIMIZE="%{optflags}" DEBUG=""

%install

install -m755 pptp -D %{buildroot}%{_sbindir}/pptp
install -m755 %{SOURCE1} -D %{buildroot}%{_sbindir}/pptp-command
install -d %{buildroot}%{_sysconfdir}/pptp.d
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/ppp/options.pptp
install -m644 pptp.8 -D %{buildroot}%{_mandir}/man8/pptp.8
install -d %{buildroot}%{_initrddir}
install -m755 %{SOURCE5} -D %{buildroot}%{_initrddir}/pptp

%clean

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



%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.7.2-6mdv2011.0
+ Revision: 667819
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.2-5mdv2011.0
+ Revision: 607204
- rebuild

* Sun Jan 31 2010 Luc Menut <lmenut@mandriva.org> 1.7.2-4mdv2010.1
+ Revision: 498662
- patch0: fix ip path (mdv bug #51704)

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.7.2-3mdv2010.0
+ Revision: 426778
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.7.2-2mdv2009.1
+ Revision: 351630
- rebuild

* Tue Aug 12 2008 Emmanuel Andry <eandry@mandriva.org> 1.7.2-1mdv2009.0
+ Revision: 271120
- New version
- Fix license

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.7.1-4mdv2009.0
+ Revision: 225045
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7.1-3mdv2008.1
+ Revision: 179259
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jun 08 2007 Adam Williamson <awilliamson@mandriva.org> 1.7.1-2mdv2008.0
+ Revision: 37056
- clean spec, rebuild for new era


* Wed Mar 08 2006 Stew Benedict <sbenedict@mandriva.com> 1.7.1-1mdk
- 1.7.1

* Thu Dec 22 2005 Stew Benedict <sbenedict@mandriva.com> 1.7.0-2mdk
- replace symlink with real init script (#20267, S3)
- modprobe ppp-compress-18 in the init script
- add "refuse-eap" to options.pptp
- kill pppd rather than pptp for a cleaner interaction with "service"
  (modified pptp-command)

* Tue Oct 04 2005 Stew Benedict <sbenedict@mandriva.com> 1.7.0-1mdk
- New release 1.7.0

* Tue Jun 21 2005 Stew Benedict <sbenedict@mandriva.com> 1.6.0-2mdk
- add stateless to options.pptp, new syntax for other mppe options (#16501)
- fix pptp initscript symlink removed in 1.5.0-2mdk (#16499)

* Wed Apr 27 2005 Olivier Blin <oblin@mandriva.com> 1.6.0-1mdk
- 1.6.0

* Tue Jan 18 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.5.0-2mdk
- update options.pptp (S2)  for new pppd
- compile with $RPM_OPT_FLAGS and without -g flag
- cleanups!

* Mon Jul 05 2004 Olivier Blin <blino@mandrake.org> 1.5.0-1mdk
- 1.5.0

* Wed May 26 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4.0-2mdk
- fix requires

* Tue May 25 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.4.0-1mdk
- 1.4.0, fix options.pptp for pppd 2.4.2 (#9376)

* Wed Jul 02 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3.1-1mdk
- 1.3.1

* Fri Apr 04 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.2.0-1mdk
- 1.2.0

