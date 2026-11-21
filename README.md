# Sistema de Reserva de Salas

Trabalho acadêmico (ADS) — sistema de reserva de salas em **Python + SQLite**.

## Estrutura

```
sistema_reservas/
├── main.py
├── database.py
├── models/
│   ├── sala.py
│   └── reserva.py
├── services/
│   └── reserva_service.py
├── views/
│   ├── login.py
│   ├── salas.py
│   └── reservas.py
└── database.sqlite3        # gerado pelo programa (ignorado pelo Git)
```

## Divisão do trabalho

| | Pessoa 1 (Brendo) | Pessoa 2 |
|---|---|---|
| **Papel** | Banco de dados, QA e documentação | Regras de negócio e interface |
| **Branch** | `dev/banco-qa-docs` | `dev/servicos-views` |
| **Arquivos** | `database.py`, `models/`, testes, documentação | `main.py`, `services/`, `views/` |

## Fluxo de Git (passo a passo)

> Regra de ouro: **ninguém commita direto na `main`**. Cada um trabalha na sua branch e integra via Pull Request (PR).

### 0. Uma vez só

```powershell
git clone https://github.com/brendoribeiron-ctrl/sistema-reservas-salas.git
cd sistema-reservas-salas
```

A Pessoa 2 precisa ser adicionada como colaboradora: GitHub → *Settings → Collaborators → Add people*.

### 1. Ir para a SUA branch (antes do primeiro commit)

```powershell
git fetch origin
git switch dev/banco-qa-docs        # Pessoa 1
# git switch dev/servicos-views     # Pessoa 2
git branch                          # confira: o * deve estar na sua branch
```

### 2. Primeiro commit

```powershell
git status
git add database.py                 # adicione arquivos específicos (evite "git add .")
git commit -m "feat(db): cria tabelas"
git push -u origin dev/banco-qa-docs   # -u só na primeira vez
```

### 3. Dia a dia (depois do primeiro commit)

```powershell
git switch SUA-BRANCH
git pull origin main                # traz o que o outro já integrou (faça ANTES de começar)
# ...trabalha...
git add <arquivos>
git commit -m "tipo(escopo): descrição curta"
git push
```

### 4. Integrar na `main` (Pull Request)

1. No GitHub: *Pull requests → New pull request* → base `main` ← compare `sua-branch`.
2. **A outra pessoa revisa** e clica em *Merge*.
3. Depois do merge, os dois atualizam:

```powershell
git switch SUA-BRANCH
git pull origin main
```

Faça PRs pequenos e frequentes para evitar conflitos.

### 5. Se der conflito

```powershell
git pull origin main                # avisa o conflito
# abra os arquivos com <<<<<<<, escolha o código certo, remova os marcadores
git add <arquivo-resolvido>
git commit
git push
```

### Padrão de commits

`feat:` nova funcionalidade · `fix:` correção · `test:` testes · `docs:` documentação · `refactor:` reorganização
