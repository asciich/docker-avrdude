# conftest.py for docker image testing

# Setup minimal virtualenv for testing docker images

#  virtualenv ve_dockertest
#  source ./ve_dockertest/bin/activate
#  pip install pytest
#  pip install doc#

import docker
import pytest


class DockerContainerError(Exception):
    pass


class DockerContainer():

    def __init__(self, container_name):
        self.name = container_name
        self._client = docker.from_env()
        self._container = None

    def check_call(self, command):
        ret =  self.exec(command)
        if ret.exit_code == 0:
            return True
        raise DockerContainerError(ret.output)

    @property
    def default_command(self):
        return '/bin/sh -c "sleep 10000"'

    def exec(self, command):
        return self._container.exec_run(command)

    @property
    def id(self):
        return self._container.id

    def kill(self):
        self._container.kill()

    def run(self):
        self._container = self._client.containers.run(self.name, self.default_command, detach=True)


@pytest.fixture(scope='module')
def docker_container(container_name):
    docker_container = DockerContainer(container_name)
    docker_container.run()
    yield docker_container
    docker_container.kill()