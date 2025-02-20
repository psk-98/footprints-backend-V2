# Welcome to My Footprints Backend

This backend is built using Django, a Python web framework for building web
applications. It also utilizes Django REST framework for creating APIs, Django
REST Knox for handling authentication, Cloudinary for hosting user-uploaded
media files and Docker for easier development and deployment on the cloud.

To get started, make sure you have Python and pip installed on your machine.
Then, clone the repository and run pip install -r requirements.txt to install
all of the dependencies.

To get started, make sure you have a [Stripe](https://stripe.com/) and
[Cloudinary](https://cloudinary.com/) account then also make sure you
have[Docker](https://www.docker.com/) and
[Docker Compose](https://docs.docker.com/compose/) installed on your machine.

Then run the following in your terminal(development) 
- cp .docker/app/Dockerfile.dev Dockerfile
-  cp .docker/app/docker-compose.dev.yml docker-compose.yml
- cp .env.examlpe.dev env #fill in the your keys
- docker-compose up --build
- docker-compose exec web bin/bash - python manage.py migrate.py #will add seeding at some point

Once the above is done, you should see the app on http://localhost:8000/

Please note that this is a mock store api, to see the front-end code go [here](https://github.com/psk-98/footprints) and to see it [live](https://footprints-lake.vercel.app)

Thank you for visiting my online backend! I hope you find it useful in building
your own project with similar stack.
