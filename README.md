# Sistema de Cifragem e Decifragem de Arquivos Binários (.jpg)

Este projeto implementa um algoritmo de criptografia simétrica baseado em cifras de bloco (inspirado na Rede de Feistel e no DES - Data Encryption Standard) para processar arquivos binários, especificamente imagens no formato `.jpg`. O projeto foi desenvolvido inteiramente em Python, sem o uso de bibliotecas de criptografia prontas.

## 1. Fundamentação Teórica

O desenvolvimento deste algoritmo baseia-se nos pilares e técnicas da Segurança da Informação. A criptografia agrupa técnicas para garantir a confidencialidade dos dados, além de também poder prover integridade e autenticidade [1]. No contexto deste software:

- **Confidencialidade:** Garante que a imagem (recurso do sistema) só possa ser lida e visualizada por usuários autorizados que detenham a senha [2].
- **Integridade:** Garante que o arquivo só possa ser modificado (cifrado/decifrado) legitimamente por usuários autorizados [2].

### Criptografia Simétrica

O sistema desenvolvido utiliza o modelo de **criptografia simétrica**, o que significa que o emissor e o receptor (ou seja, os processos de cifrar e decifrar) utilizam exatamente a mesma chave criptográfica $k$ [3, 4].

### Cifras de Bloco (Algoritmo base: DES)

A estratégia de cifragem escolhida quanto ao agrupamento de dados foi a **cifra de bloco**. Diferentemente dos cifradores de fluxo que operam byte a byte em sequência [5], a cifra de bloco recebe um bloco inteiro de elementos do texto claro e gera um bloco correspondente de saída no texto cifrado [4].

Os blocos usuais operam geralmente entre 64 e 128 bits [5]. A nossa implementação segue uma lógica matemática não-linear (Função de Feistel) em múltiplas rodadas (16 rodadas) baseada no funcionamento clássico do algoritmo **DES (Data Encryption Standard)**, criado pela IBM na década de 1970 [6]. O tamanho do bloco processado no código é de 8 bytes (64 bits), com uma chave ajustada para o mesmo tamanho.

### Modo de Operação (ECB)

Para que os blocos cifrados do arquivo da imagem operem em conjunto, adotamos o modo de operação **ECB (Electronic Codebook)** [7, 8]. Neste modo, cada bloco de 8 bytes da imagem é submetido à lógica de criptografia de forma independente, um após o outro, até o fim do arquivo.

### Técnica de Padding (Inserção)

Como as cifras de bloco exigem que os dados de entrada tenham um tamanho exato para formar blocos perfeitos, tornou-se necessária a técnica de **inserção**. O material da disciplina define inserção como o "preenchimento de dados não contidos no texto claro" original [3].

Para isso, aplicamos a lógica de padding _PKCS#7_. Esta técnica calcula quantos bytes faltam para que o arquivo alcance um tamanho múltiplo de 8 bytes e preenche o espaço final com o valor correspondente à quantidade de bytes inseridos.

---

## 2. Requisitos para Execução

- **Python 3.x** instalado na máquina.
- Não é necessária a instalação de nenhuma biblioteca externa (o código utiliza apenas as bibliotecas nativas, como `os`).
- Um arquivo de imagem original no formato `.jpg` (ex: `imagem.jpg`) salvo no mesmo diretório do script.

## 3. Instruções de Execução

Abra o terminal (ou Prompt de Comando) na pasta raiz onde se encontram o script `criptografia-jpg.py` e a sua imagem de teste.

### Passo 3.1: Cifrando o arquivo (Garantindo a Confidencialidade)

1. Execute o comando: `python criptografia-jpg.py`
2. No menu interativo, digite a opção `1` (Cifrar imagem).
3. Informe o nome do arquivo original (ex: `imagem.jpg`).
4. Informe o nome que o arquivo cifrado deve ter (ex: `cifrado.jpg`).
5. Informe uma chave secreta (senha) de sua preferência.
6. **Resultado:** O arquivo `cifrado.jpg` será gerado. Ao tentar abri-lo no sistema operacional, o visualizador de imagens exibirá um erro informando que o formato não é suportado, comprovando que o texto aberto foi devidamente embaralhado em um texto cifrado.

### Passo 3.2: Decifrando o arquivo (Revertendo o processo)

1. Execute novamente o comando: `python criptografia-jpg.py`
2. No menu interativo, digite a opção `2` (Decifrar imagem).
3. Informe o nome do arquivo corrompido/cifrado que você acabou de gerar (ex: `cifrado.jpg`).
4. Informe o nome para o arquivo recuperado (ex: `recuperado.jpg`).
5. Informe **exatamente a mesma chave secreta** (senha) utilizada no Passo 3.1.
6. **Resultado:** O algoritmo fará a leitura invertida das rodadas lógicas e removerá o _padding_ automático. O arquivo `recuperado.jpg` abrirá perfeitamente e será idêntico à imagem original.

---

## 4. Validação (Vídeo)

O vídeo demonstrando o funcionamento da ferramenta, com a comprovação da cifragem e posterior recuperação da imagem, encontra-se disponível no link abaixo:

- [Link do vídeo](https://youtu.be/URXHI0vYQAQ)
