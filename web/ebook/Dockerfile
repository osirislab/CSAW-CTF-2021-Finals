FROM surnet/alpine-python-wkhtmltopdf:3.7.3-0.12.5-small

RUN apk add --update --no-cache gcc alpine-sdk linux-headers

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./app .
COPY ./flag.txt /
COPY app.ini .
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

RUN echo -e "uwsgi\nuwsgi" | adduser uwsgi

RUN chown -R uwsgi:uwsgi /usr/src/app/DB

EXPOSE 5000
CMD ["uwsgi", "--ini", "app.ini"]