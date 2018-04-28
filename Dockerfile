FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN pip install -r req.txt
ENTRYPOINT ["python"]
CMD ["app.py"] 
