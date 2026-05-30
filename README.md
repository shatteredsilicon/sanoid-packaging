# sanoid RPM packaging

This repository contains RPM packaging files for `sanoid`.

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
│   └── prep-sanoid.sh
└── SPECS/
    └── sanoid.spec
~~~~

## Prepare sources

Run:

~~~~ {.bash}
./rpmbuild/SOURCES/prep-sanoid.sh <VERSION>
~~~~

The script downloads the upstream source tarball with the corresponding version.

Example output:

~~~~ {.text}
rpmbuild/SOURCES/sanoid-2.3.0.tar.gz
~~~~

## Build source RPM

Run:

~~~~ {.bash}
rpmbuild \
  --define "_topdir $PWD/rpmbuild" \
  -bs rpmbuild/SPECS/sanoid.spec
~~~~

## Build with mock

Build the generated source RPM with the required target mock config.

Example:

~~~~ {.bash}
mock -r oraclelinux-7-x86_64 --rebuild rpmbuild/SRPMS/sanoid-2.3.0-1.src.rpm
mock -r oraclelinux-7-aarch64 --rebuild rpmbuild/SRPMS/sanoid-2.3.0-1.src.rpm
~~~~

For EL8, EL9, or other architectures, use the matching mock config for that target.

**Notes:**

`sanoid` is packaged as `BuildArch: noarch`, but the package should still be rebuilt and validated
in both EL7 target environments to confirm dependency compatibility. The source RPM should be built
once and then reused for all target mock rebuilds.
