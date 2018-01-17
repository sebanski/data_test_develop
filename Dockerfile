FROM centos
MAINTAINER alex.balzer <sebanskimiami@gmail.com>

COPY . /opt/booj

RUN yum -y install epel-release && \
		yum -y install python-pip && \
		pip install -r /opt/booj/requirements.txt && \
		mkdir /opt/booj/output

ENTRYPOINT ["python /opt/booj/xml_parser.py --url-file /opt/booj/urls.txt --csv-out-dir /opt/booj/output/"]
