FROM python:3.10.0-alpine3.15
WORKDIR /app
COPY ./chat-maker-chat-app/websocket-service/ /app

COPY ./chat-maker-chat-app/commons/ /commons
COPY ./chat-maker-chat-app/auth-service/ /auth-service
COPY ./chat-maker-chat-app/user-service/ /user-service
COPY ./chat-maker-chat-app/chat-service/ /chat-service

# TODO remove it after switch to database
COPY ./data/ /data

RUN pip install --no-cache-dir --upgrade /app

# TODO remove when poetry be setup
RUN pip install --no-cache-dir --upgrade /commons
RUN pip install --no-cache-dir --upgrade /auth-service
RUN pip install --no-cache-dir --upgrade /user-service
RUN pip install --no-cache-dir --upgrade /chat-service

CMD python3 ./websocket_service/app.py
