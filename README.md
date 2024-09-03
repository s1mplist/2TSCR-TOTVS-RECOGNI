# Recogni
Challenge FIAP + TOTVS - Transcrição de Audio

Recogni é um projeto de transcrição de áudio que utiliza a biblioteca `faster-whisper` em Python para converter áudio em texto de forma eficiente, com suporte para modelos compilados usando `ctranslate2` para maximizar o desempenho em hardware compatível com aceleração de GPU.

## Índice

- [Introdução](#introdução)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
  - [Instalando CUDA no Windows (WSL)](#instalando-cuda-no-windows-wsl)
  - [Instalando CUDA no Ubuntu](#instalando-cuda-no-ubuntu)
  - [Instalando cuDNN](#instalando-cudnn)
  - [Configurando o projeto](#configurando-o-projeto)
- [Uso](#uso)
- [Métricas](#métricas)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Introdução

Recogni é uma ferramenta que permite transcrever áudio de forma rápida e precisa utilizando a biblioteca `faster-whisper`, uma alternativa otimizada para o Whisper da OpenAI. Para aumentar a eficiência, também é possível utilizar modelos compilados com `ctranslate2`.

## Pré-requisitos

- **Python** 3.8 ou superior
- **Pip** (gerenciador de pacotes do Python)
- **CUDA** Toolkit (11.0 ou superior)
- **cuDNN** (até a versão 8)
- Biblioteca **faster-whisper**
- Biblioteca **ctranslate2** (opcional, para uso de modelos compilados)

## Instalação

### Instalando CUDA no Windows (WSL)

1. Instale o WSL 2 (Windows Subsystem for Linux) se ainda não estiver configurado:
   - Abra o PowerShell como administrador e execute:
     ```sh
     wsl --install
     ```
   - Reinicie o computador se necessário.

2. Escolha a distribuição Linux (por exemplo, Ubuntu) e instale-a.

3. Instale o CUDA Toolkit:
   - Abra o terminal WSL e adicione o repositório da NVIDIA:
     ```sh
     wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
     sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
     sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
     sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
     sudo apt-get update
     sudo apt-get -y install cuda
     ```

4. Verifique a instalação do CUDA:
   ```sh
   nvcc --version
   ```

### Instalando CUDA no Ubuntu

1. Adicione o repositório CUDA:
   ```sh
   sudo apt-get update
   sudo apt-get install gcc-10 g++-10
   wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
   sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
   sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
   sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
   sudo apt-get update
   sudo apt-get -y install cuda
   ```

2. Verifique a instalação do CUDA:
   ```sh
   nvcc --version
   ```

### Instalando cuDNN

1. Faça o download do cuDNN na [página da NVIDIA](https://developer.nvidia.com/cudnn) para a versão correspondente ao seu CUDA.
2. Extraia o conteúdo e copie os arquivos para os diretórios correspondentes:
   ```sh
   sudo cp cuda/include/cudnn*.h /usr/local/cuda/include
   sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
   sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
   ```

3. Verifique a instalação do cuDNN:
   ```sh
   cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
   ```

### Configurando o projeto

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/recogni.git
   cd recogni
   ```

2. Crie e ative um ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate   # Linux ou WSL
   .\venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

Para utilizar o Recogni com um modelo compilado no `ctranslate2`, basta especificar o modelo durante a execução do script principal:

```sh
python recogni.py --input caminho/para/audio.wav --model caminho/para/modelo-ctranslate2
```

Isso garantirá que o modelo pré-compilado seja carregado para otimizar a transcrição.

## Métricas

Recogni calcula diversas métricas úteis para análise do texto transcrito:

- **Quantidade total de palavras**: O número total de palavras presentes no texto transcrito.
- **Quantidade de palavras por minuto**: A média de palavras transcritas por minuto de áudio.
- **Palavras mais faladas**: Uma lista das palavras mais utilizadas no texto, da mais falada para a menos falada, incluindo a quantidade de vezes que cada palavra aparece.
- **Percentual de palavras mágicas**: A frequência de ocorrência das "palavras mágicas" no texto transcrito. As palavras consideradas são:

  - Obrigado(a)
  - Por favor
  - Desculpa / Desculpe
  - Por gentileza
  - Bom dia / Boa tarde / Boa noite
  - Agradeço / Agradece
  - Gratidão
  - Sinto muito
  - Perdão / me perdoe
  - Com licença

Essas métricas são calculadas automaticamente durante a transcrição e exibidas ao final do processo.

## Contribuição

Sinta-se à vontade para contribuir com melhorias para o Recogni! Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais informações.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---