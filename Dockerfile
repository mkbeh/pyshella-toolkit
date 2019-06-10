FROM python:3.7.3

WORKDIR /pyshella-toolkit
#RUN apt-get update
COPY . .
RUN mkdir -p ~/.local/share/pyshella-toolkit
CMD ["./toolkit.sh"]
