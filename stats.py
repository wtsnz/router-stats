#!/usr/bin/python

import sys
import telnetlib
import time
import socket
import getopt

def main(argv):

    router_ip_address = ""
    router_username = ""
    router_password = ""

    statsd_server = ""
    statsd_port = 0

    try:
        opts, args = getopt.getopt(argv, '', ['router=', 'username=', 'password=', 'statsd-server=', 'statsd-port='])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('--router'):
            router_ip_address = arg
        elif opt in ('--username'):
            router_username = arg
        elif opt in ('--password'):
            router_password = arg
        elif opt in ('--statsd-server'):
            statsd_server = arg
        elif opt in ('--statsd-port'):
            statsd_port = int(arg)

    # Connect to the Router
    tn = telnetlib.Telnet(router_ip_address)
    tn.read_until("DGND3700v2 login: ")
    tn.write(router_username + "\n")
    tn.read_until("Password: ")
    tn.write(router_password + "\n")
    tn.read_until("# ")
    tn.write("adslctl info --show\n")

    # Parse the lines
    t = tn.read_until("# ")
    #print(t)
    lines = t.splitlines()

    # Close the connection
    tn.close()

    # return lines

    # Parse the upstream rate & downstream rate
    max_rates = lines[5].split()
    max_upstream_rate = max_rates[4]
    max_downstream_rate = max_rates[9]

    # Parse the bearer upstream & downstream rate
    bearer_rates = lines[6].split()
    bearer_upstream_rate = bearer_rates[5]
    bearer_downstream_rate = bearer_rates[10]

    # Parse SNR
    snr = lines[15].split()
    snr_down = snr[2]
    snr_up = snr[3]

    # Parse ATTN
    attn = lines[16].split()
    attn_down = attn[1]
    attn_up = attn[2]

    # Parse PWR
    pwr = lines[17].split()
    pwr_down = pwr[1]
    pwr_up = pwr[2]

    # Print the stats (useful for logging)

    print("Max Upstream: " + max_upstream_rate)
    print("Max Downstream: " + max_downstream_rate)
    print("Bearer Upstream: " + bearer_upstream_rate)
    print("Bearer Downstream: " + bearer_downstream_rate)
    print("SNR up: " + snr_up)
    print("SNR down: " + snr_down)
    print("ATTN up: " + attn_up)
    print("ATTN down: " + attn_down)
    print("PWR up: " + pwr_up)
    print("PWR down: " + pwr_down)


    # Connect to the server and send the packet

    UDP_IP = statsd_server
    UDP_PORT = statsd_port

    sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP

    MESSAGE = "router_max_upstream_rate:" + max_upstream_rate + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    MESSAGE = "router_max_downstream_rate:" + max_downstream_rate + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    MESSAGE = "router_bearer_upstream_rate:" + bearer_upstream_rate + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    MESSAGE = "router_bearer_downstream_rate:" + bearer_downstream_rate + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    MESSAGE = "router.snr_up:" + snr_up + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    MESSAGE = "router.snr_down:" + snr_down + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    MESSAGE = "router.attn_up:" + attn_up + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    MESSAGE = "router.attn_down:" + attn_down + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    MESSAGE = "router.pwr_up:" + pwr_up + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    MESSAGE = "router.pwr_down:" + pwr_down + "|g"
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


if __name__ == "__main__":
    main(sys.argv[1:])
    print("done")
