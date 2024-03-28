# Pull base image
FROM python:3.11.3

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/
WORKDIR /app/

RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --root-user-action=ignore --upgrade setuptools
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install --root-user-action=ignore -r /app/requirements.txt

EXPOSE 80