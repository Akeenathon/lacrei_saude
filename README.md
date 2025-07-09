# Lacrei Saúde — Desafio Técnico

## Sobre o Projeto

API RESTful para gerenciar profissionais da saúde e consultas médicas. O projeto foi pensado para ser seguro, fácil de rodar em qualquer ambiente (local, Docker, cloud) e com deploy automatizado.  
Tecnologias principais: **Django + DRF**, **PostgreSQL**, **Docker**, **Poetry** e **GitHub Actions**.

---

## Como rodar localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/lacrei-saude.git
   cd lacrei-saude
   ```

2. **Instale as dependências:**
   ```bash
   poetry install
   poetry shell
   ```

3. **Configuração do banco:**
   - Por padrão, o ambiente local usa PostgreSQL.  
   - Se quiser usar sqlite3, ajuste o `settings.py` e configure as variáveis de ambiente.

4. **Migrations e servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## Usando com Docker

1. **Suba tudo com:**
   ```bash
   docker-compose up --build
   ```

2. **Acesse:**
   - API: [http://localhost:8000](http://localhost:8000)
   - Banco: `localhost:5432` (usuário: lacrei_saude, senha: postgres)

---

## Testes

- **Local:**
  ```bash
  poetry run python manage.py test
  ```
- **Docker:**
  ```bash
  docker-compose exec web python manage.py test
  ```
- Os testes cobrem:
  - CRUD de profissionais
  - CRUD de consultas
  - Casos de erro (requisições inválidas, dados faltando, etc.)

Se quiser ver a cobertura:
```bash
poetry run coverage run manage.py test && poetry run coverage report
```

---

## Segurança e Boas Práticas

- **Validação:** Toda entrada de dados passa pelos serializers do DRF, então não entra nada “errado” no banco.
- **SQL Injection:** O Django ORM já cuida disso pra gente.
- **CORS:** Configurado com `django-cors-headers`. Só libera para domínios permitidos (ajustável por ambiente).
- **Autenticação:** JWT. Para acessar endpoints protegidos, pegue um token em `/api/v1/token/` e envie no header:
  ```
  Authorization: Bearer seu_token
  ```
- **Logs:** Tudo que é acesso e erro vai para arquivos em `/logs` (`access.log` e `errors.log`).  
  Exemplo para ver logs:
  ```bash
  cat logs/access.log
  cat logs/errors.log
  ```

---

## Endpoints principais

- `/api/v1/healthcareworker/` — CRUD de profissionais
- `/api/v1/medicalconsultation/` — CRUD de consultas
- `/api/v1/token/` — Autenticação JWT

---

## Ambientes AWS

- **Staging:** http://3.234.185.82:8080/
- **Produção:** http://52.7.195.126:8000/

Ambos estão na AWS, rodando via Docker, com deploy automatizado pelo GitHub Actions.

---

## CI/CD e Deploy

- O pipeline faz:
  - Lint (flake8)
  - Testes
  - Build
  - Deploy automático (EC2 + Docker Compose)
- Qualquer push na `main` já dispara tudo.
- O deploy faz o build, sobe containers e reinicia a aplicação.

---

## Rollback

- Se der problema, é só fazer um `git revert` do commit com bug e dar push na `main`. O pipeline faz o deploy da versão anterior.
- Para produção real, recomendo Blue/Green: dois ambientes, deploy na “cor” nova, valida, e só troca o DNS se estiver tudo certo. Se der ruim, volta o DNS pro ambiente estável.

---

## Documentação da API

- Tem uma coleção Postman pronta:  
  [Coleção Postman](./lacrei_saude.postman_collection.json)
- (Se quiser, pode plugar Swagger ou Redoc — só não deixei exposto por padrão.)

---

## Decisões, Erros e Melhorias

- **CORS:** Usei variáveis de ambiente para facilitar deploy em vários ambientes.
- **JWT:** Preferi JWT por ser simples e stateless.
- **Logs:** Separei logs de acesso e erro para facilitar debug.
- **Melhorias futuras:** Automatizar geração de docs Swagger/Redoc, adicionar monitoramento (Sentry/Prometheus), e criar testes para CORS.

---

## Autor

- [Bryan Akenathon](https://github.com/akeenathon)

<div align="center">  
  <img width="45%" height="195px" src="https://github-readme-stats.vercel.app/api?username=akeenathon&show_icons=true&count_private=true&hide_border=true&title&theme=github_dark_icons=true&bg_color=00000000" alt="Bryan Akenathon GitHub stats" /> 
  <img width="45%" height="195px" src="https://github-readme-stats.vercel.app/api/top-langs/?username=akeenathon&layout=compact&hide_border=true&title&theme=github_dark_icons=true&bg_color=00000000" />
</div>
