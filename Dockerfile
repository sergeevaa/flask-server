FROM ubuntu
RUN apt update
RUN apt install python3 python3-pip -y
RUN pip3 install flask
RUN pip3 install flask-restful
COPY . /web-server
EXPOSE 5001
CMD python3 /web-server/server.py