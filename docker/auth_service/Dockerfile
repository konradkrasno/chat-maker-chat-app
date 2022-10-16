FROM python:3.10.0-alpine3.15
WORKDIR /app
COPY ./chat-maker-chat-app/auth-service/ /app
COPY ./chat-maker-chat-app/commons/ /commons
COPY ./chat-maker-chat-app/user-service/ /user-service
# TODO remove it after switch to database
COPY ./data/ /app/data
RUN pip install --no-cache-dir --upgrade /app
RUN pip install --no-cache-dir --upgrade /commons
RUN pip install --no-cache-dir --upgrade /user-service
CMD python3 ./auth_service/app.py
