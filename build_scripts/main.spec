# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['AppKit', 'BeautifulSoup', 'Foundation', 'IPython', 'OpenSSL', 'PyQt4', 'PyQt6', 'PySide2', 'PySide6', 'Queue', 'StringIO', 'System', 'UserDict', '_aix_support', '_asyncio', '_bootsubprocess', '_brotli', '_cffi_backend', '_codecs_cn', '_codecs_hk', '_codecs_iso2022', '_codecs_jp', '_codecs_kr', '_codecs_tw', '_curses', '_dbm', '_dummy_thread', '_gdbm', '_lsprof', '_manylinux', '_markupbase', '_md5', '_multibytecodec', '_multiprocessing', '_osx_support', '_overlapped', '_posixshmem', '_posixsubprocess', '_py_abc', '_pydecimal', '_pydevd_bundle', '_pyio', '_scproxy', '_sha1', '_sha256', '_sha3', '_sqlite3', '_ssl', '_statistics', '_subprocess', '_symtable', '_threading_local', '_tkinter', '_tokenize', '_tracemalloc', '_typeshed', '_win32sysloader', '_winreg', 'appnope', 'argcomplete', 'argparse', 'arrow', 'astroid', 'asttokens', 'asyncio', 'attr', 'attrs', 'backports', 'bcrypt', 'bdb', 'black', 'botocore', 'brotli', 'brotlicffi', 'bs4', 'cPickle', 'cProfile', 'cStringIO', 'cached_property', 'cachetools', 'cchardet', 'certifi', 'cgi', 'chardet', 'charset_normalizer', 'cloudpickle', 'clr', 'cmd', 'codeop', 'com', 'comm', 'commctrl', 'concurrent', 'configparser', 'contourpy', 'cryptography', 'cssselect', 'ctags', 'curio', 'curses', 'cython', 'dbm', 'debugpy', 'decorator', 'diff', 'difflib', 'dill', 'distributed', 'distutils', 'docrepr', 'doctest', 'dummy_thread', 'dummy_threading', 'email', 'exceptiongroup', 'executing', 'fastjsonschema', 'fastparquet', 'faulthandler', 'fcntl', 'filecmp', 'fqdn', 'fractions', 'fsspec', 'ftplib', 'getopt', 'getpass', 'gettext', 'gevent', 'gi', 'gobject', 'google', 'grp', 'gssapi', 'gtk', 'html5lib', 'htmlentitydefs', 'http', 'idna', 'imp', 'importlib_metadata', 'importlib_resources', 'invoke', 'ipykernel', 'ipyparallel', 'ipywidgets', 'isal', 'isoduration', 'java', 'jedi', 'jinja2', 'jnius', 'jsonpointer', 'jsonschema', 'jsonschema_specifications', 'jupyter_client', 'jupyter_core', 'lxml', 'lxml_html_clean', 'lz4', 'lzmaffi', 'main', 'markupsafe', 'mimetypes', 'nacl', 'nbformat', 'nest_asyncio', 'netifaces', 'netrc', 'ntsecuritycon', 'nturl2path', 'numba', 'numexpr', 'numpydoc', 'odf', 'olefile', 'openpyxl', 'optparse', 'org', 'paramiko', 'parso', 'pdb', 'pexpect', 'pickle5', 'pickleshare', 'pickletools', 'pkg_resources', 'platformdirs', 'plistlib', 'posix', 'profile', 'prompt_toolkit', 'pstats', 'psutil', 'pure_eval', 'pwd', 'py_compile', 'pyarrow', 'pyasn1', 'pyasn1_modules', 'pycparser', 'pyczmq', 'pydevd', 'pydevd_file_utils', 'pydoc_data', 'pygame', 'pygments', 'pyi_rth__tkinter', 'pyi_rth_cryptography_openssl', 'pyi_rth_inspect', 'pyi_rth_mplconfig', 'pyi_rth_multiprocessing', 'pyi_rth_pkgres', 'pyi_rth_pkgutil', 'pyi_rth_pyqt5', 'pyi_rth_pythoncom', 'pyi_rth_pywintypes', 'pyi_rth_setuptools', 'pyi_rth_traitlets', 'pyimod02_importers', 'pytest', 'python_calamine', 'pythoncom', 'pyu2f', 'pywin', 'pywintypes', 'pyxlsb', 'qtpy', 'quopri', 'railroad', 'readline', 'referencing', 'requests', 'resource', 'rfc3339_validator', 'rfc3986_validator', 'rfc3987', 'rlcompleter', 'rpds', 'rsa', 'runpy', 'scikits', 'scipy', 'sets', 'setuptools', 'setuptools_scm', 'shelve', 'shiboken2', 'shiboken6', 'simplejson', 'sitecustomize', 'sksparse', 'smtplib', 'snappy', 'socketserver', 'socks', 'soupsieve', 'sparse', 'sphinx', 'sqlalchemy', 'sqlite3', 'sre_compile', 'sre_constants', 'sre_parse', 'ssl', 'sspi', 'sspicon', 'stack_data', 'statistics', 'stringprep', 'symtable', 'tables', 'termios', 'thread', 'threadpoolctl', 'timeit', 'tkinter', 'tornado', 'tracemalloc', 'traitlets', 'trio', 'trove_classifiers', 'tty', 'typing_extensions', 'uarray', 'unittest', 'uri_template', 'urllib2', 'urllib3', 'urllib3_secure_extra', 'urlparse', 'usercustomize', 'version', 'vms_lib', 'wave', 'wcwidth', 'webbrowser', 'webcolors', 'win32api', 'win32clipboard', 'win32com', 'win32con', 'win32evtlog', 'win32evtlogutil', 'win32pdh', 'win32security', 'win32trace', 'win32traceutil', 'win32ui', 'winerror', 'wx', 'xdrlib', 'xlrd', 'xlsxwriter', 'xmlrpc', 'xmlrpclib', 'yaml', 'yapf', 'zmq', 'zstandard'],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION')],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
