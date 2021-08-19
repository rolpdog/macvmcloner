# GHA M1 Build Worker Runner and Provisioner
This repo provides an Ansible playbook to provision a running ssh-accessible Apple Silicon MacOS (Monterey+) VM with the x86 version of the GHA runner and enough other bits to be used as a arm64 Python wheel builder.

The VM provisioner requires that the following steps have been accomplished manually on the target MacOS VM:
* VM disk created with at least 45GB (the default 30GB Parallels VM disk is too small to install XCode command-line tools); see http://blog.rolpdog.com/2021/08/customizing-macos-guest-vms-in.html for details.
* OOBE has been completed with an administrative user named `runner` with password `yourmom`
* spotlight indexing has been completed (FIXME: can we still disable?)
* remote login has been enabled
* the hostname has been set to something apropos for the runner name (FIXME: make it dynamic on startup)
* autologin has been configured for the `runner` user
* the VM's running IP has been captured (eg, `ipconfig getifaddr en0`)

Create an Ansible inventory file eg `hosts` similar to the following (substituting the VM's IP):
```
vmbuild ansible_host=192.168.123.123 ansible_user=runner ansible_password=yourmom ansible_python_interpreter=auto_silent
```

In the GHA runner setup page (eg https://github.com/youruser/yourrepo/settings/actions/runners/new or https://github.com/yourorg/settings/actions/runners/new), hit `Add New`, then copy the runner token displayed. 

On the host Mac with the VM started, Run `ansible-playbook -i hosts macvmsetup.yml -e repo_url=(base GH repo or org URL) -e runner_token=(token from create runner page)`. The VM will be provisioned with homebrew, XCode command-line tools, the GHA runner, and a couple of python.org arm64 CPython interpreter builds. This process usually takes 10-15 minutes (largely XCode command-line tools).

Once completed, the VM needs to be shut down. In `cloner.py`, set the `source_image_path` to the golden VM dir, and `ephemeral_image_dir` to a sibling directory with `source_image_path` where ephemeral VM clones will be cloned. Run cloner.py, and a new VM will be started that spins up a single-use runner. When the runner has completed a job (or been Ctrl-C'd), the ephemeral VM will shut down, be deleted, re-cloned from the original, and a new copy started (ad nauseum).

