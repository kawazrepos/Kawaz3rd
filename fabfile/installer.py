from fabric.api import run, cd, put, sudo
from fabric.contrib.files import exists, contains, append
from fabric.decorators import runs_once


@runs_once
def install():
    """Install environments"""
    install_requirements()
    install_pyenv()
    install_python()
    install_mysql_connector_python()
    install_kawaz()


@runs_once
def install_pyenv():
    """Install and configure the pyenv to make it ready"""
    # install pyenv via pyenv-installer
    run("curl -L "
        "https://raw.githubusercontent.com/yyuu/"
        "pyenv-installer/master/bin/pyenv-installer | bash")
    if not exists('~/.bash_profile_pyenv'):
        # push .bash_profile_pyenv
        import os
        base_dir = os.path.dirname(__file__)
        put(os.path.join(base_dir, 'statics', '.bash_profile_pyenv'),
            '~/.bash_profile_pyenv')
    if not contains('~/.bash_profile',
                    'source "$HOME/.bash_profile_pyenv"'):
        # add source line
        append('~/.bash_profile', 'source "$HOME/.bash_profile_pyenv"')


@runs_once
def install_python():
    run("pyenv install 3.4.0 --skip-existing")
    run("pyenv virtualenv 3.4.0 Kawaz --clear --force")
    run("pyenv global Kawaz")


@runs_once
def install_requirements():
    sudo("aptitude install -y git")
    # requirements of pyenv
    sudo("aptitude install -y "
         "make build-essential libssl-dev zlib1g-dev libbz2-dev "
         "libreadline-dev libsqlite3-dev wget curl llvm")
    # requirements of Pillow
    sudo("aptitude install -y "
         "libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev libwebp-dev"
         "libopenjpeg-dev")


@runs_once
def install_kawaz():
    if exists('~/Kawaz'):
        run("rm -rf ~/Kawaz")
    run("git clone https://github.com/kawazrepos/Kawaz3rd ~/Kawaz")
    with cd("~/Kawaz"):
        run("git pull --force")
        run("pip install 'django==1.6'")
        run("pip install -r requirements.txt")
        run("pip install -r requirements-test.txt")


@runs_once
def install_mysql_connector_python(version="1.2.2"):
    """
    Install mysql-connector-python to the local system.
    fabric deploy command should call this command as

    >>> run("fab install_mysql_connector_python")

    """
    import tempfile
    BASE_FILENAME = "mysql-connector-python-{}.tar.gz"
    BASE_DIRNAME = "mysql-connector-python-{}"
    BASE_URL = "http://cdn.mysql.com//Downloads/Connector-Python/{}"

    # create temporary directory
    tmpdir = tempfile.mkdtemp()

    filename = BASE_FILENAME.format(version)
    dirname = BASE_DIRNAME.format(version)
    url = BASE_URL.format(filename)

    with cd(tmpdir):
        run("curl {} -o {}".format(url, filename))
        run("tar zxvf {}".format(filename))
        run("pip install ./{}".format(dirname))
    run("rm -rf {}".format(tmpdir))
