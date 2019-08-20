# This is the official Ananaconda Dockerfile maintained by ContinuumIO. At some point
# we will probably want to peg this to a specific version that TSTools supports
FROM continuumio/anaconda3

# Create a directory for our code
RUN mkdir -p /tstools

# Copy in the Library code
COPY ./python/src /tstools/src

# Copy in the test code
COPY ./python/tests /tstools/tests

# Tell Docker that we want to do the rest of our work from this directory
WORKDIR /tstools

# Copy in our test harness
COPY ./shell/python-tests.sh ./test.sh

# Make our test runner executable in the Docker container (not the local one)
RUN chmod +x ./test.sh

# Set Bash as our entry
ENTRYPOINT [ "/bin/bash" ]
