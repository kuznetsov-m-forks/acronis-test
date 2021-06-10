# Image Rotator

This is a simple service, which allows to send, rotate and download images.

## Before Started

You will need [Docker](https://docs.docker.com/get-docker/) to run it. Install last version depending from your OS. After installation just clone this repository.

### Starting

First, create a `.env` file in repository directory and put some secret key into.
IMPORTANT: Make own unique secret key.

```
SECRET_KEY=somesupersecretkey
```

Start building the image in terminal.
NOTE: This point `.` on end is important, it's a link to Dockerfile.

```
docker build -t rotator .
```

And run the container.

```
docker run -it -p 8000:8000 rotator
```

Great, now rotator is available in your web-browser. 
NOTE: if your docker service runs on virtual machine, you must use VM ip instead `localhost`.

```
localhost:8000 OR 127.0.0.1:8000
```

## Built With

* [Flask 2.0](https://palletsprojects.com/p/flask/) - lightweight WSGI web application framework
* [Pillow 8](https://python-pillow.org/) - Python Imaging Library

## Author

* **[Andrew Smelov](https://github.com/IzmdI)**

## License

This project is licensed under the MIT License - see the LICENSE.md file for details