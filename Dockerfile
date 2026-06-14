FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --no-cache-dir pytest

WORKDIR /site
COPY . /site

EXPOSE 8080
CMD ["python3", "scripts/run_all_validations.py"]
