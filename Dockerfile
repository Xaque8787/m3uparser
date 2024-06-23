From python:3.8

WORKDIR /usr/src/app
RUN mkdir -p vars m3u VODS
COPY . .
# Environment variables
ENV HOURS=8
ENV M3U_URL=
ENV SCRUB_HEADER=
ENV REMOVE_TERMS=
ENV CLEANERS=
ENV LIVE_TV=false
ENV UNSORTED=false

RUN chmod +x run.sh && chmod +x entrypoint.sh && chmod +x moviemover.py && chmod +x unsortedmover.py && chmod +x write_vars.sh && chmod +x tvmover.py && chmod +x hours.sh && chmod u+w /usr/src/app/log_file.log



ENTRYPOINT ["./entrypoint.sh"]
