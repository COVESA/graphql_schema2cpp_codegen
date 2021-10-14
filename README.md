# **GraphQL Schema To C++ Code Generator**

Generate resolver code for VSS GraphQL Schema and deploy map.

## **Getting Started**

For this project you will need to have:
- Python 3.8.5 or later
- Pip
- Pipenv


### **Python Installation On Linux (or mac)**

If you don't have Python installed already I suggest you to use
[pyenv](https://github.com/pyenv/pyenv#installation) to install Python by using
this following command:

```bash
pyenv install <desired py version>
```

Then in this repo's folder there should be a `.python-version` file that describes
the version of python to be used, in our repo there is this file with the version 3.8.5
written. If you want to create this file by yourself and use a specific version you can run:
```bash
pyenv local <desired py version>
```

### **Pip Installation on Linux**

Make sure you have pip installed too. To check you can run

```bash
python3 -m pip -V
```

and see the version of your pip. Make sure your pip is updated with

```bash
python3 -m pip install --upgrade pip
```

If you don't have you can install with
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
```

### **Pipenv Installation on Linux**

To install Pipenv just run
```bash
python3 -m pip install --user pipenv
```
And pipenv will be installed as a python package under the `--user` flag and you
will be able to run `python3 -m pipenv --help`.

It is a good practice to set on your `.bashrc` (or other, see note 2), the
variable which configures `PIPENV` to always create the virtual environment
inside a `.env` folder the project.

```bash
echo "export PIPENV_VENV_IN_PROJECT=1" >> ~/.bashrc
source ~/.bashrc
```

> **Note 1:**
> When you install pipenv using pip with `--user` flag, you are installing
> pipenv under a folder `.local` under your home directory, so if your system
> does not recognize pipenv as a command, it's maybe because your `$PATH`
> variable does not see this `.local` folder. One alternative is to add this
> line to your `.bashrc` (or similar please see note 2) file as follows:
> ```bash
> echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc
> source ~/.bashrc
> ```
> and you will be able to run pipenv directly. If you prefer you can always
> just use:
> ```bash
> python3 -m pipenv
> ```
> when you want to just run pipenv

> **Note 2:**
> Every time `.bashrc` is referred here in this file, we are talking about the
> file that runs when your terminal is open, this file may change depending on
> the system and what shell you are using, this may be `~/.bash_profile` or
> `./zsh`.

## **Installation of GraphQL Schema To C++ Code Generator**

To install the project and dependencies you can run the following command:

```bash
pipenv sync
```

This command will install this package and its dependencies under your pipenv
isolated environment (`.env` folder if you followed Note 1). Then you can run
commands of this environment with `pipenv run <command in environment>`.

## **Execution of GraphQL Schema To C++ Code Generator**

To run the program please `cd` to root path of this project and run:

```bash
pipenv run graphql_schema2cpp_codegen --help
```

and

```bash
pipenv run vssdeploy2json --help
```

## **Contribution to the Development of GraphQL Schema To C++ Code Generator**

To install dev packages one may run:

```bash
pipenv sync -d
```

### **Linting**

One may format with autopep8 with command-line:

```bash
autopep8 --in-place --aggressive --aggressive file.py
```

And to check linting you can run:

```bash
pipenv run flake8 --config setup.cfg file.py
```

### **Check Typing**

To use mypy you can run:

```bash
pipenv run mypy --config-file ./setup.cfg file.py
```

### **Tests**

To run nosetests you can run:

```bash
pipenv run nosetests --with-doctest file.py
```
