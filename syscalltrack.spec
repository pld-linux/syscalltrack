# TODO
#	- SMP modules
#	- testing
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Utility for logging and taking action upon system calls
Summary(pl):	Narzêdzia do logowania i podejmowania akcji na skutek wywo³añ systemowych
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

%description -l pl
syscalltrack jest zrobiony jako para modu³ów j±dra Linuksa i
wspieraj±cego ¶rodowiska w przestrzeni u¿ytkownika umo¿liwiaj±cego
przechwytywanie, logowanie i ewentualnie podejmowania akcji przy
wywo³aniach systemowych pasuj±cych do kryteriów zdefiniowanych przez
u¿ytkownika. syscalltrack mo¿e pracowaæ w "tweezers mode", gdzie
¶ledzone s± tylko pewne operacje, takie jak "tylko ¶ledzenie i
logowanie prób usuniêcia /etc/passwd", albo w trybie kompatybilnym ze
strace(1), gdzie ¶ledzone s± wszystkie obs³ugiwane wywo³ania
systemowe. syscalltrack mo¿e robiæ rzeczy niemo¿liwe do zrobienia
przy u¿yciu mechanizmu ptraec, poniewa¿ jego rdzeñ dzia³a w
przestrzeni j±dra.

%package -n kernel-misc-syscalltrack
Summary:	syscalltrack Linux kernel module
Summary(pl):	Modu³ j±dra Linuksa syscalltrack
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-misc-syscalltrack
syscalltrack Linux kernel modules.

%description -n kernel-misc-syscalltrack -l pl
Modu³y j±dra Linuksa syscalltrack.

%package -n kernel-smp-misc-syscalltrack
Summary:	syscalltrack Linux SMP kernel module
Summary(pl):	Modu³ j±dra Linuksa SMP syscalltrack
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-syscalltrack
syscalltrack Linux SMP kernel modules.

%description -n kernel-smp-misc-syscalltrack -l pl
Modu³y j±dra Linuksa SMP syscalltrack.

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
