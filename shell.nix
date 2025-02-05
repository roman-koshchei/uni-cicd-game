{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "Pygame Development Environment";

  buildInputs = [
    (
      pkgs.python3.withPackages (ps: [ 
        ps.pygame
      ])
    )
  ];
}


