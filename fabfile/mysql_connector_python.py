from fabric.api import local, lcd
from fabric.decorators import runs_once
import tempfile


DEFAULT_VERSION = "1.2.2"
BASE_FILENAME = "mysql-connector-python-{}.tar.gz"
BASE_DIRNAME = "mysql-connector-python-{}"
BASE_URL = "http://cdn.mysql.com//Downloads/Connector-Python/{}"


@runs_once
def install_mysql_connector_python(version=DEFAULT_VERSION):
    """
    Install mysql-connector-python-{} to the local system.
    fabric deploy command should call this command as

    >>> run("fab install_mysql_connector_python")

    """
    # create temporary directory
    tmpdir = tempfile.mkdtemp()

    filename = BASE_FILENAME.format(version)
    dirname = BASE_DIRNAME.format(version)
    url = BASE_URL.format(filename)

    with lcd(tmpdir):
        local("curl {} -o {}".format(url, filename))
        local("tar zxvf {}".format(filename))
        local("pip3 install ./{}".format(dirname))
    local("rm -rf {}".format(tmpdir))
