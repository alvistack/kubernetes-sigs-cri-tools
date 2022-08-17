%global debug_package %{nil}

Name: cri-tools
Epoch: 100
Version: 1.25.0~rc1
Release: 1%{?dist}
Summary: CLI and validation tools for Kubelet Container Runtime Interface
License: Apache-2.0
URL: https://github.com/kubernetes-sigs/cri-tools/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.19
BuildRequires: glibc-static

%description
cri-tools provides a series of debugging and validation tools for
Kubelet CRI, which includes:
  - crictl: CLI for kubelet CRI
  - critest: validation test suites for kubelet CRI

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -o ./bin/crictl ./cmd/crictl

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/crictl
./bin/crictl completion > %{buildroot}%{_prefix}/share/bash-completion/completions/crictl

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
