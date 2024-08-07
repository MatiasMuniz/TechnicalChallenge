# Execute with the command "nix-shell"
with import <nixpkgs> {};
mkShell {
  packages = [
    (python3.withPackages (pypi: 
      with pypi; [ requests ]
    ))

    # Note: MariaDB might not work in NixOS due to permission issues and service management limitations. 
    # It's recommended to install and configure MariaDB directly on your NixOS system using `configuration.nix`. 
    # However, it should work fine if you are using WSL or Arch.
    mariadb
  ];
}
