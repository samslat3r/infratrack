# Infratrack

A lightweight demonstration DevOps-focused CRUD app built with Flask. A tracking application at heart, with the stated goal of helping infrastructure teams track hosts, tasks, system changes, etc.

## Features 

- Add/edit/delete servers with metadata (IP, hostname, OS, tags)
- Log tasks/activity (patches, reboots, installations)
- Track/log configuration changes

## Stack

- **Flask** + SQLAlchemy + WTforms + Jinja2 templates
- **Docker** and `docker-compose` (to bring up Flask app and `SQLite`)
- **Terraform** for provisioning infra (EC2, S3, etc.)
- **Ansible** for configuration
- **Github Actions** for CI/CD

*to be clear, `docker-compose` is used here to deploy the Flask App with SQLite. The stretch goal of using RDS would nullify this requirement*

## High-level deployment overview


- Deployable to AWS EC2 & S3 via Terraform
- Post-deploy config via Ansible
- CI/CD pipeline (under `.github/workflows/`)
- Infrastructured (IAM, VPC) provisioned via Terraform

## Folder Structure

- `app/`: core Flask app
- `terraform/`: AWS provisioning
- `ansible/`: server provisioning & deployment

## Stretch goals (in tentative order of preference)

- **Amazon RDS** instead of SQLite to mimic a production-like environment
- **API layer** perhaps with Flask-RESTful or FastAPI (or others)
- **Authentication** with Flask-Login or preferably OAuth2
- **Prometheus + Grafana** for monitoring metrics + app events
- **Exporting Reports** in CSV/JSON format 


