# Day 10
AWS S3 Bucket Copy Script using Docker File

This app is Containerized with Docker. The container will take the names of two AWS S3 buckets in a single region (e.g. us-east-1) and a threshold size in MB. Arguments that will be passed on to the Python application that can copy all files greater than the threshold size from one bucket to another.

Docker Image
Click the link to get an Image of the app from dockerhub. Docker-Image
Or enter this in the commandline: docker pull awiley/technical-assignment
Instructions
Copy the Docker image to your computer.

Open a docker teminal (im using Docker toolbox) and enter the following in the terminal:

Replace keys with your own keys

This command will create and run a Docker container and pass your AWS s3 access keys at the runtime as environment variables

docker run -e AWS_ACCESS_KEY_ID=your-key-id
-e AWS_SECRET_ACCESS_KEY=your-secret-key -it awiley/technical-assignment
Once the Container is runing it will prompt for three arguments:

Enter source bucket name: 

Enter destination bucket name: 

Enter threshold size in MB: 

Once the app runs it will tell you how many files were transfered and the container will stop running.
