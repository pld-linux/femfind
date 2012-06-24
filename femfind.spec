# TODO:
# - include apache configuration to config
# - pre/post play
# - logrotate file

%include	/usr/lib/rpm/macros.perl
Summary:	FemFind - crawl your network resources
Summary(pl):	FemFind - przeszukiwanie zasob�w sieciowych
Name:		FemFind
Version:	0.74
Release:	1
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://www.codefactory.de/downloads/%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
URL:		http://femfind.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_wwwsite	/home/services/httpd/html/FemFind
%define		_cgisite	/home/services/httpd/cgi-bin/femfind

%description
FemFind is a crawler for SMB shares which can be found on Windows or
Unix systems running Samba. Additionally FemFind crawls FTP servers
and provides a web interface and a Windows client as frontends.

%description -l pl
FemFind jest programem przeszukuj�cym zasoby sieci udost�pnione
poprzez protok� SMB na maszynach Windowsowych lub Uniksowych z
dzia�aj�c� Samb�. Dodatkowo FemFind przeszukuje serwery FTP, dostarcza
interfejs webowy oraz klienta Windowsowego jako frontend.

%package -n perl-FemFind-ConfigReader
Summary:	FemFind - crawl your network resources
Summary(pl):	FemFind - przeszukiwanie zasob�w sieciowych
Group:		Development/Languages/Perl

%description -n perl-FemFind-ConfigReader
FemFind::ConfigReader perl module for FemFind.

%description -n perl-FemFind-ConfigReader -l pl
Perlowy modu� FemFind::ConfigReader dla FemFinda.

%package -n perl-FemFind-Helper
Summary:	FemFind - crawl your network resources
Summary(pl):	FemFind - przeszukiwanie zasob�w sieciowych
Group:		Development/Languages/Perl

%description -n perl-FemFind-Helper
FemFind::Helper perl module for FemFind.

%description -n perl-FemFind-Helper -l pl
Perlowy modu� FemFind::Helper dla FemFinda.

%package -n FemFind-cgi
Summary:	FemFind - crawl your network resources
Summary(pl):	FemFind - przeszukiwanie zasob�w sieciowych
Group:		Networking/Utilities

%description -n FemFind-cgi
CGI scripts for FemFind frontend.

%description -n FemFind-cgi -l pl
Skrypty CGI do frontendu FemFinda.

%prep
%setup -q
%patch0 -p1

%build
cd modules
cd ConfigReader
	perl Makefile.PL
	%{__make}
cd ..
cd Helper
	perl Makefile.PL
	%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{_bindir},%{_sbindir}}
install -d $RPM_BUILD_ROOT{%{_wwwsite},%{_cgisite}/german,/var/{lib/femfind,log}}

for i in Helper ConfigReader; do
	cd modules/$i
	%{__make} install DESTDIR=$RPM_BUILD_ROOT
	cd ../../
done

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
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/femfind.conf
%attr(755,root,root) %{_sbindir}/makedb.pl
%attr(755,root,root) %{_bindir}/crawler.pl

%files -n perl-FemFind-ConfigReader
%defattr(644,root,root,755)
%{perl_sitelib}/FemFind/*.pm

%files -n perl-FemFind-Helper
%defattr(644,root,root,755)
%{perl_sitelib}/FemFind/*.pm
%{_mandir}/man3/FemFind::Helper.3pm.gz

%files -n FemFind-cgi
%defattr(644,root,root,755)
%dir %{_cgisite}
%dir %{_wwwsite}
%attr(755,root,root) %{_cgisite}/german/*.pl
%attr(644,root,root) %{_cgisite}/german/*.html
%attr(755,root,root) %{_cgisite}/*.pl
%attr(644,root,root) %{_cgisite}/*.html
%attr(644,root,root) %{_cgisite}/ftp_list
%attr(644,root,root) %{_wwwsite}/*
