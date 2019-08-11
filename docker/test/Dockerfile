# This is the official Ananaconda Dockerfile maintained by ContinuumIO. At some point
# we will probably want to peg this to a specific version that TSTools supports
FROM continuumio/anaconda3

# Create a directory for our code
RUN mkdir -p /tstools

# Copy in the Library code
COPY ./Lib /tstools/Lib

# Copy in the test code
COPY ./Test /tstools/Test

# Tell Docker that we want to do the rest of our work from this directory
WORKDIR /tstools

# Make our test runner executable
RUN chmod +x Test/test.sh

# Set Bash as our entry
ENTRYPOINT [ "/bin/bash" ]