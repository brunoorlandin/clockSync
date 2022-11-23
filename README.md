# Sincronização de Sistemas

## Dupla
- Bruno Vallone Orlandin R.A.: 22.219.032-4
- Eiji Kasai Dogen R.A.: 22.219.027-4

## Descrição 📌 <a name="description"></a>
Projeto desenvolvido para a disciplina CC7261 - Sistemas Distribuídos do Centro Universitário FEI, onde o objetivo é demonstrar a sincronização do horários sistemas, adotando o algoritmo para Berkeley para inspiração do projeto.

O projeto tem um processo responsável, chamada neste projeto de serverPython, que fica escutando requisições de outros processos para receber a temperatura junto com o tempo enviado, caso haja uma diferença de 1 segundo entre o processo responsável e processo que enviou a temperatura, é iniciado a sincronização, onde o processo responsável coleta os horário de cada processo, sincronizando-os e enviando de volta o horário sincronizado a ser atualizado nos outros processos.

# Instruções para rodar
## Clone este repositório
```bash
git clone https://github.com/brunoorlandin/clockSync.git
```
## Acesse o diretório
```bash
cd clockSync
```

Para os testes, alterar as linhas 175 e 176 do serverPython.py para os ips das máquinas na rede local da qual queira rodar. O processo da linha 175 é referente ao processo do Java (Client.java) e o processo da linha 176 é o processo c++ (client.cpp.)

No arquivo Client.java alterar na linha 18 para o ip da máquina em que será rodado o processo responsável (serverPython.py). Também no arquivo Client.java alterar na linha 22 o ip para o ip da máquina executara o processo java.

No arquivo client.cpp, na linha 48 alterar ip para o ip de rede da máquina que rodará o processo responsável (serverPython.py)

## Executar processos
Em linhas de comando separadas executar

```bash
python serverPython.py
```
```bash
python clientPython.py
```
```bash
java Client.java
```
```bash
g++ -std=c++11 -pthread client.cpp -o client
./client
```
--- 
Licença MIT ©