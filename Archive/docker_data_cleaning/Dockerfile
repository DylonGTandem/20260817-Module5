FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY 03_LibrarySystembook.csv .
COPY 03_LibrarySystemCustomers.csv .
COPY library_cleaning_app.py /app
ENTRYPOINT ["python3","library_cleaning_app.py"]