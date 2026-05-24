FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app", "--access-logfile", "-", "--error-logfile", "-"]