# Ansible - Actualización de Servicios Docker
## Estructura de carpetas

```
ansible/
├── inventory/
│   └── hosts.ini              # define localhost como destino
├── group_vars/
│   └── local.yml              # lista de los 14 servicios + rutas
└── playbooks/
    ├── update_all.yml         # actualiza los 14 servicios
    └── update_one.yml         # actualiza un solo servicio
```

---

## Configuración inicial (solo una vez)

### 1. Instalar dependencias Ansible
```bash
pip3 install ansible
```

### 2. Editar la lista de servicios
Abre `group_vars/local.yml` y reemplaza los nombres de ejemplo con
los nombres reales de tus carpetas en ~/Docker-files/

```yaml
servicios_docker:
  - nombre: akvorado
  - nombre: passbolt
  - nombre: zabbix
  # ...etc hasta los 14
```

### 3. Verificar que Ansible puede conectarse
```bash
ansible -i inventory/hosts.ini local -m ping
```

---

## Uso diario

### Actualizar los 14 servicios
```bash
ansible-playbook -i inventory/hosts.ini playbooks/update_all.yml
```

### Actualizar solo un servicio
```bash
ansible-playbook -i inventory/hosts.ini playbooks/update_one.yml -e "servicio=passbolt"
```

### Ver qué haría sin ejecutar (dry-run)
```bash
ansible-playbook -i inventory/hosts.ini playbooks/update_all.yml --check
```

### Ver output detallado
```bash
ansible-playbook -i inventory/hosts.ini playbooks/update_all.yml -v
```

---

## Notas importantes

- Si usas Docker Compose v1 (comando `docker-compose`), edita la variable
  `compose_bin` en el playbook de `"docker compose"` a `"docker-compose"`
- Los servicios fallidos NO detienen el proceso — se reportan al final
- La limpieza de imágenes huérfanas se ejecuta automáticamente al final
