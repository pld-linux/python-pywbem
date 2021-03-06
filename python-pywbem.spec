# TODO: fix docs
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_without	tests	# unit/functional tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	WBEM client and related utilities, written in pure Python
Summary(pl.UTF-8):	Klient WBEM i powiązane narzędzia, napisane w czystym Pythonie
Name:		python-pywbem
Version:	0.17.6
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://github.com/pywbem/pywbem/releases
Source0:	https://github.com/pywbem/pywbem/archive/%{version}/pywbem-%{version}.tar.gz
# Source0-md5:	af567dee3476334a232d8e5ccb7db632
Patch0:		pywbem-mock.patch
Patch1:		pywbem-threading.patch
URL:		https://github.com/pywbem/pywbem
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-FormEncode >= 1.3.1
BuildRequires:	python-M2Crypto >= 0.31.0
BuildRequires:	python-PyYAML >= 5.3
BuildRequires:	python-funcsigs >= 1.0.2
BuildRequires:	python-httpretty >= 0.9.5
BuildRequires:	python-importlib_metadata >= 0.12
#BuildRequires:	python-importlib_metadata < 1
BuildRequires:	python-lxml >= 4.2.4
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-packaging >= 16.6
BuildRequires:	python-ply >= 3.10
BuildRequires:	python-pytest >= 4.3.1
BuildRequires:	python-pytz >= 2016.10
BuildRequires:	python-requests >= 2.20.1
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-testfixtures >= 6.9.0
BuildRequires:	python-yamlloader >= 0.5.5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-FormEncode >= 1.3.1
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 5.1
BuildRequires:	python3-httpretty >= 0.9.5
%if "%{_ver_lt '%{py3_ver}' < '3.7'}" == "1"
BuildRequires:	python3-importlib_metadata >= 0.12
BuildRequires:	python3-importlib_metadata < 1
%endif
BuildRequires:	python3-lxml >= 4.4.3
BuildRequires:	python3-packaging >= 16.6
BuildRequires:	python3-ply >= 3.10
BuildRequires:	python3-pytest >= 4.4.0
BuildRequires:	python3-pytz >= 2016.10
BuildRequires:	python3-requests >= 2.20.1
BuildRequires:	python3-six >= 1.12.0
BuildRequires:	python3-testfixtures >= 6.9.0
BuildRequires:	python3-yamlloader >= 0.5.5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.749
%if %{with doc}
BuildRequires:	python3-sphinx_git >= 10.1.1
BuildRequires:	python3-sphinxcontrib-fulltoc >= 1.2.0
BuildRequires:	sphinx-pdg-3 >= 1.7.6
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pywbem is a WBEM client and WBEM indication listener, written in pure
Python.

%description -l pl.UTF-8
Pywbem to klient WBEM oraz serwis identyfikacji WBEM, napisane w
czystym Pythonie.

%package -n python3-pywbem
Summary:	WBEM client and related utilities, written in pure Python
Summary(pl.UTF-8):	Klient WBEM i powiązane narzędzia, napisane w czystym Pythonie
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-pywbem
Pywbem is a WBEM client and WBEM indication listener, written in pure
Python.

%description -n python3-pywbem -l pl.UTF-8
Pywbem to klient WBEM oraz serwis identyfikacji WBEM, napisane w
czystym Pythonie.

%package apidocs
Summary:	API documentation for Python pywbem module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pywbem
Group:		Documentation

%description apidocs
API documentation for Python pywbem module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pywbem.

%prep
%setup -q -n pywbem-%{version}
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's/\.\. git_changelog::/(missing git changelog)/' docs/changes.rst

%build
%if %{with python2}
%py_build

%if %{with tests}
PATH=$(pwd):$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests/unittest tests/functiontest
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PATH=$(pwd):$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests/unittest tests/functiontest
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/mof_compiler{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/wbemcli{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/wbemcli.py $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}

%py_postclean

cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python-pywbem-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' $RPM_BUILD_ROOT%{_examplesdir}/python-pywbem-%{version}/*.py
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/mof_compiler{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/wbemcli{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/wbemcli.py $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python3-pywbem-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-pywbem-%{version}/*.py
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.bat

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst TODO.md
%attr(755,root,root) %{_bindir}/mof_compiler-2
%attr(755,root,root) %{_bindir}/wbemcli-2
%{py_sitescriptdir}/wbemcli.py[co]
%{py_sitescriptdir}/pywbem
%{py_sitescriptdir}/pywbem_mock
%{py_sitescriptdir}/pywbem-%{version}-py*.egg-info
%{_examplesdir}/python-pywbem-%{version}
%endif

%if %{with python3}
%files -n python3-pywbem
%defattr(644,root,root,755)
%doc README.rst TODO.md
%attr(755,root,root) %{_bindir}/mof_compiler-3
%attr(755,root,root) %{_bindir}/wbemcli-3
%{py3_sitescriptdir}/wbemcli.py
%{py3_sitescriptdir}/__pycache__/wbemcli.cpython-*.py[co]
%{py3_sitescriptdir}/pywbem
%{py3_sitescriptdir}/pywbem_mock
%{py3_sitescriptdir}/pywbem-%{version}-py*.egg-info
%{_examplesdir}/python3-pywbem-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
