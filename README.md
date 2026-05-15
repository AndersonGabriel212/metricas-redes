Primeira Versão do Ambiente Experimental com Coleta
Dupla: Anderson Gabriel e João Coelho

**Inicial de Métricas**

Este documento apresenta todas as etapas funcionais realizadas para criação do ambiente experimental
utilizando Mininet, simulação de rede, coleta de métricas de QoS e preparação do dataset para o projeto de
predição de eventos de lag utilizando Machine Learning.

**1. Instalação dos Requisitos**

sudo apt update  <br>
sudo apt install -y mininet iperf3 python3-pip net-tools iproute2  <br>
sudo apt install -y python3-venv python3-full  <br>

**2. Criação do Ambiente Virtual Python**

python3 -m venv venv  <br>
source venv/bin/activate  <br>
pip install pandas scikit-learn matplotlib numpy  <br>

**3. Limpeza do Mininet**

sudo mn -c

**4. Código Funcional do Ambiente Experimental**

from mininet.net import Mininet  <br>
from mininet.link import TCLink  <br>
from mininet.cli import CLI  <br>
from mininet.log import setLogLevel  <br>


def topology():  <br>
net = Mininet(link=TCLink)  <br>
h1 = net.addHost('h1', ip='10.0.0.1/24')  <br>
h2 = net.addHost('h2', ip='10.0.0.2/24')  <br>
s1 = net.addSwitch('s1', failMode='standalone')  <br>
net.addLink(h1, s1, bw=10, delay='20ms', loss=1)  <br>
net.addLink(h2, s1, bw=10, delay='20ms', loss=1)  <br>
net.start()  <br>
net.pingAll()  <br>
CLI(net)  <br>
net.stop()  <br>

if __name__ == '__main__':  <br>
setLogLevel('info')  <br>
topology()5. Execução do Ambiente  <br>
sudo python3 experimento.py  <br>

**5. Resultado Esperado da Conectividade**

*** Ping: testing ping reachability  <br>
h1 -> h2  <br>
h2 -> h1  <br>
*** Results: 0% dropped  <br>

**6. Teste de Latência, Jitter e Perda de Pacotes**

mininet> h1 ping 10.0.0.2 -c 10

**7. Interpretação das Métricas**

Latência: Valor médio (avg) do ping.  <br>
Jitter: Valor mdev do ping.  <br>
Perda de Pacotes: Percentual packet loss.  <br>

**8. Teste de Throughput com iPerf3**
Dentro do Mininet:

**Servidor:**
mininet> h2 iperf3 -s &  <br>
**Cliente:**
mininet> h1 iperf3 -c 10.0.0.2  <br>

mininet> h1 python3 coleta_metricas.py  <br>

**9. Simulação de Cenários de Rede**
**Cenário Normal:**
delay='10ms'  <br>
loss=0  <br>
**Cenário Moderado:**
delay='80ms'  <br>
loss=2  <br>
**Cenário Severo:**
delay='200ms'  <br>
loss=10  <br>

**10. Simulação de Jitter Realista**

delay='80ms 20ms distribution normal'12. Código de Coleta Automática de Métricas
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
ping = subprocess.check_output(
"ping -c 10 10.0.0.2",
shell=True
).decode()
rtt = re.search(
r'=(.*?)/(.*?)/(.*?)/(.*?) ms',
ping
)
latencia = float(rtt.group(2))
jitter = float(rtt.group(4))
loss = re.search(
r'(\d+)% packet loss',
ping
)
perda = float(loss.group(1))
iperf = subprocess.check_output(
"iperf3 -c 10.0.0.2",
shell=True
).decode()
banda = re.findall(
r'(\d+\.\d+) Mbits/sec',
iperf
)
throughput = float(banda[-1])
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
print("Dataset criado")13. Execução da Coleta de Métricas
Dentro do Mininet:
Servidor:
mininet> h2 iperf3 -s &
Coleta:
mininet> h1 python3 coleta_metricas.py

**11. Resultado Esperado**

**Será gerado:**
dataset.csv  <br>
Exemplo:  <br>
latencia,jitter,packet_loss,throughput,classe  <br>
20,1.2,0,9.7,normal  <br>
85,8.1,2,8.4,moderado  <br>
205,30,11,2.1,severo  <br>


12. Objetivos Já Concluídos
- Ambiente experimental funcionando
- Simulação de rede no Mininet
- Coleta de métricas de QoS
- Simulação de latência e perda
- Geração inicial de dataset
- Preparação para treinamento de Machine Learning
