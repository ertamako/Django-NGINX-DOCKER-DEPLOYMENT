FROM continuumio/miniconda3:4.8.2
LABEL maintainer="gu53jut@mytum.de"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
RUN echo "source activate ncnv" > ~/.bashrc
ENV PATH /opt/conda/envs/ncnv/bin:$PATH

# Copy Django Project files
RUN mkdir /cnv_proj
ADD ./cnv_proj /cnv_proj
WORKDIR /cnv_proj

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

COPY ./scripts /scripts
# RUN chmod +x /scripts/*

EXPOSE 8000

CMD ["/scripts/entrypoint.sh"]
#CMD ["/app/start-server.sh"]