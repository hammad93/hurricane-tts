FROM python:3.10

ARG AZURE_OPENAI_API_KEY
ENV AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY

ARG AZURE_REDIS_KEY
ENV AZURE_REDIS_KEY=$AZURE_REDIS_KEY

# Entrypoint
ADD entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
ENTRYPOINT /root/entrypoint.sh