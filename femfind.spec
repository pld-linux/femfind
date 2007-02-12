#
# TODO:
# - webapps
# - include apache configuration to config
# - pre/post play
# - logrotate file
# - fix ownership of the perl_vendorlib/FemFind directory
#
%include	/usr/lib/rpm/macros.perl
Summary:	FemFind - crawl your network resources
Summary(pl.UTF-8):   FemFind - przeszukiwanie zasobów sieciowych
Name:		FemFind
Version:	0.74
Release:	2
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://www.codefactory.de/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	57de716507fb23ddb4fed17cd77cd038
Patch0:		%{name}-config.patch
URL:		http://femfind.sourceforge.net/
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_wwwsite	/home/services/httpd/html/FemFind
%define		_cgisite	/home/services/httpd/cgi-bin/femfind

%description
FemFind is a crawler for SMB shares which can be found on Windows or
Unix systems running Samba. Additionally FemFind crawls FTP servers
and provides a web interface and a Windows client as frontends.

%description -l pl.UTF-8
FemFind jest programem przeszukującym zasoby sieci udostępnione
poprzez protokół SMB na maszynach windowsowych lub uniksowych z
działającą Sambą. Dodatkowo FemFind przeszukuje serwery FTP, dostarcza
interfejs WWW oraz klienta windowsowego jako frontend.

%package -n perl-FemFind-ConfigReader
Summary:	FemFind - crawl your network resources
Summary(pl.UTF-8):   FemFind - przeszukiwanie zasobów sieciowych
Group:		Development/Languages/Perl

%description -n perl-FemFind-ConfigReader
FemFind::ConfigReader perl module for FemFind.

%description -n perl-FemFind-ConfigReader -l pl.UTF-8
Perlowy moduł FemFind::ConfigReader dla FemFinda.

%package -n perl-FemFind-Helper
Summary:	FemFind - crawl your network resources
Summary(pl.UTF-8):   FemFind - przeszukiwanie zasobów sieciowych
Group:		Development/Languages/Perl

%description -n perl-FemFind-Helper
FemFind::Helper perl module for FemFind.

%description -n perl-FemFind-Helper -l pl.UTF-8
Perlowy moduł FemFind::Helper dla FemFinda.

%package -n FemFind-cgi
Summary:	FemFind - crawl your network resources
Summary(pl.UTF-8):   FemFind - przeszukiwanie zasobów sieciowych
Group:		Networking/Utilities

%description -n FemFind-cgi
CGI scripts for FemFind frontend.

%description -n FemFind-cgi -l pl.UTF-8
Skrypty CGI do frontendu FemFinda.

%prep
%setup -q
%patch0 -p1

%build
cd modules
cd ConfigReader
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}
cd ..
cd Helper
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{_bindir},%{_sbindir}}
install -d $RPM_BUILD_ROOT{%{_wwwsite},%{_cgisite}/german,/var/{lib/femfind,log}}

%{__make} install \
	-C modules/ConfigReader \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install \
	-C modules/Helper \
	DESTDIR=$RPM_BUILD_ROOT

install femfind.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install makedb.pl	$RPM_BUILD_ROOT%{_sbindir}
install crawler.pl	$RPM_BUILD_ROOT%{_bindir}
install german/*	$RPM_BUILD_ROOT%{_cgisite}/german
install cgi-bin/femfind/*	$RPM_BUILD_ROOT%{_cgisite}
install htdocs/femfind/*	$RPM_BUILD_ROOT%{_wwwsite}

touch $RPM_BUILD_ROOT/var/log/femfind.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Remember to init database running %{_sbindir}/makedb.pl"

%files
%defattr(644,root,root,755)
%doc README
%dir /var/lib/femfind
%ghost /var/log/femfind.log
%config(noreplace) %{_sysconfdir}/femfind.conf
%attr(755,root,root) %{_sbindir}/makedb.pl
%attr(755,root,root) %{_bindir}/crawler.pl

%files -n perl-FemFind-ConfigReader
%defattr(644,root,root,755)
# ??? see Helper
%{perl_vendorlib}/FemFind/*.pm
%{_mandir}/man3/FemFind::ConfigReader.*

%files -n perl-FemFind-Helper
%defattr(644,root,root,755)
# ??? see ConfigReader
%{perl_vendorlib}/FemFind/*.pm
%{_mandir}/man3/FemFind::Helper.*

%files -n FemFind-cgi
%defattr(644,root,root,755)
%dir %{_cgisite}
%dir %{_wwwsite}
%dir %{_cgisite}/german
%attr(755,root,root) %{_cgisite}/german/*.pl
%{_cgisite}/german/*.html
%attr(755,root,root) %{_cgisite}/*.pl
%{_cgisite}/*.html
%{_cgisite}/ftp_list
%{_wwwsite}/*
