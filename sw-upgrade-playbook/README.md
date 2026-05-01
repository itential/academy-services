# sw-upgrade-playbook

Ansible playbook invoked by the Itential Software Upgrade workshop via the `GatewayManager.runService` task.

## Playbook

`software_upgrade.yml` — runs `install add` → `install activate` (auto-reload) → wait → `install commit` against a Cisco IOS-XE device in install mode.

## Required extra vars

| Var | Example | Purpose |
|---|---|---|
| `binary` | `c8000v-universalk9.17.15.03a.SPA.bin` | Target `.bin` filename (must exist in `bootflash:images/`) |

Target hosts are supplied at runtime via Inventory Manager → Gateway Manager; the playbook runs against `hosts: all` in the provided inventory.

## Device pre-reqs

- IOS-XE in install mode
- Both target `.bin` bundles pre-staged in `bootflash:images/`
- Local auth `itential` / `itential` with `enable secret itential`

## Invocation

Registered on IAG as an Ansible service. Invoked from Itential workflow via the `GatewayManager.runService` task with `binary` passed as an extra variable.
