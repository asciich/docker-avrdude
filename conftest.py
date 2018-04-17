# conftest.py for docker image testing

import docker
import os
import pytest


class DockerContainerError(Exception):
    pass


class DockerContainerExecError(DockerContainerError):
    pass

class DockerContainerFile():

    def __init__(self, docker_container, path):
        self._docker_container = docker_container
        self._path = path

    def is_file(self):
        try:
            self._docker_container.check_output('test -f {}'.format(self._path))
            return True
        except DockerContainerExecError as e:
            pass

    def is_directory(self):
        try:
            self._docker_container.check_output('test -d {}'.format(self._path))
            return True
        except DockerContainerExecError as e:
            return False

class DockerContainer():

    def __init__(self, container_name):
        self.name = container_name
        self._client = docker.from_env()
        self._container = None

    def check_output(self, command):
        ret =  self._container.exec_run(command)
        if ret.exit_code != 0:
            raise DockerContainerExecError(ret.output)
        return ret.output

    def exists(self, command):
        """
        Implement command exists like testinfra: http://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.file.File
        :param command:
        :return:
        """
        environ_paths = self.get_env('PATH').split(':')
        for environ_path in environ_paths:
            binary_path = os.path.join(environ_path, command)
            if self.file(binary_path).is_file():
                return True
        return False

    def file(self, path):
        return DockerContainerFile(self, path)

    @property
    def default_command(self):
        return '/bin/sh -c "sleep 10000"'

    def get_env(self, env_name):
        """
        Get environment variable content
        :param env_name:
        :return:
        """
        return self.check_output('/bin/sh -c "echo ${}"'.format(env_name)).decode().strip()

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