FROM continuumio/anaconda3

RUN mkdir -p /tstools
COPY ./Lib /tstools/Lib
COPY ./Test /tstools/Test

WORKDIR /tstools
RUN chmod +x Test/test.sh

ENTRYPOINT [ "/bin/bash"]