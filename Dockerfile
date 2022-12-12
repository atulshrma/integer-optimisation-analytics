
FROM python:3.10
WORKDIR /app
COPY ./requirements/base.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app
RUN pytest
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80