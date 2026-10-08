# DevOps Python Project

A containerised Flask web application with static analysis (YAPF, Pylint)
and integration testing, orchestrated via Docker Compose.

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Docker | 19.03.13 |
| docker-compose | 1.27.4 |

## Quick Start

### 1. Generate a dedicated SSH key pair

```bash
ssh-keygen -t ed25519 -f ~/.ssh/devops_project_key -N ""
```

### 2. Create `.env` from the example template

```bash
cp src/.env.example src/.env
```

Edit `src/.env` and paste the content of `~/.ssh/devops_project_key.pub`
into the `SSH_PUBLIC_KEY` variable:

```
SSH_PUBLIC_KEY=ssh-ed25519 AAAA...rest_of_key your@email.com
```

### 3. Build all images

```bash
cd src
docker-compose build
```

### 4. Start containers

```bash
docker-compose up -d
```

### 5. Check containers are running

```bash
docker-compose ps
```

---

## Running Tests

All test commands are executed from the `src/` directory.

### Full test pipeline (YAPF + Pylint + Integration)

```bash
docker compose exec tester python3 /tester/run_tests.py
```

Logs with timestamps will be printed for every stage.
Exit code 0 = all stages passed.

### Only integration tests (pytest, verbose)

```bash
docker compose exec tester python3 -m pytest /tester/tests/test_integration.py -v
```

### Only static analysis tests

```bash
docker compose exec tester python3 -m pytest /tester/tests/test_pylint_static.py -v
```

### All tests at once (pytest)

```bash
docker compose exec tester python3 -m pytest /tester/tests/ -v --tb=short
```

---

## SSH Access

### Connect to the app container

```bash
ssh -i ~/.ssh/devops_project_key -p 2222 root@127.0.0.1
```

### Connect to the tester container

```bash
ssh -i ~/.ssh/devops_project_key -p 2223 root@127.0.0.1
```

---

## Application Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main page |
| GET | `/upload` | Upload form |
| POST | `/upload` | Upload a file |
| GET | `/download/<name>` | Download a file by name |
| GET | `/files` | List all uploaded files |
| GET | `/to_files` | Redirect → `/files` |
| GET | `/success/<name>` | Welcome message |
| GET | `/increment/<int:a>` | Intentional infinite redirect (ERR_TOO_MANY_REDIRECTS demo) |
| GET | `/check_even/<int:a>` | Redirect to `/even/` or `/odd/` |
| GET | `/even/<int:a>` | Redirect back to `/check_even/` with a//2 |
| GET | `/odd/<int:a>` | Returns "{a} is odd" |
| POST | `/login` | Login (name=admin, password=password) |

Access the app on the host: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Project Structure

```
src/
├── .env.example              # Environment variable template
├── .gitignore
├── app/
│   ├── bad_code.py           # 10 intentional Pylint errors for pipeline testing
│   └── templates/
│       └── upload.html       # Custom upload template
├── docker-compose.yml
├── Dockerfile_app            # app container (Flask + SSH)
├── Dockerfile_tester         # tester container (pytest/http.server + SSH)
├── patches/
│   └── bussiness_logic.patch # Patch fixing EXAMPLE_APP blocking bugs
├── README.md
├── requirements_app.txt
├── requirements_tester.txt
├── scripts/
│   ├── start_app.sh          # Entrypoint: configure SSH + start Flask
│   └── start_tester.sh       # Entrypoint: configure SSH + start http.server
└── tester/
    ├── pylintrc              # Custom Pylint config (10 enabled rules)
    ├── run_tests.py          # Orchestrator: YAPF → Pylint → Integration
    └── tests/
        ├── __init__.py
        ├── test_pylint_static.py
        └── test_integration.py
```

---

## Patching EXAMPLE_APP

`bussiness_logic.py` from the upstream repository contains blocking issues:
- `import lti` — package does not exist on PyPI
- Missing definitions for `create_folder`, `get_files_in_folder`, `func2`

The file `patches/bussiness_logic.patch` is applied during `docker build`
using the `patch` utility. No source files from the repository are modified.

---

## Stopping and Cleanup

```bash
# Stop containers
docker-compose down

# Stop and remove volumes/images
docker-compose down --rmi all --volumes
```
