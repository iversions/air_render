FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH=”$VIRTUAL_ENV/bin:$PATH”

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./ /code

CMD ["python", "/code/main_airline.py"]
