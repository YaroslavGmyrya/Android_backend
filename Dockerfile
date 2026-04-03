FROM python:3.11.14-alpine

COPY android_server.py .

EXPOSE 3500

CMD ["python", "android_server.py"]
