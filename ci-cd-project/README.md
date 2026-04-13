# CI/CD Automation Project (Jenkins + Tests + Docker + Ansible)

## What you get
- **Jenkins pipeline** that runs automated tests, builds a Docker image, pushes to Docker Hub, and deploys via Ansible
- **Automated testing** with `pytest`
- **Dockerized** Python web app
- **Ansible-based** deployment to staging/production
- **GitHub webhook** trigger support
- **Optional manual approval** before production deployment

## Folder structure
```
ci-cd-project/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   ├── __init__.py
│   └── tests/
│       └── test_app.py
├── docker/
│   └── Dockerfile
├── jenkins/
│   └── Jenkinsfile
├── ansible/
│   ├── inventory.ini
│   ├── deploy.yml
│   └── roles/
│       └── app-deploy/
│           ├── tasks/
│           │   └── main.yml
│           └── templates/
├── .github/
│   └── webhook.md
├── .gitignore
├── pytest.ini
└── README.md
```

## Run locally (developer sanity check)
From `ci-cd-project/`:

### Run tests
```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
pytest -q
```

### Run app without Docker
```bash
python app/main.py
```
Then open `http://localhost:8000/health`.

## Docker
From `ci-cd-project/`:
```bash
docker build -f docker/Dockerfile -t my-app:local .
docker run --rm -p 8000:8000 my-app:local
```

## Ansible deployment
### 1) Configure inventory
Edit `ansible/inventory.ini` with your real server IPs/users.

Your target hosts should be Linux with Python available and reachable over SSH.

### 2) Install Ansible dependencies
```bash
ansible-galaxy collection install community.docker
```

### 3) Deploy
```bash
ansible-playbook ansible/deploy.yml -i ansible/inventory.ini -e "target_env=staging docker_image=your-dockerhub-username/my-app:latest"
ansible-playbook ansible/deploy.yml -i ansible/inventory.ini -e "target_env=production docker_image=your-dockerhub-username/my-app:latest"
```

## Jenkins setup
### Pipeline job
- Create a **Pipeline** job
- Set **Pipeline script from SCM**
- Set **Script Path** to `jenkins/Jenkinsfile`

### Credentials you must add in Jenkins
- `dockerhub-creds` as **Username with password** (Docker Hub username/password or token)

### Webhook trigger
See `.github/webhook.md`.

## Notes
- The Jenkins pipeline is written for Linux agents (uses `sh`, Docker CLI, and Ansible).
- Docker pushes only run automatically on `main`/`master` branches.

