FROM python:3.7.3

WORKDIR /pyshella-toolkit
COPY . .
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY toolkit.conf /etc/supervisor/conf.d/toolkit.conf
CMD ["./toolkit.sh"]
