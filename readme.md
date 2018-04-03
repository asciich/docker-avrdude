# avrdude Container

This container contains avrdude used to programm microcontrollers.

## Start container

The container needs ```--privileged``` mode to be able to programm microcontrollers.
Starting the container with the command below will allow access to the current working directory in /local_dir/

```
docker run --rm --privileged -v $(pwd):/local_dir/ -it asciich/ubuntu_avrdude /bin/bash
```

## Test container

To test the container run tox in the toplevel directory of this repository.

```
tox
```