%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version 2.3.0'}}

# Enable with systemctl "enable sanoid.timer"
%global _with_systemd 1

Name:		   sanoid
Version:       %{upstream_version}
Release:       1
BuildArch:	   noarch
Summary:	   A policy-driven snapshot management tool for ZFS file systems
Group:		   Applications/System
License:	   GPLv3
URL:		   https://github.com/jimsalterjrs/sanoid
Source0:       %{name}-%{upstream_version}.tar.gz

Requires:	   perl, mbuffer, lzop, pv, perl-Config-IniFiles, perl-Capture-Tiny
%if 0%{?_with_systemd}
Requires:      systemd >= 212

BuildRequires: systemd
%endif

%description
Sanoid is a policy-driven snapshot management
tool for ZFS file systems. You can use Sanoid
to create, automatically thin, and monitor snapshots
and pool health from a single eminently
human-readable TOML configuration file.

%prep
%setup -q -n %{name}-%{upstream_version}

%build
echo "Nothing to build"

%install
%{__install} -D -m 0644 sanoid.defaults.conf %{buildroot}/etc/sanoid/sanoid.defaults.conf
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -m 0755 sanoid syncoid findoid sleepymutex %{buildroot}%{_sbindir}

%if 0%{?_with_systemd}
%{__install} -d %{buildroot}%{_unitdir}
%endif

%if 0%{?fedora}
%{__install} -D -m 0644 sanoid.conf %{buildroot}%{_docdir}/%{name}/examples/sanoid.conf
%endif
%if 0%{?rhel}
%{__install} -D -m 0644 sanoid.conf %{buildroot}%{_docdir}/%{name}-%{version}/examples/sanoid.conf
%endif

%if 0%{?_with_systemd}
cat > %{buildroot}%{_unitdir}/%{name}.service <<EOF
[Unit]
Description=Snapshot ZFS Pool
Requires=zfs.target
After=zfs.target

[Service]
Environment=TZ=UTC
Type=oneshot
ExecStart=%{_sbindir}/sanoid --cron
EOF

cat > %{buildroot}%{_unitdir}/%{name}.timer <<EOF
[Unit]
Description=Run Sanoid Every Minute

[Timer]
OnCalendar=*:0/1
Persistent=true

[Install]
WantedBy=timers.target
EOF

%else
%if 0%{?fedora}
%{__install} -D -m 0644 sanoid.conf %{buildroot}%{_docdir}/%{name}/examples/sanoid.conf
%endif
%if 0%{?rhel}
echo "* * * * * root %{_sbindir}/sanoid --cron" > %{buildroot}%{_docdir}/%{name}-%{version}/examples/sanoid.cron
%endif
%endif

%post
%{?_with_systemd:%{_bindir}/systemctl daemon-reload}

%postun
%{?_with_systemd:%{_bindir}/systemctl daemon-reload}

%files
%doc CHANGELIST VERSION README.md FREEBSD.readme
%license LICENSE
%{_sbindir}/sanoid
%{_sbindir}/syncoid
%{_sbindir}/findoid
%{_sbindir}/sleepymutex
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/sanoid.defaults.conf
%if 0%{?fedora}
%{_docdir}/%{name}
%endif
%if 0%{?rhel}
%{_docdir}/%{name}-%{version}
%endif
%if 0%{?_with_systemd}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%endif

%changelog
