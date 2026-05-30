# sanoid RPM packaging

This repository contains RPM packaging files for `sanoid` and its optional `mbuffer` dependency.

## Supported targets

The package is intended to support all architectures on EL7 and newer compatible distributions. Examples:

- el7/x86_64
- el7/aarch64
- el8/x86_64
- el8/aarch64
- el9/x86_64
- el9/aarch64
- el10/x86_64
- el10/aarch64

## Layout

~~~~ {.text}
rpmbuild/
├── SOURCES/
│   ├── prep-sanoid.sh
│   └── prep-mbuffer.sh
└── SPECS/
    ├── sanoid.spec
    └── mbuffer.spec
~~~~

## Prepare sanoid sources

Run:

~~~~ {.bash}
./rpmbuild/SOURCES/prep-sanoid.sh <VERSION>
~~~~

The script downloads the upstream `sanoid` source tarball with the corresponding version.

Example output:

~~~~ {.text}
rpmbuild/SOURCES/sanoid-2.3.0.tar.gz
~~~~

## Prepare mbuffer sources

Run:

~~~~ {.bash}
./rpmbuild/SOURCES/prep-mbuffer.sh <VERSION>
~~~~

The script downloads the upstream `mbuffer` source tarball with the corresponding version.

Example output:

~~~~ {.text}
rpmbuild/SOURCES/mbuffer-20260511.tgz
~~~~

## Build source RPMs

Run:

~~~~ {.bash}
rpmbuild \
  --define "_topdir $PWD/rpmbuild" \
  -bs rpmbuild/SPECS/sanoid.spec

rpmbuild \
  --define "_topdir $PWD/rpmbuild" \
  -bs rpmbuild/SPECS/mbuffer.spec
~~~~

## Build with mock

Build the generated source RPMs with the required target mock config.

Example:

~~~~ {.bash}
mock -r oraclelinux-7-x86_64 --rebuild rpmbuild/SRPMS/sanoid-2.3.0-1.src.rpm
mock -r oraclelinux-7-aarch64 --rebuild rpmbuild/SRPMS/sanoid-2.3.0-1.src.rpm

mock -r oraclelinux-7-x86_64 --rebuild rpmbuild/SRPMS/mbuffer-20260511-1.el7.src.rpm
mock -r oraclelinux-7-aarch64 --rebuild rpmbuild/SRPMS/mbuffer-20260511-1.el7.src.rpm
~~~~

For EL8, EL9, or other architectures, use the matching mock config for that target.

**Notes:**

`sanoid` is packaged as `BuildArch: noarch`, but the package should still be rebuilt and validated
in the target environments to confirm dependency compatibility. The source RPM should be built once
and then reused for all target mock rebuilds.

`mbuffer` is written in C, so its binary RPM is architecture-specific. Build it separately for each
target architecture.

`sanoid` can run without `mbuffer`, but `mbuffer` is useful for `syncoid` replication performance.
