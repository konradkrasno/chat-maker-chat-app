FROM python:3.10.0-alpine3.15
WORKDIR /app
COPY ./chat-maker-chat-app/user-service/ /app
COPY ./chat-maker-chat-app/commons/ /commons
# TODO remove it after switch to database
COPY ./data/ /app/data
RUN pip install --no-cache-dir --upgrade /app
RUN pip install --no-cache-dir --upgrade /commons
CMD python3 ./user_service/app.py
