# Infratrack

A lightweight demonstration DevOps-focused CRUD app built with Flask. A tracking application at heart, with the stated goal of helping infrastructure teams track hosts, tasks, system changes, etc.

## Features 

- Add/edit/delete servers with metadata (IP, hostname, OS, tags)
- Log tasks/activity (patches, reboots, installations)
- Track/log configuration changes

## Stack

- **Flask** + SQLAlchemy + WTforms + Jinja2 templates
- **Docker** and `docker-compose` (to bring up Flask app and `SQLite` with `Gunicorn` and `nginx`)
- **Terraform** for provisioning infra (EC2, S3, etc.)
- **Ansible** for configuration
- **Github Actions** for CI/CD

## High-level deployment overview


- Deployable to AWS EC2 & S3 via Terraform
- Post-deploy config via Ansible
- CI/CD pipeline (under `.github/workflows/`)
- Infrastructured (IAM, VPC) provisioned via Terraform

## Folder Structure

- `app/`: core Flask app
- `infra/terraform/`: AWS provisioning
- `infra/ansible/`: server provisioning & deployment

## Running in development from root directory

```
1) SQLite Persistence
mkdir -p data

2) Build images
docker compose build

3) Launch Nginx + Gunicorn + Flask
docker compose up -d

4) Tail logs (screen/tmux)
docker compose logs -f
```
Access application at `http://localhost:8080`

## Deploying to AWS
### Terraform
```
cd infra/terraform
terraform init
terraform apply -auto-approve
    -var='prefix=infratrack'
    -var='key_name=infra-track-key'
    -var='public_key_path=~/.ssh/infra-track.pub'
    -var='deployer_principals=["arn:aws:iam::<account-id>:user/ 
    admin"]'
```

### Ansible
```
cd ../ansible
ansible-galaxy install -r requirements.yml
export TERRAFORM_BIN=/snap/bin/terraform # only if using Snap Terraform
ansible-inventory --list | jq . # should show group "web" and host "infratrack"
ansible -m ping web
```
Set the repo branch in playbook.yml (use `master` for default) and then run

`ansible-playbook playbook.yml`


## Next Steps

1. DB & Migrations

    a.  Database & Migrations - Replace SQLite with Amazon RDS Postgres

    b. Add Alembic migrations to manage schema changes over time

    c. Seed data scripts for setups - demonstrate app can handle stateful infra and database lifecycles

2. API Layer / Automated Tests

    a. REST Blueprint for Hosts/Tasks/Changes
    
    b. pytest unit and integration tests

    c. test automation with `make test` or github actions

3. CI/CD Pipeline

    a. Github Actions pipeline: lint -> test -> build Docker image -> push to ECR -> trigger Ansible deploy

    b. Add staging vs production environments with approval steps

4. Secrets & Config Management

    a. Switch from .env files to Secrets Manager (or AWS SSM Parameter Store)

    b. Get Ansible/Terraform to pull secrets at deploy time

5. Observability & Monitoring

    a. Centralize logs (CloudWatch Logs)

    b. Add a /health (or /healthz?) endpoint in the flask app

    c. Metrics from Prometheus/Opentelemetry, use a Grafana Dashboard

# Planned timeline of changes

Reality first: This is a demo as is. Postgres + health checks should make it "software"

Low hanging fruit: Inventory sync + pings means UI can update itself

Signal > Form: Autoingesting TF/Ansible artifacts turns "Changes" into an actual audit log

"Ops-Grade": CI/ Secrets, metrics, and logs. 


Here's how we'll break this up

## Week 0

1. Clean up terraform files to be more modular

## Week 1

___Infra___

1.  Provision RDS Postgres using Terraform (paramaterized: engine/version, instance class, subnet group, SG)

2. Add Secrets Manager/SSM params for DB URL; wire instance SGs

3. Limit EC2 SG to 80/22 from my IP (for simplicity, change later)

___App___

1. Add Alembic; SQLite -> Postgres

2. Implement /health endpoint (check DB connectivity and migration head)

3. Switch SQLAlchemy URI to env var (remove `db.create_all()` paths)

_Acceptance_

1. `flask db upgrade` runs clean and app boots on postgres

2. `curl /health` fails is DB creds are wrong, otherwise reports healthy

## Week 2 - Low Friction to make the app "Feel Alive" (Auto-Inventory + Pings)

_Infra_

1. Just be sure TF Outputs contain instance IDs/IPs necessary

2. Potentially export relevant tags (Owner, Env) for use as metadata

_App_

1. Add a "Sync Inventory" job/button that parses Ansible Dynamic Inventory (or Terraform JSON) to insert `Hosts` rows

2. Background job (in python, `rq/celery/apscheduler`work) to ping each host every N minutes; persist `last_seen`, `status`

3. UI: Green/Yellow/Red Badges on hosts; sortable by "last seen"

_Acceptance_

1. After `terraform apply` is run, tapping "sync inventory" should show EC2 in  hosts with no manual entry.

## Week 3

_Infra_ 

1. CI Pipeline skeleton with GHA that runs lint/tests, builds container, pushes to ECR. NO DEPLOY STEP YET

2. Parameter Store / Secrets for API Tokens

_App_

1. Versioned REST API for Hosts/Tasks/Changes (list/get/create/update/delete) with pagination/filtering

2. AuthZ: role claims in a signed token or sessions -> `viewer` `operator` `admin` etc

3. Request IDs in logs; 400/404/500 JSON problem responses

_Acceptance_ 

1. `GET /api/v1/hosts?status=unhealthy` should return inventory.

2. Admins can edit; viewer is read only.


## Week 4 - Cool, automatic change capture

_Infra_ 

1. A couple of wrapper scripts. Output the terraform plan to a plan.json with `terraform plan -out=plan.bin && terraform show -json plan.bin > plan.json` AND Use Ansible callback plugin that serializes play recap to JSON.

2. CI Step - archive `plan.json` and/or ansible recap as artifacts

_App_ 

1. Add an `/ingest/terraform` endpoint accepting `plan.json`; pase (adds, changes, destroys) -> Change a row linked to affected Hosts (by `instance_id`)

2. Add an `/ingest/ansible` endpoint for callback payload; attach play/role/task results to same change by correlation key: Commit SHA, build ID, timestamp window

3. Page should render a simple diff: counts by actions, list of resources touched, task success/fails; store raw artifacts for download

_Aceptance_ 

1. Running `terraform plan` (On CI or PR, either way) auto creates a change in infratrack

2. Ansible run posts results; Change page shows both TF and Ansible actions

## Week 5 CI/CD to Staging + Secrets Hygeine

_Infra_ 

1. Extend CI to deploy to staging via ansible once tests pasts (optional manual approval)

2. Enforce no-plaintext-secrets. app should get DB & token secrets from SSM/Secrets at start (preferably not injected by .env at this point)

_App_ 

1. Smoke Tests for `/health`, `/metrics` and one API Route; fail pipeline on regression.

2. Replace any remaining hardcoded secrets.

_Acceptance_ 

1. Merge to main -> Image Built, pushed, staging updated.

2. No secrets in repo or CI logs; app should fail when secrets are missing

## Week 6 - Observability & Monitoring

_Infra_

1. Centralize logs (Cloudwatch?); ship container log

2. Metrics: Prometheus, dashboard: Grafana

_App_

1. `/metrics` endpoint (Prometheus format) with `http_request_duration_seconds` (histogram), `http_requests_total` (by route/status), `background_job_duration_seconds`, `host_status_gauge` (health = 1/unhealthy = 0)

2. Standarize JSON logs with `request_id`, `user/role` `route` `status` and `duration`
