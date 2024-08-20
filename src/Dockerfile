FROM ubuntu:20.04
RUN apt-get update; \
    apt-get install -y gcc python3; \
    apt-get install -y python3-pip; \
    apt-get install -y ca-certificates; \
    apt-get clean all
RUN pip3 install --upgrade pip; \
    pip3 install --upgrade urllib3[secure]; \
    pip3 install ansible; \
    pip3 install jinja2-ansible-filters; \
    pip3 install requests; \
    pip3 install pandas; \ 
    pip3 install json_normalize; \
    pip3 install json; \
    pip3 install datetime; \
    pip3 install sys; \
    pip3 install argparse; \
    pip3 install subprocess; \
    pip3 install os; \
    pip3 install sys
