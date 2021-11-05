FROM tomcat:9.0

COPY ./ncWMS2.war /usr/local/tomcat/webapps
COPY ./tomcat-users.xml /usr/local/tomcat/conf
COPY ./ncWMS2.xml /usr/local/tomcat/conf/Catalina/localhost/ncWMS2.xml
RUN mkdir -p /data_s3/Archive

EXPOSE 8080