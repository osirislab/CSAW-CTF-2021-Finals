FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive
ENV INSTALLHOME=/var/lib/vacation-planner
ENV INSTALLDIR=/var/lib/vacation-planner/timeoff-management-application

RUN apt-get update && apt-get install -y jq curl python
RUN adduser --shell /bin/bash --system --group --home "$INSTALLHOME" vacation

COPY timeoff-management-application $INSTALLDIR
COPY package-lock.json $INSTALLDIR
COPY start.sh $INSTALLDIR
COPY flag.txt $INSTALLDIR

RUN chown vacation:vacation -R "$INSTALLDIR"

USER vacation

RUN \
    chmod u+w -R "$INSTALLDIR" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" &&\
    nvm install 12 && \
    nvm alias default && \
    cd $INSTALLDIR && \
    rm -rf .git && \
    npm install --local

WORKDIR /var/lib/vacation-planner/timeoff-management-application

CMD ["/bin/bash", "start.sh"]
