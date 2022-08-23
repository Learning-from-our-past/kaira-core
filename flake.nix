{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShell = pkgs.mkShell {
        nativeBuildInputs = with pkgs; [ 
          python39
          python39Packages.invoke
          bashInteractive

          libffi
          ssdeep
          zlib

          ##libxml2 <- This is actually a dependency, but it also comes with `libxslt`
          ##           and that package sets up `libxml2` correctly, whereas the actual
          ##           `libxml2` package doesn't 🙄
          libxslt
        ];
        buildInputs = [ ];
      };
    });
}
