FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/usr/src/app
# Environment variables
ENV HOURS=8
ENV M3U_URL=
ENV SCRUB_HEADER=
ENV REMOVE_TERMS=
ENV REPLACE_DEFAULTS="1/2=\u00BD, /=-"
ENV REPLACE_TERMS=
ENV CLEANERS=
ENV SCRUB_DEFAULTS="HD :, SD :"
ENV REMOVE_DEFAULTS="720p, WEB, h264, H264, HDTV, x264, 1080p, HEVC, x265, X265"
ENV CLEANERS_DEFAULTS=tv
ENV UNSORTED=False
ENV JELLYFIN_URL="http://10.21.12.8:8096"
ENV USER_NAME=
ENV PASSWORD=
ENV LIVE_TV=True
ENV EPG_URL=
ENV REFRESH_LIB=False
ENV CLEAN_SYNC=False
ENV SERVER_NAME=EZPZTV
ENV API_KEY=
ENV APP_VERSION=threadfin
ENV TF_HOST=10.21.12.9
ENV TF_PORT=34400
ENV TF_USER=
ENV TF_PASS=
ENV TF_URL=
ENV BYPASS_HEADER=

EXPOSE 2112

RUN chmod +x entrypoint.sh && chmod +x /usr/src/app/parser/parser_script.py && chmod +x /usr/src/app/parser/server_apk/apk.py



ENTRYPOINT ["./entrypoint.sh"]
