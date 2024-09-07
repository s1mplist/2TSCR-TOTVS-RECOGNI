## Recogni: Transcrição de Áudio Otimizada para Análise de NPS

**Recogni** é um projeto desenvolvido para o Challenge FIAP + TOTVS, focado na transcrição e análise de áudio para avaliação de NPS (Net Promoter Score). Utilizando a biblioteca `faster-whisper`, oferece transcrição rápida e precisa, otimizada para hardware com GPU via `ctranslate2`, e extração de métricas relevantes para NPS, como a frequência de "palavras mágicas".

## Destaques

- **Transcrição rápida e eficiente:** Utiliza `faster-whisper` para transcrever áudios com velocidade e precisão.
- **Otimização para GPU:** Compatibilidade com modelos compilados via `ctranslate2`, maximizando o desempenho em hardwares com GPU.
- **Análise de NPS:** Extrai métricas relevantes, como a frequência de "palavras mágicas" (obrigado, por favor, desculpe, etc.),  importantes para avaliar a qualidade do atendimento e a satisfação do cliente.
- **Fácil configuração e uso:**  Siga as instruções de instalação e comece a transcrever seus áudios rapidamente.

## Instalação

O Recogni requer Python 3.8 ou superior e depende de bibliotecas como `faster-whisper`, `ctranslate2`, e `CUDA`. Um guia detalhado de instalação, incluindo a configuração do CUDA no Windows (WSL) e Ubuntu, está disponível no arquivo [README.md](README.md) do projeto. 

## Utilização

```bash
python recogni.py caminho/para/audio.wav --model caminho/para/modelo-ctranslate2
```

O script `recogni.py` processa o áudio e gera um arquivo JSON com a transcrição e as métricas calculadas. 

## Métricas

Recogni calcula as seguintes métricas:

- Quantidade total de palavras
- Quantidade de palavras por minuto
- Palavras mais faladas (com suas frequências)
- Percentual de "palavras mágicas":
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

## Próximos Passos

- Implementar interface gráfica para facilitar o uso.
- Permitir a configuração personalizada das "palavras mágicas".
- Integrar com outras ferramentas de análise de dados.


## Contribuição

Contribuições são bem-vindas! Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## Licença

MIT License - consulte o arquivo [LICENSE](LICENSE) para mais informações.