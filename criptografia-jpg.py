import os

# ==========================================
# TÉCNICA DE PADDING (PKCS#7)
# ==========================================
def aplicar_padding(dados, tamanho_bloco=8):
    """
    Adiciona bytes ao final do arquivo para que o tamanho total
    seja múltiplo do tamanho do bloco (8 bytes).
    """
    bytes_faltantes = tamanho_bloco - (len(dados) % tamanho_bloco)
    # No PKCS#7, o valor do byte preenchido é igual à quantidade de bytes faltantes
    padding = bytes([bytes_faltantes] * bytes_faltantes)
    return dados + padding

def remover_padding(dados):
    """
    Lê o último byte para saber quantos bytes de padding foram
    adicionados e os remove para restaurar o arquivo original.
    """
    bytes_faltantes = dados[-1]
    return dados[:-bytes_faltantes]

# ==========================================
# ALGORITMO BASEADO EM DES (REDE DE FEISTEL)
# ==========================================
def funcao_feistel(metade_direita, subchave):
    """
    Função matemática não-linear de embaralhamento.
    Mistura a metade direita do bloco com a chave da rodada.
    """
    r_int = int.from_bytes(metade_direita, 'big')
    k_int = int.from_bytes(subchave, 'big')
    
    # Operação XOR e deslocamento de bits (Shift) para causar "confusão"
    mistura = (r_int ^ k_int)
    mistura = ((mistura << 3) & 0xFFFFFFFF) | (mistura >> 29)
    
    return mistura.to_bytes(4, 'big')

def processar_bloco(bloco, chave, operacao='cifrar'):
    """
    Aplica a Rede de Feistel em um bloco de 8 bytes.
    """
    # Divide o bloco de 8 bytes em Esquerda (L) e Direita (R) de 4 bytes
    L, R = bloco[:4], bloco[4:]
    
    # O DES utiliza 16 rodadas. Na decifragem, a ordem das subchaves é invertida.
    rodadas = range(16) if operacao == 'cifrar' else range(15, -1, -1)
    
    for i in rodadas:
        # Gera a subchave da rodada
        inicio_chave = i % 4
        subchave = chave[inicio_chave : inicio_chave + 4]
        
        # A Função de Feistel é SEMPRE aplicada na metade Direita (R) atual
        F = funcao_feistel(R, subchave)
        
        # O novo R é o XOR entre o L antigo e a saída da função. O novo L é o R antigo.
        novo_R = bytes(a ^ b for a, b in zip(L, F))
        L = R
        R = novo_R

    # No final de todas as rodadas, as metades são juntadas de forma invertida
    return R + L

# ==========================================
# MANIPULAÇÃO DE ARQUIVOS BINÁRIOS
# ==========================================
def processar_arquivo():
    print("\n")
    print("--- SISTEMA DE CRIPTOGRAFIA DE IMAGENS (.JPG) ---")
    print("1. Cifrar imagem")
    print("2. Decifrar imagem")
    escolha = input("Escolha a operação (1 ou 2): ")
    
    if escolha not in ['1', '2']:
        print("Opção inválida!")
        return

    caminho_entrada = input("Digite o caminho do arquivo de entrada (ex: imagem.jpg): ")
    caminho_saida = input("Digite o nome do arquivo de saída (ex: imagem_cifrada.jpg): ")
    senha = input("Digite a chave secreta (senha): ")

    # Ajusta a chave para ter exatamente 8 bytes (64 bits)
    chave_bytes = senha.encode('utf-8')
    if len(chave_bytes) < 8:
        chave_bytes = chave_bytes + b'\x00' * (8 - len(chave_bytes))
    chave_bytes = chave_bytes[:8]

    # Leitura do arquivo em modo binário (rb)
    try:
        with open(caminho_entrada, 'rb') as f:
            dados = f.read()
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        return

    operacao = 'cifrar' if escolha == '1' else 'decifrar'

    # Aplica o Padding se for cifragem
    if operacao == 'cifrar':
        dados = aplicar_padding(dados, 8)

    dados_processados = bytearray()

    # Processa o arquivo em blocos exatos de 8 bytes (Modo ECB)
    for i in range(0, len(dados), 8):
        bloco = dados[i:i+8]
        bloco_processado = processar_bloco(bloco, chave_bytes, operacao)
        dados_processados.extend(bloco_processado)

    # Remove o Padding se for decifragem
    if operacao == 'decifrar':
        dados_processados = remover_padding(dados_processados)

    # Gravação do arquivo em modo binário (wb)
    with open(caminho_saida, 'wb') as f:
        f.write(dados_processados)
    
    print(f"\nSucesso! Arquivo salvo como: {caminho_saida}")

if __name__ == "__main__":
    while(True):
        processar_arquivo()