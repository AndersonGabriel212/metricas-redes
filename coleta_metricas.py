import subprocess
import csv
import re
import time

arquivo = open("dataset.csv", "w", newline='')

writer = csv.writer(arquivo)

writer.writerow([
    "latencia",
    "jitter",
    "packet_loss",
    "throughput",
    "classe"
])

for i in range(20):

    print(f"Coleta {i}")

    # PING
    ping = subprocess.check_output(
        "ping -c 10 10.0.0.2",
        shell=True
    ).decode()

    # LATENCIA/JITTER
    rtt = re.search(
        r'=(.*?)/(.*?)/(.*?)/(.*?) ms',
        ping
    )

    latencia = float(rtt.group(2))
    jitter = float(rtt.group(4))

    # PACKET LOSS
    loss = re.search(
        r'(\d+)% packet loss',
        ping
    )

    perda = float(loss.group(1))

    # THROUGHPUT
    iperf = subprocess.check_output(
        "iperf3 -c 10.0.0.2",
        shell=True
    ).decode()

    banda = re.findall(
        r'(\d+\.\d+) Mbits/sec',
        iperf
    )

    throughput = float(banda[-1])

    # CLASSIFICAÇÃO

    if latencia < 50:
        classe = "normal"

    elif latencia < 120:
        classe = "moderado"

    else:
        classe = "severo"

    writer.writerow([
        latencia,
        jitter,
        perda,
        throughput,
        classe
    ])

    time.sleep(2)

arquivo.close()

print("Dataset criado")
