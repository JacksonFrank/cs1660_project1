FROM sonarqube
COPY ./sonar-scanner-cli-4.6.2.2472-linux/ .
RUN echo "sonar.forceAuthentication=false" >> conf/sonar.properties && \
    apk add curl
CMD /opt/sonarqube/sonar-scanner-4.6.2.2472-linux/bin/sonar-scanner & \
    /opt/sonarqube/bin/run.sh