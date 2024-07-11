FROM python:3

WORKDIR /usr/src/app
RUN mkdir -p VODS
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
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
ENV CLEANERS_DEFAULTS=tv,movies
ENV LIVE_TV=false
ENV UNSORTED=false

RUN chmod +x entrypoint.sh && chmod +x parser.py



ENTRYPOINT ["./entrypoint.sh"]
