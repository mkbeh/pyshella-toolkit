FROM python:3.7.3

WORKDIR /pyshella-toolkit
COPY . .
RUN mkdir -p ~/.local/share/pyshella-toolkit
CMD ["./toolkit.sh"]
