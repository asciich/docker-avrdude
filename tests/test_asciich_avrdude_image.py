import pytest

@pytest.fixture(scope='module')
def container_image():
    return 'asciich/avrdude'

class TestAsciichAvrdudeImage(object):

    def test_avrdude_installed(self, docker_container):
        assert docker_container.image.name == 'asciich/avrdude'
        assert docker_container.check_output('avrdude -h')
        assert docker_container.exists('avrdude')