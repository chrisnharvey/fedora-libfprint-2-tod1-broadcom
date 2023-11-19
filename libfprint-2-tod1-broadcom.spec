%define soname libfprint-2-tod-1-broadcom
%define udevrulesname 60-libfprint-2-device-broadcom

Name:           libfprint-2-tod1-broadcom
Version:        0.0.1
Release:        2%{?dist}
Summary:        Broadcom driver module for libfprint-2 for various Dell laptops
License:        NonFree
Group:          Hardware/Mobile
URL:            https://git.launchpad.net/~oem-solutions-engineers/libfprint-2-tod1-broadcom/+git/libfprint-2-tod1-broadcom/
BuildRequires:  git
BuildRequires:  pkgconfig(udev)
ExclusiveArch:  x86_64

%description
This is user space driver for Broadcom fingerprint module. Proprietary driver for the fingerprint reader on the various Dell laptops - direct from Dell's Ubuntu repo.

%prep
git clone %{url}
cd libfprint-2-tod1-broadcom

%build

%install
cd libfprint-2-tod1-broadcom
install -dm 0755 %{buildroot}%{_udevrulesdir} %{buildroot}%{_libdir}/libfprint-2/tod-1/
install -dm 0755 %{buildroot}%{_sharedstatedir} %{buildroot}%{_sharedstatedir}/fprint/fw/
install -m 0644 lib/udev/rules.d/%{udevrulesname}.rules %{buildroot}%{_udevrulesdir}/%{udevrulesname}.rules
install -m 0755 usr/lib/x86_64-linux-gnu/libfprint-2/tod-1/%soname.so %{buildroot}%{_libdir}/libfprint-2/tod-1/%soname.so
cp -a var/lib %{buildroot}/var/lib/

%files
%{_udevrulesdir}/%{udevrulesname}.rules
%dir %{_libdir}/libfprint-2
%dir %{_libdir}/libfprint-2/tod-1
%dir %{_sharedstatedir}/fprint
%dir %{_sharedstatedir}/fprint/fw
%{_libdir}/libfprint-2/tod-1/%soname-%{version}.so

%changelog
* Sun Nov 19 2023 Chris Harvey <chris@chrisnharvey.com> - 0.0.1
- First release
