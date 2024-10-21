{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
    webhooks = {
      name = "python-discord-webhook";
      pname = "python-discord-webhook";
      pyproject = true;
      src =  pkgs.fetchFromGitHub {
        owner = "lovvskillz";
        repo = "python-discord-webhook";
        rev = "64e5fd52c8d171442762a793c224d983a4202251";
        hash = "sha256-xiiDMXrduaKTJiwJICi74vE75+RpN1UA9gmK6DKMXQs=";
      };
      nativeBuildInputs = [
        (pkgs.python312.withPackages (pp: [
            pp.requests
        ]))
      ];
      buildInputs = [
        (pkgs.python312.withPackages (pp: [
            pp.poetry-core
        ]))
      ];
      propagatedBuildInputs = [
        (pkgs.python312.withPackages (pp: [
            pp.requests
        ]))
      ];
    };
    handler = {
      name = "python-logging-discord-handler";
      pname = "mod-manager";
      pyproject = true;
      src = pkgs.fetchFromGitHub {
        owner = "tradingstrategy-ai";
        repo = "python-logging-discord-handler";
        rev = "0c70e5d0daaba6f96780603709cc7d520b892f64";
        hash = "sha256-g/o4c88CZGzCnlKjnmutspu1mEt69WoGYNodBy1aOo4=";
      };
      nativeBuildInputs = [
        (pkgs.python312.withPackages (pp: [
            pp.requests
        ]))
      ];
      buildInputs = [
        (pkgs.python312.withPackages (pp: [
            pp.poetry-core
        ]))
      ];
      propagatedBuildInputs = [
        (pkgs.python312Packages.buildPythonPackage webhooks)
      ];
    };
  in
  {
    devShells.${system} = {
      default = pkgs.mkShell {
        packages = [
          (pkgs.python312.withPackages (pp: [
            pp.discordpy
            pp.python-dotenv
            pp.bokeh
            pp.deep-translator
          ]))
          (pkgs.python312Packages.buildPythonPackage handler)
          (pkgs.python312Packages.buildPythonPackage webhooks)
        ];
      };
    };
  };
}
