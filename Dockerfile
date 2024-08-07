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
ENV REMOVE_DEFAULTS="720p, WEB, h264, H264, HDTV, x264"
ENV CLEANERS_DEFAULTS=tv
ENV UNSORTED=False
ENV JELLYFIN_URL=
ENV USER_NAME=
ENV PASSWORD=
ENV LIVE_TV=False
ENV EPG_URL=
ENV REFRESH_LIB=False
ENV CLEAN_SYNC=False
ENV SERVER_NAME=EZPZTV
ENV API_KEY=
ENV APP_VERSION=m3uparser


RUN chmod +x entrypoint.sh && chmod +x /usr/src/app/parser/parser_script.py



ENTRYPOINT ["./entrypoint.sh"]
