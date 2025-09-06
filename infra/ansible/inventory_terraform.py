#!/usr/bin/env python3
import json, os, subprocess, sys

TF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "terraform"))
DEFAULT_USER = os.getenv("ANSIBLE_SSH_USER", "ubuntu")
DEFAULT_KEY  = os.getenv("ANSIBLE_SSH_KEY", os.path.expanduser("~/.ssh/infratrack"))
TERRAFORM_BIN = os.getenv("TERRAFORM_BIN", "terraform")

def tf_outputs():
    try:
        out = subprocess.check_output([TERRAFORM_BIN, "-chdir=" + TF_DIR, "output", "-json"])
        return json.loads(out.decode())
    except Exception:
        return {}

def build_inventory():
        o = tf_outputs()
        ip  = (o.get("instance_public_ip") or {}).get("value")
        dns = (o.get("instance_public_dns") or {}).get("value")
        name = "infratrack"

        hosts, hostvars = [], {}
        if ip:
            hosts.append(name)
            hostvars[name] = {
                "ansible_host": ip,
                "ansible_user": DEFAULT_USER,
                "ansible_ssh_private_key_file": DEFAULT_KEY,
            }
            if dns:
                hostvars[name]["public_dns"] = dns

        return {
            "_meta": {"hostvars": hostvars},
            "all": {"hosts": hosts, "vars": {}},
            "web": {"hosts": hosts},
        }

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(build_inventory()))
    elif len(sys.argv) == 3 and sys.argv[1] == "--host":
        print(json.dumps(build_inventory()["_meta"]["hostvars"].get(sys.argv[2], {})))
    else:
        print(json.dumps(build_inventory()))

