FROM python:3.10.0-alpine3.15
WORKDIR /app
COPY ./chat-maker-chat-app/chat-app/ /app
# TODO remove it after switch to database
COPY ./data/ /app/data
RUN pip install --no-cache-dir --upgrade /app
CMD ["uvicorn", "chat_app:app", "--host", "0.0.0.0", "--port", "8000"]
