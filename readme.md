# Basic discord bot + rabbitmq + workers

```bash
> echo "DISCORD_TOKEN=<bot-token>" > .env

> docker-compose up -d

> docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                   PORTS                                                                                                                                                 NAMES
0f9582c740d   discord-queue-bot      "python bot.py"          5 minutes ago   Up 5 minutes                                                                                                                                                                   dbot
cbf65dd4fc5   discord-queue-worker   "python /worker.py"      7 minutes ago   Up 7 minutes                                                                                                                                                                   worker
6388ca11528   rabbitmq:management           "docker-entrypoint.s…"   7 minutes ago   Up 7 minutes (healthy)   4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, :::5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp, :::15672->15672/tcp   rmq

> docker-compose logs -f        # and also send !draw a cat in discord
dbot    | Sent a cat to queue
worker  | Received a cat
worker  | Waiting random time to simulate work
worker  | Sent response for a cat

```

Also go to http://localhost:15672 and log in with guest/guest. You'll be able to see both queues, and also watch them fill/empty on a slight delay from real time.

### Scaling

To scale the workers, adjust the `worker.deploy.replicas` number in the `docker-compose.yml`.


### Warning

This repo is a proof-of-concept. It is not production-grade and lacks many things:

- It doesn't generate images, it has a placeholder for that logic
- Rabbitmq should be used in a high availability mode
- Quorum queues should be used instead of classic queues
- There is no authentication in front of the queues
- There is no database to store generated results
- Don't hardcode the queue names, use of an exclusive queue + reply_to for the return queue
- Docker-compose is not a production deployment tool

