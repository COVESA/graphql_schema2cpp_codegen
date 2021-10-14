# Installation of utilities

## Git Hooks

The git hooks will prevent the commit or push of files that do not comply
with some criteria.

Sample files are located at `.git/hooks` with `.sample` extension and are not
read.

The hook files of this project are located at `utils/git`. They
can be installed with by executing the script `./git/install-git-hooks.sh`
that will create a symbolic link at `.git/hooks` to this files.

## Doctests

The `doctest` module belongs to Python standard library. To perform a doctest
on a `.py` file, write a doctest file (`.md` or `.txt`) in some directory named
`tests` or `doctests` in the root directory of its package or subpackage. The
first line of the doctest must be `# relative_path_to/script.py` indicating to
which file it refers to. The path to the file is relative to the root of the
package or subpackage. For example, the doctest of
```bash
vss_deploy/model/deploy.py
```
may be a doctest file:
```bash
vss_deploy/doctest/deploy_doctest.txt
```
that contains in the first line:
```bash
# vss_deploy/model/deploy.py
```
