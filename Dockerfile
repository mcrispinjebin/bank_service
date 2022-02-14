FROM python:3

COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "4982"]
EXPOSE 4982