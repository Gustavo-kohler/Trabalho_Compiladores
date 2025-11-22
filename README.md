# Trabalho de Compiladores - INE5622 (Linguagem LSI-2025-2)

Implementação completa do Trabalho 1 (Analisador Léxico e Sintático) para a disciplina de Introdução a Compiladores da UFSC.

## Integrantes do Grupo

* **Gustavo Luiz Kohler**
* **Cleverson Borges dos Passos**
* **Breno Juliano Sayão**

---

## Requisitos

* **Python 3.12** ou superior.

---

## Estrutura de Arquivos

O projeto está organizado da seguinte forma:

```text
/trabalho (Raiz)
│
├── README.md                           # Este arquivo com instruções
│
├── parte1/                             # PARTE 1: Analisador Léxico
│   ├── lexer.py                        # Implementação da classe Lexer, Token e Tag
│   ├── teste_correto.lsi               # Teste léxico sem erros (Código pequeno)
│   └── teste_erro.lsi                  # Teste com erros léxicos (! sozinho, @, #)
│
├── parte2/                             # PARTE 2: Gramática e Tabela
│   └── Trabalho Parte 2.pdf            # PDF com a gramática transformada, 
│                                         os FIRSTs e FOLLOWs e a tabela de reconhecimento sintático
│
└── parte3/                             # PARTE 3: Analisador Sintático
    ├── parser.py                       # Implementação da classe Parser
    ├── teste_correto.lsi               # Programa completo (+50 linhas) sem erros
    ├── teste_erro_1.lsi                # Erro sintático: Falta de ponto e vírgula
    ├── teste_erro_2.lsi                # Erro sintático: Bloco IF sem fechar chaves
    └── teste_erro_3.lsi                # Erro sintático: Início de sentença inválido
    
```

---

## Instruções de Execução

Recomendamos executar todos os comandos **a partir da pasta raiz** (`/trabalho`) utilizando a flag `-m` do Python. Isso garante que os imports entre a `parte3` e a `parte1` funcionem corretamente.

### Parte 1: Analisador Léxico

O Lexer lê o arquivo de entrada, imprime a lista de tokens identificados e a tabela de símbolos final.

**Para testar com um arquivo correto:**

```bash
python3 -m parte1.lexer ./parte1/teste_correto.lsi
```

**Para testar a detecção de erros léxicos:**

```bash
python3 -m parte1.lexer ./parte1/teste_erro.lsi
```

-----

### Parte 3: Analisador Sintático (Parser)

O Parser utiliza o Lexer da Parte 1 para validar se o código segue a gramática LSI-2025-2. Ele exibe mensagens de sucesso ou aponta a linha/coluna e o token esperado em caso de erro.

#### 1\. Teste de Sucesso

**Programa completo (+50 linhas) sem erros:**

```bash
python3 -m parte3.parser ./parte3/teste_correto.lsi
```

*Saída esperada:* `Análise Sintática Concluída com Sucesso!`

#### 2\. Testes de Erro 

O parser deve identificar o erro, apontar a localização e listar os tokens que eram esperados naquele contexto.

**Caso 1: Falta de ponto e vírgula (ou vírgula) na declaração:**

```bash
python3 -m parte3.parser ./parte3/teste_erro_1.lsi
```

**Caso 2: Bloco IF não fechado (falta de `}`):**

```bash
python3 -m parte3.parser ./parte3/teste_erro_2.lsi
```

**Caso 3: Início de sentença inválido:**

```bash
python3 -m parte3.parser ./parte3/teste_erro_3.lsi
```

---