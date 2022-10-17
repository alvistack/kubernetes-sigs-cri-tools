# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: cri-tools
Epoch: 100
Version: 1.24.0
Release: 1%{?dist}
Summary: CLI and validation tools for Kubelet Container Runtime Interface
License: Apache-2.0
URL: https://github.com/kubernetes-sigs/cri-tools/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.18
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
