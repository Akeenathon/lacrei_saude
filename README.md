# Lacrei Saúde - Desafio Técnico

## Visão Geral

API RESTful para gestão de profissionais da saúde e consultas médicas, com autenticação JWT, PostgreSQL, Docker, CI/CD e testes automatizados.

##  Setup Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/lacrei-saude.git
   cd lacrei-saude
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   poetry install
   poetry shell
   ```

3. **Configure o banco de dados:**
   - Por padrão, usa SQLite para dev. Para PostgreSQL, ajuste o `settings.py`.

4. **Aplique as migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Rode o servidor:**
   ```bash
   python manage.py runserver
   ```

---

##  Setup com Docker

1. **Suba os containers:**
   ```bash
   docker-compose up --build
   ```

2. **Acesse a aplicação:**
   - API: [http://localhost:8000](http://localhost:8000)
   - Banco: `localhost:5432` (usuário/senha: lacrei_saude/postgres)

---

##  Execução dos Testes

- **Via Poetry:**
  ```bash
  poetry run python manage.py test
  ```
- **Via Docker:**
  ```bash
  docker-compose exec web python manage.py test
  ```

---

##  Fluxo de Deploy (CI/CD)

- **Pipeline GitHub Actions:**
  - Lint (flake8)
  - Testes automatizados
  - Build
  - Deploy automático para EC2 (Docker + docker-compose)

**Resumo:**
1. Push na branch `main` dispara o pipeline.
2. Código é copiado para a EC2 via SSH.
3. Comando remoto executa `docker-compose down && docker-compose up -d --build`.

---

##  Justificativas Técnicas

- **Django + DRF:** Rapidez no desenvolvimento, segurança e robustez.
- **Poetry:** Gerenciamento moderno de dependências, fácil reprodutibilidade.
- **PostgreSQL:** Banco relacional robusto, ideal para dados estruturados.
- **Docker:** Padronização do ambiente, fácil deploy e escalabilidade.
- **JWT:** Autenticação segura e stateless.
- **CI/CD (GitHub Actions):** Automatização do ciclo de vida do projeto.
- **Testes APITestCase:** Garantia de qualidade e segurança nas APIs.
- **CORS:** Permite integração segura com frontends diversos.
- **Logging:** Rastreabilidade de acessos e erros.

---

##  Proposta de Rollback Funcional

- **Rollback via GitHub Actions:**
  - Basta fazer um revert do commit com bug e dar push na `main`. O pipeline irá rodar novamente e restaurar a versão anterior automaticamente na EC2.

- **Deploy Blue/Green (Sugestão para produção):**
  - Manter dois ambientes (ex: `lacrei-saude-blue` e `lacrei-saude-green`).
  - Deploy na nova cor, validação, e troca do tráfego DNS.
  - Rollback rápido apenas alternando o DNS para o ambiente estável.

- **Preview Deploy (Sugestão):**
  - Usar branches de preview para testar features antes de ir para produção.

---

##  Endpoints principais

- `/api/v1/healthcareworker/` - CRUD de profissionais
- `/api/v1/medicalconsultation/` - CRUD de consultas
- Autenticação JWT: `/api/v1/token/`

---

##  Autor

- [Bryan Akenathon](https://github.com/akeenathon)

<div align="center">  
  <img width="45%" height="195px" src="https://github-readme-stats.vercel.app/api?username=akeenathon&show_icons=true&count_private=true&hide_border=true&title&theme=github_dark_icons=true&bg_color=00000000" alt="Bryan Akenathon GitHub stats" /> 
  <img width="45%" height="195px" src="https://github-readme-stats.vercel.app/api/top-langs/?username=akeenathon&layout=compact&hide_border=true&title&theme=github_dark_icons=true&bg_color=00000000" />
</div>

