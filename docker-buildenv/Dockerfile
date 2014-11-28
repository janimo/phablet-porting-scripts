# Set up an Ubuntu based environment suitable for building the Ubuntu Touch Android tree in
# If you have squid-deb-proxy installed on your host, it will get used in the container
# Build it and run it with your home dir bindmounted then run the build from your tree
# docker build --rm -t yourimagename .
# docker run -it -v /home/yourname/any/path:/home/developer yourimagename

FROM ubuntu:13.10

MAINTAINER Jani Monoses <jani@ubuntu.com>

RUN /sbin/ip route | awk '/default/ { print "Acquire::http::Proxy \"http://"$3":8000\";" }' > /etc/apt/apt.conf.d/30proxy

# Allow installing i386 debs required by some of the AOSP prebuilt tools

RUN dpkg --add-architecture i386

RUN apt-get update

RUN DEBIAN_FRONTEND='noninteractive' apt-get install -y cpp-4.8 ccache gcc-4.8 g++-4.8 git gnupg flex bison gperf build-essential \
  zip bzr curl libc6-dev libncurses5-dev:i386 x11proto-core-dev \
  libx11-dev:i386 libreadline6-dev:i386 libgl1-mesa-glx:i386 \
  libgl1-mesa-dev g++-multilib mingw32 ubuntu-dev-tools tofrodos \
  python-markdown libxml2-utils xsltproc zlib1g-dev:i386 schedtool bsdiff bash-completion vim

# Add default user
RUN adduser --disabled-password --quiet --gecos Developer developer

USER developer
ENV HOME /home/developer
WORKDIR /home/developer

CMD ["/bin/bash"]
