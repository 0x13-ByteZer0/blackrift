# blackRIFT

<p align="center">
  <img src="assets/blackrift-banner.svg" alt="blackRIFT banner" width="900">
</p>

blackRIFT é uma ferramenta de avaliação focada no vetor "NGINX Rift". Ela automatiza
verificações de leitura remota de arquivos via HTTP para detectar cadeias de exploração
e, opcionalmente, caminhos de exploração integrados (exploit), quando autorizado.

ATENÇÃO: use apenas contra alvos que você possui ou para os quais tem autorização explícita.

## Sumário
- **Requisitos**
- **Instalação rápida**
- **Uso básico**
- **Fan-out (subfinder)**
- **Arquivo de targets (`--targets-file`)**
- **Parâmetros úteis**
- **Saída / Artefatos**
- **Avisos de segurança**
- **Contribuição e contato**

## Requisitos
- Python 3.10 ou superior (o script usa apenas a biblioteca padrão).
- `subfinder` (opcional, recomendado para descoberta de subdomínios).
- Acesso de rede aos alvos a serem avaliados.

### Instalar o `subfinder` (opcional)
Se você tem o Go instalado, instale via:

```powershell
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
# assegure que %USERPROFILE%\go\bin esteja no PATH
```

Também é possível baixar binários em:
https://github.com/projectdiscovery/subfinder/releases

## Instalação rápida
```powershell
git clone https://github.com/0x13-ByteZer0/blackrift.git
cd blackrift
# (opcional) criar e ativar venv no Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# não há dependências Python externas; o script usa apenas a biblioteca padrão
python -V
```

## Uso básico
- Avaliar um alvo único (porta explícita):

```powershell
python blackRIFT.py --target 127.0.0.1:19321
```

- Avaliar um domínio (o script poderá executar `subfinder` automaticamente se apropriado):

```powershell
## Instalação rápida

### Windows (PowerShell)
```powershell
git clone https://github.com/0x13-ByteZer0/blackrift.git
cd blackrift
# (opcional) criar + ativar venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -V
```

### Linux / macOS (bash)
```bash
git clone https://github.com/0x13-ByteZer0/blackrift.git
cd blackrift
# (opcional) criar + ativar venv
python3 -m venv .venv
source .venv/bin/activate
python3 -V
```
python blackRIFT.py --target example.com --scheme https --port 443

## Fan-out com `subfinder`
O `subfinder` é usado para descobrir subdomínios quando `--target` for um domínio.
## Uso básico
- Avaliar um alvo único (porta explícita)

Windows (PowerShell):
```powershell
python blackRIFT.py --target 127.0.0.1:19321
```

Linux/macOS (bash):
```bash
python3 blackRIFT.py --target 127.0.0.1:19321
```
- Avaliar um domínio (o script poderá executar `subfinder` automaticamente se apropriado):

Windows (PowerShell):
```powershell
python blackRIFT.py --target example.com --scheme https --port 443
```

Linux/macOS (bash):
```bash
python3 blackRIFT.py --target example.com --scheme https --port 443
```

- Forçar execução do `subfinder`:

Windows (PowerShell) — forçar execução do `subfinder`:

```powershell
python blackRIFT.py --target example.com --subfinder --subfinder-output scans/subfinder_example.txt
```

Linux/macOS (bash) — forçar execução do `subfinder`:

```bash
python3 blackRIFT.py --target example.com --subfinder --subfinder-output scans/subfinder_example.txt
```
python blackRIFT.py --target example.com --subfinder --subfinder-output scans/subfinder_example.txt
```

Desabilitar a descoberta automática (avaliar somente o `--target` passado):

Windows (PowerShell):
```powershell
python blackRIFT.py --target example.com --no-subfinder
```

Linux/macOS (bash):
```bash
python3 blackRIFT.py --target example.com --no-subfinder
```

```powershell
python blackRIFT.py --target example.com --no-subfinder
Limitar hosts descobertos e tempo:

Windows (PowerShell):
```powershell
python blackRIFT.py --target example.com --subfinder-max-hosts 30 --subfinder-timeout 120
```

Linux/macOS (bash):
```bash
python3 blackRIFT.py --target example.com --subfinder-max-hosts 30 --subfinder-timeout 120
```

- Limitar hosts descobertos e tempo:

Se preferir só descobrir subdomínios sem rodar as avaliações, execute `subfinder` diretamente:

Windows / Linux / macOS:
```bash
subfinder -d example.com -all -silent > scans/subfinder_only.txt
```
```powershell
python blackRIFT.py --target example.com --subfinder-max-hosts 30 --subfinder-timeout 120
```

Se preferir só descobrir subdomínios sem rodar as avaliações, execute `subfinder` diretamente:

## Processar múltiplos alvos: `--targets-file`
Você pode passar um arquivo de texto com um alvo por linha (formato `host[:port]`). Linhas começando com `#` são ignoradas.

