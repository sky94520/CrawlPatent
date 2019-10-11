FROM python:3.7

VOLUME ['/code']
WORKDIR /code

COPY requirments.txt /code

RUN pip install -r requirments.txt

CMD python3 run_detail.py
