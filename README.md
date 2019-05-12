# RPI LED CONTROLLER


### Simple development

A problem I encountered a lot during this project was being able to quickly iterate on development.
To help solve this I created Docker images and unit tests that can be run separatley from a raspberry pi
to validate code before loading it onto the raspberry pi.

The led matrix takes simple numpy arrays similar to image data for values. Any animation generation can be simply tested by checking the incoming numpy data.

Build local image with:
```
./manage.sh build
```

Test locally with:
```
./manage.sh test
```


### Running on the RPI

Install packages on rpi:
```
sudo ./manage.sh install
```

#### Simple API

There is a simple JSON API to take an array of color data for web controled lighting.
This is a very simple and basic api that only handles RGB color arrays.

POSTing a array as JSON of shape (matrix_width, matrix_height, 3) of RGB data will control the matrix.

Run API:
```
sudo python3 -m app.web.web_api
```

There is a simple browser application to connect and control the led matrix in `app/web_client/`


TODOS:

- [ ] Adopt cairo as a 2d rendering library for advanced animations and remove custom canvas implementation
- [ ] Update pymunk implementation for simple and clean physics based animations
- [ ] Hook tetris engine into the led matrix
