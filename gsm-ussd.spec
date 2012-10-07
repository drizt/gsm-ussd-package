%define __provides_exclude_from %{_libexecdir}
%define __requires_exclude .*GSMUSSD.*

%global rev 25
Name:           gsm-ussd
Group:          Applications/Communications
Version:        0.4.0
Release:        0.3.%{rev}%{?dist}
Source:         http://linux.zum-quadrat.de/downloads/%{name}_%{version}-%{rev}.tar.gz
BuildArch:      noarch 
Summary:        USSD query tool

License:        GPLv2+ or LGPLv2+
Url:            http://iloapp.zum-quadrat.de/blog/linux?Home&category=2
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Expect)

# Makefile installs python scripts to lib dir. It's wrong.
# Patch serves to fix it.
Patch0:         gsm-ussd-libexec.patch

%description
gsm-ussd is a script to send USSD (Unstructured Supplementary
Services Data) queries to your broadband provider. USSD queries
are "phone numbers" like "*100#", which will result in a message
(NOT a SMS) with your current prepaid account balance.

You can use this program to query your own phone number,
replenish your prepaid account, query your free minutes left
and so on, depending on your GSM provider.

%prep
%setup -qn %{name}_%{version}-%{rev}
%patch0 -p1

%build

%install
make PREFIX=$RPM_BUILD_ROOT/usr install install-doc
# Unset executable bit
chmod 644 $RPM_BUILD_ROOT%{_mandir}/man1/* $RPM_BUILD_ROOT%{_mandir}/de/man1/*
chmod 644 $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lib/GSMUSSD/*

# gsm-ussd has gui but it depends from KDE and Gnome.
# So I've droped it to prevent many dependencies.
rm $RPM_BUILD_ROOT%{_bindir}/xussd
rm $RPM_BUILD_ROOT%{_libexecdir}/%{name}/bin/xussd.sh
rm $RPM_BUILD_ROOT%{_mandir}/man1/xussd*
rm $RPM_BUILD_ROOT%{_mandir}/de/man1/xussd*

%files
%doc README LICENSE TODO docs/README.* docs/story.txt docs/ussd-sessions.txt
%doc %{_mandir}/man1/*
%doc %{_mandir}/de/man1/*
%{_libexecdir}/%{name}/
%{_bindir}/%{name}

%changelog
* Sun Oct 07 2012 Ivan Romanov <drizt@land.ru> 0.4.0-0.3.25
- dropped xussd
- unset executable flag for perl modules
- fixed License tag
- fixed Requires tag
- filter modules from Provides

* Sat Sep 22 2012 Ivan Romanov <drizt@land.ru> 0.4.0-0.2.25
- renamed lib-exec.patch -> gsm-ussd-libexec.patch
- dropped %%defattr
- corrected license
- use %%gloabal instead of %%define

* Sun Sep 16 2012 Ivan Romanov <drizt@land.ru> 0.4.0-0.1.25
- Initial version of package based on spec.tmpl from source tarball
