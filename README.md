# Frequência QR

Sistema simples de **controle de ponto por QR Code** feito com **Django** e empacotado com **Docker**.  
Permite registrar **entrada** e **saída** com leitura de QR, calcular **horas trabalhadas** e exportar **CSV** — com uma interface limpa e corporativa.

---

## 📌 Funcionalidades

- **QR Code diário** (token único por dia).
- **Entrada / Saída**: 1ª leitura registra **entrada**; 2ª leitura registra **saída**.
- **Cadastro automático** por **CPF** (Nome no primeiro acesso).
- **Normalização do CPF**: aceita com/sem máscara; **armazena só dígitos**.
- **ID do funcionário** = **5 últimos dígitos** do CPF (sincronizado automaticamente).
- **Cálculo de horas trabalhadas** (diferença entre saída e entrada).
- **Dashboard do dia** com busca por nome e **Exportar CSV**.
- **UI corporativa** com Tailwind (CDN).

---

## 🧱 Tecnologias

- **Django 5** (Python)
- **SQLite** (desenvolvimento)
- **Docker + Docker Compose**
- **Tailwind CSS** (CDN)
- **qrcode** (geração do QR)

---

## 🗺️ Fluxo de funcionamento

1. Acesse **`/session/new/`** para gerar o **QR do dia**.  
2. O colaborador **escaneia** o QR e abre **`/s/<token>/`**:
   - 1ª batida (CPF + Nome no primeiro acesso) → **Entrada**  
   - 2ª batida (mesmo CPF) → **Saída**
3. Acompanhe em **`/dashboard/`** (total do dia, busca, **Exportar CSV**).

> **Obs.:** O QR é válido **somente no dia** da sessão.

---

## 🚀 Como rodar (Docker)

### Pré-requisitos
- **Docker** e **Docker Compose** instalados
- Porta **8000** livre

### 1) Criar `.env`
Crie o arquivo `.env` na raiz do projeto:

```env
DJANGO_SECRET_KEY=dev-secret-change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
TIME_ZONE=America/Fortaleza
```
### 2) Build & Up

```
docker compose build
```
```
docker compose up
```
Acesse no computador
```
http://localhost:8000/
```
### 3) Testar com o celular (mesma rede Wi-Fi)
- 1 Descubra o IP do seu computador (Windows/PowerShell) e anote o IPv4 (ex.: 192.168.0.110)
```
ipconfig
```
- 2 Abra o QR pelo IP (não use localhost):
```
http://SEU_IP:8000/session/new/
```
- 3 Escaneie com o celular e preencha CPF e Nome Completo
   - 1° batida → Entrada
   - 2° batida → Saída

### 🗂️ Estrutura do projeto
```
🗂️attendance/
  🗂️templates/attendance/
      base.html
      kiosk.html
      scan.html
      dashboard.html
  🗂️templatetags/
      __init__.py
      attendance_extras.py   # cpf_mask, duration_hhmm, etc.
      models.py
      views.py
      urls.py
🗂️freqqr/
  settings.py
  urls.py
Dockerfile
docker-compose.yml
manage.py
.env
``` 

### 🛠️ Dicas & Troubleshooting

- QR não abre no celular → Gere o QR acessando /session/new/ pelo IP (não localhost) e confirme que PC e celular estão na mesma rede. Libere a porta 8000 no firewall.
- CPF duplicado → O CPF é chave do funcionário; normalize sempre (o backend já faz).
- Horas com microssegundos → Os templates usam filtro duration_hhmm (sem microssegundos).