Exemplo: `scans/targets.txt`

```
# exemplo de targets
example.com
api.example.com:443
192.0.2.5:19321
```

Rodar diretamente com o argumento `--targets-file` (cross-platform):

Windows (PowerShell):
```powershell
python blackRIFT.py --targets-file scans/targets.txt
```

Linux/macOS (bash):
```bash
python3 blackRIFT.py --targets-file scans/targets.txt
```

Ou usar os scripts auxiliares incluídos em `scripts/` (conveniência):

Windows (PowerShell):
```powershell
.\scripts\run_targets.ps1 -TargetsFile scans/targets.txt
```

Linux/macOS (bash):
```bash
bash scripts/run_targets.sh scans/targets.txt
# ou tornar executável
chmod +x scripts/run_targets.sh
./scripts/run_targets.sh scans/targets.txt
```

O script processa cada linha sequencialmente; para domínios ele aplica a mesma política de `subfinder` por alvo (use `--no-subfinder` para desabilitar a descoberta).
```powershell
subfinder -d example.com -all -silent > scans/subfinder_only.txt
```

## Processar múltiplos alvos: `--targets-file`
Você pode passar um arquivo de texto com um alvo por linha (formato `host[:port]`).
Linhas começando com `#` são ignoradas.

Exemplo: `scans/targets.txt`

```
# exemplo de targets
example.com
api.example.com:443
192.0.2.5:19321
```

Rodar:

```powershell
python blackRIFT.py --targets-file scans/targets.txt
```

O script processa cada linha sequencialmente; para domínios ele aplica a mesma
política de `subfinder` por alvo (use `--no-subfinder` para desabilitar a descoberta).

## Parâmetros importantes
- `--target HOST[:PORT]` — host único ou domínio.
- `--targets-file PATH` — arquivo com alvos, um por linha.
- `--subfinder` / `--no-subfinder` — ligar/desligar descoberta automática.
- `--subfinder-output PATH` — grava lista descoberta.
- `--subfinder-max-hosts N` — limite de hosts para avaliar.
- `--subfinder-timeout N` — timeout (segundos) do `subfinder`.
- `--artifact-dir DIR` — diretório para artefatos JSON (default: `artifacts`).
- `--exploit --cmd "..."` — modo de exploração (destrutivo); exigido `--allow-multi-exploit` em fan-out.
- `--allow-multi-exploit` — permite `--exploit` em modo fan-out (use com extremo cuidado).
- `-h, --help` e `--advanced-help` — ajuda e opções avançadas.

Consulte a saída de `python blackRIFT.py -h` para a lista completa de flags.

## Saída / Artefatos
- Por padrão, cada avaliação gera um artifact JSON em `artifacts/` (nomeado por host/porta).
- O `--subfinder-output` grava a lista de hosts descoberta (útil para auditoria manual).

## Avisos de segurança e autorização
- Nunca execute `--exploit` contra alvos sem permissão explícita — isto é ilegal e perigoso.
- Em cenários de fan-out, recomenda-se apenas o uso em ambientes controlados de teste.

## Testes rápidos / Debug
- Mostrar ajuda (inclui banner):

```powershell
python blackRIFT.py -h
```

- Mostrar banner diretamente (test):

```powershell
python blackRIFT.py --target 127.0.0.1:19321 --no-subfinder
```

## Contribuição
- Pull requests, issues e correções são bem-vindas. Abra um issue descrevendo o problema antes de pull requests maiores.

## Contato
- Abra uma issue no repositório GitHub para reportar bugs ou discutir melhorias.

---
_Este README foi gerado e atualizado automaticamente. Se quiser, eu posso adicionar exemplos
de script PowerShell para rodar scans em lote ou integrar execução paralela._

## Processar múltiplos alvos (cross‑platform)

O `blackRIFT.py` oferece suporte nativo a processamento em lote através de `--targets-file` e
paralelismo via `--jobs` (ou `-j`). Use um arquivo com um alvo por linha (host[:port]).

Formato do arquivo de targets (`scans/targets.txt`):
```
# exemplo de targets
example.com
api.example.com:443
192.0.2.5:19321
```

Exemplos (Windows PowerShell):

```powershell
python blackRIFT.py --targets-file scans/targets.txt
python blackRIFT.py --targets-file scans/targets.txt --jobs 4
```

Exemplos (Linux / macOS - bash):

```bash
python3 blackRIFT.py --targets-file scans/targets.txt
python3 blackRIFT.py --targets-file scans/targets.txt --jobs 4
```

Se quiser que o `--subfinder-output` gere um arquivo por host, use placeholders `{host}` ou
`{safe_host}` (o helper interno expande automaticamente `{safe_host}` para um nome de
arquivo seguro).

O comportamento padrão é processar alvos sequencialmente; passe `--jobs N` para executar
até N processos simultâneos, cada um invocando `blackRIFT.py --target <host[:port]>`.



