FROM python:3.9.9

WORKDIR .
COPY cs_bot/ cs_bot/
COPY files/ files/
COPY main.py .
COPY .env .

COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
