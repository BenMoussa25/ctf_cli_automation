import os
import yaml
import re
import subprocess

NGINX_TEMPLATE = """
server {{
    listen 443 ssl;
    client_max_body_size 4G;

    ssl_certificate         /etc/ssl/certs/cert.pem;
    ssl_certificate_key     /etc/ssl/private/key.pem;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    server_name {subdomain}.espark.tn;
    location / {{
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:{port};
        proxy_redirect off;
    }}
}}
"""

def append_link_to_description(yaml_path, subdomain):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    link_line = f"\nLink: https://{subdomain}.espark.tn"

    if "description" in data:
        if link_line.strip() not in data["description"]:
            data["description"] += link_line
    else:
        data["description"] = link_line.strip()

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    print(f"[+] Link added to challenge description in {os.path.basename(yaml_path)}")


def normalize_subdomain(subdomain):
    # Convert to lowercase
    subdomain = subdomain.lower()
    # Replace spaces, underscores and any non a-z0-9 with "-"
    subdomain = re.sub(r"[ _]+", "-", subdomain)
    subdomain = re.sub(r"[^a-z0-9-]", "-", subdomain)
    # Replace multiple dashes with a single dash
    subdomain = re.sub(r"-+", "-", subdomain)
    # Trim leading/trailing dashes
    subdomain = subdomain.strip("-")
    return subdomain

def extract_port_from_docker_compose(compose_path):
    with open(compose_path, 'r') as f:
        compose_data = yaml.safe_load(f)
    services = compose_data.get('services', {})
    for service in services.values():
        ports = service.get('ports', [])
        for port in ports:
            match = re.match(r'(\d+):\d+', str(port))
            if match:
                return match.group(1)
    return None

def extract_subdomain_from_challenge_yaml(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    return data.get("name", None)

def generate_nginx_conf(subdomain, port, output_dir="/etc/nginx/sites-enabled"):
    clean_subdomain = normalize_subdomain(subdomain)
    conf = NGINX_TEMPLATE.format(subdomain=clean_subdomain, port=port)
    file_path = os.path.join(output_dir, f"{clean_subdomain}.espark.tn")
    with open(file_path, "w") as f:
        f.write(conf)
    print(f"[+] NGINX config written for {clean_subdomain} at port {port}")

def scan_tasks(root_dir):
    for task_name in os.listdir(root_dir):
        task_path = os.path.join(root_dir, task_name)
        if not os.path.isdir(task_path):
            continue

        compose_path = os.path.join(task_path, "challenge", "docker-compose.yml")
        yaml_path = os.path.join(task_path, "challenge.yml")

        if os.path.exists(compose_path) and os.path.exists(yaml_path):
            port = extract_port_from_docker_compose(compose_path)
            subdomain = extract_subdomain_from_challenge_yaml(yaml_path) or task_name

            if port:
                generate_nginx_conf(subdomain, port)
                append_link_to_description(yaml_path, normalize_subdomain(subdomain))
            else:
                print(f"[!] No valid port found for {task_name}")
        else:
            print(f"[!] Skipping {task_name}, missing compose or challenge.yml")

def reload_nginx():
    print("[*] Reloading NGINX...")
    subprocess.run(["nginx", "-s", "reload"])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Auto NGINX config for CTF web tasks")
    parser.add_argument("root_dir", help="Root directory of CTF tasks (e.g., ./ctf_tasks)")
    args = parser.parse_args()

    scan_tasks(args.root_dir)
    reload_nginx()
