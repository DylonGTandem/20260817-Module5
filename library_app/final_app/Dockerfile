FROM python:3.12-slim
WORKDIR /app
COPY ../../req.txt .
RUN pip install -r req.txt
COPY 03_LibrarySystembook.csv .
COPY 03_LibrarySystemCustomers.csv .
COPY library_cleaning_app.py /app
VOLUME ["/data"]
ENTRYPOINT ["python3","library_cleaning_app.py"]