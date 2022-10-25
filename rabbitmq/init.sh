(rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user $BOT_USER $BOT_PASSWORD 2>/dev/null ; \
rabbitmqctl set_permissions -p / $BOT_USER  ".*" ".*" ".*" ; \
rabbitmqctl add_user $WORKER_USER $WORKER_PASSWORD 2>/dev/null ; \
rabbitmqctl set_permissions -p / $WORKER_USER  ".*" ".*" ".*") &

rabbitmq-server $@
