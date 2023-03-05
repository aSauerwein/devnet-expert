FROM python:3.9
ENV FLASK_HOST='0.0.0.0'
EXPOSE 5000
WORKDIR /opt/flask
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py
ENTRYPOINT ["/usr/local/bin/python"]
CMD ["/opt/flask/app.py"]