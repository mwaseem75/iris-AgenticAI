ARG IMAGE=intersystemsdc/iris-community:latest
FROM $IMAGE 

WORKDIR /irisdev/app

ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD "SYS"
ENV IRISNAMESPACE "USER"

ENV PYTHON_PATH=/usr/irissys/bin/
ENV LD_LIBRARY_PATH=${ISC_PACKAGE_INSTALLDIR}/bin:${LD_LIBRARY_PATH}

ENV PATH "/home/irisowner/.local/bin:/usr/irissys/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/irisowner/bin"

COPY . .

RUN pip3 install -r requirements.txt

RUN iris start IRIS \
	&& iris session IRIS < iris.script \
    && iris stop IRIS quietly

#ENTRYPOINT ["uv", "run", "python", "/irisdev/app/src/python/aai/runMCPServer.py"]