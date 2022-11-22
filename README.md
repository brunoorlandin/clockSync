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
--- 
Licença MIT ©