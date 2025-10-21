FROM python:3.11
WORKDIR /caml
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "slep.py"]
