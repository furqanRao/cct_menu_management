How to setup this project
======================

1- Make sure Docker is running locally

2- Execute below command to set up the project:

    make dev.projectsetup

3- If you see the server still doesn't run, please execute these following commands:

    make dev.down
    make dev.start
    make dev.web.makemigrations   (run these commands in new tab)
    make dev.web.runmigrations
    make dev.web.createsuperuser

Now please check server by visiting the url http://0.0.0.0:8000/admin/.

**Note:**

For further Docker commands, please refer to Makefile in project.
These credentials are set as environment variables in Web Container in Docker Compose File.

You can now use this super user to create users/restaurants and daily menu using the postman's API collection.

Here's the [Postman Collection](https://www.getpostman.com/collections/650f4764e284b5b64740) for accessing API's, please import this collection to see how to use/access the API's.

Thank You.
