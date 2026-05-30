%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version 20260511'}}
%global debug_package %{nil}

Name:           mbuffer
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        Tool for buffering data streams

License:        GPL-3.0-or-later
URL:            https://www.maier-komor.de/mbuffer.html
Source0:        %{name}-%{version}.tgz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  openssl-devel

%description
mbuffer is a tool for buffering data streams. It is designed for backup,
replication, and other streaming workloads where steady throughput matters.

It supports TCP network targets over IPv4 and IPv6, parallel distribution to
multiple targets, multiple volumes, I/O rate limiting, configurable buffer
sizes, high/low watermark based restart criteria, and on-the-fly MD5 hash
calculation.

mbuffer is especially useful when writing backups to fast tape drives or
libraries, where buffer underruns can cause drives to stop and rewind. It uses
a highly efficient multi-threaded implementation to help keep data flowing.

%prep
%setup -q
# Keep RPM-provided compiler/hardening flags for mbuffer's configure-time
# open/read/write/fstat symbol-detection test. The upstream configure script
# temporarily uses -O0 for that test, but should not discard existing CFLAGS.
sed -i 's|CFLAGS="-O0"|CFLAGS="${CFLAGS} -O0"|' configure

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc AUTHORS ChangeLog INSTALL NEWS README
%{_bindir}/mbuffer
%config(noreplace) %{_sysconfdir}/mbuffer.rc
%{_mandir}/man1/mbuffer.1*

%changelog
