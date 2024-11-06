{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let 
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in rec {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "default";
        buildInputs = with pkgs; [
          pkgs.python3
          (pkgs.python3.withPackages(ps: with ps; [ requests flask numpy ]))
        ];
      };
    };
}
