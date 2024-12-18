FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements
COPY ./app /app
COPY ./scripts /scripts
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && \
    if [ $DEV = "true" ]; \
        then pip install --no-cache-dir -r /requirements/dev.txt ; \
    else \
        pip install --no-cache-dir -r /requirements/prod.txt ; \
    fi && \
    rm -rf /requirements && \
    apk --purge del .build-deps && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

CMD ["run.sh"]
