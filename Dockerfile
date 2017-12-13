FROM python:3.6.3
MAINTAINER Gabriel Seixas <salesseixasgabriel@gmail.com>

RUN apt-get update
RUN apt-get -y install curl

# Install Chrome for Selenium
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

# Install chromedriver for Selenium
RUN curl http://ftp.us.debian.org/debian/pool/main/c/chromium-browser/chromedriver_57.0.2987.98-1~deb8u1_amd64.deb -o /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

WORKDIR /balder

COPY . /balder 
