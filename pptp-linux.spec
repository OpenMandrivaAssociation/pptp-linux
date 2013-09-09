%define name pptp-linux
%define version 1.7.2

Summary:	VPN client 
Name:		%{name}
Version:	%{version}
Release:	8
License:	GPLv2+
Group:		Networking/Other

Source0:	http://prdownloads.sourceforge.net/pptpclient/pptp-%{version}.tar.gz
Source1: 	pptp-command
Source2: 	options.pptp
Source3: 	pptp_fe.pl
Source4: 	xpptp_fe.pl
Source5:	pptp.initd
Source6:	pptp-tmpfs.conf
Patch0:		pptp-1.7.2-compat.patch
Patch1:		pptp-1.7.2-ip-path.patch
Patch2:		pptp-1.7.2-pptpsetup.patch
Patch3:		pptp-1.7.2-makedeps.patch
Patch4:		pptp-1.7.2-pptpsetup-encrypt.patch
Patch5:		pptp-1.7.2-pptpsetup-mppe.patch
Patch6:		pptp-1.7.2-waitpid.patch
Patch7:		pptp-1.7.2-conn-free.patch
Patch8:		pptp-1.7.2-conn-free2.patch
Patch9:		pptp-1.7.2-call-disconnect-notify.patch
Patch10:	pptp-1.7.2-so_mark.patch
Patch11:	pptp-1.7.2-nohostroute-option.patch
Patch12:	pptp-1.7.2-parallel-build.patch
Patch13:	pptp-1.7.2-fsf-update.patch
Patch14:	pptp-1.7.2-sign-compare.patch
Patch15:	pptp-1.7.2-const.patch
Patch16:	pptp-1.7.2-field-init.patch
Patch17:	pptp-1.7.2-unused.patch
Patch18:	pptp-1.7.2-prototype.patch
Patch19:	pptp-1.7.2-nested-externs.patch
Patch20:	pptp-1.7.2-aliasing.patch
Patch21:	pptp-1.7.2-options.pptp.patch

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

%package setup
Summary:	PPTP Tunnel Configuration Script
Group:		Networking/Other
Requires:	%{name} = %{version}-%{release}

%description setup
This package provides a simple configuration script for setting up PPTP
tunnels.

%prep
%setup -q -n pptp-%{version}
# Remove reference to stropts.h, not shipped in F9 onwards (applied upstream)
%patch0 -p0 -b .compat

# Make location of "ip" binary build-time configurable (applied upstream)
%patch1 -p0 -b .ip-path

# Retain permissions on /etc/ppp/chap-secrets (#492090, applied upstream)
%patch2 -p0 -b .bz492090

# Fix Makefile dependencies to support parallel make (applied upstream)
%patch3 -p0 -b .makedeps
%patch12 -p0 -b .parallel

# Don't check for MPPE capability in kernel or pppd unless we're creating a
# tunnel that requires encryption (applied upstream)
%patch4 -p0 -b .encrypt

# Don't check for MPPE capability in kernel and pppd at all because current
# Fedora releases and EL ≥ 5 include MPPE support out of the box (#502967)
%patch5 -p1 -b .mppe

# Fix waitpid usage (upstream patch)
%patch6 -p0 -b .waitpid

# Move free of connection struct out of main loop (upstream patch)
%patch7 -p0 -b .conn-free

# Avoid using connection struct after it is freed (upstream patch)
%patch8 -p0 -b .conn-free2

# Add call ID of outgoing call so that Call-Disconnect-Notify from peer causes
# correct disconnection sequence (upstream patch)
%patch9 -p1 -b .cdn

# Add support for setting SO_MARK for the PPTP TCP control connection as well
# as on the GRE packets (upstream patch)
%patch10 -p1 -b .so_mark

# Implement the --nohostroute option that routing.c talks about (upstream patch)
%patch11 -p1 -b .nohostroute

# Update the FSF address references and GPLv2 license text (upstream patch)
%patch13 -p0 -b .fsf

# Fix comparisons between signed and unsigned integers (upstream patch)
%patch14 -p1 -b .sign-compare

# Fix const usage (upstream patch)
%patch15 -p1 -b .const

# Add missing field initializers (upstream patch)
%patch16 -p1 -b .field

# Suppress warnings about possibly unused variables (upstream patch)
%patch17 -p1 -b .unused

# Fix declarations that are not prototypes (upstream patch)
%patch18 -p1 -b .prototype

# Fix warnings about nested externs (upstream patch)
%patch19 -p1 -b .nested

# Fix aliasing issues (upstream patch)
%patch20 -p1 -b .alias

# Additional commentary in options.pptp regarding encryption (upstream patch)
%patch21 -b .options-comments

# Pacify rpmlint
perl -pi -e 's/install -o root -m 555 pptp/install -m 755 pptp/;' Makefile

%build
OUR_CFLAGS="-Wall %{optflags} -Wextra -Wstrict-aliasing=2 -Wnested-externs -Wstrict-prototypes"
%make CFLAGS="$OUR_CFLAGS" IP=/sbin/ip

%install
make DESTDIR=%{buildroot} install
install -d -m 750 %{buildroot}%{_localstatedir}/run/pptp

install -m755 pptp -D %{buildroot}%{_sbindir}/pptp
install -m755 %{SOURCE1} -D %{buildroot}%{_sbindir}/pptp-command
install -d %{buildroot}%{_sysconfdir}/pptp.d
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/ppp/options.pptp
install -m644 pptp.8 -D %{buildroot}%{_mandir}/man8/pptp.8
install -d %{buildroot}%{_initrddir}
install -m755 %{SOURCE5} -D %{buildroot}%{_initrddir}/pptp
install -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_prefix}/lib/tmpfiles.d/pptp.conf

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
