FROM python:3.14.6-slim-bookworm

WORKDIR /WealthManagement/WealthM

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
RUN chown -R appuser:appuser /WealthManagement/WealthM
USER appuser

ENV PORT=8080

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
