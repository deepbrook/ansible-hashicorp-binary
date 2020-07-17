Hashicorp Binaries
==================
Installs any Hashicorp Binary available at https://releases.hashicorp.com on a target
system. The role allows installing multiple versions of the binaries, as well as removing
them.

To achieve this, the role generates a symlink at `hashicorp_bin_path` named identically
to the binary it links to. The binary itself is located in the same path, with its
version string appended to it, like so (assuming a vagrant installation):

    ~/$ ls $hashicorp_bin_path
    vagrant_1.5.1
    vagrant

When installing multiple versions, `hashicorp_purge` must be set to `no`; the role
will remove all other installed binary versions in `hashicorp_bin_path` otherwise.
Also, per default, the role updates the symlink to point to the binary that was
installed last by the role. To disable this, set `hashicorp_update_symlink` to `no`.

Requirements
------------
Python 3 on the Ansible host is required if you do not specify a version for each
binary you install (i.e. if you specify `version=latest` or no version at all)

If you'd like to verify the archive using Hashicorp's PGP signature and an archive's
provided checksums, `GPG2` is required. Please note **verifying the checksums file for
 binary archives on windows targets is not yet supported**.

Role Variables
--------------
Required Variables:

- `hashicorp_binaries` - may be a list of strings or dictionaries. 
  Specifying a list:
    - Strings must be valid binary names to install (see https://releases.hashicorp.com for possible values)
    - Using this format will **always** install the latest available version
 
  Specifying a list of dicts, these keys are allowed in each of the dicts:
    - `name` (required) - name of the binary to install (see https://releases.hashicorp.com for possible values)
    - `version` [`latest`] (optional) - version of the binary to specify, when looking up its archive. Specifying `latest` will cause the role to look up the latest version available via a [python script](./files/latest-version.py).
    - `arch` [`{{ hashicorp_default_arch }}`] - architecture to specify, when looking up a binary's archive
    - `platform` [`{{ hashicorp_default_platform }}`] - platform to specify when looking up a binary's archive

Optional variables (defaults in brackets `[]`):

- `hashicorp_bin_path` [`/usr/local/bin`]- the directory to install the binaries into
- `hashicorp_tmp_path` [`/usr/local/bin`]- the directory to download the binaries' archives to
- `hashicorp_update_symlink` [`yes`] - Whether or not to update the symlink created by this role to point to the newly installed binary.
- `hashicorp_purge` [`yes`] - Setting this to `yes` will remove any previously installed binaries from `hashicorp_bin_path`.

Dependencies
------------
None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: Install a single binary's latest version
      hosts: servers
      roles:
         - role: deepbrook.hashicorp-binaries
           vars: { hashicorp_binaries: [vagrant] }

    - name: Install multiple binaries' latest version
      hosts: servers
      roles:
         - role: deepbrook.hashicorp-binaries
           vars: { hashicorp_binaries: [packer, terraform] }

    # Install a specific version of binaries; this will remove any previously installed
    # version of the binaries specified by default (per `hashicorp_purge`)
    - name: Install a specific packer and terraform binary, instead of the latest version.
      hosts: servers
      roles:
         - role: deepbrook.hashicorp-binaries
           vars:
            hashicorp_binaries:
              packer: { version: 1.5.1 }
              terraform: { version: 0.12.21 }

    # Specify the target host's architecture and platform, instead of letting the role handling
    # it. Beware that if the specified arch/platform combination cannot be looked up from
    # the Hashicorp releases page, the role will fail.
    - name: Install a specific binary version for 32-bit freebsd.
      hosts: servers
      roles:
         - role: deepbrook.hashicorp-binaries
           vars:
            hashicorp_binaries:
              consul: { version: 1.8.0, arch: 386, platform: freebsd}

    # Install multiple binary versions on the target.
    # The binary will be available for use via the `consul` and `consul_1.8.0` commands
    - name: Install a consul version
      hosts: servers
      roles:
         - role: deepbrook.hashicorp-binaries
           vars:
            hashicorp_purge: no
            hashicorp_binaries:
              consul: { version: 1.8.0 }

    # The following will only install an additional version of consul; when calling
    # `consul` from cli, it will still execute `consul_1.8.0`. However, `consul_1.5.0` is also available.
    - name: Install another consul version, keep the previously installed versions and do not update the symlinks
      hosts: servers
      roles:
         - role: deepbrook.hashicorp-binaries
           vars:
            hashicorp_purge: no
            hashircorp_update_symlink: no
            hashicorp_binaries:
              consul: { version: 1.5.0 }