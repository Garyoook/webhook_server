# An Util tool for various Webhook bot api from chatting apps

### Usage: 

set up environment variables: (use your own port and webhook api url)

    expot WEBHOOK_LISTEN_PORT=xxxx
    export DINGTALK_WEBHOOK_URL=xxxx
    the example gives a link of dingtalk, other webhooks (slack, Microsoft Teams, etc. can be set separately.)


then run the script
    
    python3 webhook_server.py

### Run with docker

Dockerfile provided, play as you wish.