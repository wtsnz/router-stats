# router-stats

I've wanted to graph my adsl line stats for a while now. After tweaking the SNR ratios on my router I've wanted to keep an eye out on the line stats to ensure my line stays reliable.

This is a little script that connects to my NETGEAR DGND3700v2 via telnet, grabs the adsl line stats, and finally sends them to a statsd server that I've got running.

This project requires python 2.7.

## Installation

Clone the repository and run the stats.py

    git clone https://github.com/wtsnz/router-stats.git
    cd router-stats
    chmod +x stats.py

## Usage

Before you run the script you will have to enable debug mode on your modem. You can do this by visiting this url in your browser.

    http://10.0.0.1/setup.cgi?todo=debug

Once you've done that you can execute the script. Make sure you're username and password are correct as there is no error handling. It either works or crashes 🙃

    $ ./stats.py --router 10.0.0.1 --username admin --password password --statsd-server server.com --statsd-port 1234
    Max Upstream: 1045
    Max Downstream: 16624
    Bearer Upstream: 1045
    Bearer Downstream: 21847
    SNR up: 13.1
    SNR down: 0.8
    ATTN up: 12.6
    ATTN down: 20.5
    PWR up: 12.1
    PWR down: 18.6
    done
    $
