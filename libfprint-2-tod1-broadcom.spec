Name:           libfprint-2-tod1-broadcom
Version:        0.0.1
Release:        2%{?dist}
Summary:        Broadcom driver module for libfprint-2 for various Dell laptops
License:        NonFree
Group:          Hardware/Mobile
URL:            https://git.launchpad.net/~oem-solutions-engineers/libfprint-2-tod1-broadcom/+git/libfprint-2-tod1-broadcom/
BuildRequires:  git
BuildRequires:  pkgconfig(udev)
BuildRequires:  selinux-policy-devel
ExclusiveArch:  x86_64
Supplements:    modalias(usb:v0A5Cp5842d*dc*dsc*dp*ic*isc*ip*)
Supplements:    modalias(usb:v0A5Cp5843d*dc*dsc*dp*ic*isc*ip*)
Supplements:    modalias(usb:v0A5Cp5844d*dc*dsc*dp*ic*isc*ip*)
Supplements:    modalias(usb:v0A5Cp5845d*dc*dsc*dp*ic*isc*ip*)

Source0:        %{url}
Source1:        libfprint-tod-tmpfiles.conf
Source2:        libfprint-tod-broadcom.te
Source3:        libfprint-tod-broadcom.fc

%description
This is user space driver for Broadcom fingerprint module. Proprietary driver for the fingerprint reader on the various Dell laptops - direct from Dell's Ubuntu repo.

%prep
git clone %{url} %{name}-git-repo --depth 1

%build
# Build SELinux policy
# Use the full path for the policy source files
make -f /usr/share/selinux/devel/Makefile %{SOURCE2} %{SOURCE3}
# The 'install' command needs the compiled policy. Let's make it here so it's ready.
# We'll just build the .pp from the sources
make -f /usr/share/selinux/devel/Makefile -C %{_sourcedir} libfprint-tod-broadcom.pp

%install

install -dm 0755 \
    %{buildroot}%{_udevrulesdir} \
    %{buildroot}%{_libdir}/libfprint-2/tod-1 \
    %{buildroot}%{_libdir}/fprint/fw/ \
    %{buildroot}%{_tmpfilesdir} \
    %{buildroot}%{_datadir}/selinux/targeted/
# License
install -Dm0644 %{name}-git-repo/LICENCE.broadcom %{buildroot}%{_datadir}/licenses/%{name}/LICENCE.broadcom

# Tmpfiles rule
#install -m 0644 %{_sourcedir}/${name}-*/libfprint-tod-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/libfprint-tod.conf
install -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/libfprint-tod.conf

# Udev rule
install -m 0644 %{name}-git-repo/lib/udev/rules.d/60-libfprint-2-device-broadcom.rules \
    %{buildroot}%{_udevrulesdir}/60-libfprint-2-device-broadcom.rules

# Firmware
install -m 0644 %{name}-git-repo/var/lib/fprint/fw/* %{buildroot}%{_libdir}/fprint/fw/

# TOD module
install -m 0755 %{name}-git-repo/usr/lib/x86_64-linux-gnu/libfprint-2/tod-1/*.so \
    %{buildroot}%{_libdir}/libfprint-2/tod-1/

# Install the SELinux policy module
install -m 0644 %{_sourcedir}/libfprint-tod-broadcom.pp %{buildroot}%{_datadir}/selinux/targeted/
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/selinux/targeted/

%post
# Load the SELinux policy module
semodule -i %{_datadir}/selinux/targeted/libfprint-tod-broadcom.pp

# Apply the SELinux file contexts
/usr/sbin/semanage fcontext -a -t fprintd_var_lib_t "/usr/lib64/fprint/fw(/.*)?"
/usr/sbin/restorecon -Rv /usr/lib64/fprint/fw

%postun
# Check if the package is being completely removed
if [ "$1" -eq 0 ]; then
    # Unload the SELinux policy module
    semodule -r libfprint-tod-broadcom

    # Remove the SELinux file contexts
    /usr/sbin/semanage fcontext -d "/usr/lib64/fprint/fw(/.*)?"
    /usr/sbin/restorecon -Rv /usr/lib64/fprint/fw
fi

%files
%license %{_datadir}/licenses/%{name}/LICENCE.broadcom
%{_udevrulesdir}/60-libfprint-2-device-broadcom.rules
%{_libdir}/libfprint-2/tod-1/*.so
%{_libdir}/fprint/fw/*
%{_tmpfilesdir}/libfprint-tod.conf
%{_datadir}/selinux/targeted/libfprint-tod-broadcom.pp
%{_datadir}/selinux/targeted/libfprint-tod-broadcom.fc

%changelog
* Sun Nov 19 2023 Chris Harvey <chris@chrisnharvey.com> - 0.0.1
- First release
