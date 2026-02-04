FROM ubuntu:20.04
RUN apt-get update; \
    apt-get install -y gcc python3; \
    apt-get install -y python3-pip; \
    apt-get install -y ca-certificates; \
    apt-get install -y curl; \
    apt-get install -y jq; \
    apt-get clean all
RUN mkdir -p export_location/
RUN pip3 install --upgrade pip; \
    pip3 install --upgrade urllib3[secure]
RUN pip3 install ansible
RUN pip3 install jinja2-ansible-filters
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install json_normalize; \
    pip3 install json; \
    pip3 install datetime; \
    pip3 install argparse; \
    pip3 install openpyxl; \
    pip3 install xlsxwriter
