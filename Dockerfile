### DOCKERFILE MULTI-STAGE ###

# ---------- Image Timezone ----------
FROM amd64/python:3.9.6 AS timezone
ENV TZ 'America/Argentina/Buenos_Aires'
RUN echo $TZ > /etc/timezone && \
      apt-get update && apt-get install -y tzdata && \
      rm /etc/localtime && \
      ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
      dpkg-reconfigure -f noninteractive tzdata && \
      apt-get clean


# ---------- Requirements ----------
FROM timezone AS requirements
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt


# ---------- Final Build ----------
FROM requirements AS build
WORKDIR /app
COPY . .
EXPOSE 80
CMD ["sh","-c","python manage.py --migrate && uvicorn main:app --host 0.0.0.0 --port 80 --forwarded-allow-ips '*'"]
