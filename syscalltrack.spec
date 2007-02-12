# TODO
#	- SMP modules
#	- testing
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Utility for logging and taking action upon system calls
Summary(pl.UTF-8):	Narzędzia do logowania i podejmowania akcji na skutek wywołań systemowych
Name:		syscalltrack
Version:	0.82
Release:	0.1
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/syscalltrack/%{name}-%{version}.tar.gz
# Source0-md5:	a090234f42e7d97be43eaca1b0eab2c7
%{?with_dist_kernel:BuildRequires: kernel-headers}
URL:		http://syscalltrack.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
syscalltrack is made of a pair of Linux kernel modules and supporting
user space environment which allow interception, logging and possibly
taking action upon system calls that match user defined
criteria. syscalltrack can operate either in "tweezers mode", where
only very specific operations are tracked, such as "only track and log
attempts to delete /etc/passwd", or in strace(1) compatible mode,
where all of the supported system calls are traced. syscalltrack can
do things that are impossible to do with the ptrace mechanism, because
its core operates in kernel space.

%description -l pl.UTF-8
syscalltrack jest zrobiony jako para modułów jądra Linuksa i
wspierającego środowiska w przestrzeni użytkownika umożliwiającego
przechwytywanie, logowanie i ewentualnie podejmowania akcji przy
wywołaniach systemowych pasujących do kryteriów zdefiniowanych przez
użytkownika. syscalltrack może pracować w "tweezers mode", gdzie
śledzone są tylko pewne operacje, takie jak "tylko śledzenie i
logowanie prób usunięcia /etc/passwd", albo w trybie kompatybilnym ze
strace(1), gdzie śledzone są wszystkie obsługiwane wywołania
systemowe. syscalltrack może robić rzeczy niemożliwe do zrobienia
przy użyciu mechanizmu ptraec, ponieważ jego rdzeń działa w
przestrzeni jądra.

%package -n kernel-misc-syscalltrack
Summary:	syscalltrack Linux kernel module
Summary(pl.UTF-8):	Moduł jądra Linuksa syscalltrack
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-misc-syscalltrack
syscalltrack Linux kernel modules.

%description -n kernel-misc-syscalltrack -l pl.UTF-8
Moduły jądra Linuksa syscalltrack.

%package -n kernel-smp-misc-syscalltrack
Summary:	syscalltrack Linux SMP kernel module
Summary(pl.UTF-8):	Moduł jądra Linuksa SMP syscalltrack
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-syscalltrack
syscalltrack Linux SMP kernel modules.

%description -n kernel-smp-misc-syscalltrack -l pl.UTF-8
Moduły jądra Linuksa SMP syscalltrack.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-linux=%{_kernelsrcdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/lib/modules/%{_kernel_ver}{,smp}/misc}

install module/rules/sct_rules.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install module/hijack/sct_hijack.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

install sct_config/sct_config $RPM_BUILD_ROOT%{_bindir}
install sctrace/sctrace $RPM_BUILD_ROOT%{_bindir}
install utils/sct_logctrl/sct_logctrl $RPM_BUILD_ROOT%{_bindir}
install utils/sctdbg/sctdbg $RPM_BUILD_ROOT%{_bindir}
install utils/sctlog/sctlog $RPM_BUILD_ROOT%{_bindir}
install module/sct_*load $RPM_BUILD_ROOT%{_bindir}

%{__make} install.doc \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-syscalltrack
%depmod %{_kernel_ver}

%postun	-n kernel-misc-syscalltrack
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-syscalltrack
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-syscalltrack
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README doc/FUTURES doc/Version-1.0-features doc/*.html doc/*.txt doc/release-*
%attr(755,root,root) %{_bindir}/sct*
%{_mandir}/man1/*

%files -n kernel-misc-syscalltrack
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/sct_*.o*

#%files -n kernel-smp-misc-syscalltrack
#%defattr(644,root,root,755)
#/lib/modules/%{_kernel_ver}smp/misc/sct_*.o*
