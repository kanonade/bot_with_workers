FROM rabbitmq:management

ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

COPY init.sh /init.sh
RUN chmod +x /init.sh

CMD ["/init.sh"]