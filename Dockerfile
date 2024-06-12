From python:3.8

WORKDIR /usr/src/app

COPY . .
# Environment variables
ENV VOD_URL=
ENV HOURS=12

RUN chmod +x run.sh && chmod +x entrypoint.sh && chmod +x moviemover.py && chmod +x tvmover.py && chmod +x hours.sh && chmod u+w /usr/src/app/log_file.log



ENTRYPOINT ["./entrypoint.sh"]
