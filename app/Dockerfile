FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY templates templates
COPY static static
COPY app.py /app
COPY views.py /app
CMD python app.py
