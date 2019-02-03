### RPI LED CONTROLLER

Build with:
```
docker build -t led-control:latest .
```

Test with:
```
docker run --rm -it --privileged led-control:latest python3 /app/python/examples/test.py
docker run --rm -it --privileged led-control:latest python3 /app/app.py --test
```

TODOS
 * Implement automated testing
 * Fix led strip matrix mapping
 * Fix installation issue with rpi and sklearn
 * Organize source code into manageable files

Send to RPI
`
rm led.zip && zip -r led.zip led && echo 'put led.zip repos' | sftp rpi
`

On Rpi
`
rm -rf led* && unzip led.zip

cd led

sudo docker build -t led-control:latest .

sudo docker run --rm -it --privileged --mount type=bind,source=/home/pi/repos/led/app,target=/app led-control:latest python3 /app/animate.py /app/media/rainbow.pkl
`