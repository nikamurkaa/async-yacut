FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=yacut

RUN groupadd --system yacut && \
    useradd --system --gid yacut --home-dir /app yacut

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .
RUN mkdir -p /app/data && chown -R yacut:yacut /app

USER yacut
EXPOSE 8000

ENTRYPOINT ["sh", "/app/infra/entrypoint.sh"]
