FROM python:3.9

WORKDIR /app

RUN apt-get update

# camelot dependencies
RUN apt-get install libgl1 -y
RUN apt-get install ghostscript python3-tk -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP="./main.py"
COPY . /app
EXPOSE 5000
CMD ["flask", "run","--host","0.0.0.0","--port","5000"]